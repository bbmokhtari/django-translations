*********
QuerySets
*********

.. module:: translations.querysets

This module contains the querysets for the Translations app.

.. class:: TranslatableQuerySet

   A queryset which provides custom translation functionalities.

   Provides functionalities like
   :meth:`translate` and :meth:`translate_related`
   to evaluate the :class:`TranslatableQuerySet`
   and also some other functionalities like
   :meth:`probe`, :meth:`filter` and :meth:`exclude`
   to probe the :class:`TranslatableQuerySet`.

   To use :class:`TranslatableQuerySet`:

   .. testsetup:: TranslatableQuerySet

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

   .. testcode:: TranslatableQuerySet

      from sample.models import Continent

      continents = Continent.objects.all(
      ).distinct(           # familiar distinct
      ).probe(['en', 'de']  # filter in English and German
      ).filter(             # familiar filtering
          countries__cities__name__startswith='Köln'
      ).translate('de'      # translate the results in German
      ).translate_related(  # translate these relations as well
          'countries', 'countries__cities',
      )

      print(continents)
      print(continents[0].countries.all())
      print(continents[0].countries.all()[0].cities.all())

   .. testoutput:: TranslatableQuerySet

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

      To initialize a :class:`TranslatableQuerySet`:

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

      .. testcode:: init

         from sample.models import Continent

         # initialize queryset
         continents = Continent.objects.all()

         print(continents)

      .. testoutput:: init

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

      To get a copy of the current :class:`TranslatableQuerySet`:

      .. testsetup:: _chain

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

      .. testcode:: _chain

         from sample.models import Continent

         # chain the queryset
         continents = Continent.objects.all()._chain()

         print(continents)

      .. testoutput:: _chain

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

      .. testsetup:: _fetch_all

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

      .. testcode:: _fetch_all

         from sample.models import Continent

         continents = Continent.objects.all()

         # evaluate the queryset
         print(continents)

      .. testoutput:: _fetch_all

         <TranslatableQuerySet [
             <Continent: Europe>,
             <Continent: Asia>,
         ]>

      To evaluate the :class:`TranslatableQuerySet`
      (using a custom language):

      .. testcode:: _fetch_all

         from sample.models import Continent

         continents = Continent.objects.translate('de')

         # evaluate the queryset
         print(continents)

      .. testoutput:: _fetch_all

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

      .. testsetup:: translate

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

      To translate the :class:`TranslatableQuerySet` in a language:

      .. testcode:: translate

         from sample.models import Continent

         # translate the queryset
         continents = Continent.objects.translate('de')

         print(continents)

      .. testoutput:: translate

         <TranslatableQuerySet [
             <Continent: Europa>,
             <Continent: Asien>,
         ]>

      .. note::

         Translating only affects the :attr:`translatable fields \
         <translations.models.Translatable.TranslatableMeta.fields>` that have
         a translation.

   .. method:: translate_related(*fields)

      Translate some relations of the :class:`TranslatableQuerySet`.

      Causes the relations of the :class:`TranslatableQuerySet` to be
      translated in the evaluation.

      :param relations: The relations of the :class:`TranslatableQuerySet`
          to translate.
      :type relations: list(str)
      :return: The :class:`TranslatableQuerySet` which the relations of will
          be translated.
      :rtype: TranslatableQuerySet

      To translate some relations of the :class:`TranslatableQuerySet`:

      .. testsetup:: translate_related

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

      .. testcode:: translate_related

         from sample.models import Continent

         # translate some relations of the queryset
         continents = Continent.objects.translate_related(
             'countries',
             'countries__cities',
         ).translate('de')

         print(continents)
         print(continents[0].countries.all())
         print(continents[0].countries.all()[0].cities.all())

      .. testoutput:: translate_related

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

         It is **recommended** for the relations of the queryset to be
         prefetched before translating them,
         in order to reach optimal performance.

         To do this use
         :meth:`~django.db.models.query.QuerySet.select_related`,
         :meth:`~django.db.models.query.QuerySet.prefetch_related` or
         :func:`~django.db.models.prefetch_related_objects`.

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

      .. testsetup:: probe

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
      (using a custom language):

      .. testcode:: probe

         from django.db.models import Q
         from sample.models import Continent

         # query the queryset
         continents = Continent.objects.probe('de').filter(
             Q(name='Europa') | Q(name='Asien'))

         print(continents)

      .. testoutput:: probe

         <TranslatableQuerySet [
             <Continent: Europe>,
             <Continent: Asia>,
         ]>

      To probe the :class:`TranslatableQuerySet` in some language(s)
      (using multiple custom languages):

      .. testcode:: probe

         from django.db.models import Q
         from sample.models import Continent

         # query the queryset
         continents = Continent.objects.probe(['en', 'de']).filter(
             Q(name='Europa') | Q(name='Asien')).distinct()

         print(continents)

      .. testoutput:: probe

         <TranslatableQuerySet [
             <Continent: Europe>,
             <Continent: Asia>,
         ]>

      .. note::

         Probing only affects the :attr:`translatable fields \
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

      .. testsetup:: filter

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

      .. testcode:: filter

         from sample.models import Continent

         # filter the queryset
         continents = Continent.objects.filter(
             countries__name__icontains='Ger')

         print(continents)

      .. testoutput:: filter

         <TranslatableQuerySet [
             <Continent: Europe>,
         ]>

      To filter the :class:`TranslatableQuerySet`
      (using a custom language):

      .. testcode:: filter

         from sample.models import Continent

         # filter the queryset
         continents = Continent.objects.probe('de').filter(
             countries__name__icontains='Deutsch')

         print(continents)

      .. testoutput:: filter

         <TranslatableQuerySet [
             <Continent: Europe>,
         ]>

      To filter the :class:`TranslatableQuerySet`
      (using multiple custom languages):

      .. testcode:: filter

         from sample.models import Continent

         # filter the queryset
         continents = Continent.objects.probe(['en', 'de']).filter(
             countries__name__icontains='Deutsch').distinct()

         print(continents)

      .. testoutput:: filter

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

      .. testsetup:: exclude

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

      .. testcode:: exclude

         from sample.models import Continent

         # exclude the queryset
         continents = Continent.objects.exclude(
             countries__name__icontains='Ger')

         print(continents)

      .. testoutput:: exclude

         <TranslatableQuerySet [
             <Continent: Asia>,
         ]>

      To exclude the :class:`TranslatableQuerySet`
      (using a custom language):

      .. testcode:: exclude

         from sample.models import Continent

         # exclude the queryset
         continents = Continent.objects.probe('de').exclude(
             countries__name__icontains='Deutsch')

         print(continents)

      .. testoutput:: exclude

         <TranslatableQuerySet [
             <Continent: Asia>,
         ]>

      To exclude the :class:`TranslatableQuerySet`
      (using multiple custom languages):

      .. testcode:: exclude

         from sample.models import Continent

         # exclude the queryset
         continents = Continent.objects.probe(['en', 'de']).exclude(
             countries__name__icontains='Deutsch').distinct()

         print(continents)

      .. testoutput:: exclude

         <TranslatableQuerySet [
             <Continent: Asia>,
         ]>
