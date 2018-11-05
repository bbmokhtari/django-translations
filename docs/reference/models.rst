***********
Ref: Models
***********

.. module:: translations.models

This module contains the models for the Translations app.

.. class:: Translation

   The model which represents the translations.

   Each translation belongs to a *unique* database address. Each address is
   composed of a :attr:`content_type` (table), an :attr:`object_id` (row) and
   a :attr:`field` (column). Each unique address must have only one
   translation :attr:`text` in a specific :attr:`language`.

   .. note::

      :attr:`content_type` and :attr:`object_id` together form something
      called a :class:`~django.contrib.contenttypes.fields.GenericForeignKey`.
      This kind of foreign key contrary to the normal foreign key (which can
      point to a row in only one table) can point to a row in any table.

   .. note::

      :attr:`object_id` is defined as a :class:`~django.db.models.CharField`
      so that it can also point to the rows in the tables which use character
      fields (like :class:`~django.db.models.UUIDField`, etc.) as primary key.

   .. warning::

      Try **not** to work with the :class:`~translations.models.Translation`
      model directly unless you *really* have to and you know what you're
      doing.

   .. testsetup:: Translation.1

      from tests.sample import create_samples

      create_samples(
          continent_names=['europe'],
      )

   To create the translation of a field manually:

   .. testcode:: Translation.1

      from django.contrib.contenttypes.models import ContentType
      from translations.models import Translation
      from sample.models import Continent

      europe = Continent.objects.get(code='EU')

      translation = Translation.objects.create(
          content_type=ContentType.objects.get_for_model(Continent),
          object_id=europe.id,
          field='name',
          language='de',
          text='Europa',
      )

      print(translation)

   .. testoutput:: Translation.1

      Europe: Europa

.. class:: Translatable

   An abstract model which provides custom translation functionalities.

   Marks the subclasses as translatable and creates some default
   configurations for them based on their structure.

   To make a model translatable:

   .. literalinclude:: ../../sample/models.py
      :lines: 4

   .. literalinclude:: ../../sample/models.py
      :pyobject: Continent
      :lines: 1-25
      :emphasize-lines: 1

   It also adds the :attr:`translations` relation to the model, just in case
   any one wants to work with the translations of an instance manually.

   .. note::

      The :attr:`translations` relation is the reverse relation of the
      :class:`~django.contrib.contenttypes.fields.GenericForeignKey`
      described in :class:`~translations.models.Translation`. It's a
      :class:`~django.contrib.contenttypes.fields.GenericRelation`.

   .. class:: TranslatableMeta

      This class contains meta information about the translation
      of the model instances.

      .. attribute:: fields

         The names of the fields to use in the translation.
         
         By default it is set to ``None``.
         This means the translation will use the text based fields
         automatically. (like :class:`~django.db.models.CharField` and
         :class:`~django.db.models.TextField` - this does not include
         :class:`~django.db.models.EmailField` or the fields with ``choices``)

         If needed, it can be set to nothing.
         This can be done by explicitly setting it to ``[]``.

         To set the translatable fields of a model:

         .. literalinclude:: ../../sample/models.py
            :pyobject: Continent
            :emphasize-lines: 1, 27-28

   .. classmethod:: get_translatable_fields(cls)

      Return the model's translatable fields.

      Returns the model's translatable fields based on the
      field names listed in :attr:`TranslatableMeta.fields`.

      :return: The translatable fields of the model.
      :rtype: list(~django.db.models.Field)

      To get the mentioned model's translatable fields:

      .. testcode:: Translatable.get_translatable_fields.1

         from sample.models import Continent

         for field in Continent.get_translatable_fields():
             print(field)

      .. testoutput:: Translatable.get_translatable_fields.1

         sample.Continent.name
         sample.Continent.denonym

   .. classmethod:: _get_translatable_fields_names(cls)

      Return the names of the model's translatable fields.

      Returns the names of the model's translatable fields based on the
      field names listed in :attr:`TranslatableMeta.fields`.

      :return: The names of the model's translatable fields.
      :rtype: list(str)

      To get the names of the mentioned model's translatable fields:

      .. testcode:: Translatable._get_translatable_fields_names.1

         from sample.models import Continent

         for name in Continent._get_translatable_fields_names():
             print(name)

      .. testoutput:: Translatable._get_translatable_fields_names.1

         name
         denonym

   .. classmethod:: _get_translatable_fields_choices(cls)

      Return the choices of the model's translatable fields.

      Returns the choices of the model's translatable fields based on the
      field names listed in :attr:`TranslatableMeta.fields`.

      :return: The choices of the model's translatable fields.
      :rtype: list(tuple(str, str))

      To get the choices of the mentioned model's translatable fields:

      .. testcode:: Translatable._get_translatable_fields_choices.1

         from sample.models import Continent

         for choice in Continent._get_translatable_fields_choices():
             print(choice)

      .. testoutput:: Translatable._get_translatable_fields_choices.1

         (None, '---------')
         ('name', 'name')
         ('denonym', 'denonym')
