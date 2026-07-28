from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import (
    AboutItem, AboutSection, Contact, Hero, Message,
    NavItem, Project, ProjectSection, SiteSettings,
)

admin.site.site_header = "Portfolio boshqaruvi"
admin.site.site_title = "Portfolio"
admin.site.index_title = "Saytdagi hamma narsani shu yerdan o'zgartirasiz"


class SingletonAdmin(admin.ModelAdmin):
    """Bitta yozuvli sozlama modellari uchun."""

    def has_add_permission(self, request):
        return not self.model.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        from django.shortcuts import redirect
        from django.urls import reverse
        obj = self.model.load()
        url = reverse(
            f"admin:{self.model._meta.app_label}_{self.model._meta.model_name}_change",
            args=[obj.pk],
        )
        return redirect(url)


def _thumb(image, height=60):
    if not image:
        return "—"
    return format_html(
        '<img src="{}" style="height:{}px;border-radius:6px;object-fit:cover;">',
        image.url, height,
    )


@admin.register(SiteSettings)
class SiteSettingsAdmin(SingletonAdmin):
    fieldsets = (
        ("Umumiy", {"fields": ("logo_text", "footer_text")}),
        ("Rasmlar va fayllar", {"fields": ("profile_image", "preview", "favicon", "cv_file")}),
    )
    readonly_fields = ("preview",)

    @admin.display(description="Profil rasmi ko'rinishi")
    def preview(self, obj):
        return _thumb(obj.profile_image, 120)


@admin.register(NavItem)
class NavItemAdmin(admin.ModelAdmin):
    list_display = ("label", "anchor", "order", "is_active", "is_button")
    list_editable = ("anchor", "order", "is_active", "is_button")
    ordering = ("order",)


@admin.register(Hero)
class HeroAdmin(SingletonAdmin):
    fields = ("badge_text", "title", "subtitle", "button_text", "button_link")


@admin.register(AboutSection)
class AboutSectionAdmin(SingletonAdmin):
    fields = ("title", "subtitle")


@admin.register(AboutItem)
class AboutItemAdmin(admin.ModelAdmin):
    list_display = ("label", "value", "order")
    list_editable = ("value", "order")
    ordering = ("order",)


@admin.register(ProjectSection)
class ProjectSectionAdmin(SingletonAdmin):
    fields = ("title", "subtitle", "empty_text")


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("thumb", "title", "tech_stack", "order", "is_published", "amallar")
    list_display_links = ("thumb", "title")
    list_editable = ("order", "is_published")
    search_fields = ("title", "description", "tech_stack")
    readonly_fields = ("preview", "created_at")
    fieldsets = (
        ("Asosiy", {"fields": ("title", "description", "tech_stack")}),
        ("Rasm", {"fields": ("image", "preview")}),
        ("Havolalar", {"fields": ("live_url", "github_url")}),
        ("Ko'rsatish", {"fields": ("order", "is_published", "created_at")}),
    )

    @admin.display(description="Rasm")
    def thumb(self, obj):
        return _thumb(obj.image, 45)

    @admin.display(description="Amallar")
    def amallar(self, obj):
        edit_url = reverse("admin:core_project_change", args=[obj.pk])
        del_url = reverse("admin:core_project_delete", args=[obj.pk])
        return format_html(
            '<a href="{}" title="Tahrirlash" '
            'style="text-decoration:none;font-size:16px;margin-right:12px;">✏️</a>'
            '<a href="{}" title="O\'chirish" '
            'style="text-decoration:none;font-size:16px;color:#dc3545;">🗑️</a>',
            edit_url, del_url,
        )

    @admin.display(description="Ko'rinishi")
    def preview(self, obj):
        return _thumb(obj.image, 180)


@admin.register(Contact)
class ContactAdmin(SingletonAdmin):
    fieldsets = (
        ("Sarlavha", {"fields": ("section_title", "section_subtitle")}),
        ("Aloqa ma'lumotlari", {
            "fields": ("email", "phone", "show_phone",
                       "github_username", "github_url", "telegram_url", "linkedin_url"),
        }),
        ("Forma matnlari", {
            "fields": ("form_name_label", "form_email_label", "form_message_label",
                       "form_button_text", "form_success_text"),
        }),
    )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "short_message", "created_at", "is_read", "sent_to_telegram")
    list_filter = ("is_read", "sent_to_telegram", "created_at")
    search_fields = ("name", "email", "message")
    readonly_fields = ("name", "email", "message", "created_at", "sent_to_telegram")
    actions = ("mark_read",)

    def has_add_permission(self, request):
        return False

    @admin.display(description="Xabar")
    def short_message(self, obj):
        return obj.message[:60] + ("…" if len(obj.message) > 60 else "")

    @admin.action(description="O'qilgan deb belgilash")
    def mark_read(self, request, queryset):
        queryset.update(is_read=True)
