from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

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
]

# Cloudinary ishlatilmasa, media fayllarni Django o'zi uzatadi.
# Kichik portfolio sayt uchun bu yetarli.
if settings.DEBUG or not settings.CLOUDINARY_URL:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
