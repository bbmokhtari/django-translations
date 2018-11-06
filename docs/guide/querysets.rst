****************
Guide: QuerySets
****************

This module provides an in depth knowledge of the Translations querysets.

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

Make querysets translatable
===========================

To make a queryset translatable
make sure the queryset model is :ref:`translatable <models.Translatable>`.

.. _querysets.TranslatableQuerySet.translate:

Translate the queryset
======================

To translate the queryset in a language use the
:meth:`~translations.querysets.TranslatableQuerySet.translate` method.
It translates the :ref:`translatable fields \
<models.Translatable.TranslatableMeta.fields>` of the queryset in a language in the evaluation.
It accepts a language code which determines the language to
translate the queryset in.

.. testsetup:: TranslatableQuerySet.translate.1

   create_doc_samples(translations=True)

.. testsetup:: TranslatableQuerySet.translate.2

   create_doc_samples(translations=True)

To translate an instance in a language:

.. testcode:: TranslatableQuerySet.translate.1

   from sample.models import Continent

   # translate the instance
   europe = Continent.objects.translate('de').get(code='EU')

   print(europe)

.. testoutput:: TranslatableQuerySet.translate.1

   Europa

To translate a queryset in a language:

.. testcode:: TranslatableQuerySet.translate.2

   from sample.models import Continent

   # translate the queryset
   continents = Continent.objects.translate('de').all()

   print(continents)

.. testoutput:: TranslatableQuerySet.translate.2

   <TranslatableQuerySet [
       <Continent: Europa>,
       <Continent: Asien>,
   ]>

The language code must already be declared in the
``LANGUAGES`` setting. It is optional and if it is
not passed in, it is automatically set to the :term:`active language` code.

.. note::

   Translating only affects the :ref:`translatable fields \
   <models.Translatable.TranslatableMeta.fields>` that have a translation.

Translate the queryset relations
================================

To translate some queryset relations use the
:meth:`~translations.querysets.TranslatableQuerySet.translate_related` method.
It translates the :ref:`translatable fields \
<models.Translatable.TranslatableMeta.fields>` of the queryset relations in the evaluation.
It accepts some relations which determines the queryset relations to
translate.

.. testsetup:: TranslatableQuerySet.translate_related.1

   create_doc_samples(translations=True)

To translate some queryset relations:

.. testcode:: TranslatableQuerySet.translate_related.1

   from sample.models import Continent

   # translate the queryset relations
   continents = Continent.objects.translate_related(
       'countries',
       'countries__cities',
   ).translate('de')

   print(continents)
   print(continents[0].countries.all())
   print(continents[0].countries.all()[0].cities.all())

.. testoutput:: TranslatableQuerySet.translate_related.1

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

Each relation may be divided into separate parts
by :data:`~django.db.models.constants.LOOKUP_SEP`
(usually ``__``) to represent a deeply nested relation.
Each part must be a ``related_name``.
The models of the relations must be
:ref:`translatable <models.Translatable>`.

.. note::

   It is **recommended** for the queryset relations to be
   prefetched before translating them,
   in order to reach optimal performance.

   To do this use
   ``select_related``,
   ``prefetch_related`` or
   ``prefetch_related_objects``.

.. warning::

   .. testsetup:: TranslatableQuerySet.translate_related.warning.1

      create_doc_samples(translations=True)

   .. testsetup:: TranslatableQuerySet.translate_related.warning.2

      create_doc_samples(translations=True)

   .. testsetup:: TranslatableQuerySet.translate_related.warning.3

      create_doc_samples(translations=True)

   Any subsequent chained methods on the relations queryset which imply
   a database query will reset previously translated results:

   .. testcode:: TranslatableQuerySet.translate_related.warning.1

      from sample.models import Continent

      continents = Continent.objects.translate_related(
          'countries',
      ).translate('de')

      # Querying after translation
      print(continents[0].countries.exclude(name=''))

   .. testoutput:: TranslatableQuerySet.translate_related.warning.1

      <TranslatableQuerySet [
          <Country: Germany>,
      ]>

   In some cases the querying can be done before the translation:

   .. testcode:: TranslatableQuerySet.translate_related.warning.2

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

   .. testoutput:: TranslatableQuerySet.translate_related.warning.2

      <TranslatableQuerySet [
          <Country: Deutschland>,
      ]>

   And in some cases the querying must be done anyway, in these cases:

   .. testcode:: TranslatableQuerySet.translate_related.warning.3

      from sample.models import Continent

      continents = Continent.objects.translate_related(
          'countries',
      ).translate('de')

      # Just `translate` the relation again after querying
      print(continents[0].countries.exclude(name='').translate('de'))

   .. testoutput:: TranslatableQuerySet.translate_related.warning.3

      <TranslatableQuerySet [
          <Country: Deutschland>,
      ]>

