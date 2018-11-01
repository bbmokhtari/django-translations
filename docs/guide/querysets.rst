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
This translates the :ref:`translatable fields \
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
