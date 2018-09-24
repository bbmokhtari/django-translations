******
Models
******

This module provides an in depth knowledge of the translatable models.

.. _translatable-models:

Make models translatable
========================

To make a model, a
:class:`translatable model <translations.models.Translatable>`
inherit the model from the :class:`~translations.models.Translatable` model.

.. literalinclude:: ../../sample/models.py
   :lines: 1-4
   :emphasize-lines: 4

.. literalinclude:: ../../sample/models.py
   :pyobject: Continent
   :lines: 1-25
   :emphasize-lines: 1

Since :class:`~translations.models.Translatable` is an abstract model there is
no need to migrate afterwards.

.. warning::

   Care not to inherit the :class:`~translations.models.Translation` model
   accidentally instead of the :class:`~translations.models.Translatable`
   model.

.. _specify-fields:

Specify model's translatable fields
===================================

To specify the model's :attr:`translatable fields \
<translations.models.Translatable.TranslatableMeta.fields>` specify the
:attr:`~translations.models.Translatable.TranslatableMeta.fields` attribute
of the :class:`~translations.models.Translatable.TranslatableMeta` class
declared inside a :class:`~translations.models.Translatable` model.

.. literalinclude:: ../../sample/models.py
   :pyobject: Continent
   :emphasize-lines: 1, 27-28

By default the
:attr:`~translations.models.Translatable.TranslatableMeta.fields` attribute is
set to ``None``. This means the translation will use the text based fields
automatically. (like :class:`~django.db.models.CharField` and
:class:`~django.db.models.TextField` - this does not include
:class:`~django.db.models.EmailField` or the fields with ``choices``)

.. literalinclude:: ../../sample/models.py
   :pyobject: City
   :emphasize-lines: 1

If needed, the
:attr:`~translations.models.Translatable.TranslatableMeta.fields` attribute
can be set to nothing. You can do this by explicitly setting it to ``[]``.

.. literalinclude:: ../../sample/models.py
   :pyobject: Timezone
   :emphasize-lines: 1, 15-16

Apply instance translations
===========================

To apply the translations of a
:class:`translatable instance <translations.models.Translatable>`
use the :meth:`~translations.models.Translatable.apply_translations`
method.

.. testsetup:: guide_apply_translations_instance

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

.. testcode:: guide_apply_translations_instance

   from sample.models import Continent

   # fetch an instance like before
   europe = Continent.objects.get(code='EU')

   # apply the translations in place
   europe.apply_translations(lang='de')

   # use the instance like before
   name = europe.name
   denonym = europe.denonym

   # output
   print('`Europe` is called `{}` in German.'.format(name))
   print('`European` is called `{}` in German.'.format(denonym))

.. testoutput:: guide_apply_translations_instance

   `Europe` is called `Europa` in German.
   `European` is called `Europäisch` in German.

The ``lang`` parameter is optional. It determines the language to apply the
translations in. It must be a language code already declared in the
:data:`~django.conf.settings.LANGUAGES` setting. If it is not passed in, it
will be automatically set to the :term:`active language` code.

If successful,
:meth:`~translations.models.Translatable.apply_translations`
applies the translations of the instance on its
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

Apply instance's relations translations
=======================================

:meth:`~translations.models.Translatable.apply_translations`
can also apply the translations of a
:class:`translatable instance <translations.models.Translatable>`\
's relations.

.. testsetup:: guide_apply_translations_instance_relations
   
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

.. testcode:: guide_apply_translations_instance_relations

   from sample.models import Continent

   # fetch an instance like before
   europe = Continent.objects.prefetch_related(
       'countries',
       'countries__cities',
   ).get(code='EU')

   # apply the translations in place
   europe.apply_translations(
       'countries',
       'countries__cities',
       lang='de',
   )

   # use the instance like before
   name = europe.name
   denonym = europe.denonym

   # use the relations like before
   germany = europe.countries.all()[0]
   cologne = germany.cities.all()[0]

   # output
   print('`Europe` is called `{}` in German.'.format(name))
   print('`European` is called `{}` in German.'.format(denonym))
   print('`Germany` is called `{}` in German.'.format(germany.name))
   print('`German` is called `{}` in German.'.format(germany.denonym))
   print('`Cologne` is called `{}` in German.'.format(cologne.name))
   print('`Cologner` is called `{}` in German.'.format(cologne.denonym))

