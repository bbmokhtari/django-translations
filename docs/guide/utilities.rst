*********
Utilities
*********

This module provides an in depth knowledge of the Translations utilities.

Make list of instances translatable
===================================

To make a list of homogeneous instances, a
:class:`translatable list of instances <translations.models.Translatable>`
:ref:`make their model translatable <translatable-models>`.

Specify list of instances' translatable fields
==============================================

To specify the list of instances' :attr:`translatable fields \
<translations.models.Translatable.TranslatableMeta.fields>`
:ref:`specify their model's translatable fields <specify-fields>`.

Apply list of instances translations
====================================

To apply the translations of a
:class:`translatable list of instances <translations.models.Translatable>`
use the
:meth:`~translations.utils.apply_translations`
method.

.. testsetup:: guide_apply_translations_list

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

.. testcode:: guide_apply_translations_list

   from sample.models import Continent
   from translations.utils import apply_translations

   # fetch a list of instances like before
   continents = list(Continent.objects.all())

   # apply the translations in place
   apply_translations(continents, lang='de')

   # use the list of instances like before
   europe = continents[0]
   asia = continents[1]

   # output
   print('`Europe` is called `{}` in German.'.format(europe.name))
   print('`European` is called `{}` in German.'.format(europe.denonym))
   print('`Asia` is called `{}` in German.'.format(asia.name))
   print('`Asian` is called `{}` in German.'.format(asia.denonym))

.. testoutput:: guide_apply_translations_list

   `Europe` is called `Europa` in German.
   `European` is called `Europäisch` in German.
   `Asia` is called `Asien` in German.
   `Asian` is called `Asiatisch` in German.

The ``lang`` parameter is optional. It determines the language to apply the
translations in. It must be a language code already declared in the
:data:`~django.conf.settings.LANGUAGES` setting. If it is not passed in, it
will be automatically set to the :term:`active language` code.

If successful,
:meth:`~translations.utils.apply_translations`
applies the translations of the instances on their
:attr:`translatable fields \
<translations.models.Translatable.TranslatableMeta.fields>` and returns
``None``. If failed, it throws the appropriate error.

.. note::

   This is a convention in python that if a method changes the object
   in place it should return ``None``.

.. note::

   If there is no translation for a field in the
   :attr:`translatable fields \
   <translations.models.Translatable.TranslatableMeta.fields>`,
   the translation of the field falls back to the value of the field
   in the instance.

Apply list of instances' relations translations
===============================================

:meth:`~translations.utils.apply_translations`
can also apply the translations of a
:class:`translatable list of instances <translations.models.Translatable>`\
's relations.

.. testsetup:: guide_apply_translations_list_relations

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

.. testcode:: guide_apply_translations_list_relations

   from django.db.models import prefetch_related_objects
   from sample.models import Continent
   from translations.utils import apply_translations

   # fetch a list of instances like before
   continents = list(Continent.objects.all())
   prefetch_related_objects(
       continents,
       'countries',
       'countries__cities',
   )

   # apply the translations in place
   apply_translations(
       continents,
       'countries',
       'countries__cities',
       lang='de',
   )

   # use the list of instances like before
   europe = continents[0]
   asia = continents[1]

   # use the relations like before
   germany = europe.countries.all()[0]
   cologne = germany.cities.all()[0]
   south_korea = asia.countries.all()[0]
   seoul = south_korea.cities.all()[0]

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

.. testoutput:: guide_apply_translations_list_relations

   `Europe` is called `Europa` in German.
   `European` is called `Europäisch` in German.
   `Germany` is called `Deutschland` in German.
   `German` is called `Deutsche` in German.
   `Cologne` is called `Köln` in German.
   `Cologner` is called `Kölner` in German.
   `Asia` is called `Asien` in German.
   `Asian` is called `Asiatisch` in German.
   `South Korea` is called `Südkorea` in German.
   `South Korean` is called `Südkoreanisch` in German.
   `Seoul` is called `Seül` in German.
   `Seouler` is called `Seüler` in German.

The ``*relations`` parameter determines the instances' relations to apply the
translations of. They must also be :class:`~translations.models.Translatable`.

If successful,
:meth:`~translations.utils.apply_translations`
applies the translations of the instances and their relations on their
:attr:`translatable fields \
<translations.models.Translatable.TranslatableMeta.fields>` and returns
``None``. If failed, it throws the appropriate error.

.. note::

   It is **recommended** for the relations of the instances to be
   prefetched before applying the translations in order to reach
   optimal performance.

   To do this use
   :meth:`~django.db.models.query.QuerySet.select_related`,
   :meth:`~django.db.models.query.QuerySet.prefetch_related` or
   :func:`~django.db.models.prefetch_related_objects`.

.. warning::

   Filtering any queryset after applying the translations will cause
   the translations of that queryset to be reset.

   .. testsetup:: guide_apply_translations_list_warning
   
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

   .. testcode:: guide_apply_translations_list_warning

      from django.db.models import prefetch_related_objects
      from sample.models import Continent
      from translations.utils import apply_translations

      continents = list(Continent.objects.all())
      prefetch_related_objects(
          continents,
          'countries',
          'countries__cities',
      )

      apply_translations(
          continents,
          'countries',
          'countries__cities',
          lang='de',
      )

      for continent in continents:
          print('Continent: {}'.format(continent))
          for country in continent.countries.exclude(name=''):  # Wrong
              print('Country: {}  -- Wrong'.format(country))
              for city in country.cities.all():
                  print('City: {}  -- Wrong'.format(city))

   .. testoutput:: guide_apply_translations_list_warning

      Continent: Europa
      Country: Germany  -- Wrong
      City: Cologne  -- Wrong
      Continent: Asien
      Country: South Korea  -- Wrong
      City: Seoul  -- Wrong

   The solution is to do the filtering before applying the
   translations. To do this on the relations use
   :class:`~django.db.models.Prefetch`.

   .. testcode:: guide_apply_translations_list_warning

      from django.db.models import Prefetch, prefetch_related_objects
      from sample.models import Continent, Country
      from translations.utils import apply_translations

      continents = list(Continent.objects.all())
      prefetch_related_objects(
          continents,
          Prefetch(
              'countries',
              queryset=Country.objects.exclude(name=''),  # Correct
          ),
          'countries__cities',
      )

      apply_translations(
          continents,
          'countries',
          'countries__cities',
          lang='de',
      )

      for continent in continents:
          print('Continent: {}'.format(continent))
          for country in continent.countries.all():
              print('Country: {}  -- Correct'.format(country))
              for city in country.cities.all():
                  print('City: {}  -- Correct'.format(city))

   .. testoutput:: guide_apply_translations_list_warning

      Continent: Europa
      Country: Deutschland  -- Correct
      City: Köln  -- Correct
      Continent: Asien
      Country: Südkorea  -- Correct
      City: Seül  -- Correct

Update list of instances translations
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
