"""
This module contains the querysets for the Translations app. It contains the
following members:

:class:`TranslatableQuerySet`
    A :class:`~django.db.models.QuerySet` which provides custom
    translation functionalities.
"""

from django.db import models, transaction

from translations.utils import apply_translations, update_translations


__docformat__ = 'restructuredtext'


class TranslatableQuerySet(models.QuerySet):
    """
    A queryset which provides custom translation functionalities.

    Provides functionalities like :meth:`apply_translations` to read and apply
    translations from the database onto the queryset, and
    :meth:`update_translations` to write and update translations from the
    queryset onto the database.
    """

    def apply_translations(self, *relations, lang=None):
        """
        Apply the translations on the queryset and the relations of it in a
        language.

        Fetches the translations of the queryset and the specified relations
        of it in a language and applies them field by field.

        :param relations: The relations of the queryset to apply the
            translations on.
        :type relations: list(str)
        :param lang: The language to fetch the translations in.
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
           :meth:`~django.db.models.query.QuerySet.select_related`,
           :meth:`~django.db.models.query.QuerySet.prefetch_related` or
           :func:`~django.db.models.prefetch_related_objects`.

        .. warning::
           Only when all the filterings are executed on the relations of the
           queryset it should go through the translation process, otherwise if
           a relation is filtered after the translation process the
           translations of that relation are reset.

           To filter a relation when fetching it use
           :class:`~django.db.models.Prefetch`.

        .. testsetup:: apply_translations

           from tests.sample import create_samples

           create_samples(
               continent_names=["europe", "asia"],
               country_names=["germany", "south korea"],
               city_names=["cologne", "munich", "seoul", "ulsan"],
               continent_fields=["name", "denonym"],
               country_fields=["name", "denonym"],
               city_fields=["name", "denonym"],
               langs=["de"]
           )

        To apply the translations on a queryset and the relations of it:

        .. testcode:: apply_translations

           from sample.models import Continent

           relations = ('countries', 'countries__cities',)

           continents = Continent.objects.prefetch_related(
               *relations
           ).apply_translations(
               *relations,
               lang="de"
           )

           for continent in continents:
               print("Continent: {}".format(continent))
               for country in continent.countries.all():
                   print("Country: {}".format(country))
                   for city in country.cities.all():
                       print("City: {}".format(city))

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
        return self

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
               continent_names=["europe", "asia"],
               country_names=["germany", "south korea"],
               city_names=["cologne", "munich", "seoul", "ulsan"],
               continent_fields=["name", "denonym"],
               country_fields=["name", "denonym"],
               city_fields=["name", "denonym"],
               langs=["de"]
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
               lang="en"
           )

           for continent in continents:
               print("Continent: {}".format(continent))
               for country in continent.countries.all():
                   print("Country: {}".format(country))
                   for city in country.cities.all():
                       print("City: {}".format(city))

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