.. _querysets.TranslatableQuerySet.probe:

Probe (filter, exclude, etc.) the queryset
==========================================

To probe the queryset in some language(s) use the
:meth:`~translations.querysets.TranslatableQuerySet.probe` method.
It probes the :ref:`translatable fields \
<models.Translatable.TranslatableMeta.fields>` of the queryset in a language in the evaluation.
It accepts some language code(s) which determines the language(s) to
probe the queryset in.

.. testsetup:: TranslatableQuerySet.probe.1

   create_doc_samples(translations=True)

.. testsetup:: TranslatableQuerySet.probe.2

   create_doc_samples(translations=True)

To probe the queryset in a custom language:

.. testcode:: TranslatableQuerySet.probe.1

   from django.db.models import Q
   from sample.models import Continent

   # probe the queryset
   continents = Continent.objects.probe('de').filter(
       Q(name='Europa') | Q(name='Asien'))

   print(continents)

.. testoutput:: TranslatableQuerySet.probe.1

   <TranslatableQuerySet [
       <Continent: Europe>,
       <Continent: Asia>,
   ]>

To probe the queryset in multiple custom languages:

.. testcode:: TranslatableQuerySet.probe.2

   from django.db.models import Q
   from sample.models import Continent

   # probe the queryset
   continents = Continent.objects.probe(['en', 'de']).filter(
       Q(name='Europa') | Q(name='Asien')).distinct()

   print(continents)

.. testoutput:: TranslatableQuerySet.probe.2

   <TranslatableQuerySet [
       <Continent: Europe>,
       <Continent: Asia>,
   ]>

The language code(s) must already be declared in the
``LANGUAGES`` setting. It is optional and if it is
not passed in, it is automatically set to the :term:`active language` code.

.. note::

   Please note that the results are returned in the default language.
   To translate them use the :ref:`translate <querysets.TranslatableQuerySet.translate>` method.

.. note::

   Probing only affects the :ref:`translatable fields \
   <models.Translatable.TranslatableMeta.fields>` that have a translation.

.. note::

   Make sure to use ``distinct`` on
   the probed queryset when using multiple languages, otherwise it may
   return duplicate results.

.. _query.TQ:

Advanced querying
=================

To encapsulate translation queries as objects that can then be combined
logically (using `&` and `|`) use the :class:`~translations.query.TQ` class.
It works just like the normal django ``Q`` object untill you specialize it
(call its object) in some language(s).
It accepts some language code(s) which determines the language(s) to
specialize the query in.

.. testsetup:: TQ.1

   create_doc_samples(translations=True)

To create complex logical combinations of queries for different languages:

.. testcode:: TQ.1

   from translations.query import TQ
   from sample.models import Continent

   continents = Continent.objects.filter(
       TQ(
           countries__cities__name__startswith='Cologne',
       )         # use probe language (default English) for this query
       |         # logical combinator
       TQ(
           countries__cities__name__startswith='Köln',
       )('de')   # use German for this query
   ).distinct()

   print(continents)

.. testoutput:: TQ.1

   <TranslatableQuerySet [
       <Continent: Europe>,
   ]>

The language code(s) must already be declared in the
``LANGUAGES`` setting. It is optional and if it is
not passed in, it is automatically set to the :term:`active language` code.

.. note::

   ``TQ`` objects act exactly like ``Q`` objects,
   untill they are called using some language(s).
