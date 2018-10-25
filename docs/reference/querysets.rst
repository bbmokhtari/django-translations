*********
QuerySets
*********

.. module:: translations.querysets

This module contains the querysets for the Translations app.

.. class:: TranslatableQuerySet

   A queryset which provides custom translation functionalities.

   Provides functionalities like :meth:`apply` and :meth:`translate_related`
   to evaluate the queryset in a specific language and also
   some other functionalities like :meth:`filter` and :meth:`exclude` to
   filter the queryset in a specific language.

   .. method:: __init__(*args, **kwargs)

      Initialize a :class:`TranslatableQuerySet`.

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

         # initialize queryset
         continents = Continent.objects.all()

         print(continents)

      .. testoutput:: __init__

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
      the chained :class:`TranslatableQuerySet`.

      :param kwargs: The keyword arguments of
          the :class:`~django.db.models.query.QuerySet`\
          's :meth:`~django.db.models.query._chain` method.
      :type kwargs: dict
      :return: The chained :class:`TranslatableQuerySet`.
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
      It translates the instances of the :class:`TranslatableQuerySet` and
      some of their relations
      (specified using the :meth:`translate_related` method)
      in a language
      (specified using the :meth:`apply` method).

      To evaluate the :class:`TranslatableQuerySet`
      (using the default language):

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

      To evaluate the :class:`TranslatableQuerySet`
      (using the applied language):

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

   .. method:: apply(lang=None)

      Apply a language on the :class:`TranslatableQuerySet`.

      Causes the :class:`TranslatableQuerySet` to translate its
      instances in the specified language in the evaluation.

      :param lang: The language to apply on the :class:`TranslatableQuerySet`.
          ``None`` means use the :term:`active language` code.
      :type lang: str or None
      :return: The :class:`TranslatableQuerySet` which the language is applied on.
      :rtype: TranslatableQuerySet
      :raise ValueError: If the language code is not included in
          the :data:`~django.conf.settings.LANGUAGES` setting.

      To apply a language on the :class:`TranslatableQuerySet`:

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

         # apply a language on the queryset
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

         Any subsequent chained methods on the relations queryset which imply
         a database query will reset previously translated results:

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

   .. method:: filter(*args, **kwargs)

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

   .. method:: exclude(*args, **kwargs)

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
