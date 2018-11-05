**************
Ref: QuerySets
**************

.. module:: translations.querysets

This module contains the querysets for the Translations app.

.. class:: TranslatableQuerySet

   A queryset which provides custom translation functionalities.

   Provides functionalities like
   :meth:`translate` and :meth:`translate_related`
   to translate the :class:`TranslatableQuerySet` and the relations of it
   and also some other functionalities like
   :meth:`probe`, :meth:`filter` and :meth:`exclude`
   to query the :class:`TranslatableQuerySet`.

   .. testsetup:: TranslatableQuerySet_1

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

   To use :class:`TranslatableQuerySet`:

   .. testcode:: TranslatableQuerySet_1

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

   .. testoutput:: TranslatableQuerySet_1

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

      .. testsetup:: __init___1

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

      To initialize a :class:`TranslatableQuerySet`:

      .. testcode:: __init___1

         from sample.models import Continent

         # initialize queryset
         continents = Continent.objects.all()

         print(continents)

      .. testoutput:: __init___1

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

      .. testsetup:: _chain_1

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

      To get a copy of the current :class:`TranslatableQuerySet`:

      .. testcode:: _chain_1

         from sample.models import Continent

         # chain the queryset
         continents = Continent.objects.all()._chain()

         print(continents)

      .. testoutput:: _chain_1

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

      .. testsetup:: _fetch_all_1

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

      .. testsetup:: _fetch_all_2

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

      To evaluate the :class:`TranslatableQuerySet`
      (using the :term:`default language`):

      .. testcode:: _fetch_all_1

         from sample.models import Continent

         continents = Continent.objects.all()

         # evaluate the queryset
         print(continents)

      .. testoutput:: _fetch_all_1

         <TranslatableQuerySet [
             <Continent: Europe>,
             <Continent: Asia>,
         ]>

      To evaluate the :class:`TranslatableQuerySet`
      (using a custom language):

      .. testcode:: _fetch_all_2

         from sample.models import Continent

         continents = Continent.objects.translate('de')

         # evaluate the queryset
         print(continents)

      .. testoutput:: _fetch_all_2

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

      .. testsetup:: translate_1

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

      .. testsetup:: translate_2

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

      To translate the :class:`TranslatableQuerySet` (an instance) in a language:

      .. testcode:: translate_1

         from sample.models import Continent

         # translate the instance
         europe = Continent.objects.translate('de').get(code='EU')

         print(europe)

      .. testoutput:: translate_1

         Europa

      To translate the :class:`TranslatableQuerySet` (a queryset) in a language:

      .. testcode:: translate_2

         from sample.models import Continent

         # translate the queryset
         continents = Continent.objects.translate('de').all()

         print(continents)

      .. testoutput:: translate_2

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

      .. testsetup:: translate_related_1

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

      To translate some :class:`TranslatableQuerySet` relations:

      .. testcode:: translate_related_1

         from sample.models import Continent

         # translate the queryset relations
         continents = Continent.objects.translate_related(
             'countries',
             'countries__cities',
         ).translate('de')

         print(continents)
         print(continents[0].countries.all())
         print(continents[0].countries.all()[0].cities.all())

      .. testoutput:: translate_related_1

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

         .. testsetup:: translate_related_warning_1

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

         .. testsetup:: translate_related_warning_2

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

         .. testsetup:: translate_related_warning_3

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

         Any subsequent chained methods on the relations queryset which imply
         a database query will reset previously translated results:

         .. testcode:: translate_related_warning_1

            from sample.models import Continent

            continents = Continent.objects.translate_related(
                'countries',
            ).translate('de')

            # Querying after translation
            print(continents[0].countries.exclude(name=''))

         .. testoutput:: translate_related_warning_1

            <TranslatableQuerySet [
                <Country: Germany>,
            ]>

         In some cases the querying can be done before the translation:

         .. testcode:: translate_related_warning_2

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

         .. testoutput:: translate_related_warning_2

            <TranslatableQuerySet [
                <Country: Deutschland>,
            ]>

         And in some cases the querying must be done anyway, in these cases:

         .. testcode:: translate_related_warning_3

            from sample.models import Continent

            continents = Continent.objects.translate_related(
                'countries',
            ).translate('de')

            # Just `translate` the relation again after querying
            print(continents[0].countries.exclude(name='').translate('de'))

         .. testoutput:: translate_related_warning_3

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

      .. testsetup:: probe_1

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

      .. testsetup:: probe_2

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

      To probe the :class:`TranslatableQuerySet` in some language(s)
      (a custom language):

      .. testcode:: probe_1

         from django.db.models import Q
         from sample.models import Continent

         # probe the queryset
         continents = Continent.objects.probe('de').filter(
             Q(name='Europa') | Q(name='Asien'))

         print(continents)

      .. testoutput:: probe_1

         <TranslatableQuerySet [
             <Continent: Europe>,
             <Continent: Asia>,
         ]>

      To probe the :class:`TranslatableQuerySet` in some language(s)
      (multiple custom languages):

      .. testcode:: probe_2

         from django.db.models import Q
         from sample.models import Continent

         # probe the queryset
         continents = Continent.objects.probe(['en', 'de']).filter(
             Q(name='Europa') | Q(name='Asien')).distinct()

         print(continents)

      .. testoutput:: probe_2

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

      .. testsetup:: filter_1

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

      .. testsetup:: filter_2

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

      .. testsetup:: filter_3

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

      To filter the :class:`TranslatableQuerySet`
      (using the :term:`default language`):

      .. testcode:: filter_1

         from sample.models import Continent

         # filter the queryset
         continents = Continent.objects.filter(
             countries__name__icontains='Ger')

         print(continents)

      .. testoutput:: filter_1

         <TranslatableQuerySet [
             <Continent: Europe>,
         ]>

      To filter the :class:`TranslatableQuerySet`
      (using a custom language):

      .. testcode:: filter_2

         from sample.models import Continent

         # filter the queryset
         continents = Continent.objects.probe('de').filter(
             countries__name__icontains='Deutsch')

         print(continents)

      .. testoutput:: filter_2

         <TranslatableQuerySet [
             <Continent: Europe>,
         ]>

      To filter the :class:`TranslatableQuerySet`
      (using multiple custom languages):

      .. testcode:: filter_3

         from sample.models import Continent

         # filter the queryset
         continents = Continent.objects.probe(['en', 'de']).filter(
             countries__name__icontains='Deutsch').distinct()

         print(continents)

      .. testoutput:: filter_3

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

      .. testsetup:: exclude_1

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

      .. testsetup:: exclude_2

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

      .. testsetup:: exclude_3

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

      To exclude the :class:`TranslatableQuerySet`
      (using the :term:`default language`):

      .. testcode:: exclude_1

         from sample.models import Continent

         # exclude the queryset
         continents = Continent.objects.exclude(
             countries__name__icontains='Ger')

         print(continents)

      .. testoutput:: exclude_1

         <TranslatableQuerySet [
             <Continent: Asia>,
         ]>

      To exclude the :class:`TranslatableQuerySet`
      (using a custom language):

      .. testcode:: exclude_2

         from sample.models import Continent

         # exclude the queryset
         continents = Continent.objects.probe('de').exclude(
             countries__name__icontains='Deutsch')

         print(continents)

      .. testoutput:: exclude_2

         <TranslatableQuerySet [
             <Continent: Asia>,
         ]>

      To exclude the :class:`TranslatableQuerySet`
      (using multiple custom languages):

      .. testcode:: exclude_3

         from sample.models import Continent

         # exclude the queryset
         continents = Continent.objects.probe(['en', 'de']).exclude(
             countries__name__icontains='Deutsch').distinct()

         print(continents)

      .. testoutput:: exclude_3

         <TranslatableQuerySet [
             <Continent: Asia>,
         ]>
