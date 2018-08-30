"""
This module contains the querysets for the Translations app. It contains the
following members:

:class:`TranslatableQuerySet`
    The translations app extended queryset.
"""

from django.db import models, transaction

from translations.utils import apply_translations, update_translations


class TranslatableQuerySet(models.QuerySet):
    """
    The translations app extended queryset.
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
           :meth:`~django.db.models.query.QuerySet.select_related` or
           :meth:`~django.db.models.query.QuerySet.prefetch_related`.

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
        update_translations(self, *relations, lang=lang)
        return self
