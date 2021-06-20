"""Variant admin."""
from django.contrib import admin
from django.forms import forms
from django.forms.models import BaseInlineFormSet
from django.utils.translation import gettext_lazy as _

from jobadvisor.polls.models import Variant


class VariantInlineFormSet(BaseInlineFormSet):
    """Variant admin."""

    def clean(self) -> None:
        """
        Validate variant.

        :return: None
        """
        forms_to_deleted = self.deleted_forms
        valid_forms = [form for form in self.forms if form.is_valid()
                       and form not in forms_to_deleted]
        positive_variants = \
            [form.cleaned_data.get("is_positive") for form in valid_forms]
        if positive_variants.count(True) > 1:
            raise forms.ValidationError(
                [{"variant": [_("You can't choose a few positive variants")]}]
            )
        if not positive_variants.count(True):
            raise forms.ValidationError(
                [{"variant": [_("There must be at least one positive option")]}]
            )

        if not positive_variants.count(False):
            raise forms.ValidationError(
                [{"variant": [_("There must be at least one negative option")]}]
            )
        super().clean()


class VariantInline(admin.StackedInline):
    """Variant inline admin."""

    model = Variant
    max_num = 3
    extra = 2
    readonly_fields = ("weight",)
    formset = VariantInlineFormSet
