import html
import logging
import threading

import requests
from django.conf import settings

logger = logging.getLogger(__name__)

API = "https://api.telegram.org/bot{token}/{method}"


def _post(method, payload):
    token = settings.TELEGRAM_BOT_TOKEN
    if not token:
        logger.warning("TELEGRAM_BOT_TOKEN o'rnatilmagan — xabar yuborilmadi.")
        return None
    try:
        r = requests.post(API.format(token=token, method=method), json=payload, timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as exc:
        logger.error("Telegram xatosi (%s): %s", method, exc)
        return None


def send_message(chat_id, text):
    if not chat_id:
        logger.warning("TELEGRAM_CHAT_ID o'rnatilmagan — xabar yuborilmadi.")
        return None
    return _post("sendMessage", {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
    })


def format_message(msg):
    return (
        "🔔 <b>Yangi xabar — Portfolio</b>\n\n"
        f"👤 <b>Ism:</b> {html.escape(msg.name)}\n"
        f"📞 <b>Telefon:</b> {html.escape(msg.phone) if msg.phone else '—'}\n"
        f"📧 <b>Email:</b> {html.escape(msg.email)}\n"
        f"💬 <b>Xabar:</b>\n{html.escape(msg.message)}\n\n"
        f"🕐 {msg.created_at:%d.%m.%Y %H:%M}"
    )


def notify_new_message(msg):
    """Fon rejimida yuboradi — forma sekinlashmaydi va Telegram
    ishlamasa ham xabar bazada qoladi."""

    def _run():
        from .models import Message
        ok = send_message(settings.TELEGRAM_CHAT_ID, format_message(msg))
        if ok:
            Message.objects.filter(pk=msg.pk).update(sent_to_telegram=True)

    threading.Thread(target=_run, daemon=True).start()
