*****
Admin
*****

.. module:: translations.admin

This module contains the admins for the Translations app.

.. class:: TranslatableAdminMixin

   An admin mixin which provides custom translation functionalities.

   Provides functionalities like :meth:`prepare_translation_inlines` to
   prepare the translation inlines of a type in some inlines based on the
   admin model.

   .. method:: prepare_translation_inlines(self, inlines, inline_type)

      Prepare the translation inlines of a type in some inlines based on the
      admin model.

      Searches the inlines for the translation inlines of the specified
      inline type and prepares the translation inlines based on the admin
      model.

      :param inlines: The inlines which contain the translation inlines to
          prepare.
      :type inlines: list(~django.contrib.admin.InlineModelAdmin)
      :param inline_type: The type of the translation inlines.
      :type inline_type: type(~django.contrib.contenttypes.admin.\
          GenericStackedInline)

      To prepare the translation inlines of a type in some inlines based on
      the admin model:

      .. literalinclude:: ../../translations/admin.py
         :pyobject: TranslationInline

      .. literalinclude:: ../../translations/admin.py
         :pyobject: TranslatableAdmin
         :emphasize-lines: 8

      .. note::

         The code above is exactly how the Translations app makes Django
         admin translatable. It can be used to make any admin translatable.

         Check out :doc:`../howto/customadmin`.

.. class:: TranslatableAdmin

   The admin which represents the :class:`~translations.models.Translatable`
   instances.

   Manages creating, reading, updating and deleting
   the :class:`~translations.models.Translatable` instances.

   To make an admin translatable:

   .. literalinclude:: ../../sample/admin.py
      :lines: 2

   .. literalinclude:: ../../sample/admin.py
      :pyobject: ContinentAdmin
      :emphasize-lines: 1

.. class:: TranslationInline

   The inline which represents the :class:`~translations.models.Translation` instances.

   Manages creating, reading, updating and deleting
   the :class:`~translations.models.Translation` instances.

   To add translation inlines to a translatable admin:

   .. literalinclude:: ../../sample/admin.py
      :lines: 2

   .. literalinclude:: ../../sample/admin.py
      :pyobject: ContinentAdmin
      :emphasize-lines: 2
