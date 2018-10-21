*******
Context
*******

.. module:: translations.context

This module contains the context managers for the Translations app.

.. class:: Context

   A context manager which provides custom translation functionalities.

   Provides CRUD functionalities like :meth:`create`, :meth:`read`,
   :meth:`update` and :meth:`delete` to work with the translations and also
   some other functionalities like :meth:`reset` to manage the :class:`Context`.

   .. method:: __init__(self, entity, *relations)

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

         # Initialize context
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

         # Initialize context
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

         # Initialize context
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
             context.create(lang='de')

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
             context.create(lang='de')

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
             context.create(lang='de')

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
             context.read(lang='de')

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
             context.read(lang='de')

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
             context.read(lang='de')

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

         Filtering the relations after reading the translations will cause
         the translations of that relation to be reset.

         .. testcode:: read

            from translations.context import Context
            from sample.models import Continent

            europe = Continent.objects.prefetch_related(
                'countries',
                'countries__cities',
            ).get(code='EU')

            with Context(europe, 'countries', 'countries__cities') as context:
                context.read(lang='de')

                # Filtering after reading
                print(europe.name)
                print(europe.countries.exclude(name='')[0].name + '  -- Wrong')
                print(europe.countries.exclude(name='')[0].cities.all()[0].name + '  -- Wrong')

         .. testoutput:: read

            Europa
            Germany  -- Wrong
            Cologne  -- Wrong

         The solution is to do the filtering before reading the translations.

         To do this use :class:`~django.db.models.Prefetch`.

         .. testcode:: read

            from django.db.models import Prefetch
            from translations.context import Context
            from sample.models import Continent, Country

            # Filtering before reading
            europe = Continent.objects.prefetch_related(
                Prefetch(
                    'countries',
                    queryset=Country.objects.exclude(name=''),
                ),
                'countries__cities',
            ).get(code='EU')

            with Context(europe, 'countries', 'countries__cities') as context:
                context.read(lang='de')

                print(europe.name)
                print(europe.countries.all()[0].name + '  -- Correct')
                print(europe.countries.all()[0].cities.all()[0].name + '  -- Correct')

         .. testoutput:: read

            Europa
            Deutschland  -- Correct
            Köln  -- Correct

   .. method:: update(lang=None)

      Update the translations of the context's purview in a language.

      Updates the translations using the :attr:`translatable fields \
      <translations.models.Translatable.TranslatableMeta.fields>` of the
      context's purview in a language.

      :param lang: The language to update the translations in.
          ``None`` means use the :term:`active language` code.
      :type lang: str or None
      :raise ValueError: If the language code is not included in
          the :data:`~django.conf.settings.LANGUAGES` setting.

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

      To update the translations of the defined purview for a model instance:

      .. testcode:: update

         from translations.context import Context
         from sample.models import Continent

         europe = Continent.objects.get(code='EU')

         with Context(europe, 'countries', 'countries__cities') as context:

             # change the instance like before
             europe.name = 'Europa (changed)'
             europe.countries.all()[0].name = 'Deutschland (changed)'
             europe.countries.all()[0].cities.all()[0].name = 'Köln (changed)'

             # update the translations in German
             context.update(lang='de')

             print('Translations updated!')

      .. testoutput:: update

         Translations updated!

      To update the translations of the defined purview for a queryset:

      .. testcode:: update

         from translations.context import Context
         from sample.models import Continent

         continents = Continent.objects.all()

         with Context(continents, 'countries', 'countries__cities') as context:

             # change the queryset like before
             continents[0].name = 'Europa (changed)'
             continents[0].countries.all()[0].name = 'Deutschland (changed)'
             continents[0].countries.all()[0].cities.all()[0].name = 'Köln (changed)'

             # update the translations in German
             context.update(lang='de')

             print('Translations updated!')

      .. testoutput:: update

         Translations updated!

      To update the translations of the defined purview for a list of instances:

      .. testcode:: update

         from translations.context import Context
         from sample.models import Continent

         continents = list(Continent.objects.all())

         with Context(continents, 'countries', 'countries__cities') as context:

             # change the list of instances like before
             continents[0].name = 'Europa (changed)'
             continents[0].countries.all()[0].name = 'Deutschland (changed)'
             continents[0].countries.all()[0].cities.all()[0].name = 'Köln (changed)'

             # update the translations in German
             context.update(lang='de')

             print('Translations updated!')

      .. testoutput:: update

         Translations updated!

      .. note::

         Updating only affects the translatable fields that have changed.

         If the value of a field is not changed, the translation for it is not
         updated. (No need to initialize all the translatable fields beforehand)

   .. method:: delete(lang=None)

      Delete the translations of the context's purview in a language.

      Deletes the translations for the :attr:`translatable fields \
      <translations.models.Translatable.TranslatableMeta.fields>` of the
      context's purview in a language.

      :param lang: The language to delete the translations in.
          ``None`` means use the :term:`active language` code.
      :type lang: str or None
      :raise ValueError: If the language code is not included in
          the :data:`~django.conf.settings.LANGUAGES` setting.

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

      To delete the translations of the defined purview for a model instance:

      .. testcode:: delete_0

         from translations.context import Context
         from sample.models import Continent

         europe = Continent.objects.get(code='EU')

         with Context(europe, 'countries', 'countries__cities') as context:

             # delete the translations in German
             context.delete(lang='de')

             print('Translations deleted!')

      .. testoutput:: delete_0

         Translations deleted!

      To delete the translations of the defined purview for a queryset:

      .. testcode:: delete_1

         from translations.context import Context
         from sample.models import Continent

         continents = Continent.objects.all()

         with Context(continents, 'countries', 'countries__cities') as context:

             # delete the translations in German
             context.delete(lang='de')

             print('Translations deleted!')

      .. testoutput:: delete_1

         Translations deleted!

      To delete the translations of the defined purview for a list of instances:

      .. testcode:: delete_2

         from translations.context import Context
         from sample.models import Continent

         continents = list(Continent.objects.all())

         with Context(continents, 'countries', 'countries__cities') as context:

             # delete the translations in German
             context.delete(lang='de')

             print('Translations deleted!')

      .. testoutput:: delete_2

         Translations deleted!

   .. method:: reset()

      Reset the translations of the context's purview to original values.

      Resets the translations on the :attr:`translatable fields \
      <translations.models.Translatable.TranslatableMeta.fields>` of the
      context's purview.

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

      To reset the translations of the defined purview for a model instance:

      .. testcode:: reset

         from translations.context import Context
         from sample.models import Continent

         europe = Continent.objects.get(code='EU')

         with Context(europe, 'countries', 'countries__cities') as context:

             # changes happened to the fields, create, read, update, delete, etc...
             context.read(lang='de')

             # reset the translations
             context.reset()

             # use the instance like before
             print(europe)
             print(europe.countries.all()[0])
             print(europe.countries.all()[0].cities.all()[0])

      .. testoutput:: reset

         Europe
         Germany
         Cologne

      To reset the translations of the defined purview for a queryset:

      .. testcode:: reset

         from translations.context import Context
         from sample.models import Continent

         continents = Continent.objects.all()

         with Context(continents, 'countries', 'countries__cities') as context:

             # changes happened to the fields, create, read, update, delete, etc...
             context.read(lang='de')

             # reset the translations
             context.reset()

             # use the queryset like before
             print(continents[0])
             print(continents[0].countries.all()[0])
             print(continents[0].countries.all()[0].cities.all()[0])

      .. testoutput:: reset

         Europe
         Germany
         Cologne

      To reset the translations of the defined purview for a list of instances:

      .. testcode:: reset

         from translations.context import Context
         from sample.models import Continent

         continents = list(Continent.objects.all())

         with Context(continents, 'countries', 'countries__cities') as context:

             # changes happened to the fields, create, read, update, delete, etc...
             context.read(lang='de')

             # reset the translations
             context.reset()

             # use the list of instances like before
             print(continents[0])
             print(continents[0].countries.all()[0])
             print(continents[0].countries.all()[0].cities.all()[0])

      .. testoutput:: reset

         Europe
         Germany
         Cologne
