"""
This module contains the querysets for the Translations app. It contains the
following members:

:class:`TranslatableQuerySet`
    A queryset which provides custom translation functionalities.
"""

from django.db import models

from translations.utils import apply_translations, update_translations


__docformat__ = 'restructuredtext'


class TranslatableQuerySet(models.QuerySet):
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
        the queryset and the relations of it.

        :param relations: The relations of the queryset to apply the
            translations of.
        :type relations: list(str)
        :param lang: The language to fetch the translations in.
            ``None`` means use the :term:`active language` code.
        :type lang: str or None
        :return: The list of instance which the translations of have been
            applied on.
        :rtype: list(~translations.models.Translatable)
        :raise ValueError: If the language code is not included in
            the :data:`~django.conf.settings.LANGUAGES` setting.
        :raise TypeError: If the models of the included relations
            are not :class:`~translations.models.Translatable`.
        :raise ~django.core.exceptions.FieldDoesNotExist: If a relation is
            pointing to the fields that don't exist.

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
           from translations.utils import apply_translations

           relations = ('countries', 'countries__cities',)

           continents = Continent.objects.prefetch_related(
               *relations
           ).apply_translations(
               *relations,
               lang='de'
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
           the translations of that queryset to be reset. The solution is to
           do the filtering before applying the translations.

           To do this on the relations use :class:`~django.db.models.Prefetch`.

           Consider this case:

           .. testcode:: apply_translations

              from sample.models import Continent
              from translations.utils import apply_translations

              relations = ('countries', 'countries__cities',)

              continents = Continent.objects.prefetch_related(
                  *relations
              ).apply_translations(
                  *relations,
                  lang='de'
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

           As we can see the translations of the filtered queryset are reset.
           To fix it:

           .. testcode:: apply_translations

              from django.db.models import Prefetch
              from sample.models import Continent, Country
              from translations.utils import apply_translations

              relations = ('countries', 'countries__cities',)

              continents = Continent.objects.prefetch_related(
                  Prefetch(
                      'countries',
                      queryset=Country.objects.exclude(name='')  # Correct
                  ),
                  'countries__cities',
              ).apply_translations(
                  *relations,
                  lang='de'
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
        clone = self._chain()
        apply_translations(clone, *relations, lang=lang)
        return list(clone)

    def update_translations(self, *relations, lang=None):
        """
        Update the translations of the queryset and the relations of it in a
        language.

        Deletes the old translations of the queryset and the specified
        relations of it in a language and creates new translations for them
        based on their fields values.

        :param relations: The relations of the queryset to update the
            translations of.
        :type relations: list(str)
        :param lang: The language to update the translations in.
            ``None`` means use the :term:`active language` code.
        :type lang: str or None
        :raise ValueError: If the language code is not included in
            the :data:`~django.conf.settings.LANGUAGES` setting.
        :raise ~django.core.exceptions.FieldDoesNotExist: If a relation is
            pointing to the fields that don't exist.

        .. warning::
           The relations of the queryset **must** be fetched before performing
           the translation process.

           To do this use
           :meth:`~django.db.models.query.QuerySet.select_related` or
           :meth:`~django.db.models.query.QuerySet.prefetch_related`.

        .. warning::
           Only when all the filterings are executed on the relations of the
           queryset it should go through the translation process, otherwise if
           a relation is filtered after the translation process the
           translations of that relation are reset.

           To filter a relation when fetching it use
           :class:`~django.db.models.Prefetch`.

        .. testsetup:: update_translations

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

        To update the translations of a queryset and the relations of it:

        .. testcode:: update_translations

           from sample.models import Continent, Country, City
           from translations.utils import update_translations

           relations = ('countries', 'countries__cities',)

           continents = Continent.objects.prefetch_related(
               *relations
           ).update_translations(
               *relations,
               lang='en'
           )

           for continent in continents:
               print('Continent: {}'.format(continent))
               for country in continent.countries.all():
                   print('Country: {}'.format(country))
                   for city in country.cities.all():
                       print('City: {}'.format(city))

        .. testoutput:: update_translations

           Continent: Europe
           Country: Germany
           City: Cologne
           City: Munich
           Continent: Asia
           Country: South Korea
           City: Seoul
           City: Ulsan
        """
        update_translations(self, *relations, lang=lang)
        return self
