from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path

from core import views

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path("", views.home, name="home"),
    path("aloqa/yuborish/", views.contact_submit, name="contact_submit"),
    path(
        "telegram/webhook/<str:secret>/",
        views.telegram_webhook,
        name="telegram_webhook",
    ),
    # Bazada saqlangan rasm/fayllarni uzatish (/media/<nom>)
    re_path(r"^media/(?P<name>.+)$", views.db_media, name="db_media"),
]
