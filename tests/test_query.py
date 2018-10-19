import copy

from django.test import TestCase
from django.db.models import Q
from django.utils.translation import override

from translations.query import _fetch_translations_query_getter, TQ

from sample.models import Continent


class FetchTranslationsQueryGetterTest(TestCase):
    """Tests for `_fetch_translations_query_getter`."""

    def test_lookup_nrel_yfield_ntrans_nsupp_strlang(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(code='EU').children,
            [
                ('code', 'EU'),
            ]
        )

    def test_lookup_nrel_yfield_ytrans_nsupp_strlang(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(name='Europa').children,
            [
                ('translations__field', 'name'),
                ('translations__language', 'de'),
                ('translations__text', 'Europa'),
            ]
        )

    def test_lookup_nrel_yfield_ntrans_ysupp_strlang(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(code__icontains='EU').children,
            [
                ('code__icontains', 'EU'),
            ]
        )

    def test_lookup_nrel_yfield_ytrans_ysupp_strlang(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(name__icontains='Europa').children,
            [
                ('translations__field', 'name'),
                ('translations__language', 'de'),
                ('translations__text__icontains', 'Europa'),
            ]
        )

    def test_lookup_yrel_nfield_nsupp_strlang(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(countries=1).children,
            [
                ('countries', 1),
            ]
        )

    def test_lookup_yrel_nfield_ysupp_strlang(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(countries__gt=1).children,
            [
                ('countries__gt', 1),
            ]
        )

    def test_lookup_yrel_yfield_ntrans_nsupp_strlang(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(countries__code='DE').children,
            [
                ('countries__code', 'DE'),
            ]
        )

    def test_lookup_yrel_yfield_ytrans_nsupp_strlang(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(countries__name='Deutschland').children,
            [
                ('countries__translations__field', 'name'),
                ('countries__translations__language', 'de'),
                ('countries__translations__text', 'Deutschland'),
            ]
        )

    def test_lookup_yrel_yfield_ntrans_ysupp_strlang(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(countries__code__icontains='DE').children,
            [
                ('countries__code__icontains', 'DE'),
            ]
        )

    def test_lookup_yrel_yfield_ytrans_ysupp_strlang(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(countries__name__icontains='Deutsch').children,
            [
                ('countries__translations__field', 'name'),
                ('countries__translations__language', 'de'),
                ('countries__translations__text__icontains', 'Deutsch'),
            ]
        )

    def test_lookup_yrelnested_yfield_ntrans_nsupp_strlang(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(countries__cities__id=1).children,
            [
                ('countries__cities__id', 1),
            ]
        )

    def test_lookup_yrelnested_yfield_ytrans_nsupp_strlang(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(countries__cities__name='Köln').children,
            [
                ('countries__cities__translations__field', 'name'),
                ('countries__cities__translations__language', 'de'),
                ('countries__cities__translations__text', 'Köln'),
            ]
        )

    def test_lookup_yrelnested_yfield_ntrans_ysupp_strlang(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(countries__cities__id__gt=1).children,
            [
                ('countries__cities__id__gt', 1),
            ]
        )

    def test_lookup_yrelnested_yfield_ytrans_ysupp_strlang(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(countries__cities__name__icontains='Kö').children,
            [
                ('countries__cities__translations__field', 'name'),
                ('countries__cities__translations__language', 'de'),
                ('countries__cities__translations__text__icontains', 'Kö'),
            ]
        )

    def test_q_nrel_yfield_ntrans_nsupp_strlang(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(Q(code='EU')).children,
            [
                ('code', 'EU'),
            ]
        )

    def test_q_nrel_yfield_ytrans_nsupp_strlang(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(Q(name='Europa')).children,
            [
                ('translations__field', 'name'),
                ('translations__language', 'de'),
                ('translations__text', 'Europa'),
            ]
        )

    def test_q_nrel_yfield_ntrans_ysupp_strlang(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(Q(code__icontains='EU')).children,
            [
                ('code__icontains', 'EU'),
            ]
        )

    def test_q_nrel_yfield_ytrans_ysupp_strlang(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(Q(name__icontains='Europa')).children,
            [
                ('translations__field', 'name'),
                ('translations__language', 'de'),
                ('translations__text__icontains', 'Europa'),
            ]
        )

    def test_q_yrel_nfield_nsupp_strlang(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(Q(countries=1)).children,
            [
                ('countries', 1),
            ]
        )

    def test_q_yrel_nfield_ysupp_strlang(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(Q(countries__gt=1)).children,
            [
                ('countries__gt', 1),
            ]
        )

    def test_q_yrel_yfield_ntrans_nsupp_strlang(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(Q(countries__code='DE')).children,
            [
                ('countries__code', 'DE'),
            ]
        )

    def test_q_yrel_yfield_ytrans_nsupp_strlang(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(Q(countries__name='Deutschland')).children,
            [
                ('countries__translations__field', 'name'),
                ('countries__translations__language', 'de'),
                ('countries__translations__text', 'Deutschland'),
            ]
        )

    def test_q_yrel_yfield_ntrans_ysupp_strlang(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(Q(countries__code__icontains='DE')).children,
            [
                ('countries__code__icontains', 'DE'),
            ]
        )

    def test_q_yrel_yfield_ytrans_ysupp_strlang(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(Q(countries__name__icontains='Deutsch')).children,
            [
                ('countries__translations__field', 'name'),
                ('countries__translations__language', 'de'),
                ('countries__translations__text__icontains', 'Deutsch'),
            ]
        )

    def test_q_yrelnested_yfield_ntrans_nsupp_strlang(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(Q(countries__cities__id=1)).children,
            [
                ('countries__cities__id', 1),
            ]
        )

    def test_q_yrelnested_yfield_ytrans_nsupp_strlang(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(Q(countries__cities__name='Köln')).children,
            [
                ('countries__cities__translations__field', 'name'),
                ('countries__cities__translations__language', 'de'),
                ('countries__cities__translations__text', 'Köln'),
            ]
        )

    def test_q_yrelnested_yfield_ntrans_ysupp_strlang(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(Q(countries__cities__id__gt=1)).children,
            [
                ('countries__cities__id__gt', 1),
            ]
        )

    def test_q_yrelnested_yfield_ytrans_ysupp_strlang(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(Q(countries__cities__name__icontains='Kö')).children,
            [
                ('countries__cities__translations__field', 'name'),
                ('countries__cities__translations__language', 'de'),
                ('countries__cities__translations__text__icontains', 'Kö'),
            ]
        )

    def test_tq_nrel_yfield_ntrans_nsupp_strlang(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(TQ(code='EU', _lang='de')).children,
            [
                ('code', 'EU'),
            ]
        )

    def test_tq_nrel_yfield_ytrans_nsupp_strlang(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(TQ(name='Europa', _lang='de')).children,
            [
                ('translations__field', 'name'),
                ('translations__language', 'de'),
                ('translations__text', 'Europa'),
            ]
        )

    def test_tq_nrel_yfield_ntrans_ysupp_strlang(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(TQ(code__icontains='EU', _lang='de')).children,
            [
                ('code__icontains', 'EU'),
            ]
        )

    def test_tq_nrel_yfield_ytrans_ysupp_strlang(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(TQ(name__icontains='Europa', _lang='de')).children,
            [
                ('translations__field', 'name'),
                ('translations__language', 'de'),
                ('translations__text__icontains', 'Europa'),
            ]
        )

    def test_tq_yrel_nfield_nsupp_strlang(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(TQ(countries=1, _lang='de')).children,
            [
                ('countries', 1),
            ]
        )

    def test_tq_yrel_nfield_ysupp_strlang(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(TQ(countries__gt=1, _lang='de')).children,
            [
                ('countries__gt', 1),
            ]
        )

    def test_tq_yrel_yfield_ntrans_nsupp_strlang(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(TQ(countries__code='DE', _lang='de')).children,
            [
                ('countries__code', 'DE'),
            ]
        )

    def test_tq_yrel_yfield_ytrans_nsupp_strlang(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(TQ(countries__name='Deutschland', _lang='de')).children,
            [
                ('countries__translations__field', 'name'),
                ('countries__translations__language', 'de'),
                ('countries__translations__text', 'Deutschland'),
            ]
        )

    def test_tq_yrel_yfield_ntrans_ysupp_strlang(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(TQ(countries__code__icontains='DE', _lang='de')).children,
            [
                ('countries__code__icontains', 'DE'),
            ]
        )

    def test_tq_yrel_yfield_ytrans_ysupp_strlang(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(TQ(countries__name__icontains='Deutsch', _lang='de')).children,
            [
                ('countries__translations__field', 'name'),
                ('countries__translations__language', 'de'),
                ('countries__translations__text__icontains', 'Deutsch'),
            ]
        )

    def test_tq_yrelnested_yfield_ntrans_nsupp_strlang(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(TQ(countries__cities__id=1, _lang='de')).children,
            [
                ('countries__cities__id', 1),
            ]
        )

    def test_tq_yrelnested_yfield_ytrans_nsupp_strlang(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(TQ(countries__cities__name='Köln', _lang='de')).children,
            [
                ('countries__cities__translations__field', 'name'),
                ('countries__cities__translations__language', 'de'),
                ('countries__cities__translations__text', 'Köln'),
            ]
        )

    def test_tq_yrelnested_yfield_ntrans_ysupp_strlang(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(TQ(countries__cities__id__gt=1, _lang='de')).children,
            [
                ('countries__cities__id__gt', 1),
            ]
        )

    def test_tq_yrelnested_yfield_ytrans_ysupp_strlang(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(TQ(countries__cities__name__icontains='Kö', _lang='de')).children,
            [
                ('countries__cities__translations__field', 'name'),
                ('countries__cities__translations__language', 'de'),
                ('countries__cities__translations__text__icontains', 'Kö'),
            ]
        )

    def test_lookup_nrel_yfield_ntrans_nsupp_strlangdef(self):
        getter = _fetch_translations_query_getter(Continent, 'en')

        self.assertListEqual(
            getter(code='EU').children,
            [
                ('code', 'EU'),
            ]
        )

    def test_lookup_nrel_yfield_ytrans_nsupp_strlangdef(self):
        getter = _fetch_translations_query_getter(Continent, 'en')

        self.assertListEqual(
            getter(name='Europa').children,
            [
                ('name', 'Europa'),
            ]
        )

    def test_lookup_nrel_yfield_ntrans_ysupp_strlangdef(self):
        getter = _fetch_translations_query_getter(Continent, 'en')

        self.assertListEqual(
            getter(code__icontains='EU').children,
            [
                ('code__icontains', 'EU'),
            ]
        )

    def test_lookup_nrel_yfield_ytrans_ysupp_strlangdef(self):
        getter = _fetch_translations_query_getter(Continent, 'en')

        self.assertListEqual(
            getter(name__icontains='Europa').children,
            [
                ('name__icontains', 'Europa'),
            ]
        )

    def test_lookup_yrel_nfield_nsupp_strlangdef(self):
        getter = _fetch_translations_query_getter(Continent, 'en')

        self.assertListEqual(
            getter(countries=1).children,
            [
                ('countries', 1),
            ]
        )

    def test_lookup_yrel_nfield_ysupp_strlangdef(self):
        getter = _fetch_translations_query_getter(Continent, 'en')

        self.assertListEqual(
            getter(countries__gt=1).children,
            [
                ('countries__gt', 1),
            ]
        )

    def test_lookup_yrel_yfield_ntrans_nsupp_strlangdef(self):
        getter = _fetch_translations_query_getter(Continent, 'en')

        self.assertListEqual(
            getter(countries__code='en').children,
            [
                ('countries__code', 'en'),
            ]
        )

    def test_lookup_yrel_yfield_ytrans_nsupp_strlangdef(self):
        getter = _fetch_translations_query_getter(Continent, 'en')

        self.assertListEqual(
            getter(countries__name='Deutschland').children,
            [
                ('countries__name', 'Deutschland'),
            ]
        )

    def test_lookup_yrel_yfield_ntrans_ysupp_strlangdef(self):
        getter = _fetch_translations_query_getter(Continent, 'en')

        self.assertListEqual(
            getter(countries__code__icontains='en').children,
            [
                ('countries__code__icontains', 'en'),
            ]
        )

    def test_lookup_yrel_yfield_ytrans_ysupp_strlangdef(self):
        getter = _fetch_translations_query_getter(Continent, 'en')

        self.assertListEqual(
            getter(countries__name__icontains='Deutsch').children,
            [
                ('countries__name__icontains', 'Deutsch'),
            ]
        )

    def test_lookup_yrelnested_yfield_ntrans_nsupp_strlangdef(self):
        getter = _fetch_translations_query_getter(Continent, 'en')

        self.assertListEqual(
            getter(countries__cities__id=1).children,
            [
                ('countries__cities__id', 1),
            ]
        )

    def test_lookup_yrelnested_yfield_ytrans_nsupp_strlangdef(self):
        getter = _fetch_translations_query_getter(Continent, 'en')

        self.assertListEqual(
            getter(countries__cities__name='Köln').children,
            [
                ('countries__cities__name', 'Köln'),
            ]
        )

    def test_lookup_yrelnested_yfield_ntrans_ysupp_strlangdef(self):
        getter = _fetch_translations_query_getter(Continent, 'en')

        self.assertListEqual(
            getter(countries__cities__id__gt=1).children,
            [
                ('countries__cities__id__gt', 1),
            ]
        )

    def test_lookup_yrelnested_yfield_ytrans_ysupp_strlangdef(self):
        getter = _fetch_translations_query_getter(Continent, 'en')

        self.assertListEqual(
            getter(countries__cities__name__icontains='Kö').children,
            [
                ('countries__cities__name__icontains', 'Kö'),
            ]
        )

    def test_q_nrel_yfield_ntrans_nsupp_strlangdef(self):
        getter = _fetch_translations_query_getter(Continent, 'en')

        self.assertListEqual(
            getter(Q(code='EU')).children,
            [
                ('code', 'EU'),
            ]
        )

    def test_q_nrel_yfield_ytrans_nsupp_strlangdef(self):
        getter = _fetch_translations_query_getter(Continent, 'en')

        self.assertListEqual(
            getter(Q(name='Europa')).children,
            [
                ('name', 'Europa'),
            ]
        )

    def test_q_nrel_yfield_ntrans_ysupp_strlangdef(self):
        getter = _fetch_translations_query_getter(Continent, 'en')

        self.assertListEqual(
            getter(Q(code__icontains='EU')).children,
            [
                ('code__icontains', 'EU'),
            ]
        )

    def test_q_nrel_yfield_ytrans_ysupp_strlangdef(self):
        getter = _fetch_translations_query_getter(Continent, 'en')

        self.assertListEqual(
            getter(Q(name__icontains='Europa')).children,
            [
                ('name__icontains', 'Europa'),
            ]
        )

    def test_q_yrel_nfield_nsupp_strlangdef(self):
        getter = _fetch_translations_query_getter(Continent, 'en')

        self.assertListEqual(
            getter(Q(countries=1)).children,
            [
                ('countries', 1),
            ]
        )

    def test_q_yrel_nfield_ysupp_strlangdef(self):
        getter = _fetch_translations_query_getter(Continent, 'en')

        self.assertListEqual(
            getter(Q(countries__gt=1)).children,
            [
                ('countries__gt', 1),
            ]
        )

    def test_q_yrel_yfield_ntrans_nsupp_strlangdef(self):
        getter = _fetch_translations_query_getter(Continent, 'en')

        self.assertListEqual(
            getter(Q(countries__code='en')).children,
            [
                ('countries__code', 'en'),
            ]
        )

    def test_q_yrel_yfield_ytrans_nsupp_strlangdef(self):
        getter = _fetch_translations_query_getter(Continent, 'en')

        self.assertListEqual(
            getter(Q(countries__name='Deutschland')).children,
            [
                ('countries__name', 'Deutschland'),
            ]
        )

    def test_q_yrel_yfield_ntrans_ysupp_strlangdef(self):
        getter = _fetch_translations_query_getter(Continent, 'en')

        self.assertListEqual(
            getter(Q(countries__code__icontains='en')).children,
            [
                ('countries__code__icontains', 'en'),
            ]
        )

    def test_q_yrel_yfield_ytrans_ysupp_strlangdef(self):
        getter = _fetch_translations_query_getter(Continent, 'en')

        self.assertListEqual(
            getter(Q(countries__name__icontains='Deutsch')).children,
            [
                ('countries__name__icontains', 'Deutsch'),
            ]
        )

    def test_q_yrelnested_yfield_ntrans_nsupp_strlangdef(self):
        getter = _fetch_translations_query_getter(Continent, 'en')

        self.assertListEqual(
            getter(Q(countries__cities__id=1)).children,
            [
                ('countries__cities__id', 1),
            ]
        )

    def test_q_yrelnested_yfield_ytrans_nsupp_strlangdef(self):
        getter = _fetch_translations_query_getter(Continent, 'en')

        self.assertListEqual(
            getter(Q(countries__cities__name='Köln')).children,
            [
                ('countries__cities__name', 'Köln'),
            ]
        )

    def test_q_yrelnested_yfield_ntrans_ysupp_strlangdef(self):
        getter = _fetch_translations_query_getter(Continent, 'en')

        self.assertListEqual(
            getter(Q(countries__cities__id__gt=1)).children,
            [
                ('countries__cities__id__gt', 1),
            ]
        )

    def test_q_yrelnested_yfield_ytrans_ysupp_strlangdef(self):
        getter = _fetch_translations_query_getter(Continent, 'en')

        self.assertListEqual(
            getter(Q(countries__cities__name__icontains='Kö')).children,
            [
                ('countries__cities__name__icontains', 'Kö'),
            ]
        )

    def test_tq_nrel_yfield_ntrans_nsupp_strlangdef(self):
        getter = _fetch_translations_query_getter(Continent, 'en')

        self.assertListEqual(
            getter(TQ(code='EU', _lang='en')).children,
            [
                ('code', 'EU'),
            ]
        )

    def test_tq_nrel_yfield_ytrans_nsupp_strlangdef(self):
        getter = _fetch_translations_query_getter(Continent, 'en')

        self.assertListEqual(
            getter(TQ(name='Europa', _lang='en')).children,
            [
                ('name', 'Europa'),
            ]
        )

    def test_tq_nrel_yfield_ntrans_ysupp_strlangdef(self):
        getter = _fetch_translations_query_getter(Continent, 'en')

        self.assertListEqual(
            getter(TQ(code__icontains='EU', _lang='en')).children,
            [
                ('code__icontains', 'EU'),
            ]
        )

    def test_tq_nrel_yfield_ytrans_ysupp_strlangdef(self):
        getter = _fetch_translations_query_getter(Continent, 'en')

        self.assertListEqual(
            getter(TQ(name__icontains='Europa', _lang='en')).children,
            [
                ('name__icontains', 'Europa'),
            ]
        )

    def test_tq_yrel_nfield_nsupp_strlangdef(self):
        getter = _fetch_translations_query_getter(Continent, 'en')

        self.assertListEqual(
            getter(TQ(countries=1, _lang='en')).children,
            [
                ('countries', 1),
            ]
        )

    def test_tq_yrel_nfield_ysupp_strlangdef(self):
        getter = _fetch_translations_query_getter(Continent, 'en')

        self.assertListEqual(
            getter(TQ(countries__gt=1, _lang='en')).children,
            [
                ('countries__gt', 1),
            ]
        )

    def test_tq_yrel_yfield_ntrans_nsupp_strlangdef(self):
        getter = _fetch_translations_query_getter(Continent, 'en')

        self.assertListEqual(
            getter(TQ(countries__code='en', _lang='en')).children,
            [
                ('countries__code', 'en'),
            ]
        )

    def test_tq_yrel_yfield_ytrans_nsupp_strlangdef(self):
        getter = _fetch_translations_query_getter(Continent, 'en')

        self.assertListEqual(
            getter(TQ(countries__name='Deutschland', _lang='en')).children,
            [
                ('countries__name', 'Deutschland'),
            ]
        )

    def test_tq_yrel_yfield_ntrans_ysupp_strlangdef(self):
        getter = _fetch_translations_query_getter(Continent, 'en')

        self.assertListEqual(
            getter(TQ(countries__code__icontains='en', _lang='en')).children,
            [
                ('countries__code__icontains', 'en'),
            ]
        )

    def test_tq_yrel_yfield_ytrans_ysupp_strlangdef(self):
        getter = _fetch_translations_query_getter(Continent, 'en')

        self.assertListEqual(
            getter(TQ(countries__name__icontains='Deutsch', _lang='en')).children,
            [
                ('countries__name__icontains', 'Deutsch'),
            ]
        )

    def test_tq_yrelnested_yfield_ntrans_nsupp_strlangdef(self):
        getter = _fetch_translations_query_getter(Continent, 'en')

        self.assertListEqual(
            getter(TQ(countries__cities__id=1, _lang='en')).children,
            [
                ('countries__cities__id', 1),
            ]
        )

    def test_tq_yrelnested_yfield_ytrans_nsupp_strlangdef(self):
        getter = _fetch_translations_query_getter(Continent, 'en')

        self.assertListEqual(
            getter(TQ(countries__cities__name='Köln', _lang='en')).children,
            [
                ('countries__cities__name', 'Köln'),
            ]
        )

    def test_tq_yrelnested_yfield_ntrans_ysupp_strlangdef(self):
        getter = _fetch_translations_query_getter(Continent, 'en')

        self.assertListEqual(
            getter(TQ(countries__cities__id__gt=1, _lang='en')).children,
            [
                ('countries__cities__id__gt', 1),
            ]
        )

    def test_tq_yrelnested_yfield_ytrans_ysupp_strlangdef(self):
        getter = _fetch_translations_query_getter(Continent, 'en')

        self.assertListEqual(
            getter(TQ(countries__cities__name__icontains='Kö', _lang='en')).children,
            [
                ('countries__cities__name__icontains', 'Kö'),
            ]
        )

    def test_lookup_nrel_yfield_ntrans_nsupp_listlang(self):
        getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])

        self.assertListEqual(
            getter(code='EU').children,
            [
                ('code', 'EU'),
            ]
        )

    def test_lookup_nrel_yfield_ytrans_nsupp_listlang(self):
        getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])

        self.assertListEqual(
            getter(name='Europa').children,
            [
                ('translations__field', 'name'),
                ('translations__language__in', ['de', 'tr']),
                ('translations__text', 'Europa'),
            ]
        )

    def test_lookup_nrel_yfield_ntrans_ysupp_listlang(self):
        getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])

        self.assertListEqual(
            getter(code__icontains='EU').children,
            [
                ('code__icontains', 'EU'),
            ]
        )

    def test_lookup_nrel_yfield_ytrans_ysupp_listlang(self):
        getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])

        self.assertListEqual(
            getter(name__icontains='Europa').children,
            [
                ('translations__field', 'name'),
                ('translations__language__in', ['de', 'tr']),
                ('translations__text__icontains', 'Europa'),
            ]
        )

    def test_lookup_yrel_nfield_nsupp_listlang(self):
        getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])

        self.assertListEqual(
            getter(countries=1).children,
            [
                ('countries', 1),
            ]
        )

    def test_lookup_yrel_nfield_ysupp_listlang(self):
        getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])

        self.assertListEqual(
            getter(countries__gt=1).children,
            [
                ('countries__gt', 1),
            ]
        )

    def test_lookup_yrel_yfield_ntrans_nsupp_listlang(self):
        getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])

        self.assertListEqual(
            getter(countries__code='de').children,
            [
                ('countries__code', 'de'),
            ]
        )

    def test_lookup_yrel_yfield_ytrans_nsupp_listlang(self):
        getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])

        self.assertListEqual(
            getter(countries__name='Deutschland').children,
            [
                ('countries__translations__field', 'name'),
                ('countries__translations__language__in', ['de', 'tr']),
                ('countries__translations__text', 'Deutschland'),
            ]
        )

    def test_lookup_yrel_yfield_ntrans_ysupp_listlang(self):
        getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])

        self.assertListEqual(
            getter(countries__code__icontains=['de', 'tr']).children,
            [
                ('countries__code__icontains', ['de', 'tr']),
            ]
        )

    def test_lookup_yrel_yfield_ytrans_ysupp_listlang(self):
        getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])

        self.assertListEqual(
            getter(countries__name__icontains='Deutsch').children,
            [
                ('countries__translations__field', 'name'),
                ('countries__translations__language__in', ['de', 'tr']),
                ('countries__translations__text__icontains', 'Deutsch'),
            ]
        )

    def test_lookup_yrelnested_yfield_ntrans_nsupp_listlang(self):
        getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])

        self.assertListEqual(
            getter(countries__cities__id=1).children,
            [
                ('countries__cities__id', 1),
            ]
        )

    def test_lookup_yrelnested_yfield_ytrans_nsupp_listlang(self):
        getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])

        self.assertListEqual(
            getter(countries__cities__name='Köln').children,
            [
                ('countries__cities__translations__field', 'name'),
                ('countries__cities__translations__language__in', ['de', 'tr']),
                ('countries__cities__translations__text', 'Köln'),
            ]
        )

    def test_lookup_yrelnested_yfield_ntrans_ysupp_listlang(self):
        getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])

        self.assertListEqual(
            getter(countries__cities__id__gt=1).children,
            [
                ('countries__cities__id__gt', 1),
            ]
        )

    def test_lookup_yrelnested_yfield_ytrans_ysupp_listlang(self):
        getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])

        self.assertListEqual(
            getter(countries__cities__name__icontains='Kö').children,
            [
                ('countries__cities__translations__field', 'name'),
                ('countries__cities__translations__language__in', ['de', 'tr']),
                ('countries__cities__translations__text__icontains', 'Kö'),
            ]
        )

    def test_q_nrel_yfield_ntrans_nsupp_listlang(self):
        getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])

        self.assertListEqual(
            getter(Q(code='EU')).children,
            [
                ('code', 'EU'),
            ]
        )

    def test_q_nrel_yfield_ytrans_nsupp_listlang(self):
        getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])

        self.assertListEqual(
            getter(Q(name='Europa')).children,
            [
                ('translations__field', 'name'),
                ('translations__language__in', ['de', 'tr']),
                ('translations__text', 'Europa'),
            ]
        )

    def test_q_nrel_yfield_ntrans_ysupp_listlang(self):
        getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])

        self.assertListEqual(
            getter(Q(code__icontains='EU')).children,
            [
                ('code__icontains', 'EU'),
            ]
        )

    def test_q_nrel_yfield_ytrans_ysupp_listlang(self):
        getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])

        self.assertListEqual(
            getter(Q(name__icontains='Europa')).children,
            [
                ('translations__field', 'name'),
                ('translations__language__in', ['de', 'tr']),
                ('translations__text__icontains', 'Europa'),
            ]
        )

    def test_q_yrel_nfield_nsupp_listlang(self):
        getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])

        self.assertListEqual(
            getter(Q(countries=1)).children,
            [
                ('countries', 1),
            ]
        )

    def test_q_yrel_nfield_ysupp_listlang(self):
        getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])

        self.assertListEqual(
            getter(Q(countries__gt=1)).children,
            [
                ('countries__gt', 1),
            ]
        )

    def test_q_yrel_yfield_ntrans_nsupp_listlang(self):
        getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])

        self.assertListEqual(
            getter(Q(countries__code='de')).children,
            [
                ('countries__code', 'de'),
            ]
        )

    def test_q_yrel_yfield_ytrans_nsupp_listlang(self):
        getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])

        self.assertListEqual(
            getter(Q(countries__name='Deutschland')).children,
            [
                ('countries__translations__field', 'name'),
                ('countries__translations__language__in', ['de', 'tr']),
                ('countries__translations__text', 'Deutschland'),
            ]
        )

    def test_q_yrel_yfield_ntrans_ysupp_listlang(self):
        getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])

        self.assertListEqual(
            getter(Q(countries__code__icontains=['de', 'tr'])).children,
            [
                ('countries__code__icontains', ['de', 'tr']),
            ]
        )

    def test_q_yrel_yfield_ytrans_ysupp_listlang(self):
        getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])

        self.assertListEqual(
            getter(Q(countries__name__icontains='Deutsch')).children,
            [
                ('countries__translations__field', 'name'),
                ('countries__translations__language__in', ['de', 'tr']),
                ('countries__translations__text__icontains', 'Deutsch'),
            ]
        )

    def test_q_yrelnested_yfield_ntrans_nsupp_listlang(self):
        getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])

        self.assertListEqual(
            getter(Q(countries__cities__id=1)).children,
            [
                ('countries__cities__id', 1),
            ]
        )

    def test_q_yrelnested_yfield_ytrans_nsupp_listlang(self):
        getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])

        self.assertListEqual(
            getter(Q(countries__cities__name='Köln')).children,
            [
                ('countries__cities__translations__field', 'name'),
                ('countries__cities__translations__language__in', ['de', 'tr']),
                ('countries__cities__translations__text', 'Köln'),
            ]
        )

    def test_q_yrelnested_yfield_ntrans_ysupp_listlang(self):
        getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])

        self.assertListEqual(
            getter(Q(countries__cities__id__gt=1)).children,
            [
                ('countries__cities__id__gt', 1),
            ]
        )

    def test_q_yrelnested_yfield_ytrans_ysupp_listlang(self):
        getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])

        self.assertListEqual(
            getter(Q(countries__cities__name__icontains='Kö')).children,
            [
                ('countries__cities__translations__field', 'name'),
                ('countries__cities__translations__language__in', ['de', 'tr']),
                ('countries__cities__translations__text__icontains', 'Kö'),
            ]
        )

    def test_tq_nrel_yfield_ntrans_nsupp_listlang(self):
        getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])

        self.assertListEqual(
            getter(TQ(code='EU', _lang=['de', 'tr'])).children,
            [
                ('code', 'EU'),
            ]
        )

    def test_tq_nrel_yfield_ytrans_nsupp_listlang(self):
        getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])

        self.assertListEqual(
            getter(TQ(name='Europa', _lang=['de', 'tr'])).children,
            [
                ('translations__field', 'name'),
                ('translations__language__in', ['de', 'tr']),
                ('translations__text', 'Europa'),
            ]
        )

    def test_tq_nrel_yfield_ntrans_ysupp_listlang(self):
        getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])

        self.assertListEqual(
            getter(TQ(code__icontains='EU', _lang=['de', 'tr'])).children,
            [
                ('code__icontains', 'EU'),
            ]
        )

    def test_tq_nrel_yfield_ytrans_ysupp_listlang(self):
        getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])

        self.assertListEqual(
            getter(TQ(name__icontains='Europa', _lang=['de', 'tr'])).children,
            [
                ('translations__field', 'name'),
                ('translations__language__in', ['de', 'tr']),
                ('translations__text__icontains', 'Europa'),
            ]
        )

    def test_tq_yrel_nfield_nsupp_listlang(self):
        getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])

        self.assertListEqual(
            getter(TQ(countries=1, _lang=['de', 'tr'])).children,
            [
                ('countries', 1),
            ]
        )

    def test_tq_yrel_nfield_ysupp_listlang(self):
        getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])

        self.assertListEqual(
            getter(TQ(countries__gt=1, _lang=['de', 'tr'])).children,
            [
                ('countries__gt', 1),
            ]
        )

    def test_tq_yrel_yfield_ntrans_nsupp_listlang(self):
        getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])

        self.assertListEqual(
            getter(TQ(countries__code='de', _lang=['de', 'tr'])).children,
            [
                ('countries__code', 'de'),
            ]
        )

    def test_tq_yrel_yfield_ytrans_nsupp_listlang(self):
        getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])

        self.assertListEqual(
            getter(TQ(countries__name='Deutschland', _lang=['de', 'tr'])).children,
            [
                ('countries__translations__field', 'name'),
                ('countries__translations__language__in', ['de', 'tr']),
                ('countries__translations__text', 'Deutschland'),
            ]
        )

    def test_tq_yrel_yfield_ntrans_ysupp_listlang(self):
        getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])

        self.assertListEqual(
            getter(TQ(countries__code__icontains=['de', 'tr'], _lang=['de', 'tr'])).children,
            [
                ('countries__code__icontains', ['de', 'tr']),
            ]
        )

    def test_tq_yrel_yfield_ytrans_ysupp_listlang(self):
        getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])

        self.assertListEqual(
            getter(TQ(countries__name__icontains='Deutsch', _lang=['de', 'tr'])).children,
            [
                ('countries__translations__field', 'name'),
                ('countries__translations__language__in', ['de', 'tr']),
                ('countries__translations__text__icontains', 'Deutsch'),
            ]
        )

    def test_tq_yrelnested_yfield_ntrans_nsupp_listlang(self):
        getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])

        self.assertListEqual(
            getter(TQ(countries__cities__id=1, _lang=['de', 'tr'])).children,
            [
                ('countries__cities__id', 1),
            ]
        )

    def test_tq_yrelnested_yfield_ytrans_nsupp_listlang(self):
        getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])

        self.assertListEqual(
            getter(TQ(countries__cities__name='Köln', _lang=['de', 'tr'])).children,
            [
                ('countries__cities__translations__field', 'name'),
                ('countries__cities__translations__language__in', ['de', 'tr']),
                ('countries__cities__translations__text', 'Köln'),
            ]
        )

    def test_tq_yrelnested_yfield_ntrans_ysupp_listlang(self):
        getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])

        self.assertListEqual(
            getter(TQ(countries__cities__id__gt=1, _lang=['de', 'tr'])).children,
            [
                ('countries__cities__id__gt', 1),
            ]
        )

    def test_tq_yrelnested_yfield_ytrans_ysupp_listlang(self):
        getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])

        self.assertListEqual(
            getter(TQ(countries__cities__name__icontains='Kö', _lang=['de', 'tr'])).children,
            [
                ('countries__cities__translations__field', 'name'),
                ('countries__cities__translations__language__in', ['de', 'tr']),
                ('countries__cities__translations__text__icontains', 'Kö'),
            ]
        )

    def test_lookup_nrel_yfield_ntrans_nsupp_listlangdef(self):
        getter = _fetch_translations_query_getter(Continent, ['en', 'de'])

        self.assertListEqual(
            getter(code='EU').children,
            [
                ('code', 'EU'),
            ]
        )

    def test_lookup_nrel_yfield_ytrans_nsupp_listlangdef(self):
        getter = _fetch_translations_query_getter(Continent, ['en', 'de'])

        self.assertListEqual(
            getter(name='Europa').children,
            [
                ('name', 'Europa'),
                Q(
                    ('translations__field', 'name'),
                    ('translations__language__in', ['de']),
                    ('translations__text', 'Europa'),
                ),
            ]
        )

    def test_lookup_nrel_yfield_ntrans_ysupp_listlangdef(self):
        getter = _fetch_translations_query_getter(Continent, ['en', 'de'])

        self.assertListEqual(
            getter(code__icontains='EU').children,
            [
                ('code__icontains', 'EU'),
            ]
        )

    def test_lookup_nrel_yfield_ytrans_ysupp_listlangdef(self):
        getter = _fetch_translations_query_getter(Continent, ['en', 'de'])

        self.assertListEqual(
            getter(name__icontains='Europa').children,
            [
                ('name__icontains', 'Europa'),
                Q(
                    ('translations__field', 'name'),
                    ('translations__language__in', ['de']),
                    ('translations__text__icontains', 'Europa'),
                ),
            ]
        )

    def test_lookup_yrel_nfield_nsupp_listlangdef(self):
        getter = _fetch_translations_query_getter(Continent, ['en', 'de'])

        self.assertListEqual(
            getter(countries=1).children,
            [
                ('countries', 1),
            ]
        )

    def test_lookup_yrel_nfield_ysupp_listlangdef(self):
        getter = _fetch_translations_query_getter(Continent, ['en', 'de'])

        self.assertListEqual(
            getter(countries__gt=1).children,
            [
                ('countries__gt', 1),
            ]
        )

    def test_lookup_yrel_yfield_ntrans_nsupp_listlangdef(self):
        getter = _fetch_translations_query_getter(Continent, ['en', 'de'])

        self.assertListEqual(
            getter(countries__code='de').children,
            [
                ('countries__code', 'de'),
            ]
        )

    def test_lookup_yrel_yfield_ytrans_nsupp_listlangdef(self):
        getter = _fetch_translations_query_getter(Continent, ['en', 'de'])

        self.assertListEqual(
            getter(countries__name='Deutschland').children,
            [
                ('countries__name', 'Deutschland'),
                Q(
                    ('countries__translations__field', 'name'),
                    ('countries__translations__language__in', ['de']),
                    ('countries__translations__text', 'Deutschland'),
                ),
            ]
        )

    def test_lookup_yrel_yfield_ntrans_ysupp_listlangdef(self):
        getter = _fetch_translations_query_getter(Continent, ['en', 'de'])

        self.assertListEqual(
            getter(countries__code__icontains=['de']).children,
            [
                ('countries__code__icontains', ['de']),
            ]
        )

    def test_lookup_yrel_yfield_ytrans_ysupp_listlangdef(self):
        getter = _fetch_translations_query_getter(Continent, ['en', 'de'])

        self.assertListEqual(
            getter(countries__name__icontains='Deutsch').children,
            [
                ('countries__name__icontains', 'Deutsch'),
                Q(
                    ('countries__translations__field', 'name'),
                    ('countries__translations__language__in', ['de']),
                    ('countries__translations__text__icontains', 'Deutsch'),
                ),
            ]
        )

    def test_lookup_yrelnested_yfield_ntrans_nsupp_listlangdef(self):
        getter = _fetch_translations_query_getter(Continent, ['en', 'de'])

        self.assertListEqual(
            getter(countries__cities__id=1).children,
            [
                ('countries__cities__id', 1),
            ]
        )

    def test_lookup_yrelnested_yfield_ytrans_nsupp_listlangdef(self):
        getter = _fetch_translations_query_getter(Continent, ['en', 'de'])

        self.assertListEqual(
            getter(countries__cities__name='Köln').children,
            [
                ('countries__cities__name', 'Köln'),
                Q(
                    ('countries__cities__translations__field', 'name'),
                    ('countries__cities__translations__language__in', ['de']),
                    ('countries__cities__translations__text', 'Köln'),
                ),
            ]
        )

    def test_lookup_yrelnested_yfield_ntrans_ysupp_listlangdef(self):
        getter = _fetch_translations_query_getter(Continent, ['en', 'de'])

        self.assertListEqual(
            getter(countries__cities__id__gt=1).children,
            [
                ('countries__cities__id__gt', 1),
            ]
        )

    def test_lookup_yrelnested_yfield_ytrans_ysupp_listlangdef(self):
        getter = _fetch_translations_query_getter(Continent, ['en', 'de'])

        self.assertListEqual(
            getter(countries__cities__name__icontains='Kö').children,
            [
                ('countries__cities__name__icontains', 'Kö'),
                Q(
                    ('countries__cities__translations__field', 'name'),
                    ('countries__cities__translations__language__in', ['de']),
                    ('countries__cities__translations__text__icontains', 'Kö'),
                ),
            ]
        )

    def test_q_nrel_yfield_ntrans_nsupp_listlangdef(self):
        getter = _fetch_translations_query_getter(Continent, ['en', 'de'])

        self.assertListEqual(
            getter(Q(code='EU')).children,
            [
                ('code', 'EU'),
            ]
        )

    def test_q_nrel_yfield_ytrans_nsupp_listlangdef(self):
        getter = _fetch_translations_query_getter(Continent, ['en', 'de'])

        self.assertListEqual(
            getter(Q(name='Europa')).children,
            [
                ('name', 'Europa'),
                Q(
                    ('translations__field', 'name'),
                    ('translations__language__in', ['de']),
                    ('translations__text', 'Europa'),
                ),
            ]
        )

    def test_q_nrel_yfield_ntrans_ysupp_listlangdef(self):
        getter = _fetch_translations_query_getter(Continent, ['en', 'de'])

        self.assertListEqual(
            getter(Q(code__icontains='EU')).children,
            [
                ('code__icontains', 'EU'),
            ]
        )

    def test_q_nrel_yfield_ytrans_ysupp_listlangdef(self):
        getter = _fetch_translations_query_getter(Continent, ['en', 'de'])

        self.assertListEqual(
            getter(Q(name__icontains='Europa')).children,
            [
                ('name__icontains', 'Europa'),
                Q(
                    ('translations__field', 'name'),
                    ('translations__language__in', ['de']),
                    ('translations__text__icontains', 'Europa'),
                ),
            ]
        )

    def test_q_yrel_nfield_nsupp_listlangdef(self):
        getter = _fetch_translations_query_getter(Continent, ['en', 'de'])

        self.assertListEqual(
            getter(Q(countries=1)).children,
            [
                ('countries', 1),
            ]
        )

    def test_q_yrel_nfield_ysupp_listlangdef(self):
        getter = _fetch_translations_query_getter(Continent, ['en', 'de'])

        self.assertListEqual(
            getter(Q(countries__gt=1)).children,
            [
                ('countries__gt', 1),
            ]
        )

    def test_q_yrel_yfield_ntrans_nsupp_listlangdef(self):
        getter = _fetch_translations_query_getter(Continent, ['en', 'de'])

        self.assertListEqual(
            getter(Q(countries__code=['de'])).children,
            [
                ('countries__code', ['de']),
            ]
        )

    def test_q_yrel_yfield_ytrans_nsupp_listlangdef(self):
        getter = _fetch_translations_query_getter(Continent, ['en', 'de'])

        self.assertListEqual(
            getter(Q(countries__name='Deutschland')).children,
            [
                ('countries__name', 'Deutschland'),
                Q(
                    ('countries__translations__field', 'name'),
                    ('countries__translations__language__in', ['de']),
                    ('countries__translations__text', 'Deutschland'),
                ),
            ]
        )

    def test_q_yrel_yfield_ntrans_ysupp_listlangdef(self):
        getter = _fetch_translations_query_getter(Continent, ['en', 'de'])

        self.assertListEqual(
            getter(Q(countries__code__icontains=['de'])).children,
            [
                ('countries__code__icontains', ['de']),
            ]
        )

    def test_q_yrel_yfield_ytrans_ysupp_listlangdef(self):
        getter = _fetch_translations_query_getter(Continent, ['en', 'de'])

        self.assertListEqual(
            getter(Q(countries__name__icontains='Deutsch')).children,
            [
                ('countries__name__icontains', 'Deutsch'),
                Q(
                    ('countries__translations__field', 'name'),
                    ('countries__translations__language__in', ['de']),
                    ('countries__translations__text__icontains', 'Deutsch'),
                )
            ]
        )

    def test_q_yrelnested_yfield_ntrans_nsupp_listlangdef(self):
        getter = _fetch_translations_query_getter(Continent, ['en', 'de'])

        self.assertListEqual(
            getter(Q(countries__cities__id=1)).children,
            [
                ('countries__cities__id', 1),
            ]
        )

    def test_q_yrelnested_yfield_ytrans_nsupp_listlangdef(self):
        getter = _fetch_translations_query_getter(Continent, ['en', 'de'])

        self.assertListEqual(
            getter(Q(countries__cities__name='Köln')).children,
            [
                ('countries__cities__name', 'Köln'),
                Q(
                    ('countries__cities__translations__field', 'name'),
                    ('countries__cities__translations__language__in', ['de']),
                    ('countries__cities__translations__text', 'Köln'),
                )
            ]
        )

    def test_q_yrelnested_yfield_ntrans_ysupp_listlangdef(self):
        getter = _fetch_translations_query_getter(Continent, ['en', 'de'])

        self.assertListEqual(
            getter(Q(countries__cities__id__gt=1)).children,
            [
                ('countries__cities__id__gt', 1),
            ]
        )

    def test_q_yrelnested_yfield_ytrans_ysupp_listlangdef(self):
        getter = _fetch_translations_query_getter(Continent, ['en', 'de'])

        self.assertListEqual(
            getter(Q(countries__cities__name__icontains='Kö')).children,
            [
                ('countries__cities__name__icontains', 'Kö'),
                Q(
                    ('countries__cities__translations__field', 'name'),
                    ('countries__cities__translations__language__in', ['de']),
                    ('countries__cities__translations__text__icontains', 'Kö'),
                )
            ]
        )

    def test_tq_nrel_yfield_ntrans_nsupp_listlangdef(self):
        getter = _fetch_translations_query_getter(Continent, ['en', 'de'])

        self.assertListEqual(
            getter(TQ(code='EU', _lang=['en', 'de'])).children,
            [
                ('code', 'EU'),
            ]
        )

    def test_tq_nrel_yfield_ytrans_nsupp_listlangdef(self):
        getter = _fetch_translations_query_getter(Continent, ['en', 'de'])

        self.assertListEqual(
            getter(TQ(name='Europa', _lang=['en', 'de'])).children,
            [
                ('name', 'Europa'),
                Q(
                    ('translations__field', 'name'),
                    ('translations__language__in', ['de']),
                    ('translations__text', 'Europa'),
                ),
            ]
        )

    def test_tq_nrel_yfield_ntrans_ysupp_listlangdef(self):
        getter = _fetch_translations_query_getter(Continent, ['en', 'de'])

        self.assertListEqual(
            getter(TQ(code__icontains='EU', _lang=['en', 'de'])).children,
            [
                ('code__icontains', 'EU'),
            ]
        )

    def test_tq_nrel_yfield_ytrans_ysupp_listlangdef(self):
        getter = _fetch_translations_query_getter(Continent, ['en', 'de'])

        self.assertListEqual(
            getter(TQ(name__icontains='Europa', _lang=['en', 'de'])).children,
            [
                ('name__icontains', 'Europa'),
                Q(
                    ('translations__field', 'name'),
                    ('translations__language__in', ['de']),
                    ('translations__text__icontains', 'Europa'),
                ),
            ]
        )

    def test_tq_yrel_nfield_nsupp_listlangdef(self):
        getter = _fetch_translations_query_getter(Continent, ['en', 'de'])

        self.assertListEqual(
            getter(TQ(countries=1, _lang=['en', 'de'])).children,
            [
                ('countries', 1),
            ]
        )

    def test_tq_yrel_nfield_ysupp_listlangdef(self):
        getter = _fetch_translations_query_getter(Continent, ['en', 'de'])

        self.assertListEqual(
            getter(TQ(countries__gt=1, _lang=['en', 'de'])).children,
            [
                ('countries__gt', 1),
            ]
        )

    def test_tq_yrel_yfield_ntrans_nsupp_listlangdef(self):
        getter = _fetch_translations_query_getter(Continent, ['en', 'de'])

        self.assertListEqual(
            getter(TQ(countries__code=['de'], _lang=['en', 'de'])).children,
            [
                ('countries__code', ['de']),
            ]
        )

    def test_tq_yrel_yfield_ytrans_nsupp_listlangdef(self):
        getter = _fetch_translations_query_getter(Continent, ['en', 'de'])

        self.assertListEqual(
            getter(TQ(countries__name='Deutschland', _lang=['en', 'de'])).children,
            [
                ('countries__name', 'Deutschland'),
                Q(
                    ('countries__translations__field', 'name'),
                    ('countries__translations__language__in', ['de']),
                    ('countries__translations__text', 'Deutschland'),
                ),
            ]
        )

    def test_tq_yrel_yfield_ntrans_ysupp_listlangdef(self):
        getter = _fetch_translations_query_getter(Continent, ['en', 'de'])

        self.assertListEqual(
            getter(TQ(countries__code__icontains=['de'], _lang=['en', 'de'])).children,
            [
                ('countries__code__icontains', ['de']),
            ]
        )

    def test_tq_yrel_yfield_ytrans_ysupp_listlangdef(self):
        getter = _fetch_translations_query_getter(Continent, ['en', 'de'])

        self.assertListEqual(
            getter(TQ(countries__name__icontains='Deutsch', _lang=['en', 'de'])).children,
            [
                ('countries__name__icontains', 'Deutsch'),
                Q(
                    ('countries__translations__field', 'name'),
                    ('countries__translations__language__in', ['de']),
                    ('countries__translations__text__icontains', 'Deutsch'),
                )
            ]
        )

    def test_tq_yrelnested_yfield_ntrans_nsupp_listlangdef(self):
        getter = _fetch_translations_query_getter(Continent, ['en', 'de'])

        self.assertListEqual(
            getter(TQ(countries__cities__id=1, _lang=['en', 'de'])).children,
            [
                ('countries__cities__id', 1),
            ]
        )

    def test_tq_yrelnested_yfield_ytrans_nsupp_listlangdef(self):
        getter = _fetch_translations_query_getter(Continent, ['en', 'de'])

        self.assertListEqual(
            getter(TQ(countries__cities__name='Köln', _lang=['en', 'de'])).children,
            [
                ('countries__cities__name', 'Köln'),
                Q(
                    ('countries__cities__translations__field', 'name'),
                    ('countries__cities__translations__language__in', ['de']),
                    ('countries__cities__translations__text', 'Köln'),
                )
            ]
        )

    def test_tq_yrelnested_yfield_ntrans_ysupp_listlangdef(self):
        getter = _fetch_translations_query_getter(Continent, ['en', 'de'])

        self.assertListEqual(
            getter(TQ(countries__cities__id__gt=1, _lang=['en', 'de'])).children,
            [
                ('countries__cities__id__gt', 1),
            ]
        )

    def test_tq_yrelnested_yfield_ytrans_ysupp_listlangdef(self):
        getter = _fetch_translations_query_getter(Continent, ['en', 'de'])

        self.assertListEqual(
            getter(TQ(countries__cities__name__icontains='Kö', _lang=['en', 'de'])).children,
            [
                ('countries__cities__name__icontains', 'Kö'),
                Q(
                    ('countries__cities__translations__field', 'name'),
                    ('countries__cities__translations__language__in', ['de']),
                    ('countries__cities__translations__text__icontains', 'Kö'),
                )
            ]
        )

class TQTest(TestCase):
    """Tests for `_fetch_translations_query_getter`."""

    def test_init(self):
        tq = TQ(_lang='de')

        self.assertEqual(tq.lang, 'de')

    @override(language='de', deactivate=True)
    def test_init_no_lang(self):
        tq = TQ()

        self.assertEqual(tq.lang, 'de')

    def test_init_invalid_lang(self):
        with self.assertRaises(ValueError) as error:
            tq = TQ(_lang='xx')

        self.assertEqual(
            error.exception.args[0],
            'The language code `xx` is not supported.'
        )

    def test_deepcopy(self):
        tq = TQ(_lang='de')
        tq_copy = copy.deepcopy(tq)

        self.assertEqual(tq_copy.lang, 'de')
