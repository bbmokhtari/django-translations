*******
Context
*******

.. module:: translations.context

This module contains the context managers for the Translations app.

.. class:: Context

   A context manager which provides custom translation functionalities.

   Provides CRUD functionalities like
   :meth:`create`, :meth:`read`, :meth:`update` and :meth:`delete`
   to work with the translations and also some other functionalities like
   :meth:`reset`
   to manage the :class:`Context`.

   To use :class:`Context`:

   .. testsetup:: Context

      from tests.sample import create_samples

      create_samples(
          continent_names=['europe', 'asia'],
          country_names=['germany', 'south korea'],
          city_names=['cologne', 'seoul'],
          continent_fields=['name', 'denonym'],
          country_fields=['name', 'denonym'],
          city_fields=['name', 'denonym'],
          langs=['de']
      )

   .. testcode:: Context

      from translations.context import Context
      from sample.models import Continent

      continents = Continent.objects.all()
      relations = ('countries', 'countries__cities',)

      with Context(continents, *relations) as context:
          context.read('de')    # read the translations onto the context
          print('----------')   # use the objects like before
          print(continents)
          print(continents[0].countries.all())
          print(continents[0].countries.all()[0].cities.all())

          continents[0].countries.all()[0].name = 'Change the name'
          context.update('de')  # update the translations from the context

          context.delete('de')  # delete the translations of the context

          context.reset()       # reset the translations of the context
          print('----------')   # use the objects like before
          print(continents)
          print(continents[0].countries.all())
          print(continents[0].countries.all()[0].cities.all())

   .. testoutput:: Context

      ----------
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
      ----------
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

      Initialize a :class:`Context` with an entity and some relations of it.

      Defines the entity and the relations of it as
      the :class:`Context`\ 's :term:`purview`.

      :param entity: The entity to use in the :class:`Context`.
      :type entity: ~django.db.models.Model or
          ~collections.Iterable(~django.db.models.Model)
      :param relations: The relations of the entity to use in the :class:`Context`.
      :type relations: list(str)
      :raise TypeError:

          - If the entity is neither a model instance nor
            an iterable of model instances.

          - If the model of the entity is
            not :class:`~translations.models.Translatable`.

          - If the models of the included relations are
            not :class:`~translations.models.Translatable`.

      :raise ~django.core.exceptions.FieldDoesNotExist: If a relation is
          pointing to the fields that don't exist.

      .. testsetup:: init

         from tests.sample import create_samples

         create_samples(
             continent_names=['europe', 'asia'],
             country_names=['germany', 'south korea'],
             city_names=['cologne', 'seoul'],
             continent_fields=['name', 'denonym'],
             country_fields=['name', 'denonym'],
             city_fields=['name', 'denonym'],
             langs=['de']
         )

      To Initialize a :class:`Context` with an entity (an instance)
      and some relations of it:

      .. testcode:: init

         from translations.context import Context
         from sample.models import Continent

         europe = Continent.objects.get(code='EU')
         relations = ('countries', 'countries__cities',)

         # initialize context
         with Context(europe, *relations) as context:
             print('Context Initialized!')

      .. testoutput:: init

         Context Initialized!

      To Initialize a :class:`Context` with an entity (a queryset)
      and some relations of it:

      .. testcode:: init

         from translations.context import Context
         from sample.models import Continent

         continents = Continent.objects.all()
         relations = ('countries', 'countries__cities',)

         # initialize context
         with Context(continents, *relations) as context:
             print('Context Initialized!')

      .. testoutput:: init

         Context Initialized!

      To Initialize a :class:`Context` with an entity (a list of instances)
      and some relations of it:

      .. testcode:: init

         from translations.context import Context
         from sample.models import Continent

         continents = list(Continent.objects.all())
         relations = ('countries', 'countries__cities',)

         # initialize context
         with Context(continents, *relations) as context:
             print('Context Initialized!')

      .. testoutput:: init

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
      the :class:`Context`\ 's :term:`purview`.

      Yields the info about the changed fields using
      the :attr:`translatable fields \
      <translations.models.Translatable.TranslatableMeta.fields>` of the
      :class:`Context`\ 's :term:`purview`.

      :return: The info about the changed fields in
          the :class:`Context`\ 's :term:`purview`.
      :rtype: ~collections.Iterable(tuple(dict, str))

      To get the info about the changed fields in
      the :class:`Context`\ 's :term:`purview`:

      .. testsetup:: _get_changed_fields

         from tests.sample import create_samples

         create_samples(
             continent_names=['europe', 'asia'],
             country_names=['germany', 'south korea'],
             city_names=['cologne', 'seoul'],
             langs=['de']
         )

      .. testcode:: _get_changed_fields

         from translations.context import Context
         from sample.models import Continent

         europe = Continent.objects.get(code='EU')

         with Context(europe) as context:
             # change the field values
             europe.name = 'Europa'
             europe.denonym = 'Europäisch'

             # get the change fields
             changed = [info[1]
                        for info in context._get_changed_fields()]

             print(changed)

      .. testoutput:: _get_changed_fields

         [
             'Europa',
             'Europäisch',
         ]

   .. method:: create(lang=None)

      Create the translations of the :class:`Context`\ 's :term:`purview` in
      a language.

      Creates the translations using the :attr:`translatable fields \
      <translations.models.Translatable.TranslatableMeta.fields>` of the
      :class:`Context`\ 's :term:`purview` in a language.

      :param lang: The language to create the translations in.
          ``None`` means use the :term:`active language` code.
      :type lang: str or None
      :raise ValueError: If the language code is not supported.
      :raise ~django.db.utils.IntegrityError: If duplicate translations
          are created for a specific field of a unique instance in a
          language.

      .. testsetup:: create_0

         from tests.sample import create_samples

         create_samples(
             continent_names=['europe', 'asia'],
             country_names=['germany', 'south korea'],
             city_names=['cologne', 'seoul'],
             langs=['de']
         )

      .. testsetup:: create_1

         from tests.sample import create_samples

         create_samples(
             continent_names=['europe', 'asia'],
             country_names=['germany', 'south korea'],
             city_names=['cologne', 'seoul'],
             langs=['de']
         )

      .. testsetup:: create_2

         from tests.sample import create_samples

         create_samples(
             continent_names=['europe', 'asia'],
             country_names=['germany', 'south korea'],
             city_names=['cologne', 'seoul'],
             langs=['de']
         )

      To create the translations of the :class:`Context`\ 's :term:`purview`
      (an instance and some relations of it):

      .. testcode:: create_0

         from translations.context import Context
         from sample.models import Continent

         europe = Continent.objects.get(code='EU')
         relations = ('countries', 'countries__cities',)

         with Context(europe, *relations) as context:
             # change the field values
             europe.name = 'Europa'
             europe.countries.all()[0].name = 'Deutschland'
             europe.countries.all()[0].cities.all()[0].name = 'Köln'

             # create the translations
             context.create('de')

             print('Translations created!')

      .. testoutput:: create_0

         Translations created!

      To create the translations of the :class:`Context`\ 's :term:`purview`
      (a queryset and some relations of it):

      .. testcode:: create_1

         from translations.context import Context
         from sample.models import Continent

         continents = Continent.objects.all()
         relations = ('countries', 'countries__cities',)

         with Context(continents, *relations) as context:
             # change the field values
             continents[0].name = 'Europa'
             continents[0].countries.all()[0].name = 'Deutschland'
             continents[0].countries.all()[0].cities.all()[0].name = 'Köln'

             # create the translations
             context.create('de')

             print('Translations created!')

      .. testoutput:: create_1

         Translations created!

      To create the translations of the :class:`Context`\ 's :term:`purview`
      (a list of instances and some relations of it):

      .. testcode:: create_2

         from translations.context import Context
         from sample.models import Continent

         continents = list(Continent.objects.all())
         relations = ('countries', 'countries__cities',)

         with Context(continents, *relations) as context:
             # change the field values
             continents[0].name = 'Europa'
             continents[0].countries.all()[0].name = 'Deutschland'
             continents[0].countries.all()[0].cities.all()[0].name = 'Köln'

             # create the translations
             context.create('de')

             print('Translations created!')

      .. testoutput:: create_2

         Translations created!

      .. note::

         Creating only affects the translatable fields that have changed.

         If the value of a field is not changed, the translation for it is not
         created. (No need to set all the translatable fields beforehand)

   .. method:: read(lang=None)

      Read the translations of the :class:`Context`\ 's :term:`purview` in
      a language.

      Applies the translations on the :attr:`translatable fields \
      <translations.models.Translatable.TranslatableMeta.fields>` of the
      :class:`Context`\ 's :term:`purview` in a language.

      :param lang: The language to fetch the translations in.
          ``None`` means use the :term:`active language` code.
      :type lang: str or None
      :raise ValueError: If the language code is not supported.

      .. testsetup:: read

         from tests.sample import create_samples

         create_samples(
             continent_names=['europe', 'asia'],
             country_names=['germany', 'south korea'],
             city_names=['cologne', 'seoul'],
             continent_fields=['name', 'denonym'],
             country_fields=['name', 'denonym'],
             city_fields=['name', 'denonym'],
             langs=['de']
         )

      To read the translations of the :class:`Context`\ 's :term:`purview`
      (an instance and some relations of it):

      .. testcode:: read

         from translations.context import Context
         from sample.models import Continent

         europe = Continent.objects.get(code='EU')
         relations = ('countries', 'countries__cities',)

         with Context(europe, *relations) as context:
             # read the translations
             context.read('de')

             # use the field values
             print(europe.name)
             print(europe.countries.all()[0].name)
             print(europe.countries.all()[0].cities.all()[0].name)

      .. testoutput:: read

         Europa
         Deutschland
         Köln

      To read the translations of the :class:`Context`\ 's :term:`purview`
      (a queryset and some relations of it):

      .. testcode:: read

         from translations.context import Context
         from sample.models import Continent

         continents = Continent.objects.all()
         relations = ('countries', 'countries__cities',)

         with Context(continents, *relations) as context:
             # read the translations
             context.read('de')

             # use the field values
             print(continents[0].name)
             print(continents[0].countries.all()[0].name)
             print(continents[0].countries.all()[0].cities.all()[0].name)

      .. testoutput:: read

         Europa
         Deutschland
         Köln

      To read the translations of the :class:`Context`\ 's :term:`purview`
      (a list of instances and some relations of it):

      .. testcode:: read

         from translations.context import Context
         from sample.models import Continent

         continents = list(Continent.objects.all())
         relations = ('countries', 'countries__cities',)

         with Context(continents, *relations) as context:
             # read the translations
             context.read('de')

             # use the field values
             print(continents[0].name)
             print(continents[0].countries.all()[0].name)
             print(continents[0].countries.all()[0].cities.all()[0].name)

      .. testoutput:: read

         Europa
         Deutschland
         Köln

      .. note::

         Reading only affects the translatable fields that have a translation.

         If there is no translation for a field, the value of the field is not
         changed. (It remains what it was before)

      .. warning::

         Any methods on the relations queryset which imply
         a database query will reset previously translated results:

         .. testcode:: read

            from translations.context import Context
            from sample.models import Continent

            continents = Continent.objects.prefetch_related(
                'countries',
            )

            with Context(continents, 'countries') as context:
                context.read('de')
                # querying after translation
                print(continents[0].countries.exclude(name=''))

         .. testoutput:: read

            <TranslatableQuerySet [
                <Country: Germany>,
            ]>

         In some cases the querying can be done before the translation:

         .. testcode:: read

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

         .. testoutput:: read

            <TranslatableQuerySet [
                <Country: Deutschland>,
            ]>

   .. method:: update(lang=None)

      Update the translations of the :class:`Context`\ 's :term:`purview` in
      a language.

      Updates the translations using the :attr:`translatable fields \
      <translations.models.Translatable.TranslatableMeta.fields>` of the
      :class:`Context`\ 's :term:`purview` in a language.

      :param lang: The language to update the translations in.
          ``None`` means use the :term:`active language` code.
      :type lang: str or None
      :raise ValueError: If the language code is not supported.

      .. testsetup:: update

         from tests.sample import create_samples

         create_samples(
             continent_names=['europe', 'asia'],
             country_names=['germany', 'south korea'],
             city_names=['cologne', 'seoul'],
             continent_fields=['name', 'denonym'],
             country_fields=['name', 'denonym'],
             city_fields=['name', 'denonym'],
             langs=['de']
         )

      To update the translations of the :class:`Context`\ 's :term:`purview`
      (an instance and some relations of it):

      .. testcode:: update

         from translations.context import Context
         from sample.models import Continent

         europe = Continent.objects.get(code='EU')
         relations = ('countries', 'countries__cities',)

         with Context(europe, *relations) as context:
             # change the field values
             europe.name = 'Europa (changed)'
             europe.countries.all()[0].name = 'Deutschland (changed)'
             europe.countries.all()[0].cities.all()[0].name = 'Köln (changed)'

             # update the translations
             context.update('de')

             print('Translations updated!')

      .. testoutput:: update

         Translations updated!

      To update the translations of the :class:`Context`\ 's :term:`purview`
      (a queryset and some relations of it):

      .. testcode:: update

         from translations.context import Context
         from sample.models import Continent

         continents = Continent.objects.all()
         relations = ('countries', 'countries__cities',)

         with Context(continents, *relations) as context:
             # change the field values
             continents[0].name = 'Europa (changed)'
             continents[0].countries.all()[0].name = 'Deutschland (changed)'
             continents[0].countries.all()[0].cities.all()[0].name = 'Köln (changed)'

             # update the translations
             context.update('de')

             print('Translations updated!')

      .. testoutput:: update

         Translations updated!

      To update the translations of the :class:`Context`\ 's :term:`purview`
      (a list of instances and some relations of it):

      .. testcode:: update

         from translations.context import Context
         from sample.models import Continent

         continents = list(Continent.objects.all())
         relations = ('countries', 'countries__cities',)

         with Context(continents, *relations) as context:
             # change the field values
             continents[0].name = 'Europa (changed)'
             continents[0].countries.all()[0].name = 'Deutschland (changed)'
             continents[0].countries.all()[0].cities.all()[0].name = 'Köln (changed)'

             # update the translations
             context.update('de')

             print('Translations updated!')

      .. testoutput:: update

         Translations updated!

      .. note::

         Updating only affects the translatable fields that have changed.

         If the value of a field is not changed, the translation for it is not
         updated. (No need to initialize all the translatable fields beforehand)

   .. method:: delete(lang=None)

      Delete the translations of the :class:`Context`\ 's :term:`purview` in
      a language.

      Deletes the translations for the :attr:`translatable fields \
      <translations.models.Translatable.TranslatableMeta.fields>` of the
      :class:`Context`\ 's :term:`purview` in a language.

      :param lang: The language to delete the translations in.
          ``None`` means use the :term:`active language` code.
      :type lang: str or None
      :raise ValueError: If the language code is not supported.

      .. testsetup:: delete_0

         from tests.sample import create_samples

         create_samples(
             continent_names=['europe', 'asia'],
             country_names=['germany', 'south korea'],
             city_names=['cologne', 'seoul'],
             continent_fields=['name', 'denonym'],
             country_fields=['name', 'denonym'],
             city_fields=['name', 'denonym'],
             langs=['de']
         )

      .. testsetup:: delete_1

         from tests.sample import create_samples

         create_samples(
             continent_names=['europe', 'asia'],
             country_names=['germany', 'south korea'],
             city_names=['cologne', 'seoul'],
             continent_fields=['name', 'denonym'],
             country_fields=['name', 'denonym'],
             city_fields=['name', 'denonym'],
             langs=['de']
         )

      .. testsetup:: delete_2

         from tests.sample import create_samples

         create_samples(
             continent_names=['europe', 'asia'],
             country_names=['germany', 'south korea'],
             city_names=['cologne', 'seoul'],
             continent_fields=['name', 'denonym'],
             country_fields=['name', 'denonym'],
             city_fields=['name', 'denonym'],
             langs=['de']
         )

      To delete the translations of the :class:`Context`\ 's :term:`purview`
      (an instance and some relations of it):

      .. testcode:: delete_0

         from translations.context import Context
         from sample.models import Continent

         europe = Continent.objects.get(code='EU')
         relations = ('countries', 'countries__cities',)

         with Context(europe, *relations) as context:
             # delete the translations
             context.delete('de')

             print('Translations deleted!')

      .. testoutput:: delete_0

         Translations deleted!

      To delete the translations of the :class:`Context`\ 's :term:`purview`
      (a queryset and some relations of it):

      .. testcode:: delete_1

         from translations.context import Context
         from sample.models import Continent

         continents = Continent.objects.all()
         relations = ('countries', 'countries__cities',)

         with Context(continents, *relations) as context:
             # delete the translations
             context.delete('de')

             print('Translations deleted!')

      .. testoutput:: delete_1

         Translations deleted!

      To delete the translations of the :class:`Context`\ 's :term:`purview`
      (a list of instances and some relations of it):

      .. testcode:: delete_2

         from translations.context import Context
         from sample.models import Continent

         continents = list(Continent.objects.all())
         relations = ('countries', 'countries__cities',)

         with Context(continents, *relations) as context:
             # delete the translations
             context.delete('de')

             print('Translations deleted!')

      .. testoutput:: delete_2

         Translations deleted!

   .. method:: reset()

      Reset the translations of the :class:`Context`\ 's :term:`purview` to
      the :term:`default language`.

      Resets the translations on the :attr:`translatable fields \
      <translations.models.Translatable.TranslatableMeta.fields>` of the
      :class:`Context`\ 's :term:`purview` to the :term:`default language`.

      .. testsetup:: reset

         from tests.sample import create_samples

         create_samples(
             continent_names=['europe', 'asia'],
             country_names=['germany', 'south korea'],
             city_names=['cologne', 'seoul'],
             continent_fields=['name', 'denonym'],
             country_fields=['name', 'denonym'],
             city_fields=['name', 'denonym'],
             langs=['de']
         )

      To reset the translations of the :class:`Context`\ 's :term:`purview`
      (an instance and some relations of it):

      .. testcode:: reset

         from translations.context import Context
         from sample.models import Continent

         europe = Continent.objects.get(code='EU')
         relations = ('countries', 'countries__cities',)

         with Context(europe, *relations) as context:
             # changes happened to the fields...
             context.read('de')

             # reset the translations
             context.reset()

             # use the field values
             print(europe)
             print(europe.countries.all()[0])
             print(europe.countries.all()[0].cities.all()[0])

      .. testoutput:: reset

         Europe
         Germany
         Cologne

      To reset the translations of the :class:`Context`\ 's :term:`purview`
      (a queryset and some relations of it):

      .. testcode:: reset

         from translations.context import Context
         from sample.models import Continent

         continents = Continent.objects.all()
         relations = ('countries', 'countries__cities',)

         with Context(continents, *relations) as context:
             # changes happened to the fields...
             context.read('de')

             # reset the translations
             context.reset()

             # use the field values
             print(continents[0])
             print(continents[0].countries.all()[0])
             print(continents[0].countries.all()[0].cities.all()[0])

      .. testoutput:: reset

         Europe
         Germany
         Cologne

      To reset the translations of the :class:`Context`\ 's :term:`purview`
      (a list of instances and some relations of it):

      .. testcode:: reset

         from translations.context import Context
         from sample.models import Continent

         continents = list(Continent.objects.all())
         relations = ('countries', 'countries__cities',)

         with Context(continents, *relations) as context:
             # changes happened to the fields...
             context.read('de')

             # reset the translations
             context.reset()

             # use the field values
             print(continents[0])
             print(continents[0].countries.all()[0])
             print(continents[0].countries.all()[0].cities.all()[0])

      .. testoutput:: reset

         Europe
         Germany
         Cologne
