******
Models
******

This module provides an in depth knowledge of the translatable models.

Make models translatable
========================

To make a model translatable inherit the model from the
:class:`~translations.models.Translatable` model.

.. literalinclude:: ../../sample/models.py
   :lines: 1-6, 24-48
   :emphasize-lines: 4, 7

Since :class:`~translations.models.Translatable` is an abstract model there is
no need to migrate afterwards.

.. warning::

   Care not to inherit the :class:`~translations.models.Translation` model
   accidentally instead of the :class:`~translations.models.Translatable`
   model.

Specify translatable fields
===========================

To specify the translatable fields specify the
:attr:`~translations.models.Translatable.TranslatableMeta.fields` attribute
of the :class:`~translations.models.Translatable.TranslatableMeta` class
declared inside a :class:`~translations.models.Translatable` model.

.. literalinclude:: ../../sample/models.py
   :lines: 1-6, 24-51
   :emphasize-lines: 33-34

By default the
:attr:`~translations.models.Translatable.TranslatableMeta.fields` attribute is
set to ``None``. This means the translation will use the text based fields
automatically, fields like :class:`~django.db.models.CharField` and
:class:`~django.db.models.TextField`. (it automatically ignores the fields with
the ``choices`` and :class:`~django.db.models.EmailField`)

If needed, the
:attr:`~translations.models.Translatable.TranslatableMeta.fields` attribute
can be set to nothing. You can do this by explicitly setting it to ``[]``.

Apply instance translations
===========================

To apply the translations of an instance use the
:meth:`~translations.models.Translatable.apply_translations` method.

.. testsetup:: guide_apply_translations_instance
   
   from tests.sample import create_samples

   create_samples(
       continent_names=['europe', 'asia'],
       country_names=['germany', 'south korea'],
       city_names=['cologne', 'munich', 'seoul', 'ulsan'],
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
   print('Europe is called `{}` in German.'.format(europe.name))
   print('European is called `{}` in German.'.format(europe.denonym))

.. testoutput:: guide_apply_translations_instance

   Europe is called `Europa` in German.
   European is called `Europäisch` in German.

The ``lang`` parameter is optional. It determines the language to apply the
translations in. It must be a language code already declared in the
:data:`~django.conf.settings.LANGUAGES` setting. If it is not passed in, it
will be automatically set to the :term:`active language` code.

If successful, :meth:`~translations.models.Translatable.apply_translations`
applies the translations on the translatable
:attr:`~translations.models.Translatable.TranslatableMeta.fields` of the
instance in place and returns ``None``. If it fails it throws the appropriate
error.

.. note::

   This is a convention in python that if a method changes the instance
   in place it should return ``None``.

.. note::

   If there is no translation for a field in the translatable
   :attr:`~translations.models.Translatable.TranslatableMeta.fields`,
   the translation of the field falls back to the value of the field
   in the instance.

Apply relations translations
============================

:meth:`~translations.models.Translatable.apply_translations` can also apply
the translations of the instance's relations.

.. testsetup:: guide_apply_translations_relations
   
   from tests.sample import create_samples

   create_samples(
       continent_names=['europe', 'asia'],
       country_names=['germany', 'south korea'],
       city_names=['cologne', 'munich', 'seoul', 'ulsan'],
       continent_fields=['name', 'denonym'],
       country_fields=['name', 'denonym'],
       city_fields=['name', 'denonym'],
       langs=['de']
   )

.. testcode:: guide_apply_translations_relations

   from sample.models import Continent

   # fetch an instance like before
   europe = Continent.objects.prefetch_related(
       'countries',
       'countries__cities',
   ).get(code='EU')

   # apply translations in place
   europe.apply_translations(
       'countries',
       'countries__cities',
       lang='de',
   )

   # use the instance like before
   print('Europe is called `{}` in German.'.format(europe.name))
   print('European is called `{}` in German.'.format(europe.denonym))

   # use the relations like before
   germany = europe.countries.all()[0]
   cologne = germany.cities.all()[0]
   print('Germany is called `{}` in German.'.format(germany.name))
   print('German is called `{}` in German.'.format(germany.denonym))
   print('Cologne is called `{}` in German.'.format(cologne.name))
   print('Cologner is called `{}` in German.'.format(cologne.denonym))

.. testoutput:: guide_apply_translations_relations

   Europe is called `Europa` in German.
   European is called `Europäisch` in German.
   Germany is called `Deutschland` in German.
   German is called `Deutsche` in German.
   Cologne is called `Köln` in German.
   Cologner is called `Kölner` in German.

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
   the translations of that queryset to be reset. The solution is to
   do the filtering before applying the translations.

   To do this on the relations use :class:`~django.db.models.Prefetch`.

   .. testsetup:: guide_apply_translations_warning
   
      from tests.sample import create_samples

      create_samples(
          continent_names=['europe', 'asia'],
          country_names=['germany', 'south korea'],
          city_names=['cologne', 'munich', 'seoul', 'ulsan'],
          continent_fields=['name', 'denonym'],
          country_fields=['name', 'denonym'],
          city_fields=['name', 'denonym'],
          langs=['de']
      )

   Consider this case:

   .. testcode:: guide_apply_translations_warning

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

   .. testoutput:: guide_apply_translations_warning

      Continent: Europa
      Country: Germany  -- Wrong
      City: Cologne  -- Wrong
      City: Munich  -- Wrong

   As we can see the translations of the filtered queryset are reset.
   To fix it:

   .. testcode:: guide_apply_translations_warning

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
          print('Country: {}'.format(country))
          for city in country.cities.all():
              print('City: {}'.format(city))

   .. testoutput:: guide_apply_translations_warning

      Continent: Europa
      Country: Deutschland
      City: Köln
      City: München

