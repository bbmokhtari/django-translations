**************
Ref: QuerySets
**************

.. module:: translations.querysets

This module contains the querysets for the Translations app.

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

.. class:: TranslatableQuerySet

   A queryset which provides custom translation functionalities.

   Provides functionalities like
   :meth:`translate` and :meth:`translate_related`
   to translate the :class:`TranslatableQuerySet` and the relations of it
   and also some other functionalities like
   :meth:`probe`, :meth:`filter` and :meth:`exclude`
   to query the :class:`TranslatableQuerySet`.

   .. testsetup:: TranslatableQuerySet.1

      from sample.utils import create_samples

      create_samples(
          continent_names=['europe', 'asia'],
          country_names=['germany', 'south korea'],
          city_names=['cologne', 'seoul'],
          continent_fields=['name', 'denonym'],
          country_fields=['name', 'denonym'],
          city_fields=['name', 'denonym'],
          langs=['de']
      )

   To use :class:`TranslatableQuerySet`:

   .. testcode:: TranslatableQuerySet.1

      from sample.models import Continent

      continents = Continent.objects.all(
      ).distinct(           # familiar distinct
      ).probe(['en', 'de']  # probe (filter, exclude, etc.) in English and German
      ).filter(             # familiar filtering
          countries__cities__name__startswith='Köln'
      ).translate('de'      # translate the results in German
      ).translate_related(  # translate these relations as well
          'countries', 'countries__cities',
      )

      print(continents)
      print(continents[0].countries.all())
      print(continents[0].countries.all()[0].cities.all())

   .. testoutput:: TranslatableQuerySet.1

      <TranslatableQuerySet [
          <Continent: Europa>,
      ]>
      <TranslatableQuerySet [
          <Country: Deutschland>,
      ]>
      <TranslatableQuerySet [
          <City: Köln>,
      ]>

   .. method:: __init__(*args, **kwargs)

      Initialize a :class:`TranslatableQuerySet`
      with :class:`~django.db.models.query.QuerySet` arguments.

      This is an overriden version of
      the :class:`~django.db.models.query.QuerySet`\ 's
      :meth:`~django.db.models.query.QuerySet.__init__` method.
      It defines custom translation configurations on
      the :class:`TranslatableQuerySet`.

      :param args: The arguments of
          the :class:`~django.db.models.query.QuerySet`\
          's :meth:`~django.db.models.query.QuerySet.__init__` method.
      :type args: list
      :param kwargs: The keyword arguments of
          the :class:`~django.db.models.query.QuerySet`\
          's :meth:`~django.db.models.query.QuerySet.__init__` method.
      :type kwargs: dict

      .. testsetup:: TranslatableQuerySet.__init__.1

         from sample.utils import create_samples

         create_samples(
             continent_names=['europe', 'asia'],
             country_names=['germany', 'south korea'],
             city_names=['cologne', 'seoul'],
             continent_fields=['name', 'denonym'],
             country_fields=['name', 'denonym'],
             city_fields=['name', 'denonym'],
             langs=['de']
         )

      To initialize a :class:`TranslatableQuerySet`:

      .. testcode:: TranslatableQuerySet.__init__.1

         from sample.models import Continent

         # initialize queryset
         continents = Continent.objects.all()

         print(continents)

      .. testoutput:: TranslatableQuerySet.__init__.1

         <TranslatableQuerySet [
             <Continent: Europe>,
             <Continent: Asia>,
         ]>

   .. method:: _chain(**kwargs)

      Return a copy of the current :class:`TranslatableQuerySet`.

      This is an overriden version of
      the :class:`~django.db.models.query.QuerySet`\ 's
      :meth:`~django.db.models.query._chain` method.
      It copies the custom translation configurations from
      the current :class:`TranslatableQuerySet` to
      the copied :class:`TranslatableQuerySet`.

      :param kwargs: The keyword arguments of
          the :class:`~django.db.models.query.QuerySet`\
          's :meth:`~django.db.models.query._chain` method.
      :type kwargs: dict
      :return: The copy of the current :class:`TranslatableQuerySet`.
      :rtype: TranslatableQuerySet

      .. testsetup:: TranslatableQuerySet._chain.1

         from sample.utils import create_samples

         create_samples(
             continent_names=['europe', 'asia'],
             country_names=['germany', 'south korea'],
             city_names=['cologne', 'seoul'],
             continent_fields=['name', 'denonym'],
             country_fields=['name', 'denonym'],
             city_fields=['name', 'denonym'],
             langs=['de']
         )

      To get a copy of the current :class:`TranslatableQuerySet`:

      .. testcode:: TranslatableQuerySet._chain.1

         from sample.models import Continent

         # chain the queryset
         continents = Continent.objects.all()._chain()

         print(continents)

      .. testoutput:: TranslatableQuerySet._chain.1

         <TranslatableQuerySet [
             <Continent: Europe>,
             <Continent: Asia>,
         ]>

   .. method:: _fetch_all()

      Evaluate the :class:`TranslatableQuerySet`.

      This is an overriden version of
      the :class:`~django.db.models.query.QuerySet`\ 's
      :meth:`~django.db.models.query._fetch_all` method.
      It translates the :class:`TranslatableQuerySet`
      and some relations of it
      (specified using the :meth:`translate_related` method)
      in a language
      (specified using the :meth:`translate` method).

      .. testsetup:: TranslatableQuerySet._fetch_all.1

         from sample.utils import create_samples

         create_samples(
             continent_names=['europe', 'asia'],
             country_names=['germany', 'south korea'],
             city_names=['cologne', 'seoul'],
             continent_fields=['name', 'denonym'],
             country_fields=['name', 'denonym'],
             city_fields=['name', 'denonym'],
             langs=['de']
         )

      .. testsetup:: TranslatableQuerySet._fetch_all.2

         from sample.utils import create_samples

         create_samples(
             continent_names=['europe', 'asia'],
             country_names=['germany', 'south korea'],
             city_names=['cologne', 'seoul'],
             continent_fields=['name', 'denonym'],
             country_fields=['name', 'denonym'],
             city_fields=['name', 'denonym'],
             langs=['de']
         )

      To evaluate the :class:`TranslatableQuerySet`
      (using the :term:`default language`):

      .. testcode:: TranslatableQuerySet._fetch_all.1

         from sample.models import Continent

         continents = Continent.objects.all()

         # evaluate the queryset
         print(continents)

      .. testoutput:: TranslatableQuerySet._fetch_all.1

         <TranslatableQuerySet [
             <Continent: Europe>,
             <Continent: Asia>,
         ]>

      To evaluate the :class:`TranslatableQuerySet`
      (using a custom language):

      .. testcode:: TranslatableQuerySet._fetch_all.2

         from sample.models import Continent

         continents = Continent.objects.translate('de')

         # evaluate the queryset
         print(continents)

      .. testoutput:: TranslatableQuerySet._fetch_all.2

         <TranslatableQuerySet [
             <Continent: Europa>,
             <Continent: Asien>,
         ]>

   .. method:: translate(lang=None)

      Translate the :class:`TranslatableQuerySet` in a language.

      Causes the :class:`TranslatableQuerySet` to be
      translated in the specified language in the evaluation.

      :param lang: The language to translate the :class:`TranslatableQuerySet`
          in.
          ``None`` means use the :term:`active language` code.
      :type lang: str or None
      :return: The :class:`TranslatableQuerySet` which will be translated in the
          specified language.
      :rtype: TranslatableQuerySet
      :raise ValueError: If the language code is not included in
          the :data:`~django.conf.settings.LANGUAGES` setting.

      .. testsetup:: TranslatableQuerySet.translate.1

         from sample.utils import create_samples

         create_samples(
             continent_names=['europe', 'asia'],
             country_names=['germany', 'south korea'],
             city_names=['cologne', 'seoul'],
             continent_fields=['name', 'denonym'],
             country_fields=['name', 'denonym'],
             city_fields=['name', 'denonym'],
             langs=['de']
         )

      .. testsetup:: TranslatableQuerySet.translate.2

         from sample.utils import create_samples

         create_samples(
             continent_names=['europe', 'asia'],
             country_names=['germany', 'south korea'],
             city_names=['cologne', 'seoul'],
             continent_fields=['name', 'denonym'],
             country_fields=['name', 'denonym'],
             city_fields=['name', 'denonym'],
             langs=['de']
         )

      To translate the :class:`TranslatableQuerySet` (an instance) in a language:

      .. testcode:: TranslatableQuerySet.translate.1

         from sample.models import Continent

         # translate the instance
         europe = Continent.objects.translate('de').get(code='EU')

         print(europe)

      .. testoutput:: TranslatableQuerySet.translate.1

         Europa

      To translate the :class:`TranslatableQuerySet` (a queryset) in a language:

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

      .. note::

         Translating only affects the :attr:`TranslatableMeta.fields \
         <translations.models.Translatable.TranslatableMeta.fields>` that have
         a translation.

   .. method:: translate_related(*fields)

      Translate some :class:`TranslatableQuerySet` relations.

      Causes the :class:`TranslatableQuerySet` relations to be
      translated in the evaluation.

      :param relations: The :class:`TranslatableQuerySet` relations
          to translate.
      :type relations: list(str)
      :return: The :class:`TranslatableQuerySet` which the relations of will
          be translated.
      :rtype: TranslatableQuerySet
      :raise TypeError: If the models of the relations are
          not :class:`~translations.models.Translatable`.
      :raise ~django.core.exceptions.FieldDoesNotExist: If a relation is
          pointing to the fields that don't exist.

      .. testsetup:: TranslatableQuerySet.translate_related.1

         from sample.utils import create_samples

         create_samples(
             continent_names=['europe', 'asia'],
             country_names=['germany', 'south korea'],
             city_names=['cologne', 'seoul'],
             continent_fields=['name', 'denonym'],
             country_fields=['name', 'denonym'],
             city_fields=['name', 'denonym'],
             langs=['de']
         )

      To translate some :class:`TranslatableQuerySet` relations:

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

      .. note::

         It is **recommended** for the queryset relations to be
         prefetched before translating them,
         in order to reach optimal performance.

         To do this use
         :meth:`~django.db.models.query.QuerySet.select_related`,
         :meth:`~django.db.models.query.QuerySet.prefetch_related` or
         :func:`~django.db.models.prefetch_related_objects`.

      .. warning::

         .. testsetup:: TranslatableQuerySet.translate_related.warning.1

            from sample.utils import create_samples

            create_samples(
                continent_names=['europe', 'asia'],
                country_names=['germany', 'south korea'],
                city_names=['cologne', 'seoul'],
                continent_fields=['name', 'denonym'],
                country_fields=['name', 'denonym'],
                city_fields=['name', 'denonym'],
                langs=['de']
            )

         .. testsetup:: TranslatableQuerySet.translate_related.warning.2

            from sample.utils import create_samples

            create_samples(
                continent_names=['europe', 'asia'],
                country_names=['germany', 'south korea'],
                city_names=['cologne', 'seoul'],
                continent_fields=['name', 'denonym'],
                country_fields=['name', 'denonym'],
                city_fields=['name', 'denonym'],
                langs=['de']
            )

         .. testsetup:: TranslatableQuerySet.translate_related.warning.3

            from sample.utils import create_samples

            create_samples(
                continent_names=['europe', 'asia'],
                country_names=['germany', 'south korea'],
                city_names=['cologne', 'seoul'],
                continent_fields=['name', 'denonym'],
                country_fields=['name', 'denonym'],
                city_fields=['name', 'denonym'],
                langs=['de']
            )

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

   .. method:: probe(lang=None)

      Probe the :class:`TranslatableQuerySet` in some language(s).

      Causes the :class:`TranslatableQuerySet` to be
      probed in the specified language(s) in the evaluation.

      :param lang: The language(s) to probe the :class:`TranslatableQuerySet`
          in.
          ``None`` means use the :term:`active language` code.
      :type lang: str or list or None
      :return: The :class:`TranslatableQuerySet` which will be probed in the
          specified language(s).
      :rtype: TranslatableQuerySet
      :raise ValueError: If the language code is not included in
          the :data:`~django.conf.settings.LANGUAGES` setting.

      .. testsetup:: TranslatableQuerySet.probe.1

         from sample.utils import create_samples

         create_samples(
             continent_names=['europe', 'asia'],
             country_names=['germany', 'south korea'],
             city_names=['cologne', 'seoul'],
             continent_fields=['name', 'denonym'],
             country_fields=['name', 'denonym'],
             city_fields=['name', 'denonym'],
             langs=['de']
         )

      .. testsetup:: TranslatableQuerySet.probe.2

         from sample.utils import create_samples

         create_samples(
             continent_names=['europe', 'asia'],
             country_names=['germany', 'south korea'],
             city_names=['cologne', 'seoul'],
             continent_fields=['name', 'denonym'],
             country_fields=['name', 'denonym'],
             city_fields=['name', 'denonym'],
             langs=['de']
         )

      To probe the :class:`TranslatableQuerySet` in some language(s)
      (a custom language):

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

      To probe the :class:`TranslatableQuerySet` in some language(s)
      (multiple custom languages):

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

      .. note::

         Probing only affects the :attr:`TranslatableMeta.fields \
         <translations.models.Translatable.TranslatableMeta.fields>` that have
         a translation.

      .. note::

         Make sure to use :meth:`~django.db.models.query.QuerySet.distinct` on
         the probed queryset when using multiple languages, otherwise it may
         return duplicate results.

   .. method:: filter(*args, **kwargs)

      Filter the :class:`TranslatableQuerySet`.

      This is an overriden version of
      the :class:`~django.db.models.query.QuerySet`\ 's
      :meth:`~django.db.models.query.QuerySet.filter` method.
      It filters the :class:`TranslatableQuerySet` in the probe language(s).

      :param args: The arguments of
          the :class:`~django.db.models.query.QuerySet`\
          's :meth:`~django.db.models.query.QuerySet.filter` method.
      :type args: list
      :param kwargs: The keyword arguments of
          the :class:`~django.db.models.query.QuerySet`\
          's :meth:`~django.db.models.query.QuerySet.filter` method.
      :type kwargs: dict

      .. testsetup:: TranslatableQuerySet.filter.1

         from sample.utils import create_samples

         create_samples(
             continent_names=['europe', 'asia'],
             country_names=['germany', 'south korea'],
             city_names=['cologne', 'seoul'],
             continent_fields=['name', 'denonym'],
             country_fields=['name', 'denonym'],
             city_fields=['name', 'denonym'],
             langs=['de']
         )

      .. testsetup:: TranslatableQuerySet.filter.2

         from sample.utils import create_samples

         create_samples(
             continent_names=['europe', 'asia'],
             country_names=['germany', 'south korea'],
             city_names=['cologne', 'seoul'],
             continent_fields=['name', 'denonym'],
             country_fields=['name', 'denonym'],
             city_fields=['name', 'denonym'],
             langs=['de']
         )

      .. testsetup:: TranslatableQuerySet.filter.3

         from sample.utils import create_samples

         create_samples(
             continent_names=['europe', 'asia'],
             country_names=['germany', 'south korea'],
             city_names=['cologne', 'seoul'],
             continent_fields=['name', 'denonym'],
             country_fields=['name', 'denonym'],
             city_fields=['name', 'denonym'],
             langs=['de']
         )

      To filter the :class:`TranslatableQuerySet`
      (using the :term:`default language`):

      .. testcode:: TranslatableQuerySet.filter.1

         from sample.models import Continent

         # filter the queryset
         continents = Continent.objects.filter(
             countries__name__icontains='Ger')

         print(continents)

      .. testoutput:: TranslatableQuerySet.filter.1

         <TranslatableQuerySet [
             <Continent: Europe>,
         ]>

      To filter the :class:`TranslatableQuerySet`
      (using a custom language):

      .. testcode:: TranslatableQuerySet.filter.2

         from sample.models import Continent

         # filter the queryset
         continents = Continent.objects.probe('de').filter(
             countries__name__icontains='Deutsch')

         print(continents)

      .. testoutput:: TranslatableQuerySet.filter.2

         <TranslatableQuerySet [
             <Continent: Europe>,
         ]>

      To filter the :class:`TranslatableQuerySet`
      (using multiple custom languages):

      .. testcode:: TranslatableQuerySet.filter.3

         from sample.models import Continent

         # filter the queryset
         continents = Continent.objects.probe(['en', 'de']).filter(
             countries__name__icontains='Deutsch').distinct()

         print(continents)

      .. testoutput:: TranslatableQuerySet.filter.3

         <TranslatableQuerySet [
             <Continent: Europe>,
         ]>

   .. method:: exclude(*args, **kwargs)

      Exclude the :class:`TranslatableQuerySet`.

      This is an overriden version of
      the :class:`~django.db.models.query.QuerySet`\ 's
      :meth:`~django.db.models.query.QuerySet.exclude` method.
      It excludes the :class:`TranslatableQuerySet` in the probe language(s).

      :param args: The arguments of
          the :class:`~django.db.models.query.QuerySet`\
          's :meth:`~django.db.models.query.QuerySet.exclude` method.
      :type args: list
      :param kwargs: The keyword arguments of
          the :class:`~django.db.models.query.QuerySet`\
          's :meth:`~django.db.models.query.QuerySet.exclude` method.
      :type kwargs: dict

      .. testsetup:: TranslatableQuerySet.exclude.1

         from sample.utils import create_samples

         create_samples(
             continent_names=['europe', 'asia'],
             country_names=['germany', 'south korea'],
             city_names=['cologne', 'seoul'],
             continent_fields=['name', 'denonym'],
             country_fields=['name', 'denonym'],
             city_fields=['name', 'denonym'],
             langs=['de']
         )

      .. testsetup:: TranslatableQuerySet.exclude.2

         from sample.utils import create_samples

         create_samples(
             continent_names=['europe', 'asia'],
             country_names=['germany', 'south korea'],
             city_names=['cologne', 'seoul'],
             continent_fields=['name', 'denonym'],
             country_fields=['name', 'denonym'],
             city_fields=['name', 'denonym'],
             langs=['de']
         )

      .. testsetup:: TranslatableQuerySet.exclude.3

         from sample.utils import create_samples

         create_samples(
             continent_names=['europe', 'asia'],
             country_names=['germany', 'south korea'],
             city_names=['cologne', 'seoul'],
             continent_fields=['name', 'denonym'],
             country_fields=['name', 'denonym'],
             city_fields=['name', 'denonym'],
             langs=['de']
         )

      To exclude the :class:`TranslatableQuerySet`
      (using the :term:`default language`):

      .. testcode:: TranslatableQuerySet.exclude.1

         from sample.models import Continent

         # exclude the queryset
         continents = Continent.objects.exclude(
             countries__name__icontains='Ger')

         print(continents)

      .. testoutput:: TranslatableQuerySet.exclude.1

         <TranslatableQuerySet [
             <Continent: Asia>,
         ]>

      To exclude the :class:`TranslatableQuerySet`
      (using a custom language):

      .. testcode:: TranslatableQuerySet.exclude.2

         from sample.models import Continent

         # exclude the queryset
         continents = Continent.objects.probe('de').exclude(
             countries__name__icontains='Deutsch')

         print(continents)

      .. testoutput:: TranslatableQuerySet.exclude.2

         <TranslatableQuerySet [
             <Continent: Asia>,
         ]>

      To exclude the :class:`TranslatableQuerySet`
      (using multiple custom languages):

      .. testcode:: TranslatableQuerySet.exclude.3

         from sample.models import Continent

         # exclude the queryset
         continents = Continent.objects.probe(['en', 'de']).exclude(
             countries__name__icontains='Deutsch').distinct()

         print(continents)

      .. testoutput:: TranslatableQuerySet.exclude.3

         <TranslatableQuerySet [
             <Continent: Asia>,
         ]>
