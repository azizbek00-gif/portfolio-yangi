"""Saytning boshlang'ich mazmunini yaratadi (menyu va 'Men haqimda' qatorlari).

Loyihalar YARATILMAYDI — ularni admin paneldan o'zingiz qo'shasiz.

Ishlatish:  python manage.py boshlangich
"""
from django.core.management.base import BaseCommand

from core.models import (
    AboutItem, AboutSection, Contact, Hero, NavItem,
    ProjectSection, SiteSettings,
)

NAV = [
    ("Asosiy", "#home", False),
    ("Men haqimda", "#about", False),
    ("Loyihalar", "#projects", False),
    ("Aloqa", "#contact", False),
    ("Bog'lanish", "#contact", True),
]

ABOUT = [
    ("Ism", "Azizbek Omonov"),
    ("Tug'ilgan sana", "2009-06-29"),
    ("Manzil", "Farg'ona shahar"),
    ("O'qish", "Robbit Akademiyasi o'quvchisi"),
]


class Command(BaseCommand):
    help = "Menyu va boshlang'ich matnlarni yaratadi (loyihalarsiz)."

    def handle(self, *args, **options):
        for model in (SiteSettings, Hero, AboutSection, ProjectSection, Contact):
            model.load()
        self.stdout.write("Sozlama yozuvlari tayyor.")

        # Aloqa ma'lumotlari bo'sh bo'lsa — eski sayt qiymatlari bilan to'ldiramiz.
        c = Contact.load()
        changed = False
        if not c.email:
            c.email = "azizbek2004uzbek@gmail.com"; changed = True
        if not c.phone:
            c.phone = "+998 33 996 36 30"; changed = True
        if not c.github_username:
            c.github_username = "azizbek00-gif"; changed = True
        if not c.github_url:
            c.github_url = "https://github.com/azizbek00-gif"; changed = True
        c.show_phone = True
        if changed or True:
            c.save()
            self.stdout.write("Aloqa ma'lumotlari to'ldirildi.")

        if NavItem.objects.exists():
            self.stdout.write("Menyu allaqachon mavjud — o'tkazib yuborildi.")
        else:
            for i, (label, anchor, is_btn) in enumerate(NAV):
                NavItem.objects.create(
                    label=label, anchor=anchor, order=i, is_button=is_btn
                )
            self.stdout.write(f"{len(NAV)} ta menyu elementi qo'shildi.")

        if AboutItem.objects.exists():
            self.stdout.write("'Men haqimda' qatorlari mavjud — o'tkazib yuborildi.")
        else:
            for i, (label, value) in enumerate(ABOUT):
                AboutItem.objects.create(label=label, value=value, order=i)
            self.stdout.write(f"{len(ABOUT)} ta qator qo'shildi.")

        self.stdout.write(self.style.SUCCESS(
            "Tayyor. Qolganini admin paneldan o'zgartirasiz."
        ))