.. testoutput:: guide_apply_translations_instance_relations

   `Europe` is called `Europa` in German.
   `European` is called `Europäisch` in German.
   `Germany` is called `Deutschland` in German.
   `German` is called `Deutsche` in German.
   `Cologne` is called `Köln` in German.
   `Cologner` is called `Kölner` in German.

The ``*relations`` parameter determines the instance's relations to apply the
translations of. They must also be :class:`~translations.models.Translatable`.

If successful,
:meth:`~translations.models.Translatable.apply_translations`
applies the translations of the instance and its relations on their
:attr:`translatable fields \
<translations.models.Translatable.TranslatableMeta.fields>` and returns
``None``. If failed, it throws the appropriate error.

.. note::

   It is **recommended** for the relations of the instance to be
   prefetched before applying the translations in order to reach
   optimal performance.

   To do this use
   :meth:`~django.db.models.query.QuerySet.select_related`,
   :meth:`~django.db.models.query.QuerySet.prefetch_related` or
   :func:`~django.db.models.prefetch_related_objects`.

.. warning::

   Filtering any queryset after applying the translations will cause
   the translations of that queryset to be reset.

   .. testsetup:: guide_apply_translations_instance_warning
   
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

   .. testcode:: guide_apply_translations_instance_warning

      from sample.models import Continent

      europe = Continent.objects.prefetch_related(
          'countries',
          'countries__cities',
      ).get(code='EU')

      europe.apply_translations(
          'countries',
          'countries__cities',
          lang='de',
      )

      print('Continent: {}'.format(europe))
      for country in europe.countries.exclude(name=''):  # Wrong
          print('Country: {}  -- Wrong'.format(country))
          for city in country.cities.all():
              print('City: {}  -- Wrong'.format(city))

   .. testoutput:: guide_apply_translations_instance_warning

      Continent: Europa
      Country: Germany  -- Wrong
      City: Cologne  -- Wrong

   The solution is to do the filtering before applying the
   translations. To do this on the relations use
   :class:`~django.db.models.Prefetch`.

   .. testcode:: guide_apply_translations_instance_warning

      from django.db.models import Prefetch
      from sample.models import Continent, Country

      europe = Continent.objects.prefetch_related(
          Prefetch(
              'countries',
              queryset=Country.objects.exclude(name=''),  # Correct
          ),
          'countries__cities',
      ).get(code='EU')

      europe.apply_translations(
          'countries',
          'countries__cities',
          lang='de',
      )

      print('Continent: {}'.format(europe))
      for country in europe.countries.all():
          print('Country: {}  -- Correct'.format(country))
          for city in country.cities.all():
              print('City: {}  -- Correct'.format(city))

   .. testoutput:: guide_apply_translations_instance_warning

      Continent: Europa
      Country: Deutschland  -- Correct
      City: Köln  -- Correct

Update instance translations
============================

To update the translations of a :class:`~translations.models.Translatable`
instance use the :meth:`~translations.models.Translatable.update_translations`
method.

.. testsetup:: guide_update_translations_instance
   
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

.. testcode:: guide_update_translations_instance

   from sample.models import Continent

   # fetch an instance like before
   europe = Continent.objects.get(code='EU')

   # apply the translations in place
   europe.apply_translations(lang='de')

   # use the instance like before
   print('`Europe` is called `{}` in German.'.format(europe.name))
   print('`European` is called `{}` in German.'.format(europe.denonym))

   # change the instance
   print('\nChanging...\n')
   europe.name = 'Europa (changed)'
   europe.denonym = 'Europäisch (changed)'

   # update the translations in place
   europe.update_translations(lang='de')

   # re-apply the translations in place
   europe.apply_translations(lang='de')

   # use the instance like before
   print('`Europe` is called `{}` in German.'.format(europe.name))
   print('`European` is called `{}` in German.'.format(europe.denonym))

.. testoutput:: guide_update_translations_instance

   `Europe` is called `Europa` in German.
   `European` is called `Europäisch` in German.

   Changing...

   `Europe` is called `Europa (changed)` in German.
   `European` is called `Europäisch (changed)` in German.

The ``lang`` parameter is optional. It determines the language to update the
translations in. It must be a language code already declared in the
:data:`~django.conf.settings.LANGUAGES` setting. If it is not passed in, it
will be automatically set to the :term:`active language` code.

If successful, :meth:`~translations.models.Translatable.update_translations`
updates the translations of the instance using its translatable
:attr:`~translations.models.Translatable.TranslatableMeta.fields` and returns
``None``. If failed, it throws the appropriate error.

