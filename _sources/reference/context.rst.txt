******************
Reference: Context
******************

.. module:: translations.context

This module contains the context managers for the Translations app.

.. important::

   The examples are assumed to CRUD this dataset.

   +---------------+-------------+-------------+
   | Type\\Lang    | English     | German      |
   +===============+=============+=============+
   | Continent     | Europe      | Europa      |
   |               +-------------+-------------+
   |               | Asia        | Asien       |
   +---------------+-------------+-------------+
   | Country       | Germany     | Deutschland |
   |               +-------------+-------------+
   |               | South Korea | Südkorea    |
   +---------------+-------------+-------------+
   | City          | Cologne     | Köln        |
   |               +-------------+-------------+
   |               | Seoul       | Seul        |
   +---------------+-------------+-------------+

   Please memorize this dataset in order to understand the examples better.

.. class:: Context

   A context manager which provides custom translation functionalities.

   Provides CRUD functionalities like
   :meth:`create`, :meth:`read`, :meth:`update` and :meth:`delete`
   to work with the translations and also some other functionalities like
   :meth:`reset`
   to manage the :class:`Context`.

   .. testsetup:: Context.1

      create_doc_samples(translations=True)

   To use :class:`Context`:

   .. testcode:: Context.1

      from translations.context import Context
      from sample.models import Continent

      continents = Continent.objects.all()
      relations = ('countries', 'countries__cities',)

      with Context(continents, *relations) as context:
          context.read('de')    # read the translations onto the context
          print(':')            # use the objects like before
          print(continents)
          print(continents[0].countries.all())
          print(continents[0].countries.all()[0].cities.all())

          continents[0].countries.all()[0].name = 'Change the name'
          context.update('de')  # update the translations from the context

          context.delete('de')  # delete the translations of the context

          context.reset()       # reset the translations of the context
          print(':')            # use the objects like before
          print(continents)
          print(continents[0].countries.all())
          print(continents[0].countries.all()[0].cities.all())

   .. testoutput:: Context.1

      :
      <TranslatableQuerySet [
          <Continent: Europa>,
          <Continent: Asien>,
      ]>
      <TranslatableQuerySet [
          <Country: Deutschland>,
      ]>
      <TranslatableQuerySet [
          <City: Köln>,
      ]>
      :
      <TranslatableQuerySet [
          <Continent: Europe>,
          <Continent: Asia>,
      ]>
      <TranslatableQuerySet [
          <Country: Germany>,
      ]>
      <TranslatableQuerySet [
          <City: Cologne>,
      ]>

   .. method:: __init__(entity, *relations)

      Initialize a :class:`Context` for an entity and some relations of it.

      Defines the entity and the relations of it as
      the :class:`Context`\ 's purview.

      :param entity: The entity to initialize the :class:`Context` for.
      :type entity: ~django.db.models.Model or
          ~collections.Iterable(~django.db.models.Model)
      :param relations: The relations of the entity to initialize
          the :class:`Context` for.
          Each relation may be divided into separate parts
          by :data:`~django.db.models.constants.LOOKUP_SEP`
          (usually ``__``) to represent a deeply nested relation.
          Each part must be a ``related_name``.
      :type relations: list(str)
      :raise TypeError:

          - If the entity is neither a model instance nor
            an iterable of model instances.

          - If the model of the entity is
            not :class:`~translations.models.Translatable`.

          - If the models of the relations are
            not :class:`~translations.models.Translatable`.

      .. testsetup:: Context.__init__.1

         create_doc_samples(translations=True)

      .. testsetup:: Context.__init__.2

         create_doc_samples(translations=True)

      .. testsetup:: Context.__init__.3

         create_doc_samples(translations=True)

      To Initialize a :class:`Context` for an entity (an instance)
      and some relations of it:

      .. testcode:: Context.__init__.1

         from translations.context import Context
         from sample.models import Continent

         europe = Continent.objects.get(code='EU')
         relations = ('countries', 'countries__cities',)

         # initialize context
         with Context(europe, *relations) as context:
             print('Context Initialized!')

      .. testoutput:: Context.__init__.1

         Context Initialized!

      To Initialize a :class:`Context` for an entity (a queryset)
      and some relations of it:

      .. testcode:: Context.__init__.2

         from translations.context import Context
         from sample.models import Continent

         continents = Continent.objects.all()
         relations = ('countries', 'countries__cities',)

         # initialize context
         with Context(continents, *relations) as context:
             print('Context Initialized!')

      .. testoutput:: Context.__init__.2

         Context Initialized!

      To Initialize a :class:`Context` for an entity (a list of instances)
      and some relations of it:

      .. testcode:: Context.__init__.3

         from translations.context import Context
         from sample.models import Continent

         continents = list(Continent.objects.all())
         relations = ('countries', 'countries__cities',)

         # initialize context
         with Context(continents, *relations) as context:
             print('Context Initialized!')

      .. testoutput:: Context.__init__.3

         Context Initialized!

      .. note::

         It is **recommended** for the relations of the entity to be
         prefetched before initializing a :class:`Context`,
         in order to reach optimal performance.

         To do this use
         :meth:`~django.db.models.query.QuerySet.select_related`,
         :meth:`~django.db.models.query.QuerySet.prefetch_related` or
         :func:`~django.db.models.prefetch_related_objects`.

   .. method:: _get_changed_fields()

      Yield the info about the changed fields in
      the :class:`Context`\ 's purview.

      Yields the info about the changed fields in
      the :attr:`TranslatableMeta.fields \
      <translations.models.Translatable.TranslatableMeta.fields>` of the
      :class:`Context`\ 's purview.

      :return: The info about the changed fields in
          the :class:`Context`\ 's purview.
      :rtype: ~collections.Iterable(tuple(dict, str))

      .. testsetup:: Context._get_changed_fields.1

         create_doc_samples(translations=False)

      To get the info about the changed fields in
      the :class:`Context`\ 's purview:

      .. testcode:: Context._get_changed_fields.1

         from translations.context import Context
         from sample.models import Continent

         europe = Continent.objects.get(code='EU')

         with Context(europe) as context:

             # change the instance like before
             europe.name = 'Europa'
             europe.denonym = 'Europäisch'

             # get the change fields
             changed = [info[1]
                        for info in context._get_changed_fields()]

             print(changed)

      .. testoutput:: Context._get_changed_fields.1

         [
             'Europa',
             'Europäisch',
         ]

   .. method:: create(lang=None)

      Create the translations of the :class:`Context`\ 's purview in
      a language.

      Creates the translations using the :attr:`TranslatableMeta.fields \
      <translations.models.Translatable.TranslatableMeta.fields>` of the
      :class:`Context`\ 's purview in a language.

      :param lang: The language to create the translations in.
          ``None`` means use the :term:`active language` code.
      :type lang: str or None
      :raise ValueError: If the language code is not supported.
      :raise ~django.db.utils.IntegrityError: If duplicate translations
          are created for a specific field of a unique instance in a
          language.

      .. testsetup:: Context.create.1

         create_doc_samples(translations=False)

      .. testsetup:: Context.create.2

         create_doc_samples(translations=False)

      .. testsetup:: Context.create.3

         create_doc_samples(translations=False)

      To create the translations of the :class:`Context`\ 's purview
      (an instance and some relations of it):

      .. testcode:: Context.create.1

         from translations.context import Context
         from sample.models import Continent

         europe = Continent.objects.get(code='EU')
         relations = ('countries', 'countries__cities',)

         with Context(europe, *relations) as context:

             # change the instance like before
             europe.name = 'Europa'
             europe.countries.all()[0].name = 'Deutschland'
             europe.countries.all()[0].cities.all()[0].name = 'Köln'

             # create the translations in German
             context.create('de')

             print('Translations created!')

      .. testoutput:: Context.create.1

         Translations created!

      To create the translations of the :class:`Context`\ 's purview
      (a queryset and some relations of it):

      .. testcode:: Context.create.2

         from translations.context import Context
         from sample.models import Continent

         continents = Continent.objects.all()
         relations = ('countries', 'countries__cities',)

         with Context(continents, *relations) as context:

             # change the queryset like before
             continents[0].name = 'Europa'
             continents[0].countries.all()[0].name = 'Deutschland'
             continents[0].countries.all()[0].cities.all()[0].name = 'Köln'

             # create the translations in German
             context.create('de')

             print('Translations created!')

      .. testoutput:: Context.create.2

         Translations created!

      To create the translations of the :class:`Context`\ 's purview
      (a list of instances and some relations of it):

      .. testcode:: Context.create.3

         from translations.context import Context
         from sample.models import Continent

         continents = list(Continent.objects.all())
         relations = ('countries', 'countries__cities',)

         with Context(continents, *relations) as context:

             # change the list of instances like before
             continents[0].name = 'Europa'
             continents[0].countries.all()[0].name = 'Deutschland'
             continents[0].countries.all()[0].cities.all()[0].name = 'Köln'

             # create the translations in German
             context.create('de')

             print('Translations created!')

      .. testoutput:: Context.create.3

         Translations created!

      .. note::

         Creating only affects the translatable fields that have changed.

         If the value of a field is not changed, the translation for it is not
         created. (No need to set all the translatable fields beforehand)

   .. method:: read(lang=None)

      Read the translations of the :class:`Context`\ 's purview in
      a language.

      Reads the translations onto the :attr:`TranslatableMeta.fields \
      <translations.models.Translatable.TranslatableMeta.fields>` of the
      :class:`Context`\ 's purview in a language.

      :param lang: The language to read the translations in.
          ``None`` means use the :term:`active language` code.
      :type lang: str or None
      :raise ValueError: If the language code is not supported.

      .. testsetup:: Context.read.1

         create_doc_samples(translations=True)

      .. testsetup:: Context.read.2

         create_doc_samples(translations=True)

      .. testsetup:: Context.read.3

         create_doc_samples(translations=True)

      To read the translations of the :class:`Context`\ 's purview
      (an instance and some relations of it):

      .. testcode:: Context.read.1

         from translations.context import Context
         from sample.models import Continent

         europe = Continent.objects.get(code='EU')
         relations = ('countries', 'countries__cities',)

         with Context(europe, *relations) as context:

             # read the translations in German
             context.read('de')

             # use the instance like before
             print(europe)
             print(europe.countries.all())
             print(europe.countries.all()[0].cities.all())

      .. testoutput:: Context.read.1

         Europa
         <TranslatableQuerySet [
             <Country: Deutschland>,
         ]>
         <TranslatableQuerySet [
             <City: Köln>,
         ]>

      To read the translations of the :class:`Context`\ 's purview
      (a queryset and some relations of it):

      .. testcode:: Context.read.2

         from translations.context import Context
         from sample.models import Continent

         continents = Continent.objects.all()
         relations = ('countries', 'countries__cities',)

         with Context(continents, *relations) as context:

             # read the translations in German
             context.read('de')

             # use the queryset like before
             print(continents)
             print(continents[0].countries.all())
             print(continents[0].countries.all()[0].cities.all())

      .. testoutput:: Context.read.2

         <TranslatableQuerySet [
             <Continent: Europa>,
             <Continent: Asien>,
         ]>
         <TranslatableQuerySet [
             <Country: Deutschland>,
         ]>
         <TranslatableQuerySet [
             <City: Köln>,
         ]>

      To read the translations of the :class:`Context`\ 's purview
      (a list of instances and some relations of it):

      .. testcode:: Context.read.3

         from translations.context import Context
         from sample.models import Continent

         continents = list(Continent.objects.all())
         relations = ('countries', 'countries__cities',)

         with Context(continents, *relations) as context:

             # read the translations in German
             context.read('de')

             # use the list of instances like before
             print(continents)
             print(continents[0].countries.all())
             print(continents[0].countries.all()[0].cities.all())

      .. testoutput:: Context.read.3

         [
             <Continent: Europa>,
             <Continent: Asien>,
         ]
         <TranslatableQuerySet [
             <Country: Deutschland>,
         ]>
         <TranslatableQuerySet [
             <City: Köln>,
         ]>

      .. note::

         Reading only affects the translatable fields that have a translation.

         If there is no translation for a field, the value of the field is not
         changed. (It remains what it was before)

      .. warning::

         .. testsetup:: Context.read.warning.1

            create_doc_samples(translations=True)

         .. testsetup:: Context.read.warning.2

            create_doc_samples(translations=True)

         Any methods on the relations queryset which imply
         a database query will reset previously translated results:

         .. testcode:: Context.read.warning.1

            from translations.context import Context
            from sample.models import Continent

            continents = Continent.objects.prefetch_related(
                'countries',
            )

            with Context(continents, 'countries') as context:
                context.read('de')
                # querying after translation
                print(continents[0].countries.exclude(name=''))

         .. testoutput:: Context.read.warning.1

            <TranslatableQuerySet [
                <Country: Germany>,
            ]>

         In some cases the querying can be done before the translation:

         .. testcode:: Context.read.warning.2

            from django.db.models import Prefetch
            from translations.context import Context
            from sample.models import Continent, Country

            # querying before translation
            continents = Continent.objects.prefetch_related(
                Prefetch(
                    'countries',
                    queryset=Country.objects.exclude(name=''),
                ),
            )

            with Context(continents, 'countries') as context:
                context.read('de')
                print(continents[0].countries.all())

         .. testoutput:: Context.read.warning.2

            <TranslatableQuerySet [
                <Country: Deutschland>,
            ]>

   .. method:: update(lang=None)

      Update the translations of the :class:`Context`\ 's purview in
      a language.

      Updates the translations using the :attr:`TranslatableMeta.fields \
      <translations.models.Translatable.TranslatableMeta.fields>` of the
      :class:`Context`\ 's purview in a language.

      :param lang: The language to update the translations in.
          ``None`` means use the :term:`active language` code.
      :type lang: str or None
      :raise ValueError: If the language code is not supported.

      .. testsetup:: Context.update.1

         create_doc_samples(translations=True)

      .. testsetup:: Context.update.2

         create_doc_samples(translations=True)

      .. testsetup:: Context.update.3

         create_doc_samples(translations=True)

      To update the translations of the :class:`Context`\ 's purview
      (an instance and some relations of it):

      .. testcode:: Context.update.1

         from translations.context import Context
         from sample.models import Continent

         europe = Continent.objects.get(code='EU')
         relations = ('countries', 'countries__cities',)

         with Context(europe, *relations) as context:

             # change the instance like before
             europe.name = 'Europa (changed)'
             europe.countries.all()[0].name = 'Deutschland (changed)'
             europe.countries.all()[0].cities.all()[0].name = 'Köln (changed)'

             # update the translations in German
             context.update('de')

             print('Translations updated!')

      .. testoutput:: Context.update.1

         Translations updated!

      To update the translations of the :class:`Context`\ 's purview
      (a queryset and some relations of it):

      .. testcode:: Context.update.2

         from translations.context import Context
         from sample.models import Continent

         continents = Continent.objects.all()
         relations = ('countries', 'countries__cities',)

         with Context(continents, *relations) as context:

             # change the queryset like before
             continents[0].name = 'Europa (changed)'
             continents[0].countries.all()[0].name = 'Deutschland (changed)'
             continents[0].countries.all()[0].cities.all()[0].name = 'Köln (changed)'

             # update the translations in German
             context.update('de')

             print('Translations updated!')

      .. testoutput:: Context.update.2

         Translations updated!

      To update the translations of the :class:`Context`\ 's purview
      (a list of instances and some relations of it):

      .. testcode:: Context.update.3

         from translations.context import Context
         from sample.models import Continent

         continents = list(Continent.objects.all())
         relations = ('countries', 'countries__cities',)

         with Context(continents, *relations) as context:

             # change the list of instances like before
             continents[0].name = 'Europa (changed)'
             continents[0].countries.all()[0].name = 'Deutschland (changed)'
             continents[0].countries.all()[0].cities.all()[0].name = 'Köln (changed)'

             # update the translations in German
             context.update('de')

             print('Translations updated!')

      .. testoutput:: Context.update.3

         Translations updated!

      .. note::

         Updating only affects the translatable fields that have changed.

         If the value of a field is not changed, the translation for it is not
         updated. (No need to initialize all the translatable fields beforehand)

   .. method:: delete(lang=None)

      Delete the translations of the :class:`Context`\ 's purview in
      a language.

      Deletes the translations for the :attr:`TranslatableMeta.fields \
      <translations.models.Translatable.TranslatableMeta.fields>` of the
      :class:`Context`\ 's purview in a language.

      :param lang: The language to delete the translations in.
          ``None`` means use the :term:`active language` code.
      :type lang: str or None
      :raise ValueError: If the language code is not supported.

      .. testsetup:: Context.delete.1

         create_doc_samples(translations=True)

      .. testsetup:: Context.delete.2

         create_doc_samples(translations=True)

      .. testsetup:: Context.delete.3

         create_doc_samples(translations=True)

      To delete the translations of the :class:`Context`\ 's purview
      (an instance and some relations of it):

      .. testcode:: Context.delete.1

         from translations.context import Context
         from sample.models import Continent

         europe = Continent.objects.get(code='EU')
         relations = ('countries', 'countries__cities',)

         with Context(europe, *relations) as context:

             # delete the translations in German
             context.delete('de')

             print('Translations deleted!')

      .. testoutput:: Context.delete.1

         Translations deleted!

      To delete the translations of the :class:`Context`\ 's purview
      (a queryset and some relations of it):

      .. testcode:: Context.delete.2

         from translations.context import Context
         from sample.models import Continent

         continents = Continent.objects.all()
         relations = ('countries', 'countries__cities',)

         with Context(continents, *relations) as context:

             # delete the translations in German
             context.delete('de')

             print('Translations deleted!')

      .. testoutput:: Context.delete.2

         Translations deleted!

      To delete the translations of the :class:`Context`\ 's purview
      (a list of instances and some relations of it):

      .. testcode:: Context.delete.3

         from translations.context import Context
         from sample.models import Continent

         continents = list(Continent.objects.all())
         relations = ('countries', 'countries__cities',)

         with Context(continents, *relations) as context:

             # delete the translations in German
             context.delete('de')

             print('Translations deleted!')

      .. testoutput:: Context.delete.3

         Translations deleted!

   .. method:: reset()

      Reset the translations of the :class:`Context`\ 's purview to
      the :term:`default language`.

      Resets the translations on the :attr:`TranslatableMeta.fields \
      <translations.models.Translatable.TranslatableMeta.fields>` of the
      :class:`Context`\ 's purview to the :term:`default language`.

      .. testsetup:: Context.reset.1

         create_doc_samples(translations=True)

      .. testsetup:: Context.reset.2

         create_doc_samples(translations=True)

      .. testsetup:: Context.reset.3

         create_doc_samples(translations=True)

      To reset the translations of the :class:`Context`\ 's purview
      (an instance and some relations of it):

      .. testcode:: Context.reset.1

         from translations.context import Context
         from sample.models import Continent

         europe = Continent.objects.get(code='EU')
         relations = ('countries', 'countries__cities',)

         with Context(europe, *relations) as context:

             # changes happened to the fields, create, read, update, delete, etc...
             context.read('de')

             # reset the translations
             context.reset()

             # use the instance like before
             print(europe)
             print(europe.countries.all())
             print(europe.countries.all()[0].cities.all())

      .. testoutput:: Context.reset.1

         Europe
         <TranslatableQuerySet [
             <Country: Germany>,
         ]>
         <TranslatableQuerySet [
             <City: Cologne>,
         ]>

      To reset the translations of the :class:`Context`\ 's purview
      (a queryset and some relations of it):

      .. testcode:: Context.reset.2

         from translations.context import Context
         from sample.models import Continent

         continents = Continent.objects.all()
         relations = ('countries', 'countries__cities',)

         with Context(continents, *relations) as context:

             # changes happened to the fields, create, read, update, delete, etc...
             context.read('de')

             # reset the translations
             context.reset()

             # use the queryset like before
             print(continents)
             print(continents[0].countries.all())
             print(continents[0].countries.all()[0].cities.all())

      .. testoutput:: Context.reset.2

         <TranslatableQuerySet [
             <Continent: Europe>,
             <Continent: Asia>,
         ]>
         <TranslatableQuerySet [
             <Country: Germany>,
         ]>
         <TranslatableQuerySet [
             <City: Cologne>,
         ]>

      To reset the translations of the :class:`Context`\ 's purview
      (a list of instances and some relations of it):

      .. testcode:: Context.reset.3

         from translations.context import Context
         from sample.models import Continent

         continents = list(Continent.objects.all())
         relations = ('countries', 'countries__cities',)

         with Context(continents, *relations) as context:

             # changes happened to the fields, create, read, update, delete, etc...
             context.read('de')

             # reset the translations
             context.reset()

             # use the list of instances like before
             print(continents)
             print(continents[0].countries.all())
             print(continents[0].countries.all()[0].cities.all())

      .. testoutput:: Context.reset.3

         [
             <Continent: Europe>,
             <Continent: Asia>,
         ]
         <TranslatableQuerySet [
             <Country: Germany>,
         ]>
         <TranslatableQuerySet [
             <City: Cologne>,
         ]>
