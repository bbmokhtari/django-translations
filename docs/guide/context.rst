*******
Context
*******

This module provides an in depth knowledge of the Translations context.

What is context
===============

When something is going to be stated it can be done so in the context of a
certain language.

Initiate a context
==================

To initiate a context use the :class:`~translations.context.Context`
class. The context's margin must be defined in the initiation, meaning which
``entity`` and what ``*relations`` of that entity should it affect.

All the actions like `reading the translations`_,
`updating the translations`_, etc only affects the
objects in the defined margin.

.. testsetup:: guide_init

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

To initiate a context for a model instance:

.. testcode:: guide_init

   from sample.models import Continent
   from translations.context import Context

   # fetch an instance
   europe = Continent.objects.get(code='EU')

   # initiate context
   with Context(europe, 'countries', 'countries__cities') as context:
       print('Context created!')

.. testoutput:: guide_init

   Context created!

To initiate a context for a queryset:

.. testcode:: guide_init

   from sample.models import Continent
   from translations.context import Context

   # fetch a queryset
   continents = Continent.objects.all()

   # initiate context
   with Context(continents, 'countries', 'countries__cities') as context:
       print('Context created!')

.. testoutput:: guide_init

   Context created!

To initiate a context for a list of model instances:

.. testcode:: guide_init

   from sample.models import Continent
   from translations.context import Context

   # fetch a list of instances
   continents = list(Continent.objects.all())

   # initiate context
   with Context(continents, 'countries', 'countries__cities') as context:
       print('Context created!')

.. testoutput:: guide_init

   Context created!

The ``entity`` must be a model instance, a queryset or a list of model
instances.
The model of the ``entity`` must be
:class:`~translations.models.Translatable`.

The ``*relations`` must be an unpacked list of strings.
They may be separated by ``__``\ s to represent a deeply nested relation.
The model of the ``*relations`` must be
:class:`~translations.models.Translatable`.

.. note::

   It is **recommended** for the relations of the entity to be
   prefetched before initiating a :class:`~translations.context.Context`,
   in order to reach optimal performance.

   To do this use
   :meth:`~django.db.models.query.QuerySet.select_related`,
   :meth:`~django.db.models.query.QuerySet.prefetch_related` or
   :func:`~django.db.models.prefetch_related_objects`.

Reading the translations
========================

To read the translations of the defined margin in a language and apply them on
the context, just specify the ``lang`` code of the language.

.. testsetup:: guide_read

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

To read the translations of the defined margin for a model instance:

.. testcode:: guide_read

   from sample.models import Continent
   from translations.context import Context

   # fetch an instance
   europe = Continent.objects.get(code='EU')

   # initiate context
   with Context(europe, 'countries', 'countries__cities') as context:
       # read the context in German
       context.read(lang='de')

       # use the instance like before
       print(europe)
       print(europe.countries.all()[0])
       print(europe.countries.all()[0].cities.all()[0])

.. testoutput:: guide_read

   Europa
   Deutschland
   Köln

To read the translations of the defined margin for a queryset:

.. testcode:: guide_read

   from sample.models import Continent
   from translations.context import Context

   # fetch a queryset
   continents = Continent.objects.all()

   # initiate context
   with Context(continents, 'countries', 'countries__cities') as context:
       # read the context in German
       context.read(lang='de')

       # use the queryset like before
       print(continents[0])
       print(continents[0].countries.all()[0])
       print(continents[0].countries.all()[0].cities.all()[0])

.. testoutput:: guide_read

   Europa
   Deutschland
   Köln

To read the translations of the defined margin for a list of instances:

.. testcode:: guide_read

   from sample.models import Continent
   from translations.context import Context

   # fetch a list of instances
   continents = list(Continent.objects.all())

   # initiate context
   with Context(continents, 'countries', 'countries__cities') as context:
       # read the context in German
       context.read(lang='de')

       # use the list of instances like before
       print(continents[0])
       print(continents[0].countries.all()[0])
       print(continents[0].countries.all()[0].cities.all()[0])

.. testoutput:: guide_read

   Europa
   Deutschland
   Köln

The ``lang`` must be a language code already declared in the
:data:`~django.conf.settings.LANGUAGES` setting. It is optional and if it is
not passed in, it is automatically set to the :term:`active language` code.

