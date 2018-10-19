from django.test import TestCase
from django.db.models import Q

from translations.query import _fetch_translations_query_getter

from sample.models import Continent


class FetchTranslationsQueryGetter(TestCase):
    """Tests for `_fetch_translations_query_getter`."""

    def test_get_translations_queries_lookup_nr_yf_nt_nl(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(code='EU').children,
            [
                ('code', 'EU'),
            ]
        )

    def test_get_translations_queries_lookup_nr_yf_yt_nl(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(name='Europa').children,
            [
                ('translations__field', 'name'),
                ('translations__language', 'de'),
                ('translations__text', 'Europa'),
            ]
        )

    def test_get_translations_queries_lookup_nr_yf_nt_yl(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(code__icontains='EU').children,
            [
                ('code__icontains', 'EU'),
            ]
        )

    def test_get_translations_queries_lookup_nr_yf_yt_yl(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(name__icontains='Europa').children,
            [
                ('translations__field', 'name'),
                ('translations__language', 'de'),
                ('translations__text__icontains', 'Europa'),
            ]
        )

    def test_get_translations_queries_lookup_yr_nf_nl(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(countries=1).children,
            [
                ('countries', 1),
            ]
        )

    def test_get_translations_queries_lookup_yr_nf_yl(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(countries__gt=1).children,
            [
                ('countries__gt', 1),
            ]
        )

    def test_get_translations_queries_lookup_yr_yf_nt_nl(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(countries__code='DE').children,
            [
                ('countries__code', 'DE'),
            ]
        )

    def test_get_translations_queries_lookup_yr_yf_yt_nl(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(countries__name='Deutschland').children,
            [
                ('countries__translations__field', 'name'),
                ('countries__translations__language', 'de'),
                ('countries__translations__text', 'Deutschland'),
            ]
        )

    def test_get_translations_queries_lookup_yr_yf_nt_yl(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(countries__code__icontains='DE').children,
            [
                ('countries__code__icontains', 'DE'),
            ]
        )

    def test_get_translations_queries_lookup_yr_yf_yt_yl(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(countries__name__icontains='Deutsch').children,
            [
                ('countries__translations__field', 'name'),
                ('countries__translations__language', 'de'),
                ('countries__translations__text__icontains', 'Deutsch'),
            ]
        )

    def test_get_translations_queries_lookup_yrnested_yf_nt_nl(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(countries__cities__id=1).children,
            [
                ('countries__cities__id', 1),
            ]
        )

    def test_get_translations_queries_lookup_yrnested_yf_yt_nl(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(countries__cities__name='Köln').children,
            [
                ('countries__cities__translations__field', 'name'),
                ('countries__cities__translations__language', 'de'),
                ('countries__cities__translations__text', 'Köln'),
            ]
        )

    def test_get_translations_queries_lookup_yrnested_yf_nt_yl(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(countries__cities__id__gt=1).children,
            [
                ('countries__cities__id__gt', 1),
            ]
        )

    def test_get_translations_queries_lookup_yrnested_yf_yt_yl(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(countries__cities__name__icontains='Kö').children,
            [
                ('countries__cities__translations__field', 'name'),
                ('countries__cities__translations__language', 'de'),
                ('countries__cities__translations__text__icontains', 'Kö'),
            ]
        )

    def test_get_translations_queries_query_nr_yf_nt_nl(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(Q(code='EU')).children,
            [
                ('code', 'EU'),
            ]
        )

    def test_get_translations_queries_query_nr_yf_yt_nl(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(Q(name='Europa')).children,
            [
                ('translations__field', 'name'),
                ('translations__language', 'de'),
                ('translations__text', 'Europa'),
            ]
        )

    def test_get_translations_queries_query_nr_yf_nt_yl(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(Q(code__icontains='EU')).children,
            [
                ('code__icontains', 'EU'),
            ]
        )

    def test_get_translations_queries_query_nr_yf_yt_yl(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(Q(name__icontains='Europa')).children,
            [
                ('translations__field', 'name'),
                ('translations__language', 'de'),
                ('translations__text__icontains', 'Europa'),
            ]
        )

    def test_get_translations_queries_query_yr_nf_nl(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(Q(countries=1)).children,
            [
                ('countries', 1),
            ]
        )

    def test_get_translations_queries_query_yr_nf_yl(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(Q(countries__gt=1)).children,
            [
                ('countries__gt', 1),
            ]
        )

    def test_get_translations_queries_query_yr_yf_nt_nl(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(Q(countries__code='DE')).children,
            [
                ('countries__code', 'DE'),
            ]
        )

    def test_get_translations_queries_query_yr_yf_yt_nl(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(Q(countries__name='Deutschland')).children,
            [
                ('countries__translations__field', 'name'),
                ('countries__translations__language', 'de'),
                ('countries__translations__text', 'Deutschland')
            ]
        )

    def test_get_translations_queries_query_yr_yf_nt_yl(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(Q(countries__code__icontains='DE')).children,
            [
                ('countries__code__icontains', 'DE'),
            ]
        )

    def test_get_translations_queries_query_yr_yf_yt_yl(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(Q(countries__name__icontains='Deutsch')).children,
            [
                ('countries__translations__field', 'name'),
                ('countries__translations__language', 'de'),
                ('countries__translations__text__icontains', 'Deutsch'),
            ]
        )

    def test_get_translations_queries_query_yrnested_yf_nt_nl(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(Q(countries__cities__id=1)).children,
            [
                ('countries__cities__id', 1),
            ]
        )

    def test_get_translations_queries_query_yrnested_yf_yt_nl(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(Q(countries__cities__name='Köln')).children,
            [
                ('countries__cities__translations__field', 'name'),
                ('countries__cities__translations__language', 'de'),
                ('countries__cities__translations__text', 'Köln'),
            ]
        )

    def test_get_translations_queries_query_yrnested_yf_nt_yl(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(Q(countries__cities__id__gt=1)).children,
            [
                ('countries__cities__id__gt', 1),
            ]
        )

    def test_get_translations_queries_query_yrnested_yf_yt_yl(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(Q(countries__cities__name__icontains='Kö')).children,
            [
                ('countries__cities__translations__field', 'name'),
                ('countries__cities__translations__language', 'de'),
                ('countries__cities__translations__text__icontains', 'Kö'),
            ]
        )

    def test_get_translations_queries_query_nested_query(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(Q(countries__cities__name__icontains='Kö')).children,
            [
                ('countries__cities__translations__field', 'name'),
                ('countries__cities__translations__language', 'de'),
                ('countries__cities__translations__text__icontains', 'Kö'),
            ]
        )
