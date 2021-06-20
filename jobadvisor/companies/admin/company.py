"""Company admin."""
from django import forms
from django.contrib import admin
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _

from jobadvisor.companies.models import Company
from jobadvisor.users.models import User

from .subscription import SubscriptionInline
from .vacancy import VacancyInline


class CompanyForm(forms.ModelForm):
    """Company admin form."""

    class Meta:
        """Meta."""

        model = Company
        fields: list = [
            "owner",
            "is_validated",
            "is_banned",
        ]

    def clean_owner(self):
        """
        Validate owner.

        :return: User
        """
        owner: User = self.cleaned_data.get("owner")
        if not self.instance.owner == owner:
            if hasattr(owner, "company"):
                raise forms.ValidationError(_("User already has company"))
            if not owner.level == User.EMPLOYER:
                raise forms.ValidationError(
                    _("Only the employer can be the owner"))
            if owner.workings.exists():
                raise forms.ValidationError(_("Owner should not have works"))
        return owner


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    """Company admin."""

    model = Company
    form = CompanyForm
    list_display: tuple = ("id", "name", "owner")
    list_display_links: tuple = list_display
    list_filter: tuple = ("is_validated", "is_banned")
    search_fields: tuple = ("name", "website", "description")
    ordering: tuple = ("id", "name")
    inlines: list = [SubscriptionInline, VacancyInline]
    readonly_fields: tuple = (
        "owner_phone",
        "owner_email",

        "name",
        "logo_img",
        "founded",
        "industry",
        "website",
        "size",
        "description",

        "deleted_at",

        "workers",
    )
    fieldsets: tuple = (
        (_("Owner info"), {"fields": (
            (
                "owner",
                "owner_phone",
                "owner_email",
            ),
        )}
         ),
        (_("Company Info"), {"fields": (
            "name",
            "logo_img",
            "founded",
            "industry",
            "website",
            "size",
            "description",
        )}),
        (_("Company parameters"), {"fields": (
            "deleted_at",
            (
                "is_validated",
                "is_best",
                "is_banned",
            ),
        )}),
        (_("Workers"), {"fields": ("workers",)}),
    )
    autocomplete_fields: tuple = ("owner",)

    def has_add_permission(self, request: HttpRequest) -> bool:
        """
        Check add permission.

        :param request:
        :return: False
        """
        return False
