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

    def handle_translation_inlines(self, inlines):
        """
        Manipulate the translation inlines based on the admin model.

        Processes the admin model and customizes the translation inlines
        based on that in place.

        A basic usage:

        .. literalinclude:: ../../translations/admin.py
           :pyobject: TranslatableAdmin.get_inline_instances
           :emphasize-lines: 4
        """
        choices = self._get_translation_choices()
        form = generate_translation_form(choices)
        remove_inlines = []
        for i, v in enumerate(inlines):
            if isinstance(v, TranslationInline):
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

    The basic usage:

    .. literalinclude:: ../../sample/admin.py
       :pyobject: ContinentAdmin
       :emphasize-lines: 1
    """
    def get_inline_instances(self, request, obj=None):
        inlines = super(TranslatableAdmin, self).get_inline_instances(request, obj)
        inlines = list(inlines)
        self.handle_translation_inlines(inlines)
        return inlines


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
