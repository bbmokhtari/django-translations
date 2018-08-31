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

    Provides functionalities like :meth:`handle_translation_inlines` to
    manipulate the translation inlines based on the admin model.

    .. note::

       It can be used to make any admin translatable. Not only the default
       admins but also the custom admins.

       Check out :ref:`How to make custom admins translatable?`.
    """

    def _get_translation_choices(self):
        """
        Return the choices made out of the translatable fields.

        Fetches the translatable fields of the admin's model, creates choices
        out of them and then returns them.

        :return: The choices made out of the translatable fields.
        :rtype: list(tuple(str, str))

        To get the choices of a model admin:

        .. testcode::

           from django.contrib.admin import site
           from sample.models import Continent
           from sample.admin import ContinentAdmin

           admin = ContinentAdmin(Continent, site)
           print(admin._get_translation_choices())

        .. testoutput::

           [(None, '---------'), ('name', 'name'), ('denonym', 'denonym')]
        """
        choices = [
            (None, '---------')
        ]
        if issubclass(self.model, Translatable):
            for field in self.model.get_translatable_fields():
                choices.append((field.name, field.verbose_name))
        return choices

    def handle_translation_inlines(self, inlines, thetype):
        """
        Manipulate the translation inlines of one type based on the admin.

        Processes the admin and manipulates the translation inlines of one
        type based on that in place.

        :param inlines: The translation inlines to manipulate based on the
            admin.
        :type inlines: list(~django.contrib.contenttypes.admin
            .GenericStackedInline)
        :param thetype: The type of the inlines.
        :type thetype: type(~django.contrib.contenttypes.admin
            .GenericStackedInline)

        To manipulate translation inlines in place override this in admin:

        .. literalinclude:: ../../translations/admin.py
           :pyobject: TranslatableAdmin.get_inline_instances
           :emphasize-lines: 8
        """
        choices = self._get_translation_choices()
        form = generate_translation_form(choices)
        remove_inlines = []
        for i, v in enumerate(inlines):
            if isinstance(v, thetype):
                if len(choices) == 1:
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
        self.handle_translation_inlines(inlines, TranslationInline)
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
