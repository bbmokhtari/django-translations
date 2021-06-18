"""This module contains the admins for the Translations app."""

from django.contrib.contenttypes.admin import GenericStackedInline
from django.contrib import admin

from translations.models import Translation
from translations.forms import generate_translation_form


__docformat__ = 'restructuredtext'


class TranslatableAdminMixin:
    """An admin mixin which provides custom translation functionalities."""

    def prepare_translation_inlines(self, inlines, inline_type):
        """
        Prepare the translation inlines of a type in some inlines based on the
        admin model.
        """
        form = generate_translation_form(self.model)
        remove_inlines = []
        for i, v in enumerate(inlines):
            if isinstance(v, inline_type):
                if len(form.base_fields['field'].choices) == 1:
                    remove_inlines.append(i)
                else:
                    inlines[i].form = form
        remove_inlines.reverse()
        for index in remove_inlines:
            inlines.pop(index)


class TranslatableAdmin(TranslatableAdminMixin, admin.ModelAdmin):
    """The admin which represents the `Translatable` instances."""

    def get_inline_instances(self, request, obj=None):
        inlines = list(
            super(TranslatableAdmin, self).get_inline_instances(request, obj)
        )
        self.prepare_translation_inlines(inlines, TranslationInline)
        return inlines


class TranslationInline(GenericStackedInline):
    """The inline which represents the `Translation` instances."""

    model = Translation
    extra = 1
