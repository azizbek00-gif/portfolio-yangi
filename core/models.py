from django.db import models

from core.db_storage import DatabaseStorage

_db_storage = DatabaseStorage()


class SingletonModel(models.Model):
    """Faqat bitta yozuvga ega model (sozlamalar uchun)."""

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class SiteSettings(SingletonModel):
    logo_text = models.CharField("Logo matni", max_length=50, default="AZIZBEK")
    profile_image = models.ImageField(
        "Profil rasmi", upload_to="profil/", blank=True, null=True,
        storage=_db_storage,
    )
    favicon = models.ImageField(
        "Favicon", upload_to="favicon/", blank=True, null=True, storage=_db_storage
    )
    footer_text = models.CharField(
        "Footer matni",
        max_length=200,
        default="Barcha huquqlar himoyalangan.",
    )
    cv_file = models.FileField(
        "CV fayli (PDF)", upload_to="cv/", blank=True, null=True, storage=_db_storage
    )

    class Meta:
        verbose_name = "Sayt sozlamalari"
        verbose_name_plural = "Sayt sozlamalari"

    def __str__(self):
        return "Sayt sozlamalari"


class NavItem(models.Model):
    label = models.CharField("Nomi", max_length=50)
    anchor = models.CharField(
        "Havola", max_length=100,
        help_text="Masalan: #home, #about, #projects, #contact",
    )
    order = models.PositiveIntegerField("Tartib", default=0)
    is_active = models.BooleanField("Ko'rsatilsin", default=True)
    is_button = models.BooleanField(
        "Tugma ko'rinishida", default=False,
        help_text="Oxirgi element uchun belgilang — ko'k tugma bo'lib chiqadi.",
    )

    class Meta:
        ordering = ["order"]
        verbose_name = "Menyu elementi"
        verbose_name_plural = "Menyu (Nav)"

    def __str__(self):
        return self.label


class Hero(SingletonModel):
    badge_text = models.CharField("Kichik yozuv", max_length=60, default="AZIZBEK")
    title = models.CharField(
        "Sarlavha", max_length=120, default="FULL-STACK\nDASTURCHI",
        help_text="Yangi qatorga tushirish uchun Enter bosing.",
    )
    subtitle = models.TextField(
        "Tavsif",
        default="Zamonaviy va foydali veb-ilovalarni yaratishga qiziqaman.",
    )
    button_text = models.CharField("Tugma matni", max_length=60, default="Loyiha boshlash")
    button_link = models.CharField("Tugma havolasi", max_length=100, default="#projects")

    class Meta:
        verbose_name = "Hero (bosh ekran)"
        verbose_name_plural = "Hero (bosh ekran)"

    def __str__(self):
        return "Hero"


class AboutSection(SingletonModel):
    title = models.CharField("Sarlavha", max_length=100, default="Men haqimda")
    subtitle = models.TextField("Qo'shimcha matn", blank=True)

    class Meta:
        verbose_name = "Men haqimda — sarlavha"
        verbose_name_plural = "Men haqimda — sarlavha"

    def __str__(self):
        return "Men haqimda"


class AboutItem(models.Model):
    label = models.CharField("Nomi", max_length=60, help_text="Masalan: Ism, Manzil")
    value = models.CharField("Qiymati", max_length=200)
    order = models.PositiveIntegerField("Tartib", default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Men haqimda — qator"
        verbose_name_plural = "Men haqimda — qatorlar"

    def __str__(self):
        return f"{self.label}: {self.value}"


class ProjectSection(SingletonModel):
    title = models.CharField("Sarlavha", max_length=100, default="Avvalgi loyihalarim")
    subtitle = models.CharField(
        "Qo'shimcha matn", max_length=200,
        default="Mening ishlarim va dasturiy yechimlarim",
    )
    empty_text = models.CharField(
        "Bo'sh holat matni", max_length=200,
        default="Loyihalar tez orada qo'shiladi.",
    )

    class Meta:
        verbose_name = "Loyihalar — sarlavha"
        verbose_name_plural = "Loyihalar — sarlavha"

    def __str__(self):
        return "Loyihalar bo'limi"


class Project(models.Model):
    title = models.CharField("Loyiha nomi", max_length=120)
    description = models.TextField("Tavsif")
    image = models.ImageField(
        "Rasm", upload_to="loyihalar/", blank=True, null=True,
        storage=_db_storage,
        help_text="Kompyuteringizdan rasm tanlang.",
    )
    live_url = models.URLField(
        "Sayt havolasi", blank=True,
        help_text="Agar loyiha veb-sayt bo'lsa, manzilini kiriting.",
    )
    github_url = models.URLField("GitHub havolasi", blank=True)
    tech_stack = models.CharField(
        "Texnologiyalar", max_length=200, blank=True,
        help_text="Vergul bilan ajrating: Django, PostgreSQL, JavaScript",
    )
    order = models.PositiveIntegerField("Tartib", default=0)
    is_published = models.BooleanField("Saytda ko'rinsin", default=True)
    created_at = models.DateTimeField("Qo'shilgan sana", auto_now_add=True)

    class Meta:
        ordering = ["order", "-created_at"]
        verbose_name = "Loyiha"
        verbose_name_plural = "Loyihalar"

    def __str__(self):
        return self.title

    def tech_list(self):
        return [t.strip() for t in self.tech_stack.split(",") if t.strip()]


class Contact(SingletonModel):
    section_title = models.CharField(
        "Sarlavha", max_length=100, default="Keling, birga ishlaymiz!"
    )
    section_subtitle = models.CharField("Qo'shimcha matn", max_length=200, blank=True)
    email = models.EmailField("Email", blank=True)
    phone = models.CharField("Telefon", max_length=40, blank=True)
    show_phone = models.BooleanField(
        "Telefon saytda ko'rinsin", default=False,
        help_text="Ochiq raqam spam yig'uvchi botlar nishoniga aylanadi.",
    )
    github_username = models.CharField("GitHub foydalanuvchi nomi", max_length=60, blank=True)
    github_url = models.URLField("GitHub havolasi", blank=True)
    telegram_url = models.URLField("Telegram havolasi", blank=True)
    linkedin_url = models.URLField("LinkedIn havolasi", blank=True)

    form_name_label = models.CharField("Forma: ism maydoni", max_length=60, default="Ismingiz")
    form_email_label = models.CharField("Forma: email maydoni", max_length=60, default="Email")
    form_message_label = models.CharField("Forma: xabar maydoni", max_length=60, default="Xabar")
    form_button_text = models.CharField("Forma: tugma matni", max_length=60, default="Yuborish")
    form_success_text = models.CharField(
        "Forma: muvaffaqiyat matni", max_length=200,
        default="Xabaringiz yuborildi. Tez orada bog'lanaman.",
    )

    class Meta:
        verbose_name = "Aloqa"
        verbose_name_plural = "Aloqa"

    def __str__(self):
        return "Aloqa"


class Message(models.Model):
    name = models.CharField("Ism", max_length=120)
    email = models.EmailField("Email")
    message = models.TextField("Xabar")
    created_at = models.DateTimeField("Kelgan vaqti", auto_now_add=True)
    is_read = models.BooleanField("O'qilgan", default=False)
    sent_to_telegram = models.BooleanField("Telegramga yuborildi", default=False)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Kelgan xabar"
        verbose_name_plural = "Kelgan xabarlar"

    def __str__(self):
        return f"{self.name} — {self.created_at:%d.%m.%Y %H:%M}"
