"""
This module contains the admins for the Translations app. It contains the
following members:

:class:`TranslatableAdminMixin`
    An admin mixin which provides custom translation functionalities.
:class:`TranslatableAdmin`
    The admin which represents the translatables.
:class:`TranslationInline`
    The admin inline which represents the translations.
"""
from django.contrib.contenttypes.admin import GenericStackedInline
from django.contrib import admin

from .models import Translation, Translatable
from .forms import generate_translation_form


__docformat__ = 'restructuredtext'


class TranslatableAdminMixin(object):
    """
    An admin mixin which provides custom translation functionalities.

    Provides functionalities like :meth:`prepare_translation_inlines` to
    prepare the translation inlines of a specific inline type based on the
    admin model.

    .. note::

       It can be used to make any admin translatable, even the custom admins
       other than the default Django admin.

       Check out :doc:`../howto/customadmin`.
    """

    def prepare_translation_inlines(self, inlines, thetype):
        """
        Prepare the translation inlines of a specific inline type based on the
        admin model.

        Searches the inlines for the translation inlines of the specific
        inline type and prepares the translation inlines based on the admin
        model.

        :param inlines: The admin inlines to prepare.
        :type inlines: list(~django.contrib.admin.InlineModelAdmin)
        :param thetype: The type of the translation inlines.
        :type thetype: type(~django.contrib.contenttypes.admin
            .GenericStackedInline)

        To prepare the translation inlines of a specific inline type based on
        the admin model:

        .. literalinclude:: ../../translations/admin.py
           :pyobject: TranslatableAdmin.get_inline_instances
           :emphasize-lines: 8
        """
        form = generate_translation_form(self.model)
        remove_inlines = []
        for i, v in enumerate(inlines):
            if isinstance(v, thetype):
                if len(form.base_fields['field'].choices) == 1:
                    remove_inlines.append(i)
                else:
                    inlines[i].form = form
        remove_inlines.reverse()
        for index in remove_inlines:
            inlines.pop(index)


class TranslatableAdmin(TranslatableAdminMixin, admin.ModelAdmin):
    """
    The admin which represents the translatables.

    Manages creating, reading, updating and deleting the translatable admin
    object.

    To make an admin translatable:

    .. literalinclude:: ../../sample/admin.py
       :pyobject: ContinentAdmin
       :emphasize-lines: 1
    """
    def get_inline_instances(self, request, obj=None):
        inlines = list(
            super(TranslatableAdmin, self).get_inline_instances(
                request,
                obj
            )
        )
        self.prepare_translation_inlines(inlines, TranslationInline)
        return inlines


class TranslationInline(GenericStackedInline):
    """
    The admin inline which represents the translations.

    Manages creating, reading, updating and deleting the admin object's
    translation inline objects.

    To add translation inlines to a translatable admin:

    .. literalinclude:: ../../sample/admin.py
       :pyobject: ContinentAdmin
       :emphasize-lines: 2
    """

    model = Translation
    extra = 1
