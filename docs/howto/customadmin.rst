*******************************
Make custom admins translatable
*******************************

All you have to do is to extend the custom admin you want to make translatable
with the :class:`~translations.admin.TranslatableAdminMixin` functionalities.

Take `django-nested-inline`_ library for example.

.. _`django-nested-inline`: https://github.com/s-block/django-nested-inline

To make it translatable you can do:

.. code-block:: python

   from django.contrib.contenttypes.admin import GenericStackedInline
   from nested_inline.admin import NestedStackedInline, NestedModelAdmin
   from translations.admin import TranslatableAdminMixin
   from translations.models import Translation


   class TranslationInline(NestedStackedInline, GenericStackedInline):
       """This can be used like our own `TranslationInline`."""
       model = Translation
       extra = 1

   class TranslatableAdmin(TranslatableAdminMixin, NestedModelAdmin):
       """
       This can be used like django-nested-inlines `NestedModelAdmin` but
       it's translatable.
       """

       def get_inline_instances(self, request, obj=None):
           """Override this method in the custom admin."""
           inlines = list(
               super(TranslatableAdmin, self).get_inline_instances(
                   request,
                   obj
               )
           )
           # use `TranslatableAdminMixin.prepare_translation_inlines`
           self.prepare_translation_inlines(inlines, TranslationInline)
           return inlines

   class TranslatableInline(TranslatableAdminMixin, NestedStackedInline):
       """
       This can be used like django-nested-inlines `NestedStackedInline` but
       it's translatable.
       """

       def get_inline_instances(self, request, obj=None):
           """Override this method in the custom admin."""
           inlines = list(
               super(TranslatableInline, self).get_inline_instances(
                   request,
                   obj
               )
           )
           # use `TranslatableAdminMixin.prepare_translation_inlines`
           self.prepare_translation_inlines(inlines, TranslationInline)
           return inlines