.. note::

   If there is no translation for a field in the
   :attr:`translatable fields \
   <translations.models.Translatable.TranslatableMeta.fields>`,
   the value of the field is not changed and remains what it was before.

.. warning::

   Filtering any queryset after reading the translations will cause
   the translations of that queryset to be reset.

   .. testcode:: guide_read

      from sample.models import Continent
      from translations.context import Context

      europe = Continent.objects.prefetch_related(
          'countries',
          'countries__cities',
      ).get(code='EU')

      with Context(europe, 'countries', 'countries__cities') as context:
          context.read(lang='de')

          print(europe.name)
          print(europe.countries.exclude(name='')[0].name + '  -- Wrong')
          print(europe.countries.exclude(name='')[0].cities.all()[0].name + '  -- Wrong')

   .. testoutput:: guide_read

      Europa
      Germany  -- Wrong
      Cologne  -- Wrong

   The solution is to do the filtering before reading the
   translations. To do this on the relations use
   :class:`~django.db.models.Prefetch`.

   .. testcode:: guide_read

      from django.db.models import Prefetch
      from sample.models import Continent, Country
      from translations.context import Context

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

   .. testoutput:: guide_read

      Europa
      Deutschland  -- Correct
      Köln  -- Correct

.. Update list of instances translations
   =====================================
   
   To update the translations of a
   :class:`translatable list of instances <translations.models.Translatable>`
   use the
   :meth:`~translations.utils.update_translations`
   method.
   
   .. testsetup:: guide_update_translations_list
   
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
   
   .. testcode:: guide_update_translations_list
   
      from sample.models import Continent
      from translations.utils import update_translations
   
      # fetch a list of instances like before
      continents = list(Continent.objects.all())
   
      # change the instances in place
      europe = continents[0]
      asia = continents[1]
      europe.name = 'Europa (changed)'
      europe.denonym = 'Europäisch (changed)'
      asia.name = 'Asien (changed)'
      asia.denonym = 'Asiatisch (changed)'
   
      # update the translations
      update_translations(continents, lang='de')
   
      # output
      print('`Europe` is called `{}` in German.'.format(europe.name))
      print('`European` is called `{}` in German.'.format(europe.denonym))
      print('`Asia` is called `{}` in German.'.format(asia.name))
      print('`Asian` is called `{}` in German.'.format(asia.denonym))
   
   .. testoutput:: guide_update_translations_list
   
      `Europe` is called `Europa (changed)` in German.
      `European` is called `Europäisch (changed)` in German.
      `Asia` is called `Asien (changed)` in German.
      `Asian` is called `Asiatisch (changed)` in German.
   
   The ``lang`` parameter is optional. It determines the language to update the
   translations in. It must be a language code already declared in the
   :data:`~django.conf.settings.LANGUAGES` setting. If it is not passed in, it
   will be automatically set to the :term:`active language` code.
   
   If successful,
   :meth:`~translations.utils.update_translations`
   updates the translations of the instances using their
   :attr:`translatable fields \
   <translations.models.Translatable.TranslatableMeta.fields>` and returns
   ``None``. If failed, it throws the appropriate error.
   
   Update list of instances' relations translations
   ================================================
   
   :meth:`~translations.utils.update_translations`
   can also update the translations of a
   :class:`translatable list of instances <translations.models.Translatable>`\
   ' relations.
   
   .. testsetup:: guide_update_translations_list_relations
      
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
   
   .. testcode:: guide_update_translations_list_relations
   
      from django.db.models import prefetch_related_objects
      from sample.models import Continent
      from translations.utils import update_translations
   
      # fetch a list of instances like before
      continents = list(Continent.objects.all())
      prefetch_related_objects(
          continents,
          'countries',
          'countries__cities',
      )
   
      # change the instances in place
      europe = continents[0]
      asia = continents[1]
      europe.name = 'Europa (changed)'
      europe.denonym = 'Europäisch (changed)'
      asia.name = 'Asien (changed)'
      asia.denonym = 'Asiatisch (changed)'
   
      # change the relations in place
      germany = europe.countries.all()[0]
      cologne = germany.cities.all()[0]
      south_korea = asia.countries.all()[0]
      seoul = south_korea.cities.all()[0]
      germany.name = 'Deutschland (changed)'
      germany.denonym = 'Deutsche (changed)'
      cologne.name = 'Köln (changed)'
      cologne.denonym = 'Kölner (changed)'
      south_korea.name = 'Südkorea (changed)'
      south_korea.denonym = 'Südkoreanisch (changed)'
      seoul.name = 'Seül (changed)'
      seoul.denonym = 'Seüler (changed)'
   
      # update the translations
      update_translations(
          continents,
          'countries',
          'countries__cities',
          lang='de',
      )
   
      # output
      print('`Europe` is called `{}` in German.'.format(europe.name))
      print('`European` is called `{}` in German.'.format(europe.denonym))
      print('`Germany` is called `{}` in German.'.format(germany.name))
      print('`German` is called `{}` in German.'.format(germany.denonym))
      print('`Cologne` is called `{}` in German.'.format(cologne.name))
      print('`Cologner` is called `{}` in German.'.format(cologne.denonym))
      print('`Asia` is called `{}` in German.'.format(asia.name))
      print('`Asian` is called `{}` in German.'.format(asia.denonym))
      print('`South Korea` is called `{}` in German.'.format(south_korea.name))
      print('`South Korean` is called `{}` in German.'.format(south_korea.denonym))
      print('`Seoul` is called `{}` in German.'.format(seoul.name))
      print('`Seouler` is called `{}` in German.'.format(seoul.denonym))
   
   .. testoutput:: guide_update_translations_list_relations
   
      `Europe` is called `Europa (changed)` in German.
      `European` is called `Europäisch (changed)` in German.
      `Germany` is called `Deutschland (changed)` in German.
      `German` is called `Deutsche (changed)` in German.
      `Cologne` is called `Köln (changed)` in German.
      `Cologner` is called `Kölner (changed)` in German.
      `Asia` is called `Asien (changed)` in German.
      `Asian` is called `Asiatisch (changed)` in German.
      `South Korea` is called `Südkorea (changed)` in German.
      `South Korean` is called `Südkoreanisch (changed)` in German.
      `Seoul` is called `Seül (changed)` in German.
      `Seouler` is called `Seüler (changed)` in German.
   
   The ``*relations`` parameter determines the instances' relations to update the
   translations of. They must also be :class:`~translations.models.Translatable`.
   
   If successful,
   :meth:`~translations.utils.update_translations`
   updates the translations of the instances and their relations using their
   :attr:`translatable fields \
   <translations.models.Translatable.TranslatableMeta.fields>` and returns
   ``None``. If failed, it throws the appropriate error.
   
   .. note::
   
      It is **mandatory** for the relations of the instances to be
      prefetched before making any changes to them so that the changes
      can be fetched later.
   
      To do this use
      :meth:`~django.db.models.query.QuerySet.select_related`,
      :meth:`~django.db.models.query.QuerySet.prefetch_related` or
      :func:`~django.db.models.prefetch_related_objects`.
   
      .. testsetup:: guide_update_translations_list_note
      
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
   
      Consider this case:
   
      .. testcode:: guide_update_translations_list_note
   
         from sample.models import Continent
   
         # un-prefetched queryset
         europe = Continent.objects.get(code='EU')
   
         # first query
         europe.countries.all()[0].name = 'Germany (changed)'
   
         # does a second query
         new_name = europe.countries.all()[0].name
   
         print('Country: {}'.format(new_name))
   
      .. testoutput:: guide_update_translations_list_note
   
         Country: Germany
   
      As we can see the new query did not fetch the changes we made
      before. To fix it:
   
      .. testcode:: guide_update_translations_list_note
   
         from sample.models import Continent
   
         # prefetched queryset
         europe = Continent.objects.prefetch_related(
             'countries',
         ).get(code='EU')
   
         # first query
         europe.countries.all()[0].name = 'Germany (changed)'
   
         # uses the first query
         new_name = europe.countries.all()[0].name
   
         print('Country: {}'.format(new_name))
   
      .. testoutput:: guide_update_translations_list_note
   
         Country: Germany (changed)
      
