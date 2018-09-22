"""
This module contains the querysets for the Translations app. It contains the
following members:

:class:`TranslatableQuerySet`
    A queryset which provides custom translation functionalities.
"""

from django.db.models import query

from .utils import apply_translations, update_translations


__docformat__ = 'restructuredtext'


class TranslatableQuerySet(query.QuerySet):
    """
    A queryset which provides custom translation functionalities.

    Provides functionalities like :meth:`apply_translations` to read the
    translations from the database and apply them on the queryset, and
    :meth:`update_translations` to update the translations from the queryset
    and write them on the database.
    """

    def apply_translations(self, *relations, lang=None):
        """
        Apply the translations of the queryset and some relations of it in a
        language.

        Fetches the translations of the queryset and the specified relations
        of it in a language and applies them on the translatable
        :attr:`~translations.models.Translatable.TranslatableMeta.fields` of
        the queryset and the relations of it in place.

        :param relations: The relations of the queryset to apply the
            translations of.
        :type relations: list(str)
        :param lang: The language to fetch the translations in.
            ``None`` means use the :term:`active language` code.
        :type lang: str or None
        :raise TypeError: If the models of the included relations are
            not :class:`~translations.models.Translatable`.
        :raise ~django.core.exceptions.FieldDoesNotExist: If a relation is
            pointing to the fields that don't exist.
        :raise ValueError: If the language code is not included in
            the :data:`~django.conf.settings.LANGUAGES` setting.

        .. testsetup:: apply_translations

           from tests.sample import create_samples

           create_samples(
               continent_names=['europe', 'asia'],
               country_names=['germany', 'south korea'],
               city_names=['cologne', 'munich', 'seoul', 'ulsan'],
               continent_fields=['name', 'denonym'],
               country_fields=['name', 'denonym'],
               city_fields=['name', 'denonym'],
               langs=['de']
           )

        .. note::

           If there is no translation for a field in translatable
           :attr:`~translations.models.Translatable.TranslatableMeta.fields`,
           the translation of the field falls back to the value of the field
           in the instance.

        .. note::

           It is **recommended** for the relations of the queryset to be
           prefetched before applying the translations in order to reach
           optimal performance.

           To do this use
           :meth:`~django.db.models.query.QuerySet.select_related`,
           :meth:`~django.db.models.query.QuerySet.prefetch_related` or
           :func:`~django.db.models.prefetch_related_objects`.

        To apply the translations of a queryset and the relations of it:

        .. testcode:: apply_translations

           from sample.models import Continent

           relations = ('countries', 'countries__cities',)

           continents = Continent.objects.prefetch_related(
               *relations,
           )

           continents.apply_translations(
               *relations,
               lang='de',
           )

           for continent in continents:
               print('Continent: {}'.format(continent))
               for country in continent.countries.all():
                   print('Country: {}'.format(country))
                   for city in country.cities.all():
                       print('City: {}'.format(city))

        .. testoutput:: apply_translations

           Continent: Europa
           Country: Deutschland
           City: Köln
           City: München
           Continent: Asien
           Country: Südkorea
           City: Seül
           City: Ulsän

        .. warning::

           Filtering any queryset after applying the translations will cause
           the translations of that queryset to be reset.

           .. testcode:: apply_translations

              from sample.models import Continent

              relations = ('countries', 'countries__cities',)

              continents = Continent.objects.prefetch_related(
                  *relations,
              )

              continents.apply_translations(
                  *relations,
                  lang='de',
              )

              for continent in continents:
                  print('Continent: {}'.format(continent))
                  for country in continent.countries.exclude(name=''):  # Wrong
                      print('Country: {}  -- Wrong'.format(country))
                      for city in country.cities.all():
                          print('City: {}  -- Wrong'.format(city))

           .. testoutput:: apply_translations

              Continent: Europa
              Country: Germany  -- Wrong
              City: Cologne  -- Wrong
              City: Munich  -- Wrong
              Continent: Asien
              Country: South Korea  -- Wrong
              City: Seoul  -- Wrong
              City: Ulsan  -- Wrong

           The solution is to do the filtering before applying the
           translations. To do this on the relations use
           :class:`~django.db.models.Prefetch`.

           .. testcode:: apply_translations

              from django.db.models import Prefetch
              from sample.models import Continent, Country

              relations = ('countries', 'countries__cities',)

              continents = Continent.objects.prefetch_related(
                  Prefetch(
                      'countries',
                      queryset=Country.objects.exclude(name=''),  # Correct
                  ),
                  'countries__cities',
              )

              continents.apply_translations(
                  *relations,
                  lang='de',
              )

              for continent in continents:
                  print('Continent: {}'.format(continent))
                  for country in continent.countries.all():
                      print('Country: {}'.format(country))
                      for city in country.cities.all():
                          print('City: {}'.format(city))

           .. testoutput:: apply_translations

              Continent: Europa
              Country: Deutschland
              City: Köln
              City: München
              Continent: Asien
              Country: Südkorea
              City: Seül
              City: Ulsän
        """
        apply_translations(self, *relations, lang=lang)

    def update_translations(self, *relations, lang=None):
        """
        Update the translations of the queryset and some relations of it in a
        language.

        Deletes the old translations of the queryset and the specified
        relations of it in a language and creates new translations out of the
        translatable
        :attr:`~translations.models.Translatable.TranslatableMeta.fields` of
        the queryset and the relations of it.

        :param relations: The relations of the queryset to update the
            translations of.
        :type relations: list(str)
        :param lang: The language to update the translations in.
            ``None`` means use the :term:`active language` code.
        :type lang: str or None
        :raise TypeError: If the models of the included relations
            are not :class:`~translations.models.Translatable`.
        :raise ~django.core.exceptions.FieldDoesNotExist: If a relation is
            pointing to the fields that don't exist.
        :raise ValueError: If the language code is not included in
            the :data:`~django.conf.settings.LANGUAGES` setting.
        :raise RuntimeError: If any of the relations is not prefetched.

        .. testsetup:: update_translations_0

           from tests.sample import create_samples

           create_samples(
               continent_names=['europe', 'asia'],
               country_names=['germany', 'south korea'],
               city_names=['cologne', 'munich', 'seoul', 'ulsan'],
               continent_fields=['name', 'denonym'],
               country_fields=['name', 'denonym'],
               city_fields=['name', 'denonym'],
               langs=['de']
           )

        .. testsetup:: update_translations_1

           from tests.sample import create_samples

           create_samples(
               continent_names=['europe', 'asia'],
               country_names=['germany', 'south korea'],
               city_names=['cologne', 'munich', 'seoul', 'ulsan'],
               continent_fields=['name', 'denonym'],
               country_fields=['name', 'denonym'],
               city_fields=['name', 'denonym'],
               langs=['de']
           )

        .. note::

           It is **mandatory** for the relations of the queryset to be
           prefetched before making any changes to them so that the changes
           can be fetched later.

           To do this use
           :meth:`~django.db.models.query.QuerySet.select_related`,
           :meth:`~django.db.models.query.QuerySet.prefetch_related` or
           :func:`~django.db.models.prefetch_related_objects`.

           Consider this case:

           .. testcode:: update_translations_0

              from sample.models import Continent

              # un-prefetched queryset
              europe = Continent.objects.get(code='EU')

              # first query
              europe.countries.all()[0].name = 'Germany (changed)'

              # does a second query
              new_name = europe.countries.all()[0].name

              print('Country: {}'.format(new_name))

           .. testoutput:: update_translations_0

              Country: Germany

           As we can see the new query did not fetch the changes we made
           before. To fix it:

           .. testcode:: update_translations_0

              from sample.models import Continent

              # prefetched queryset
              europe = Continent.objects.prefetch_related(
                  'countries',
              ).get(code='EU')

              # first query
              europe.countries.all()[0].name = 'Germany (changed)'

              # uses the first query
              new_name = europe.countries.all()[0].name

              print('Country: {}'.format(new_name))

           .. testoutput:: update_translations_0

              Country: Germany (changed)

        To update the translations of a queryset and the relations of it:

        .. testcode:: update_translations_1

           from sample.models import Continent

           relations = ('countries', 'countries__cities',)

           continents = Continent.objects.prefetch_related(
               *relations,
           )

           print('OLD TRANSLATIONS:')
           print('-----------------')

           continents.apply_translations(
               *relations,
               lang='de',
           )

           for continent in continents:
               print('Continent: {}'.format(continent))
               for country in continent.countries.all():
                   print('Country: {}'.format(country))
                   for city in country.cities.all():
                       print('City: {}'.format(city))

           print('\\nCHANGING...\\n')

           continents[0].name = 'Europa (changed)'
           continents[0].countries.all()[0].name = 'Deutschland (changed)'

           continents.update_translations(
               *relations,
               lang='de',
           )

           print('NEW TRANSLATIONS:')
           print('-----------------')

           continents.apply_translations(
               *relations,
               lang='de',
           )

           for continent in continents:
               print('Continent: {}'.format(continent))
               for country in continent.countries.all():
                   print('Country: {}'.format(country))
                   for city in country.cities.all():
                       print('City: {}'.format(city))

        .. testoutput:: update_translations_1

           OLD TRANSLATIONS:
           -----------------
           Continent: Europa
           Country: Deutschland
           City: Köln
           City: München
           Continent: Asien
           Country: Südkorea
           City: Seül
           City: Ulsän

           CHANGING...

           NEW TRANSLATIONS:
           -----------------
           Continent: Europa (changed)
           Country: Deutschland (changed)
           City: Köln
           City: München
           Continent: Asien
           Country: Südkorea
           City: Seül
           City: Ulsän
        """
        update_translations(self, *relations, lang=lang)
