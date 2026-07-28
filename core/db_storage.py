"""Fayllarni tashqi xizmatsiz, to'g'ridan-to'g'ri bazaga saqlaydigan storage.

Cloudinary/S3 kabi xizmatlar ba'zi mamlakatlarda ochilmaydi. Bu storage
rasm/fayllarni DBFile jadvaliga (baza ichiga) yozadi va ularni
/media/<nom> manzili orqali qaytaradi. Portfolio hajmidagi sayt uchun
bu yetarli va hech qanday tashqi akkaunt talab qilmaydi.
"""
import hashlib
import posixpath

from django.core.files.base import ContentFile
from django.core.files.storage import Storage
from django.db import models
from django.urls import reverse
from django.utils.deconstruct import deconstructible


class DBFile(models.Model):
    """Baza ichida saqlanadigan bitta fayl."""

    name = models.CharField(max_length=255, unique=True, db_index=True)
    content = models.BinaryField()
    content_type = models.CharField(max_length=100, default="application/octet-stream")
    size = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Fayl (bazada)"
        verbose_name_plural = "Fayllar (bazada)"

    def __str__(self):
        return self.name


_CONTENT_TYPES = {
    ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png",
    ".gif": "image/gif", ".webp": "image/webp", ".svg": "image/svg+xml",
    ".ico": "image/x-icon", ".pdf": "application/pdf",
}


@deconstructible
class DatabaseStorage(Storage):
    """Fayllarni DBFile jadvaliga yozadigan Django storage."""

    def _open(self, name, mode="rb"):
        row = DBFile.objects.get(name=name)
        return ContentFile(bytes(row.content), name=name)

    def _save(self, name, content):
        data = content.read()
        ext = posixpath.splitext(name)[1].lower()
        ctype = _CONTENT_TYPES.get(ext, "application/octet-stream")
        DBFile.objects.update_or_create(
            name=name,
            defaults={"content": data, "content_type": ctype, "size": len(data)},
        )
        return name

    def exists(self, name):
        return DBFile.objects.filter(name=name).exists()

    def get_available_name(self, name, max_length=None):
        # Nomlar to'qnashmasligi uchun kontent xeshini qo'shamiz.
        base, ext = posixpath.splitext(name)
        # Bir xil nom kelsa, ustiga yozilmasin — noyob qilamiz.
        candidate = name
        i = 1
        while DBFile.objects.filter(name=candidate).exists():
            candidate = f"{base}_{i}{ext}"
            i += 1
        return candidate

    def delete(self, name):
        DBFile.objects.filter(name=name).delete()

    def size(self, name):
        return DBFile.objects.get(name=name).size

    def url(self, name):
        return reverse("db_media", args=[name])
