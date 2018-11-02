*********
QuerySets
*********

This module provides an in depth knowledge of the Translations querysets.

Make querysets translatable
===========================

To make a queryset translatable
make sure the queryset model is :ref:`translatable <translatable-models>`.

Translate the queryset
======================

To translate the queryset in a language use the
:meth:`~translations.querysets.TranslatableQuerySet.translate` method.
It translates the :ref:`translatable fields \
<specify-fields>` of the queryset in the evaluation.
It accepts a language code which determines the language to
translate the queryset in.

.. testsetup:: guide_translate

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

To translate an instance:

.. testcode:: guide_translate

   from sample.models import Continent

   # translate the instance
   europe = Continent.objects.translate('de').get(code='EU')

   print(europe)

.. testoutput:: guide_translate

   Europa

To translate a queryset:

.. testcode:: guide_translate

   from sample.models import Continent

   # translate the queryset
   continents = Continent.objects.translate('de').all()

   print(continents)

.. testoutput:: guide_translate

   <TranslatableQuerySet [
       <Continent: Europa>,
       <Continent: Asien>,
   ]>

The language code must already be declared in the
``LANGUAGES`` setting. It is optional and if it is
not passed in, it is automatically set to the :term:`active language` code.

.. note::

   Translating only affects the :ref:`translatable fields \
   <specify-fields>` that have a translation.

Translate the queryset relations
================================

To translate some queryset relations use the
:meth:`~translations.querysets.TranslatableQuerySet.translate_related` method.
It translates the :ref:`translatable fields \
<specify-fields>` of the queryset relations in the evaluation.
It accepts some relations which determines the queryset relations to
translate.

.. testsetup:: guide_translate_related

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

To translate some queryset relations:

.. testcode:: guide_translate_related

   from sample.models import Continent

   # translate the queryset relations
   continents = Continent.objects.translate_related(
       'countries',
       'countries__cities',
   ).translate('de')

   print(continents)
   print(continents[0].countries.all())
   print(continents[0].countries.all()[0].cities.all())

.. testoutput:: guide_translate_related

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

The relations must be an unpacked list of strings.
They may be separated by ``__``\ s to represent a deeply nested relation.
The models of the relations must be :ref:`translatable <translatable-models>`.

.. note::

   It is **recommended** for the queryset relations to be
   prefetched before translating them,
   in order to reach optimal performance.

   To do this use
   ``select_related``,
   ``prefetch_related`` or
   ``prefetch_related_objects``.

.. warning::

   Any subsequent chained methods on the relations queryset which imply
   a database query will reset previously translated results:

   .. testcode:: translate_related

      from sample.models import Continent

      continents = Continent.objects.translate_related(
          'countries',
      ).translate('de')

      # Querying after translation
      print(continents[0].countries.exclude(name=''))

   .. testoutput:: translate_related

      <TranslatableQuerySet [
          <Country: Germany>,
      ]>

   In some cases the querying can be done before the translation:

   .. testcode:: translate_related

      from django.db.models import Prefetch
      from sample.models import Continent, Country

      # Querying before translation
      continents = Continent.objects.prefetch_related(
          Prefetch(
              'countries',
              queryset=Country.objects.exclude(name=''),
          ),
      ).translate_related(
          'countries',
      ).translate('de')

      print(continents[0].countries.all())

   .. testoutput:: translate_related

      <TranslatableQuerySet [
          <Country: Deutschland>,
      ]>

   And in some cases the querying must be done anyway, in these cases:

   .. testcode:: translate_related

      from sample.models import Continent

      continents = Continent.objects.translate_related(
          'countries',
      ).translate('de')

      # Just `translate` the relation again after querying
      print(continents[0].countries.exclude(name='').translate('de'))

   .. testoutput:: translate_related

      <TranslatableQuerySet [
          <Country: Deutschland>,
      ]>
