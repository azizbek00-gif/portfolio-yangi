import json
import logging

from django.conf import settings
from django.contrib import messages as flash
from django.core.cache import cache
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .forms import ContactForm
from .models import (
    AboutItem, AboutSection, Contact, Hero, NavItem,
    Project, ProjectSection, SiteSettings,
)
from .telegram import notify_new_message, send_message

logger = logging.getLogger(__name__)

RATE_LIMIT_SECONDS = 60
RATE_LIMIT_COUNT = 3


def _client_ip(request):
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR", "")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "")


def _rate_limited(request):
    key = f"contact:{_client_ip(request)}"
    count = cache.get(key, 0)
    if count >= RATE_LIMIT_COUNT:
        return True
    cache.set(key, count + 1, RATE_LIMIT_SECONDS)
    return False


def _page_context(form=None):
    return {
        "site": SiteSettings.load(),
        "hero": Hero.load(),
        "about": AboutSection.load(),
        "about_items": AboutItem.objects.all(),
        "project_section": ProjectSection.load(),
        "projects": Project.objects.filter(is_published=True),
        "contact": Contact.load(),
        "nav_items": NavItem.objects.filter(is_active=True),
        "form": form or ContactForm(),
    }


def home(request):
    return render(request, "index.html", _page_context())


@require_POST
def contact_submit(request):
    if _rate_limited(request):
        flash.error(request, "Juda ko'p urinish. Bir daqiqadan keyin qayta yuboring.")
        return redirect("/#contact")

    form = ContactForm(request.POST)
    if form.is_valid():
        msg = form.save()
        notify_new_message(msg)
        flash.success(request, Contact.load().form_success_text)
        return redirect("/#contact")

    flash.error(request, "Formani tekshiring — ba'zi maydonlar to'ldirilmagan.")
    return render(request, "index.html", _page_context(form=form))


@csrf_exempt
def telegram_webhook(request, secret):
    if not settings.TELEGRAM_WEBHOOK_SECRET or secret != settings.TELEGRAM_WEBHOOK_SECRET:
        return HttpResponseForbidden("Ruxsat yo'q")

    if request.method != "POST":
        return HttpResponse("ok")

    try:
        update = json.loads(request.body.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        return JsonResponse({"ok": False}, status=400)

    message = update.get("message") or {}
    chat_id = (message.get("chat") or {}).get("id")
    text = (message.get("text") or "").strip()

    if not chat_id:
        return JsonResponse({"ok": True})

    if text.startswith("/start"):
        send_message(
            chat_id,
            "Salom! Portfolio saytingizdan kelgan xabarlar shu yerga tushadi.\n\n"
            f"Sizning chat ID: <code>{chat_id}</code>\n\n"
            "Buyruqlar:\n/xabarlar — oxirgi 5 ta xabar",
        )
    elif text.startswith("/xabarlar"):
        from .models import Message
        recent = Message.objects.all()[:5]
        if not recent:
            send_message(chat_id, "Hozircha xabar yo'q.")
        else:
            lines = [
                f"• <b>{m.name}</b> ({m.email}) — {m.created_at:%d.%m %H:%M}"
                for m in recent
            ]
            send_message(chat_id, "Oxirgi xabarlar:\n\n" + "\n".join(lines))

    return JsonResponse({"ok": True})
