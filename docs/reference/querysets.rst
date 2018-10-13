*********
QuerySets
*********

.. module:: translations.querysets

This module contains the querysets for the Translations app.

.. class:: TranslatableQuerySet

   A queryset which provides custom translation functionalities.

   .. method:: _chain(self, **kwargs)

      Return a translatable chained queryset.

      This is an overriden version of
      the default :class:`~django.db.models.query.QuerySet`\ 's
      :meth:`~django.db.models.query._chain` method. It copies custom
      translation configurations from the queryset to the chained queryset.

      :param kwargs: the default :class:`~django.db.models.query.QuerySet`\
          's :meth:`~django.db.models.query._chain` method keyword arguments.
      :type kwargs: dict
      :return: The chained queryset.
      :rtype: TranslatableQuerySet

      To get a translatable chained queryset:

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

         # get translatable chained queryset
         continents = Continent.objects.all()._chain()

         # use the queryset like before
         print(continents)

      .. testoutput:: _chain

         <TranslatableQuerySet [<Continent: Europe>, <Continent: Asia>]>

   .. 
      method:: apply(self, *relations, lang=None)

      Apply a language to be used on the queryset and some of its relations.

      Causes the queryset to work with the translated values in the
      specified language while querying the database.

      Causes the queryset's specified relations to be translated in the
      specified language while evaluating the queryset.

      :param lang: The language to be used on the queryset.
          ``None`` means use the :term:`active language` code.
      :type lang: str or None
      :param relations: The relations of the queryset to use the language on.
      :type relations: list(str)
      :raise ValueError: If the language code is not included in
          the :data:`~django.conf.settings.LANGUAGES` setting.

      To apply a language to be used on the queryset and some of its relations:

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

         relations = ('countries', 'countries__cities',)

         # apply German on the queryset and its specified relations
         continents = Continent.objects.apply(*relations, lang='de')

         # use the queryset like before
         print(continents[0].name)
         print(continents[0].countries.all()[0].name)
         print(continents[0].countries.all()[0].cities.all()[0].name)

      .. testoutput:: apply

         Europa
         Deutschland
         Köln

      .. note::

         Applying only affects the :attr:`translatable fields \
         <translations.models.Translatable.TranslatableMeta.fields>` that have
         a translation.

      .. note::

         It is **recommended** for the relations of the queryset to be
         prefetched before applying a language on them,
         in order to reach optimal performance.

         To do this use
         :meth:`~django.db.models.query.QuerySet.select_related`,
         :meth:`~django.db.models.query.QuerySet.prefetch_related` or
         :func:`~django.db.models.prefetch_related_objects`.

      .. warning::

         Filtering the relations after applying the translations will cause
         the translations of that relation to be reset.

         .. testcode:: apply

            from sample.models import Continent

            relations = ('countries', 'countries__cities',)

            europe = Continent.objects.prefetch_related(
                *relations
            ).apply(*relations, lang='de').get(code='EU')

            # Filtering after applying
            print(europe.name)
            print(europe.countries.exclude(name='')[0].name + '  -- Wrong')
            print(europe.countries.exclude(name='')[0].cities.all()[0].name + '  -- Wrong')

         .. testoutput:: apply

            Europa
            Germany  -- Wrong
            Cologne  -- Wrong

         The solution is to do the filtering before applying the translations.

         To do this use :class:`~django.db.models.Prefetch`.

         .. testcode:: apply

            from django.db.models import Prefetch
            from sample.models import Continent, Country

            relations = ('countries', 'countries__cities',)

            # Filtering before applying
            europe = Continent.objects.prefetch_related(
                Prefetch(
                    'countries',
                    queryset=Country.objects.exclude(name=''),
                ),
                'countries__cities',
            ).apply(*relations, lang='de').get(code='EU')

            print(europe.name)
            print(europe.countries.all()[0].name + '  -- Correct')
            print(europe.countries.all()[0].cities.all()[0].name + '  -- Correct')

         .. testoutput:: apply

            Europa
            Deutschland  -- Correct
            Köln  -- Correct

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

         <TranslatableQuerySet [<Continent: Europe>, <Continent: Asia>]>
         <TranslatableQuerySet [<Continent: Europa>, <Continent: Asien>]>

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

         <TranslatableQuerySet [<Continent: Europe>, <Continent: Asia>]>
         <TranslatableQuerySet [<Continent: Europa>, <Continent: Asien>]>

   .. method:: filter(self, *args, **kwargs)

      Filter the queryset.
