from django.test import TestCase
from django.db.models import Q

from translations.query import _fetch_translations_query_getter

from sample.models import Continent


class FetchTranslationsQueryGetter(TestCase):
    """Tests for `_fetch_translations_query_getter`."""

    def test_lookup_nrel_yfield_ntrans_nsupp(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(code='EU').children,
            [
                ('code', 'EU'),
            ]
        )

    def test_lookup_nrel_yfield_ytrans_nsupp(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(name='Europa').children,
            [
                ('translations__field', 'name'),
                ('translations__language', 'de'),
                ('translations__text', 'Europa'),
            ]
        )

    def test_lookup_nrel_yfield_ntrans_ysupp(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(code__icontains='EU').children,
            [
                ('code__icontains', 'EU'),
            ]
        )

    def test_lookup_nrel_yfield_ytrans_ysupp(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(name__icontains='Europa').children,
            [
                ('translations__field', 'name'),
                ('translations__language', 'de'),
                ('translations__text__icontains', 'Europa'),
            ]
        )

    def test_lookup_yrel_nfield_nsupp(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(countries=1).children,
            [
                ('countries', 1),
            ]
        )

    def test_lookup_yrel_nfield_ysupp(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(countries__gt=1).children,
            [
                ('countries__gt', 1),
            ]
        )

    def test_lookup_yrel_yfield_ntrans_nsupp(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(countries__code='DE').children,
            [
                ('countries__code', 'DE'),
            ]
        )

    def test_lookup_yrel_yfield_ytrans_nsupp(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(countries__name='Deutschland').children,
            [
                ('countries__translations__field', 'name'),
                ('countries__translations__language', 'de'),
                ('countries__translations__text', 'Deutschland'),
            ]
        )

    def test_lookup_yrel_yfield_ntrans_ysupp(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(countries__code__icontains='DE').children,
            [
                ('countries__code__icontains', 'DE'),
            ]
        )

    def test_lookup_yrel_yfield_ytrans_ysupp(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(countries__name__icontains='Deutsch').children,
            [
                ('countries__translations__field', 'name'),
                ('countries__translations__language', 'de'),
                ('countries__translations__text__icontains', 'Deutsch'),
            ]
        )

    def test_lookup_yrelnested_yfield_ntrans_nsupp(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(countries__cities__id=1).children,
            [
                ('countries__cities__id', 1),
            ]
        )

    def test_lookup_yrelnested_yfield_ytrans_nsupp(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(countries__cities__name='Köln').children,
            [
                ('countries__cities__translations__field', 'name'),
                ('countries__cities__translations__language', 'de'),
                ('countries__cities__translations__text', 'Köln'),
            ]
        )

    def test_lookup_yrelnested_yfield_ntrans_ysupp(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(countries__cities__id__gt=1).children,
            [
                ('countries__cities__id__gt', 1),
            ]
        )

    def test_lookup_yrelnested_yfield_ytrans_ysupp(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(countries__cities__name__icontains='Kö').children,
            [
                ('countries__cities__translations__field', 'name'),
                ('countries__cities__translations__language', 'de'),
                ('countries__cities__translations__text__icontains', 'Kö'),
            ]
        )

    def test_query_nrel_yfield_ntrans_nsupp(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(Q(code='EU')).children,
            [
                ('code', 'EU'),
            ]
        )

    def test_query_nrel_yfield_ytrans_nsupp(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(Q(name='Europa')).children,
            [
                ('translations__field', 'name'),
                ('translations__language', 'de'),
                ('translations__text', 'Europa'),
            ]
        )

    def test_query_nrel_yfield_ntrans_ysupp(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(Q(code__icontains='EU')).children,
            [
                ('code__icontains', 'EU'),
            ]
        )

    def test_query_nrel_yfield_ytrans_ysupp(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(Q(name__icontains='Europa')).children,
            [
                ('translations__field', 'name'),
                ('translations__language', 'de'),
                ('translations__text__icontains', 'Europa'),
            ]
        )

    def test_query_yrel_nfield_nsupp(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(Q(countries=1)).children,
            [
                ('countries', 1),
            ]
        )

    def test_query_yrel_nfield_ysupp(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(Q(countries__gt=1)).children,
            [
                ('countries__gt', 1),
            ]
        )

    def test_query_yrel_yfield_ntrans_nsupp(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(Q(countries__code='DE')).children,
            [
                ('countries__code', 'DE'),
            ]
        )

    def test_query_yrel_yfield_ytrans_nsupp(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(Q(countries__name='Deutschland')).children,
            [
                ('countries__translations__field', 'name'),
                ('countries__translations__language', 'de'),
                ('countries__translations__text', 'Deutschland')
            ]
        )

    def test_query_yrel_yfield_ntrans_ysupp(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(Q(countries__code__icontains='DE')).children,
            [
                ('countries__code__icontains', 'DE'),
            ]
        )

    def test_query_yrel_yfield_ytrans_ysupp(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(Q(countries__name__icontains='Deutsch')).children,
            [
                ('countries__translations__field', 'name'),
                ('countries__translations__language', 'de'),
                ('countries__translations__text__icontains', 'Deutsch'),
            ]
        )

    def test_query_yrelnested_yfield_ntrans_nsupp(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(Q(countries__cities__id=1)).children,
            [
                ('countries__cities__id', 1),
            ]
        )

    def test_query_yrelnested_yfield_ytrans_nsupp(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(Q(countries__cities__name='Köln')).children,
            [
                ('countries__cities__translations__field', 'name'),
                ('countries__cities__translations__language', 'de'),
                ('countries__cities__translations__text', 'Köln'),
            ]
        )

    def test_query_yrelnested_yfield_ntrans_ysupp(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(Q(countries__cities__id__gt=1)).children,
            [
                ('countries__cities__id__gt', 1),
            ]
        )

    def test_query_yrelnested_yfield_ytrans_ysupp(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(Q(countries__cities__name__icontains='Kö')).children,
            [
                ('countries__cities__translations__field', 'name'),
                ('countries__cities__translations__language', 'de'),
                ('countries__cities__translations__text__icontains', 'Kö'),
            ]
        )
