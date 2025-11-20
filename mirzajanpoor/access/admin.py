from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from access.models import User

# Register your models here.


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    search_fields = ["phone_number", "first_name", "last_name"]
    readonly_fields = ["id", "created_at", "updated_at"]
    list_display = ["phone_number", "first_name", "is_active", "is_admin", "created_at"]
    list_filter = ["is_active", "is_admin", "created_at"]
    date_hierarchy = "created_at"
    ordering = ["-created_at"]
    add_fieldsets = (
        (
            _("Details"),
            {
                "fields": [
                    "phone_number",
                    "first_name",
                    "last_name",
                    # "bio",
                ]
            },
        ),
        (
            _("Access"),
            {"fields": ["is_active", "is_admin"]},
        ),
    )
    fieldsets = (
        (
            _("Details"),
            {
                "fields": [
                    "id",
                    # "uuid",
                    "phone_number",
                    "first_name",
                    "last_name",
                    # "bio",
                ]
            },
        ),
        (
            _("Access"),
            {
                "fields": [
                    "is_active",
                    "is_admin",
                    "password",
                ]
            },
        ),
        (_("Dates"), {"fields": ["created_at", "updated_at"]}),
    )

    class Media:
        pass
