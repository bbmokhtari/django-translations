from django.contrib.contenttypes.admin import GenericStackedInline
from django.contrib import admin

from .models import Translation, Translatable
from .forms import generate_translation_form


class TranslationInline(GenericStackedInline):
    """
    The admin inline which represents the translations.

    Manages creating, reading, updating and deleting the admin object's
    translation inline objects.

    The basic usage:

    .. literalinclude:: ../../sample/admin.py
       :pyobject: ContinentAdmin
       :emphasize-lines: 2
    """

    model = Translation
    extra = 1


class TranslatableAdminMixin(object):
    """
    An admin mixin which provides custom translation functionalities.

    Provides functionalities like :meth:`handle_translation_inlines` to
    manipulate the translation inlines based on the the parent object
    specifications.
    """

    def _get_translation_choices(self):
        """
        Return the choices made out of the translatable fields.

        Fetches the translatable fields of the admin's model, creates choices
        out of them and then returns them.

        :return: The choices made out of the translatable fields.
        :rtype: list(tuple(str, str))
        """
        choices = [
            (None, '---------')
        ]
        if issubclass(self.model, Translatable):
            for field in self.model.get_translatable_fields():
                choices.append((field.name, field.verbose_name))
        return choices

    def handle_translation_inlines(self, inlines):
        choices = self._get_translation_choices()
        remove_inlines = []
        for i, v in enumerate(inlines):
            if isinstance(v, TranslationInline):
                if len(choices) == 1:
                    remove_inlines.append(i)
                else:
                    inlines[i].form = generate_translation_form(choices)
        remove_inlines.reverse()
        for index in remove_inlines:
            inlines.pop(index)


class TranslatableAdmin(TranslatableAdminMixin, admin.ModelAdmin):
    def get_inline_instances(self, request, obj=None):
        inlines = super(TranslatableAdmin, self).get_inline_instances(request, obj)
        inlines = list(inlines)
        self.handle_translation_inlines(inlines)
        return inlines


"""
from nested_inline.admin import NestedStackedInline, NestedModelAdmin


class TranslationInline(NestedStackedInline, GenericStackedInline):
    model = Translation
    extra = 1


class TranslatableAdmin(TranslatableAdminMixin, NestedModelAdmin):
    def get_inline_instances(self, request, obj=None):
        inlines = super(TranslatableAdmin, self).get_inline_instances(request, obj)
        inlines = list(inlines)
        self.handle_translation_inlines(inlines)
        return inlines


class TranslatableInline(TranslatableAdminMixin, NestedStackedInline):
    def get_inline_instances(self, request, obj=None):
        inlines = super(TranslatableInline, self).get_inline_instances(request, obj)
        inlines = list(inlines)
        self.handle_translation_inlines(inlines)
        return inlines

"""
