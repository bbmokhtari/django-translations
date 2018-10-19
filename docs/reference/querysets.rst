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
      :meth:`~django.db.models.query.QuerySet.__init__` method.
      It defines custom translation configurations on the queryset.

      :param args: The arguments of
          the :class:`default queryset <django.db.models.query.QuerySet>`\
          's :meth:`~django.db.models.query.QuerySet.__init__` method.
      :type args: list
      :param kwargs: The keyword arguments of
          the :class:`default queryset <django.db.models.query.QuerySet>`\
          's :meth:`~django.db.models.query.QuerySet.__init__` method.
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

   .. method:: apply(self, lang=None)

      Apply a language on the queryset.

      Causes the queryset to query the database in the specified language.

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

         Any subsequent chained methods on the relations which imply a
         different database query will reset previously translated results:

         .. testcode:: translate_related

            from sample.models import Continent

            continents = Continent.objects.translate_related(
                'countries',
            ).apply('de')

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
            ).apply('de')

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
            ).apply('de')

            # Just `apply` on the relation again after querying
            print(continents[0].countries.exclude(name='').apply('de'))

         .. testoutput:: translate_related

            <TranslatableQuerySet [
                <Country: Deutschland>,
            ]>

   .. method:: cipher(self)

      Use the applied language in the queryset.

      Causes the queryset to use the applied language from there on.

      :return: The queryset which uses the applied language.
      :rtype: TranslatableQuerySet

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

         # use the applied language
         print(continents.cipher())

      .. testoutput:: cipher

         <TranslatableQuerySet [
             <Continent: Europa>,
             <Continent: Asien>,
         ]>

   .. method:: decipher(self)

      Use the default language in the queryset.

      Causes the queryset to use the default language from there on.

      :return: The queryset which uses the default language.
      :rtype: TranslatableQuerySet

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

         # use the default language
         print(continents.decipher())

      .. testoutput:: decipher

         <TranslatableQuerySet [
             <Continent: Europe>,
             <Continent: Asia>,
         ]>

   .. method:: filter(self, *args, **kwargs)

      Filter the queryset with lookups and queries.

      This is an overriden version of
      the :class:`default queryset <django.db.models.query.QuerySet>`\ 's
      :meth:`~django.db.models.query.QuerySet.filter` method.
      It filters the queryset in the specified language if the queryset is in
      translate mode.

      :param args: The arguments of
          the :class:`default queryset <django.db.models.query.QuerySet>`\
          's :meth:`~django.db.models.query.QuerySet.filter` method.
      :type args: list
      :param kwargs: The keyword arguments of
          the :class:`default queryset <django.db.models.query.QuerySet>`\
          's :meth:`~django.db.models.query.QuerySet.filter` method.
      :type kwargs: dict

      To filter the queryset in normal mode:

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

      To filter the queryset in translate mode:

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

      .. testcode:: filter

         from sample.models import Continent

         # filter the queryset
         continents = Continent.objects.apply('de').filter(
            countries__name__icontains='Deutsch')

         print(continents)

      .. testoutput:: filter

         <TranslatableQuerySet [
             <Continent: Europa>,
         ]>

   .. method:: exclude(self, *args, **kwargs)

      Exclude the queryset with lookups and queries.

      This is an overriden version of
      the :class:`default queryset <django.db.models.query.QuerySet>`\ 's
      :meth:`~django.db.models.query.QuerySet.exclude` method.
      It excludes the queryset in the specified language if the queryset is in
      translate mode.

      :param args: The arguments of
          the :class:`default queryset <django.db.models.query.QuerySet>`\
          's :meth:`~django.db.models.query.QuerySet.exclude` method.
      :type args: list
      :param kwargs: The keyword arguments of
          the :class:`default queryset <django.db.models.query.QuerySet>`\
          's :meth:`~django.db.models.query.QuerySet.exclude` method.
      :type kwargs: dict

      To exclude the queryset in normal mode:

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

      To exclude the queryset in translate mode:

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

      .. testcode:: exclude

         from sample.models import Continent

         # exclude the queryset
         continents = Continent.objects.apply('de').exclude(
            countries__name__icontains='Deutsch')

         print(continents)

      .. testoutput:: exclude

         <TranslatableQuerySet [
             <Continent: Asien>,
         ]>
