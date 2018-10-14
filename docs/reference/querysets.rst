*********
QuerySets
*********

.. module:: translations.querysets

This module contains the querysets for the Translations app.

.. class:: TranslatableQuerySet

   A queryset which provides custom translation functionalities.

   .. method:: __init__(*args, **kwargs)

      Initialize the queryset.

      This is an overriden version of
      the :class:`default queryset <django.db.models.query.QuerySet>`\ 's
      :meth:`~django.db.models.query.__init__` method.
      It defines custom translation configurations on the queryset.

      :param args: The arguments of
          the :class:`default queryset <django.db.models.query.QuerySet>`\
          's :meth:`~django.db.models.query.__init__` method.
      :type args: list
      :param kwargs: The keyword arguments of
          the :class:`default queryset <django.db.models.query.QuerySet>`\
          's :meth:`~django.db.models.query.__init__` method.
      :type kwargs: dict

      To get the queryset's custom translation configurations:

      .. testsetup:: __init__

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

      .. testcode:: __init__

         from sample.models import Continent

         continents = Continent.objects.all()

         # access the ``_trans_*`` attributes of the queryset
         print(continents._trans_lang)
         print(continents._trans_rels)

      .. testoutput:: __init__

         None
         ()

   .. method:: _chain(self, **kwargs)

      Return a copy of the current queryset.

      This is an overriden version of
      the :class:`default queryset <django.db.models.query.QuerySet>`\ 's
      :meth:`~django.db.models.query._chain` method.
      It copies custom translation configurations from the current queryset
      to the chained queryset.

      :param kwargs: The keyword arguments of
          the :class:`default queryset <django.db.models.query.QuerySet>`\
          's :meth:`~django.db.models.query._chain` method.
      :type kwargs: dict
      :return: The chained queryset.
      :rtype: TranslatableQuerySet

      To get a copy of the current queryset:

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

         # get a copy of the current queryset
         continents = Continent.objects.all()._chain()

         print(continents)

      .. testoutput:: _chain

         <TranslatableQuerySet [
             <Continent: Europe>,
             <Continent: Asia>,
         ]>

   .. method:: _translate_mode(self)

      Return whether the queryset is in translate mode.

      Checks whether a language is applied on the queryset and also if the
      queryset is in cipher mode.

      :return: whether the queryset is in translate mode.
      :rtype: bool

      To check if the queryset is in translate mode:

      .. testsetup:: _translate_mode

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

      .. testcode:: _translate_mode

         from sample.models import Continent

         continents = Continent.objects.apply('de').decipher()

         # check if the queryset is in translate mode
         print(continents._translate_mode())

      .. testoutput:: _translate_mode

         False

   .. method:: _fetch_all(self)

      Evaluate the queryset.

      This is an overriden version of
      the :class:`default queryset <django.db.models.query.QuerySet>`\ 's
      :meth:`~django.db.models.query._fetch_all` method.
      It translates the instances of the queryset and their specified
      relations in the evaluation if the queryset is in translate mode.

      To evaluate the queryset in normal mode:

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

      To evaluate the queryset in translate mode:

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

      .. testcode:: _fetch_all

         from sample.models import Continent

         continents = Continent.objects.apply('de')

         # evaluate the queryset
         print(continents)

      .. testoutput:: _fetch_all

         <TranslatableQuerySet [
             <Continent: Europa>,
             <Continent: Asien>,
         ]>

   .. method:: _get_translations_queries(self, *queries, **lookup)

      Return the translations queries of some lookups and queries.

      If the lookups or the queries are on the :attr:`translatable fields \
      <translations.models.Translatable.TranslatableMeta.fields>` it returns
      the translations equivalent of the lookup or the query as a new query,
      otherwise it returns the lookup or the query without any change.

      :param queries: The queries to get the translations queries of.
      :type queries: list
      :param lookup: The lookups to get the translations queries of.
      :type lookup: dict
      :return: The translations queries of lookups and queries.
      :rtype: list(~django.db.models.Q)

      To get the translations queries of some lookups and queries:

      .. testcode:: _get_translations_queries

         from sample.models import Continent

         queries = Continent.objects.all()._get_translations_queries(
             countries__name__icontains='Deutsch')

         # output
         print(queries)
   
      .. testoutput:: _get_translations_queries
   
         [
             <Q: (AND:
                 ('countries__translations__field', 'name'),
                 ('countries__translations__language', None),
                 ('countries__translations__text__icontains', 'Deutsch'),
             )>,
         ]

   .. method:: apply(self, lang=None)

      Apply a language on the queryset.

      Causes the queryset to query the translated values in the
      specified language.

      :param lang: The language to apply on the queryset.
          ``None`` means use the :term:`active language` code.
      :type lang: str or None
      :return: The queryset which the language is applied on.
      :rtype: TranslatableQuerySet
      :raise ValueError: If the language code is not included in
          the :data:`~django.conf.settings.LANGUAGES` setting.

      To apply a language on the queryset:

      .. testsetup:: apply

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

      .. testcode:: apply

         from sample.models import Continent

         # apply `German` on the queryset
         continents = Continent.objects.apply(lang='de')

         print(continents)

      .. testoutput:: apply

         <TranslatableQuerySet [
             <Continent: Europa>,
             <Continent: Asien>,
         ]>

      .. note::

         Applying only affects the :attr:`translatable fields \
         <translations.models.Translatable.TranslatableMeta.fields>` that have
         a translation.

   .. method:: translate_related(*fields)

      Translate some relations of the queryset.

      Causes the queryset's specified relations to be translated while
      evaluating the queryset.

      :param relations: The relations of the queryset to translate.
      :type relations: list(str)
      :return: The queryset which the relations of are translated.
      :rtype: TranslatableQuerySet

      To translate some relations of the queryset:

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
         ).apply(lang='de')

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

         Filtering the relations after the translation will cause
         the translations of that relation to be reset.

         .. testcode:: translate_related

            from sample.models import Continent

            continents = Continent.objects.prefetch_related(
                'countries', 'countries__cities',
            ).translate_related(
                'countries', 'countries__cities',
            ).apply('de')

            # Filtering after applying
            print(continents)
            print(continents[0].countries.exclude(name=''))
            print(continents[0].countries.exclude(name='')[0].cities.all())

         .. testoutput:: translate_related

            <TranslatableQuerySet [
                <Continent: Europa>,
                <Continent: Asien>,
            ]>
            <TranslatableQuerySet [
                <Country: Germany>,
            ]>
            <TranslatableQuerySet [
                <City: Cologne>,
            ]>

         The solution is to do the filtering before applying the translations.

         To do this use :class:`~django.db.models.Prefetch`.

         .. testcode:: translate_related

            from django.db.models import Prefetch
            from sample.models import Continent, Country

            # Filtering before applying
            continents = Continent.objects.prefetch_related(
                Prefetch(
                    'countries',
                    queryset=Country.objects.exclude(name=''),
                ),
                'countries__cities',
            ).translate_related(
                'countries', 'countries__cities',
            ).apply('de')

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

   .. method:: cipher(self)

      Use the applied language in the queryset.

      Causes the queryset to use the applied language from there on.

      To use the applied language in the queryset:

      .. testsetup:: cipher

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

      .. testcode:: cipher

         from sample.models import Continent

         # apply German on the queryset
         continents = Continent.objects.apply(lang='de')

         # decipher
         print(continents.decipher())  # use the default language

         # cipher
         print(continents.cipher())    # use the applied language

      .. testoutput:: cipher

         <TranslatableQuerySet [
             <Continent: Europe>,
             <Continent: Asia>,
         ]>
         <TranslatableQuerySet [
             <Continent: Europa>,
             <Continent: Asien>,
         ]>

   .. method:: decipher(self)

      Use the default language in the queryset.

      Causes the queryset to use the default language from there on.

      To use the default language in the queryset:

      .. testsetup:: decipher

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

      .. testcode:: decipher

         from sample.models import Continent

         # apply German on the queryset
         continents = Continent.objects.apply(lang='de')

         # decipher
         print(continents.decipher())  # use the default language

         # cipher
         print(continents.cipher())    # use the applied language

      .. testoutput:: decipher

         <TranslatableQuerySet [
             <Continent: Europe>,
             <Continent: Asia>,
         ]>
         <TranslatableQuerySet [
             <Continent: Europa>,
             <Continent: Asien>,
         ]>

   .. method:: filter(self, *args, **kwargs)

      Filter the queryset.