Update instance's relations translations
========================================

:meth:`~translations.models.Translatable.update_translations` can also update
the translations of a :class:`~translations.models.Translatable` instance's
relations.

.. testsetup:: guide_update_translations_relations
   
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

.. testcode:: guide_update_translations_relations

   from sample.models import Continent

   # fetch an instance like before
   europe = Continent.objects.prefetch_related(
       'countries',
       'countries__cities',
   ).get(code='EU')

   # apply the translations in place
   europe.apply_translations(
       'countries',
       'countries__cities',
       lang='de',
   )

   # use the instance like before
   print('`Europe` is called `{}` in German.'.format(europe.name))
   print('`European` is called `{}` in German.'.format(europe.denonym))

   # use the relations like before
   germany = europe.countries.all()[0]
   cologne = germany.cities.all()[0]
   print('`Germany` is called `{}` in German.'.format(germany.name))
   print('`German` is called `{}` in German.'.format(germany.denonym))
   print('`Cologne` is called `{}` in German.'.format(cologne.name))
   print('`Cologner` is called `{}` in German.'.format(cologne.denonym))

   # change the instance
   print('\nChanging...\n')
   europe.name = 'Europa (changed)'
   europe.denonym = 'Europäisch (changed)'

   # change the relations
   germany.name = 'Deutschland (changed)'
   germany.denonym = 'Deutsche (changed)'
   cologne.name = 'Köln (changed)'
   cologne.denonym = 'Kölner (changed)'

   # update the translations in place
   europe.update_translations(
       'countries',
       'countries__cities',
       lang='de',
   )

   # re-apply the translations in place
   europe.apply_translations(
       'countries',
       'countries__cities',
       lang='de',
   )

   # use the instance like before
   print('`Europe` is called `{}` in German.'.format(europe.name))
   print('`European` is called `{}` in German.'.format(europe.denonym))

   # use the relations like before
   germany = europe.countries.all()[0]
   cologne = germany.cities.all()[0]
   print('`Germany` is called `{}` in German.'.format(germany.name))
   print('`German` is called `{}` in German.'.format(germany.denonym))
   print('`Cologne` is called `{}` in German.'.format(cologne.name))
   print('`Cologner` is called `{}` in German.'.format(cologne.denonym))

.. testoutput:: guide_update_translations_relations

   `Europe` is called `Europa` in German.
   `European` is called `Europäisch` in German.
   `Germany` is called `Deutschland` in German.
   `German` is called `Deutsche` in German.
   `Cologne` is called `Köln` in German.
   `Cologner` is called `Kölner` in German.

   Changing...

   `Europe` is called `Europa (changed)` in German.
   `European` is called `Europäisch (changed)` in German.
   `Germany` is called `Deutschland (changed)` in German.
   `German` is called `Deutsche (changed)` in German.
   `Cologne` is called `Köln (changed)` in German.
   `Cologner` is called `Kölner (changed)` in German.

The ``*relations`` parameter determines the instance's relations to update the
translations of. They must also be :class:`~translations.models.Translatable`.

If successful, :meth:`~translations.models.Translatable.update_translations`
updates the translations of the instance and its relations using their
translatable :attr:`~translations.models.Translatable.TranslatableMeta.fields`
and returns ``None``. If failed, it throws the appropriate error.

.. note::

   It is **mandatory** for the relations of the instance to be
   prefetched before making any changes to them so that the changes
   can be fetched later.

   To do this use
   :meth:`~django.db.models.query.QuerySet.select_related`,
   :meth:`~django.db.models.query.QuerySet.prefetch_related` or
   :func:`~django.db.models.prefetch_related_objects`.

   .. testsetup:: guide_update_translations_note
   
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

   .. testcode:: guide_update_translations_note

      from sample.models import Continent

      # un-prefetched queryset
      europe = Continent.objects.get(code='EU')

      # first query
      europe.countries.all()[0].name = 'Germany (changed)'

      # does a second query
      new_name = europe.countries.all()[0].name

      print('Country: {}'.format(new_name))

   .. testoutput:: guide_update_translations_note

      Country: Germany

   As we can see the new query did not fetch the changes we made
   before. To fix it:

   .. testcode:: guide_update_translations_note

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

   .. testoutput:: guide_update_translations_note

      Country: Germany (changed)
