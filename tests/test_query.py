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
            getter(
                code='EU'
            ).children[0].children,
            [
                ('code', 'EU'),
            ]
        )

    def test_lookup_nrel_yfield_ytrans_nsupp_strlang(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(
                name='Europa'
            ).children[0].children,
            [
                ('translations__field', 'name'),
                ('translations__language', 'de'),
                ('translations__text', 'Europa'),
            ]
        )

    def test_lookup_nrel_yfield_ntrans_ysupp_strlang(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(
                code__icontains='EU'
            ).children[0].children,
            [
                ('code__icontains', 'EU'),
            ]
        )

    def test_lookup_nrel_yfield_ytrans_ysupp_strlang(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(
                name__icontains='Europa'
            ).children[0].children,
            [
                ('translations__field', 'name'),
                ('translations__language', 'de'),
                ('translations__text__icontains', 'Europa'),
            ]
        )

    def test_lookup_yrel_nfield_nsupp_strlang(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(
                countries=1
            ).children[0].children,
            [
                ('countries', 1),
            ]
        )

    def test_lookup_yrel_nfield_ysupp_strlang(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(
                countries__gt=1
            ).children[0].children,
            [
                ('countries__gt', 1),
            ]
        )

    def test_lookup_yrel_yfield_ntrans_nsupp_strlang(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(
                countries__code='DE'
            ).children[0].children,
            [
                ('countries__code', 'DE'),
            ]
        )

    def test_lookup_yrel_yfield_ytrans_nsupp_strlang(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(
                countries__name='Deutschland'
            ).children[0].children,
            [
                ('countries__translations__field', 'name'),
                ('countries__translations__language', 'de'),
                ('countries__translations__text', 'Deutschland'),
            ]
        )

    def test_lookup_yrel_yfield_ntrans_ysupp_strlang(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(
                countries__code__icontains='DE'
            ).children[0].children,
            [
                ('countries__code__icontains', 'DE'),
            ]
        )

    def test_lookup_yrel_yfield_ytrans_ysupp_strlang(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(
                countries__name__icontains='Deutsch'
            ).children[0].children,
            [
                ('countries__translations__field', 'name'),
                ('countries__translations__language', 'de'),
                ('countries__translations__text__icontains', 'Deutsch'),
            ]
        )

    def test_lookup_yrelnested_yfield_ntrans_nsupp_strlang(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(
                countries__cities__id=1
            ).children[0].children,
            [
                ('countries__cities__id', 1),
            ]
        )

    def test_lookup_yrelnested_yfield_ytrans_nsupp_strlang(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(
                countries__cities__name='Köln'
            ).children[0].children,
            [
                ('countries__cities__translations__field', 'name'),
                ('countries__cities__translations__language', 'de'),
                ('countries__cities__translations__text', 'Köln'),
            ]
        )

    def test_lookup_yrelnested_yfield_ntrans_ysupp_strlang(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(
                countries__cities__id__gt=1
            ).children[0].children,
            [
                ('countries__cities__id__gt', 1),
            ]
        )

    def test_lookup_yrelnested_yfield_ytrans_ysupp_strlang(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(
                countries__cities__name__icontains='Kö'
            ).children[0].children,
            [
                ('countries__cities__translations__field', 'name'),
                ('countries__cities__translations__language', 'de'),
                ('countries__cities__translations__text__icontains', 'Kö'),
            ]
        )

    def test_lookup_nrel_yfield_ntrans_nsupp_strlangdef(self):
        getter = _fetch_translations_query_getter(Continent, 'en')

        self.assertListEqual(
            getter(
                code='EU'
            ).children[0].children,
            [
                ('code', 'EU'),
            ]
        )

    def test_lookup_nrel_yfield_ytrans_nsupp_strlangdef(self):
        getter = _fetch_translations_query_getter(Continent, 'en')

        self.assertListEqual(
            getter(
                name='Europa'
            ).children[0].children,
            [
                ('name', 'Europa'),
            ]
        )

    def test_lookup_nrel_yfield_ntrans_ysupp_strlangdef(self):
        getter = _fetch_translations_query_getter(Continent, 'en')

        self.assertListEqual(
            getter(
                code__icontains='EU'
            ).children[0].children,
            [
                ('code__icontains', 'EU'),
            ]
        )

    def test_lookup_nrel_yfield_ytrans_ysupp_strlangdef(self):
        getter = _fetch_translations_query_getter(Continent, 'en')

        self.assertListEqual(
            getter(
                name__icontains='Europa'
            ).children[0].children,
            [
                ('name__icontains', 'Europa'),
            ]
        )

    def test_lookup_yrel_nfield_nsupp_strlangdef(self):
        getter = _fetch_translations_query_getter(Continent, 'en')

        self.assertListEqual(
            getter(
                countries=1
            ).children[0].children,
            [
                ('countries', 1),
            ]
        )

    def test_lookup_yrel_nfield_ysupp_strlangdef(self):
        getter = _fetch_translations_query_getter(Continent, 'en')

        self.assertListEqual(
            getter(
                countries__gt=1
            ).children[0].children,
            [
                ('countries__gt', 1),
            ]
        )

    def test_lookup_yrel_yfield_ntrans_nsupp_strlangdef(self):
        getter = _fetch_translations_query_getter(Continent, 'en')

        self.assertListEqual(
            getter(
                countries__code='en'
            ).children[0].children,
            [
                ('countries__code', 'en'),
            ]
        )

    def test_lookup_yrel_yfield_ytrans_nsupp_strlangdef(self):
        getter = _fetch_translations_query_getter(Continent, 'en')

        self.assertListEqual(
            getter(
                countries__name='Deutschland'
            ).children[0].children,
            [
                ('countries__name', 'Deutschland'),
            ]
        )

    def test_lookup_yrel_yfield_ntrans_ysupp_strlangdef(self):
        getter = _fetch_translations_query_getter(Continent, 'en')

        self.assertListEqual(
            getter(
                countries__code__icontains='en'
            ).children[0].children,
            [
                ('countries__code__icontains', 'en'),
            ]
        )

    def test_lookup_yrel_yfield_ytrans_ysupp_strlangdef(self):
        getter = _fetch_translations_query_getter(Continent, 'en')

        self.assertListEqual(
            getter(
                countries__name__icontains='Deutsch'
            ).children[0].children,
            [
                ('countries__name__icontains', 'Deutsch'),
            ]
        )

    def test_lookup_yrelnested_yfield_ntrans_nsupp_strlangdef(self):
        getter = _fetch_translations_query_getter(Continent, 'en')

        self.assertListEqual(
            getter(
                countries__cities__id=1
            ).children[0].children,
            [
                ('countries__cities__id', 1),
            ]
        )

    def test_lookup_yrelnested_yfield_ytrans_nsupp_strlangdef(self):
        getter = _fetch_translations_query_getter(Continent, 'en')

        self.assertListEqual(
            getter(
                countries__cities__name='Köln'
            ).children[0].children,
            [
                ('countries__cities__name', 'Köln'),
            ]
        )

    def test_lookup_yrelnested_yfield_ntrans_ysupp_strlangdef(self):
        getter = _fetch_translations_query_getter(Continent, 'en')

        self.assertListEqual(
            getter(
                countries__cities__id__gt=1
            ).children[0].children,
            [
                ('countries__cities__id__gt', 1),
            ]
        )

    def test_lookup_yrelnested_yfield_ytrans_ysupp_strlangdef(self):
        getter = _fetch_translations_query_getter(Continent, 'en')

        self.assertListEqual(
            getter(
                countries__cities__name__icontains='Kö'
            ).children[0].children,
            [
                ('countries__cities__name__icontains', 'Kö'),
            ]
        )

    def test_lookup_nrel_yfield_ntrans_nsupp_listlang(self):
        getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])

        self.assertListEqual(
            getter(
                code='EU'
            ).children[0].children,
            [
                ('code', 'EU'),
            ]
        )

    def test_lookup_nrel_yfield_ytrans_nsupp_listlang(self):
        getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])

        self.assertListEqual(
            getter(
                name='Europa'
            ).children[0].children,
            [
                ('translations__field', 'name'),
                ('translations__language__in', ['de', 'tr']),
                ('translations__text', 'Europa'),
            ]
        )

    def test_lookup_nrel_yfield_ntrans_ysupp_listlang(self):
        getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])

        self.assertListEqual(
            getter(
                code__icontains='EU'
            ).children[0].children,
            [
                ('code__icontains', 'EU'),
            ]
        )

    def test_lookup_nrel_yfield_ytrans_ysupp_listlang(self):
        getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])

        self.assertListEqual(
            getter(
                name__icontains='Europa'
            ).children[0].children,
            [
                ('translations__field', 'name'),
                ('translations__language__in', ['de', 'tr']),
                ('translations__text__icontains', 'Europa'),
            ]
        )

    def test_lookup_yrel_nfield_nsupp_listlang(self):
        getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])

        self.assertListEqual(
            getter(
                countries=1
            ).children[0].children,
            [
                ('countries', 1),
            ]
        )

    def test_lookup_yrel_nfield_ysupp_listlang(self):
        getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])

        self.assertListEqual(
            getter(
                countries__gt=1
            ).children[0].children,
            [
                ('countries__gt', 1),
            ]
        )

    def test_lookup_yrel_yfield_ntrans_nsupp_listlang(self):
        getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])

        self.assertListEqual(
            getter(
                countries__code='de'
            ).children[0].children,
            [
                ('countries__code', 'de'),
            ]
        )

    def test_lookup_yrel_yfield_ytrans_nsupp_listlang(self):
        getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])

        self.assertListEqual(
            getter(
                countries__name='Deutschland'
            ).children[0].children,
            [
                ('countries__translations__field', 'name'),
                ('countries__translations__language__in', ['de', 'tr']),
                ('countries__translations__text', 'Deutschland'),
            ]
        )

    def test_lookup_yrel_yfield_ntrans_ysupp_listlang(self):
        getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])

        self.assertListEqual(
            getter(
                countries__code__icontains=['de', 'tr']
            ).children[0].children,
            [
                ('countries__code__icontains', ['de', 'tr']),
            ]
        )

    def test_lookup_yrel_yfield_ytrans_ysupp_listlang(self):
        getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])

        self.assertListEqual(
            getter(
                countries__name__icontains='Deutsch'
            ).children[0].children,
            [
                ('countries__translations__field', 'name'),
                ('countries__translations__language__in', ['de', 'tr']),
                ('countries__translations__text__icontains', 'Deutsch'),
            ]
        )

    def test_lookup_yrelnested_yfield_ntrans_nsupp_listlang(self):
        getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])

        self.assertListEqual(
            getter(
                countries__cities__id=1
            ).children[0].children,
            [
                ('countries__cities__id', 1),
            ]
        )

    def test_lookup_yrelnested_yfield_ytrans_nsupp_listlang(self):
        getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])

        self.assertListEqual(
            getter(
                countries__cities__name='Köln'
            ).children[0].children,
            [
                ('countries__cities__translations__field', 'name'),
                (
                    'countries__cities__translations__language__in',
                    ['de', 'tr']
                ),
                ('countries__cities__translations__text', 'Köln'),
            ]
        )

    def test_lookup_yrelnested_yfield_ntrans_ysupp_listlang(self):
        getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])

        self.assertListEqual(
            getter(
                countries__cities__id__gt=1
            ).children[0].children,
            [
                ('countries__cities__id__gt', 1),
            ]
        )

    def test_lookup_yrelnested_yfield_ytrans_ysupp_listlang(self):
        getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])

        self.assertListEqual(
            getter(
                countries__cities__name__icontains='Kö'
            ).children[0].children,
            [
                ('countries__cities__translations__field', 'name'),
                (
                    'countries__cities__translations__language__in',
                    ['de', 'tr']
                ),
                ('countries__cities__translations__text__icontains', 'Kö'),
            ]
        )

    def test_lookup_nrel_yfield_ntrans_nsupp_listlangdef(self):
        getter = _fetch_translations_query_getter(Continent, ['en', 'de'])

        self.assertListEqual(
            getter(
                code='EU'
            ).children[0].children,
            [
                ('code', 'EU'),
            ]
        )

    def test_lookup_nrel_yfield_ytrans_nsupp_listlangdef(self):
        getter = _fetch_translations_query_getter(Continent, ['en', 'de'])

        self.assertListEqual(
            getter(
                name='Europa'
            ).children[0].children,
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
            getter(
                code__icontains='EU'
            ).children[0].children,
            [
                ('code__icontains', 'EU'),
            ]
        )

    def test_lookup_nrel_yfield_ytrans_ysupp_listlangdef(self):
        getter = _fetch_translations_query_getter(Continent, ['en', 'de'])

        self.assertListEqual(
            getter(
                name__icontains='Europa'
            ).children[0].children,
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
            getter(
                countries=1
            ).children[0].children,
            [
                ('countries', 1),
            ]
        )

    def test_lookup_yrel_nfield_ysupp_listlangdef(self):
        getter = _fetch_translations_query_getter(Continent, ['en', 'de'])

        self.assertListEqual(
            getter(
                countries__gt=1
            ).children[0].children,
            [
                ('countries__gt', 1),
            ]
        )

    def test_lookup_yrel_yfield_ntrans_nsupp_listlangdef(self):
        getter = _fetch_translations_query_getter(Continent, ['en', 'de'])

        self.assertListEqual(
            getter(
                countries__code='de'
            ).children[0].children,
            [
                ('countries__code', 'de'),
            ]
        )

    def test_lookup_yrel_yfield_ytrans_nsupp_listlangdef(self):
        getter = _fetch_translations_query_getter(Continent, ['en', 'de'])

        self.assertListEqual(
            getter(
                countries__name='Deutschland'
            ).children[0].children,
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
            getter(
                countries__code__icontains=['de']
            ).children[0].children,
            [
                ('countries__code__icontains', ['de']),
            ]
        )

    def test_lookup_yrel_yfield_ytrans_ysupp_listlangdef(self):
        getter = _fetch_translations_query_getter(Continent, ['en', 'de'])

        self.assertListEqual(
            getter(
                countries__name__icontains='Deutsch'
            ).children[0].children,
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
            getter(
                countries__cities__id=1
            ).children[0].children,
            [
                ('countries__cities__id', 1),
            ]
        )

    def test_lookup_yrelnested_yfield_ytrans_nsupp_listlangdef(self):
        getter = _fetch_translations_query_getter(Continent, ['en', 'de'])

        self.assertListEqual(
            getter(
                countries__cities__name='Köln'
            ).children[0].children,
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
            getter(
                countries__cities__id__gt=1
            ).children[0].children,
            [
                ('countries__cities__id__gt', 1),
            ]
        )

    def test_lookup_yrelnested_yfield_ytrans_ysupp_listlangdef(self):
        getter = _fetch_translations_query_getter(Continent, ['en', 'de'])

        self.assertListEqual(
            getter(
                countries__cities__name__icontains='Kö'
            ).children[0].children,
            [
                ('countries__cities__name__icontains', 'Kö'),
                Q(
                    ('countries__cities__translations__field', 'name'),
                    ('countries__cities__translations__language__in', ['de']),
                    ('countries__cities__translations__text__icontains', 'Kö'),
                ),
            ]
        )

    def test_q_nrel_yfield_ntrans_nsupp_strlang(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(
                Q(
                    code='EU'
                )
            ).children[0].children[0].children,
            [
                ('code', 'EU'),
            ]
        )

    def test_q_nrel_yfield_ytrans_nsupp_strlang(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(
                Q(
                    name='Europa'
                )
            ).children[0].children[0].children,
            [
                ('translations__field', 'name'),
                ('translations__language', 'de'),
                ('translations__text', 'Europa'),
            ]
        )

    def test_q_nrel_yfield_ntrans_ysupp_strlang(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(
                Q(
                    code__icontains='EU'
                )
            ).children[0].children[0].children,
            [
                ('code__icontains', 'EU'),
            ]
        )

    def test_q_nrel_yfield_ytrans_ysupp_strlang(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(
                Q(
                    name__icontains='Europa'
                )
            ).children[0].children[0].children,
            [
                ('translations__field', 'name'),
                ('translations__language', 'de'),
                ('translations__text__icontains', 'Europa'),
            ]
        )

    def test_q_yrel_nfield_nsupp_strlang(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(
                Q(
                    countries=1
                )
            ).children[0].children[0].children,
            [
                ('countries', 1),
            ]
        )

    def test_q_yrel_nfield_ysupp_strlang(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(
                Q(
                    countries__gt=1
                )
            ).children[0].children[0].children,
            [
                ('countries__gt', 1),
            ]
        )

    def test_q_yrel_yfield_ntrans_nsupp_strlang(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(
                Q(
                    countries__code='DE'
                )
            ).children[0].children[0].children,
            [
                ('countries__code', 'DE'),
            ]
        )

    def test_q_yrel_yfield_ytrans_nsupp_strlang(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(
                Q(
                    countries__name='Deutschland'
                )
            ).children[0].children[0].children,
            [
                ('countries__translations__field', 'name'),
                ('countries__translations__language', 'de'),
                ('countries__translations__text', 'Deutschland'),
            ]
        )

    def test_q_yrel_yfield_ntrans_ysupp_strlang(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(
                Q(
                    countries__code__icontains='DE'
                )
            ).children[0].children[0].children,
            [
                ('countries__code__icontains', 'DE'),
            ]
        )

    def test_q_yrel_yfield_ytrans_ysupp_strlang(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(
                Q(
                    countries__name__icontains='Deutsch'
                )
            ).children[0].children[0].children,
            [
                ('countries__translations__field', 'name'),
                ('countries__translations__language', 'de'),
                ('countries__translations__text__icontains', 'Deutsch'),
            ]
        )

    def test_q_yrelnested_yfield_ntrans_nsupp_strlang(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(
                Q(
                    countries__cities__id=1
                )
            ).children[0].children[0].children,
            [
                ('countries__cities__id', 1),
            ]
        )

    def test_q_yrelnested_yfield_ytrans_nsupp_strlang(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(
                Q(
                    countries__cities__name='Köln'
                )
            ).children[0].children[0].children,
            [
                ('countries__cities__translations__field', 'name'),
                ('countries__cities__translations__language', 'de'),
                ('countries__cities__translations__text', 'Köln'),
            ]
        )

    def test_q_yrelnested_yfield_ntrans_ysupp_strlang(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(
                Q(
                    countries__cities__id__gt=1
                )
            ).children[0].children[0].children,
            [
                ('countries__cities__id__gt', 1),
            ]
        )

    def test_q_yrelnested_yfield_ytrans_ysupp_strlang(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(
                Q(
                    countries__cities__name__icontains='Kö'
                )
            ).children[0].children[0].children,
            [
                ('countries__cities__translations__field', 'name'),
                ('countries__cities__translations__language', 'de'),
                ('countries__cities__translations__text__icontains', 'Kö'),
            ]
        )

    def test_q_nrel_yfield_ntrans_nsupp_strlangdef(self):
        getter = _fetch_translations_query_getter(Continent, 'en')

        self.assertListEqual(
            getter(
                Q(
                    code='EU'
                )
            ).children[0].children[0].children,
            [
                ('code', 'EU'),
            ]
        )

    def test_q_nrel_yfield_ytrans_nsupp_strlangdef(self):
        getter = _fetch_translations_query_getter(Continent, 'en')

        self.assertListEqual(
            getter(
                Q(
                    name='Europa'
                )
            ).children[0].children[0].children,
            [
                ('name', 'Europa'),
            ]
        )

    def test_q_nrel_yfield_ntrans_ysupp_strlangdef(self):
        getter = _fetch_translations_query_getter(Continent, 'en')

        self.assertListEqual(
            getter(
                Q(
                    code__icontains='EU'
                )
            ).children[0].children[0].children,
            [
                ('code__icontains', 'EU'),
            ]
        )

    def test_q_nrel_yfield_ytrans_ysupp_strlangdef(self):
        getter = _fetch_translations_query_getter(Continent, 'en')

        self.assertListEqual(
            getter(
                Q(
                    name__icontains='Europa'
                )
            ).children[0].children[0].children,
            [
                ('name__icontains', 'Europa'),
            ]
        )

    def test_q_yrel_nfield_nsupp_strlangdef(self):
        getter = _fetch_translations_query_getter(Continent, 'en')

        self.assertListEqual(
            getter(
                Q(
                    countries=1
                )
            ).children[0].children[0].children,
            [
                ('countries', 1),
            ]
        )

    def test_q_yrel_nfield_ysupp_strlangdef(self):
        getter = _fetch_translations_query_getter(Continent, 'en')

        self.assertListEqual(
            getter(
                Q(
                    countries__gt=1
                )
            ).children[0].children[0].children,
            [
                ('countries__gt', 1),
            ]
        )

    def test_q_yrel_yfield_ntrans_nsupp_strlangdef(self):
        getter = _fetch_translations_query_getter(Continent, 'en')

        self.assertListEqual(
            getter(
                Q(
                    countries__code='en'
                )
            ).children[0].children[0].children,
            [
                ('countries__code', 'en'),
            ]
        )

    def test_q_yrel_yfield_ytrans_nsupp_strlangdef(self):
        getter = _fetch_translations_query_getter(Continent, 'en')

        self.assertListEqual(
            getter(
                Q(
                    countries__name='Deutschland'
                )
            ).children[0].children[0].children,
            [
                ('countries__name', 'Deutschland'),
            ]
        )

    def test_q_yrel_yfield_ntrans_ysupp_strlangdef(self):
        getter = _fetch_translations_query_getter(Continent, 'en')

        self.assertListEqual(
            getter(
                Q(
                    countries__code__icontains='en'
                )
            ).children[0].children[0].children,
            [
                ('countries__code__icontains', 'en'),
            ]
        )

    def test_q_yrel_yfield_ytrans_ysupp_strlangdef(self):
        getter = _fetch_translations_query_getter(Continent, 'en')

        self.assertListEqual(
            getter(
                Q(
                    countries__name__icontains='Deutsch'
                )
            ).children[0].children[0].children,
            [
                ('countries__name__icontains', 'Deutsch'),
            ]
        )

    def test_q_yrelnested_yfield_ntrans_nsupp_strlangdef(self):
        getter = _fetch_translations_query_getter(Continent, 'en')

        self.assertListEqual(
            getter(
                Q(
                    countries__cities__id=1
                )
            ).children[0].children[0].children,
            [
                ('countries__cities__id', 1),
            ]
        )

    def test_q_yrelnested_yfield_ytrans_nsupp_strlangdef(self):
        getter = _fetch_translations_query_getter(Continent, 'en')

        self.assertListEqual(
            getter(
                Q(
                    countries__cities__name='Köln'
                )
            ).children[0].children[0].children,
            [
                ('countries__cities__name', 'Köln'),
            ]
        )

    def test_q_yrelnested_yfield_ntrans_ysupp_strlangdef(self):
        getter = _fetch_translations_query_getter(Continent, 'en')

        self.assertListEqual(
            getter(
                Q(
                    countries__cities__id__gt=1
                )
            ).children[0].children[0].children,
            [
                ('countries__cities__id__gt', 1),
            ]
        )

    def test_q_yrelnested_yfield_ytrans_ysupp_strlangdef(self):
        getter = _fetch_translations_query_getter(Continent, 'en')

        self.assertListEqual(
            getter(
                Q(
                    countries__cities__name__icontains='Kö'
                )
            ).children[0].children[0].children,
            [
                ('countries__cities__name__icontains', 'Kö'),
            ]
        )

    def test_q_nrel_yfield_ntrans_nsupp_listlang(self):
        getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])

        self.assertListEqual(
            getter(
                Q(
                    code='EU'
                )
            ).children[0].children[0].children,
            [
                ('code', 'EU'),
            ]
        )

    def test_q_nrel_yfield_ytrans_nsupp_listlang(self):
        getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])

        self.assertListEqual(
            getter(
                Q(
                    name='Europa'
                )
            ).children[0].children[0].children,
            [
                ('translations__field', 'name'),
                ('translations__language__in', ['de', 'tr']),
                ('translations__text', 'Europa'),
            ]
        )

    def test_q_nrel_yfield_ntrans_ysupp_listlang(self):
        getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])

        self.assertListEqual(
            getter(
                Q(
                    code__icontains='EU'
                )
            ).children[0].children[0].children,
            [
                ('code__icontains', 'EU'),
            ]
        )

    def test_q_nrel_yfield_ytrans_ysupp_listlang(self):
        getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])

        self.assertListEqual(
            getter(
                Q(
                    name__icontains='Europa'
                )
            ).children[0].children[0].children,
            [
                ('translations__field', 'name'),
                ('translations__language__in', ['de', 'tr']),
                ('translations__text__icontains', 'Europa'),
            ]
        )

    def test_q_yrel_nfield_nsupp_listlang(self):
        getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])

        self.assertListEqual(
            getter(
                Q(
                    countries=1
                )
            ).children[0].children[0].children,
            [
                ('countries', 1),
            ]
        )

    def test_q_yrel_nfield_ysupp_listlang(self):
        getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])

        self.assertListEqual(
            getter(
                Q(
                    countries__gt=1
                )
            ).children[0].children[0].children,
            [
                ('countries__gt', 1),
            ]
        )

    def test_q_yrel_yfield_ntrans_nsupp_listlang(self):
        getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])

        self.assertListEqual(
            getter(
                Q(
                    countries__code='de'
                )
            ).children[0].children[0].children,
            [
                ('countries__code', 'de'),
            ]
        )

    def test_q_yrel_yfield_ytrans_nsupp_listlang(self):
        getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])

        self.assertListEqual(
            getter(
                Q(
                    countries__name='Deutschland'
                )
            ).children[0].children[0].children,
            [
                ('countries__translations__field', 'name'),
                ('countries__translations__language__in', ['de', 'tr']),
                ('countries__translations__text', 'Deutschland'),
            ]
        )

    def test_q_yrel_yfield_ntrans_ysupp_listlang(self):
        getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])

        self.assertListEqual(
            getter(
                Q(
                    countries__code__icontains=['de', 'tr']
                )
            ).children[0].children[0].children,
            [
                ('countries__code__icontains', ['de', 'tr']),
            ]
        )

    def test_q_yrel_yfield_ytrans_ysupp_listlang(self):
        getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])

        self.assertListEqual(
            getter(
                Q(
                    countries__name__icontains='Deutsch'
                )
            ).children[0].children[0].children,
            [
                ('countries__translations__field', 'name'),
                ('countries__translations__language__in', ['de', 'tr']),
                ('countries__translations__text__icontains', 'Deutsch'),
            ]
        )

    def test_q_yrelnested_yfield_ntrans_nsupp_listlang(self):
        getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])

        self.assertListEqual(
            getter(
                Q(
                    countries__cities__id=1
                )
            ).children[0].children[0].children,
            [
                ('countries__cities__id', 1),
            ]
        )

    def test_q_yrelnested_yfield_ytrans_nsupp_listlang(self):
        getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])

        self.assertListEqual(
            getter(
                Q(
                    countries__cities__name='Köln'
                )
            ).children[0].children[0].children,
            [
                ('countries__cities__translations__field', 'name'),
                (
                    'countries__cities__translations__language__in',
                    ['de', 'tr']
                ),
                ('countries__cities__translations__text', 'Köln'),
            ]
        )

    def test_q_yrelnested_yfield_ntrans_ysupp_listlang(self):
        getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])

        self.assertListEqual(
            getter(
                Q(
                    countries__cities__id__gt=1
                )
            ).children[0].children[0].children,
            [
                ('countries__cities__id__gt', 1),
            ]
        )

    def test_q_yrelnested_yfield_ytrans_ysupp_listlang(self):
        getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])

        self.assertListEqual(
            getter(
                Q(
                    countries__cities__name__icontains='Kö'
                )
            ).children[0].children[0].children,
            [
                ('countries__cities__translations__field', 'name'),
                (
                    'countries__cities__translations__language__in',
                    ['de', 'tr']
                ),
                ('countries__cities__translations__text__icontains', 'Kö'),
            ]
        )

    def test_q_nrel_yfield_ntrans_nsupp_listlangdef(self):
        getter = _fetch_translations_query_getter(Continent, ['en', 'de'])

        self.assertListEqual(
            getter(
                Q(
                    code='EU'
                )
            ).children[0].children[0].children,
            [
                ('code', 'EU'),
            ]
        )

    def test_q_nrel_yfield_ytrans_nsupp_listlangdef(self):
        getter = _fetch_translations_query_getter(Continent, ['en', 'de'])

        self.assertListEqual(
            getter(
                Q(
                    name='Europa'
                )
            ).children[0].children[0].children,
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
            getter(
                Q(
                    code__icontains='EU'
                )
            ).children[0].children[0].children,
            [
                ('code__icontains', 'EU'),
            ]
        )

    def test_q_nrel_yfield_ytrans_ysupp_listlangdef(self):
        getter = _fetch_translations_query_getter(Continent, ['en', 'de'])

        self.assertListEqual(
            getter(
                Q(
                    name__icontains='Europa'
                )
            ).children[0].children[0].children,
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
            getter(
                Q(
                    countries=1
                )
            ).children[0].children[0].children,
            [
                ('countries', 1),
            ]
        )

    def test_q_yrel_nfield_ysupp_listlangdef(self):
        getter = _fetch_translations_query_getter(Continent, ['en', 'de'])

        self.assertListEqual(
            getter(
                Q(
                    countries__gt=1
                )
            ).children[0].children[0].children,
            [
                ('countries__gt', 1),
            ]
        )

    def test_q_yrel_yfield_ntrans_nsupp_listlangdef(self):
        getter = _fetch_translations_query_getter(Continent, ['en', 'de'])

        self.assertListEqual(
            getter(
                Q(
                    countries__code=['de']
                )
            ).children[0].children[0].children,
            [
                ('countries__code', ['de']),
            ]
        )

    def test_q_yrel_yfield_ytrans_nsupp_listlangdef(self):
        getter = _fetch_translations_query_getter(Continent, ['en', 'de'])

        self.assertListEqual(
            getter(
                Q(
                    countries__name='Deutschland'
                )
            ).children[0].children[0].children,
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
            getter(
                Q(
                    countries__code__icontains=['de']
                )
            ).children[0].children[0].children,
            [
                ('countries__code__icontains', ['de']),
            ]
        )

    def test_q_yrel_yfield_ytrans_ysupp_listlangdef(self):
        getter = _fetch_translations_query_getter(Continent, ['en', 'de'])

        self.assertListEqual(
            getter(
                Q(
                    countries__name__icontains='Deutsch'
                )
            ).children[0].children[0].children,
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
            getter(
                Q(
                    countries__cities__id=1
                )
            ).children[0].children[0].children,
            [
                ('countries__cities__id', 1),
            ]
        )

    def test_q_yrelnested_yfield_ytrans_nsupp_listlangdef(self):
        getter = _fetch_translations_query_getter(Continent, ['en', 'de'])

        self.assertListEqual(
            getter(
                Q(
                    countries__cities__name='Köln'
                )
            ).children[0].children[0].children,
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
            getter(
                Q(
                    countries__cities__id__gt=1
                )
            ).children[0].children[0].children,
            [
                ('countries__cities__id__gt', 1),
            ]
        )

    def test_q_yrelnested_yfield_ytrans_ysupp_listlangdef(self):
        getter = _fetch_translations_query_getter(Continent, ['en', 'de'])

        self.assertListEqual(
            getter(
                Q(
                    countries__cities__name__icontains='Kö'
                )
            ).children[0].children[0].children,
            [
                ('countries__cities__name__icontains', 'Kö'),
                Q(
                    ('countries__cities__translations__field', 'name'),
                    ('countries__cities__translations__language__in', ['de']),
                    ('countries__cities__translations__text__icontains', 'Kö'),
                )
            ]
        )

    def test_tq_nrel_yfield_ntrans_nsupp_strlang(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(
                TQ(
                    code='EU',
                    )('de'
                )
            ).children[0].children[0].children,
            [
                ('code', 'EU'),
            ]
        )

    def test_tq_nrel_yfield_ytrans_nsupp_strlang(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(
                TQ(
                    name='Europa',
                    )('de'
                )
            ).children[0].children[0].children,
            [
                ('translations__field', 'name'),
                ('translations__language', 'de'),
                ('translations__text', 'Europa'),
            ]
        )

    def test_tq_nrel_yfield_ntrans_ysupp_strlang(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(
                TQ(
                    code__icontains='EU',
                    )('de'
                )
            ).children[0].children[0].children,
            [
                ('code__icontains', 'EU'),
            ]
        )

    def test_tq_nrel_yfield_ytrans_ysupp_strlang(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(
                TQ(
                    name__icontains='Europa',
                    )('de'
                )
            ).children[0].children[0].children,
            [
                ('translations__field', 'name'),
                ('translations__language', 'de'),
                ('translations__text__icontains', 'Europa'),
            ]
        )

    def test_tq_yrel_nfield_nsupp_strlang(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(
                TQ(
                    countries=1,
                    )('de'
                )
            ).children[0].children[0].children,
            [
                ('countries', 1),
            ]
        )

    def test_tq_yrel_nfield_ysupp_strlang(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(
                TQ(
                    countries__gt=1,
                    )('de'
                )
            ).children[0].children[0].children,
            [
                ('countries__gt', 1),
            ]
        )

    def test_tq_yrel_yfield_ntrans_nsupp_strlang(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(
                TQ(
                    countries__code='DE',
                    )('de'
                )
            ).children[0].children[0].children,
            [
                ('countries__code', 'DE'),
            ]
        )

    def test_tq_yrel_yfield_ytrans_nsupp_strlang(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(
                TQ(
                    countries__name='Deutschland',
                    )('de'
                )
            ).children[0].children[0].children,
            [
                ('countries__translations__field', 'name'),
                ('countries__translations__language', 'de'),
                ('countries__translations__text', 'Deutschland'),
            ]
        )

    def test_tq_yrel_yfield_ntrans_ysupp_strlang(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(
                TQ(
                    countries__code__icontains='DE',
                    )('de'
                )
            ).children[0].children[0].children,
            [
                ('countries__code__icontains', 'DE'),
            ]
        )

    def test_tq_yrel_yfield_ytrans_ysupp_strlang(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(
                TQ(
                    countries__name__icontains='Deutsch',
                    )('de'
                )
            ).children[0].children[0].children,
            [
                ('countries__translations__field', 'name'),
                ('countries__translations__language', 'de'),
                ('countries__translations__text__icontains', 'Deutsch'),
            ]
        )

    def test_tq_yrelnested_yfield_ntrans_nsupp_strlang(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(
                TQ(
                    countries__cities__id=1,
                    )('de'
                )
            ).children[0].children[0].children,
            [
                ('countries__cities__id', 1),
            ]
        )

    def test_tq_yrelnested_yfield_ytrans_nsupp_strlang(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(
                TQ(
                    countries__cities__name='Köln',
                    )('de'
                )
            ).children[0].children[0].children,
            [
                ('countries__cities__translations__field', 'name'),
                ('countries__cities__translations__language', 'de'),
                ('countries__cities__translations__text', 'Köln'),
            ]
        )

    def test_tq_yrelnested_yfield_ntrans_ysupp_strlang(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(
                TQ(
                    countries__cities__id__gt=1,
                    )('de'
                )
            ).children[0].children[0].children,
            [
                ('countries__cities__id__gt', 1),
            ]
        )

    def test_tq_yrelnested_yfield_ytrans_ysupp_strlang(self):
        getter = _fetch_translations_query_getter(Continent, 'de')

        self.assertListEqual(
            getter(
                TQ(
                    countries__cities__name__icontains='Kö',
                    )('de'
                )
            ).children[0].children[0].children,
            [
                ('countries__cities__translations__field', 'name'),
                ('countries__cities__translations__language', 'de'),
                ('countries__cities__translations__text__icontains', 'Kö'),
            ]
        )

    def test_tq_nrel_yfield_ntrans_nsupp_strlangdef(self):
        getter = _fetch_translations_query_getter(Continent, 'en')

        self.assertListEqual(
            getter(
                TQ(
                    code='EU',
                    )('en'
                )
            ).children[0].children[0].children,
            [
                ('code', 'EU'),
            ]
        )

    def test_tq_nrel_yfield_ytrans_nsupp_strlangdef(self):
        getter = _fetch_translations_query_getter(Continent, 'en')

        self.assertListEqual(
            getter(
                TQ(
                    name='Europa',
                    )('en'
                )
            ).children[0].children[0].children,
            [
                ('name', 'Europa'),
            ]
        )

    def test_tq_nrel_yfield_ntrans_ysupp_strlangdef(self):
        getter = _fetch_translations_query_getter(Continent, 'en')

        self.assertListEqual(
            getter(
                TQ(
                    code__icontains='EU',
                    )('en'
                )
            ).children[0].children[0].children,
            [
                ('code__icontains', 'EU'),
            ]
        )

    def test_tq_nrel_yfield_ytrans_ysupp_strlangdef(self):
        getter = _fetch_translations_query_getter(Continent, 'en')

        self.assertListEqual(
            getter(
                TQ(
                    name__icontains='Europa',
                    )('en'
                )
            ).children[0].children[0].children,
            [
                ('name__icontains', 'Europa'),
            ]
        )

    def test_tq_yrel_nfield_nsupp_strlangdef(self):
        getter = _fetch_translations_query_getter(Continent, 'en')

        self.assertListEqual(
            getter(
                TQ(
                    countries=1,
                    )('en'
                )
            ).children[0].children[0].children,
            [
                ('countries', 1),
            ]
        )

    def test_tq_yrel_nfield_ysupp_strlangdef(self):
        getter = _fetch_translations_query_getter(Continent, 'en')

        self.assertListEqual(
            getter(
                TQ(
                    countries__gt=1,
                    )('en'
                )
            ).children[0].children[0].children,
            [
                ('countries__gt', 1),
            ]
        )

    def test_tq_yrel_yfield_ntrans_nsupp_strlangdef(self):
        getter = _fetch_translations_query_getter(Continent, 'en')

        self.assertListEqual(
            getter(
                TQ(
                    countries__code='en',
                    )('en'
                )
            ).children[0].children[0].children,
            [
                ('countries__code', 'en'),
            ]
        )

    def test_tq_yrel_yfield_ytrans_nsupp_strlangdef(self):
        getter = _fetch_translations_query_getter(Continent, 'en')

        self.assertListEqual(
            getter(
                TQ(
                    countries__name='Deutschland',
                    )('en'
                )
            ).children[0].children[0].children,
            [
                ('countries__name', 'Deutschland'),
            ]
        )

    def test_tq_yrel_yfield_ntrans_ysupp_strlangdef(self):
        getter = _fetch_translations_query_getter(Continent, 'en')

        self.assertListEqual(
            getter(
                TQ(
                    countries__code__icontains='en',
                    )('en'
                )
            ).children[0].children[0].children,
            [
                ('countries__code__icontains', 'en'),
            ]
        )

    def test_tq_yrel_yfield_ytrans_ysupp_strlangdef(self):
        getter = _fetch_translations_query_getter(Continent, 'en')

        self.assertListEqual(
            getter(
                TQ(
                    countries__name__icontains='Deutsch',
                    )('en'
                )
            ).children[0].children[0].children,
            [
                ('countries__name__icontains', 'Deutsch'),
            ]
        )

    def test_tq_yrelnested_yfield_ntrans_nsupp_strlangdef(self):
        getter = _fetch_translations_query_getter(Continent, 'en')

        self.assertListEqual(
            getter(
                TQ(
                    countries__cities__id=1,
                    )('en'
                )
            ).children[0].children[0].children,
            [
                ('countries__cities__id', 1),
            ]
        )

    def test_tq_yrelnested_yfield_ytrans_nsupp_strlangdef(self):
        getter = _fetch_translations_query_getter(Continent, 'en')

        self.assertListEqual(
            getter(
                TQ(
                    countries__cities__name='Köln',
                    )('en'
                )
            ).children[0].children[0].children,
            [
                ('countries__cities__name', 'Köln'),
            ]
        )

    def test_tq_yrelnested_yfield_ntrans_ysupp_strlangdef(self):
        getter = _fetch_translations_query_getter(Continent, 'en')

        self.assertListEqual(
            getter(
                TQ(
                    countries__cities__id__gt=1,
                    )('en'
                )
            ).children[0].children[0].children,
            [
                ('countries__cities__id__gt', 1),
            ]
        )

    def test_tq_yrelnested_yfield_ytrans_ysupp_strlangdef(self):
        getter = _fetch_translations_query_getter(Continent, 'en')

        self.assertListEqual(
            getter(
                TQ(
                    countries__cities__name__icontains='Kö',
                    )('en'
                )
            ).children[0].children[0].children,
            [
                ('countries__cities__name__icontains', 'Kö'),
            ]
        )

    def test_tq_nrel_yfield_ntrans_nsupp_listlang(self):
        getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])

        self.assertListEqual(
            getter(
                TQ(
                    code='EU',
                    )(['de', 'tr']
                )
            ).children[0].children[0].children,
            [
                ('code', 'EU'),
            ]
        )

    def test_tq_nrel_yfield_ytrans_nsupp_listlang(self):
        getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])

        self.assertListEqual(
            getter(
                TQ(
                    name='Europa',
                    )(['de', 'tr']
                )
            ).children[0].children[0].children,
            [
                ('translations__field', 'name'),
                ('translations__language__in', ['de', 'tr']),
                ('translations__text', 'Europa'),
            ]
        )

    def test_tq_nrel_yfield_ntrans_ysupp_listlang(self):
        getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])

        self.assertListEqual(
            getter(
                TQ(
                    code__icontains='EU',
                    )(['de', 'tr']
                )
            ).children[0].children[0].children,
            [
                ('code__icontains', 'EU'),
            ]
        )

    def test_tq_nrel_yfield_ytrans_ysupp_listlang(self):
        getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])

        self.assertListEqual(
            getter(
                TQ(
                    name__icontains='Europa',
                    )(['de', 'tr']
                )
            ).children[0].children[0].children,
            [
                ('translations__field', 'name'),
                ('translations__language__in', ['de', 'tr']),
                ('translations__text__icontains', 'Europa'),
            ]
        )

    def test_tq_yrel_nfield_nsupp_listlang(self):
        getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])

        self.assertListEqual(
            getter(
                TQ(
                    countries=1,
                    )(['de', 'tr']
                )
            ).children[0].children[0].children,
            [
                ('countries', 1),
            ]
        )

    def test_tq_yrel_nfield_ysupp_listlang(self):
        getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])

        self.assertListEqual(
            getter(
                TQ(
                    countries__gt=1,
                    )(['de', 'tr']
                )
            ).children[0].children[0].children,
            [
                ('countries__gt', 1),
            ]
        )

    def test_tq_yrel_yfield_ntrans_nsupp_listlang(self):
        getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])

        self.assertListEqual(
            getter(
                TQ(
                    countries__code='de',
                    )(['de', 'tr']
                )
            ).children[0].children[0].children,
            [
                ('countries__code', 'de'),
            ]
        )

    def test_tq_yrel_yfield_ytrans_nsupp_listlang(self):
        getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])

        self.assertListEqual(
            getter(
                TQ(
                    countries__name='Deutschland',
                    )(['de', 'tr']
                )
            ).children[0].children[0].children,
            [
                ('countries__translations__field', 'name'),
                ('countries__translations__language__in', ['de', 'tr']),
                ('countries__translations__text', 'Deutschland'),
            ]
        )

    def test_tq_yrel_yfield_ntrans_ysupp_listlang(self):
        getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])

        self.assertListEqual(
            getter(
                TQ(
                    countries__code__icontains=['de', 'tr'],
                    )(['de', 'tr']
                )
            ).children[0].children[0].children,
            [
                ('countries__code__icontains', ['de', 'tr']),
            ]
        )

    def test_tq_yrel_yfield_ytrans_ysupp_listlang(self):
        getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])

        self.assertListEqual(
            getter(
                TQ(
                    countries__name__icontains='Deutsch',
                    )(['de', 'tr']
                )
            ).children[0].children[0].children,
            [
                ('countries__translations__field', 'name'),
                ('countries__translations__language__in', ['de', 'tr']),
                ('countries__translations__text__icontains', 'Deutsch'),
            ]
        )

    def test_tq_yrelnested_yfield_ntrans_nsupp_listlang(self):
        getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])

        self.assertListEqual(
            getter(
                TQ(
                    countries__cities__id=1,
                    )(['de', 'tr']
                )
            ).children[0].children[0].children,
            [
                ('countries__cities__id', 1),
            ]
        )

    def test_tq_yrelnested_yfield_ytrans_nsupp_listlang(self):
        getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])

        self.assertListEqual(
            getter(
                TQ(
                    countries__cities__name='Köln',
                    )(['de', 'tr']
                )
            ).children[0].children[0].children,
            [
                ('countries__cities__translations__field', 'name'),
                (
                    'countries__cities__translations__language__in',
                    ['de', 'tr']
                ),
                ('countries__cities__translations__text', 'Köln'),
            ]
        )

    def test_tq_yrelnested_yfield_ntrans_ysupp_listlang(self):
        getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])

        self.assertListEqual(
            getter(
                TQ(
                    countries__cities__id__gt=1,
                    )(['de', 'tr']
                )
            ).children[0].children[0].children,
            [
                ('countries__cities__id__gt', 1),
            ]
        )

    def test_tq_yrelnested_yfield_ytrans_ysupp_listlang(self):
        getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])

        self.assertListEqual(
            getter(
                TQ(
                    countries__cities__name__icontains='Kö',
                    )(['de', 'tr']
                )
            ).children[0].children[0].children,
            [
                ('countries__cities__translations__field', 'name'),
                (
                    'countries__cities__translations__language__in',
                    ['de', 'tr']
                ),
                ('countries__cities__translations__text__icontains', 'Kö'),
            ]
        )

    def test_tq_nrel_yfield_ntrans_nsupp_listlangdef(self):
        getter = _fetch_translations_query_getter(Continent, ['en', 'de'])

        self.assertListEqual(
            getter(
                TQ(
                    code='EU',
                    )(['en', 'de']
                )
            ).children[0].children[0].children,
            [
                ('code', 'EU'),
            ]
        )

    def test_tq_nrel_yfield_ytrans_nsupp_listlangdef(self):
        getter = _fetch_translations_query_getter(Continent, ['en', 'de'])

        self.assertListEqual(
            getter(
                TQ(
                    name='Europa',
                    )(['en', 'de']
                )
            ).children[0].children[0].children,
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
            getter(
                TQ(
                    code__icontains='EU',
                    )(['en', 'de']
                )
            ).children[0].children[0].children,
            [
                ('code__icontains', 'EU'),
            ]
        )

    def test_tq_nrel_yfield_ytrans_ysupp_listlangdef(self):
        getter = _fetch_translations_query_getter(Continent, ['en', 'de'])

        self.assertListEqual(
            getter(
                TQ(
                    name__icontains='Europa',
                    )(['en', 'de']
                )
            ).children[0].children[0].children,
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
            getter(
                TQ(
                    countries=1,
                    )(['en', 'de']
                    )
                ).children[0].children[0].children,
            [
                ('countries', 1),
            ]
        )

    def test_tq_yrel_nfield_ysupp_listlangdef(self):
        getter = _fetch_translations_query_getter(Continent, ['en', 'de'])

        self.assertListEqual(
            getter(
                TQ(
                    countries__gt=1,
                    )(['en', 'de']
                )
            ).children[0].children[0].children,
            [
                ('countries__gt', 1),
            ]
        )

    def test_tq_yrel_yfield_ntrans_nsupp_listlangdef(self):
        getter = _fetch_translations_query_getter(Continent, ['en', 'de'])

        self.assertListEqual(
            getter(
                TQ(
                    countries__code=['de'],
                    )(['en', 'de']
                )
            ).children[0].children[0].children,
            [
                ('countries__code', ['de']),
            ]
        )

    def test_tq_yrel_yfield_ytrans_nsupp_listlangdef(self):
        getter = _fetch_translations_query_getter(Continent, ['en', 'de'])

        self.assertListEqual(
            getter(
                TQ(
                    countries__name='Deutschland',
                    )(['en', 'de']
                )
            ).children[0].children[0].children,
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
            getter(
                TQ(
                    countries__code__icontains=['de'],
                    )(['en', 'de']
                )
            ).children[0].children[0].children,
            [
                ('countries__code__icontains', ['de']),
            ]
        )

    def test_tq_yrel_yfield_ytrans_ysupp_listlangdef(self):
        getter = _fetch_translations_query_getter(Continent, ['en', 'de'])

        self.assertListEqual(
            getter(
                TQ(
                    countries__name__icontains='Deutsch',
                    )(['en', 'de']
                )
            ).children[0].children[0].children,
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
            getter(
                TQ(
                    countries__cities__id=1,
                    )(['en', 'de']
                )
            ).children[0].children[0].children,
            [
                ('countries__cities__id', 1),
            ]
        )

    def test_tq_yrelnested_yfield_ytrans_nsupp_listlangdef(self):
        getter = _fetch_translations_query_getter(Continent, ['en', 'de'])

        self.assertListEqual(
            getter(
                TQ(
                    countries__cities__name='Köln',
                    )(['en', 'de']
                )
            ).children[0].children[0].children,
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
            getter(
                TQ(
                    countries__cities__id__gt=1,
                    )(['en', 'de']
                )
            ).children[0].children[0].children,
            [
                ('countries__cities__id__gt', 1),
            ]
        )

    def test_tq_yrelnested_yfield_ytrans_ysupp_listlangdef(self):
        getter = _fetch_translations_query_getter(Continent, ['en', 'de'])

        self.assertListEqual(
            getter(
                TQ(
                    countries__cities__name__icontains='Kö',
                    )(['en', 'de']
                )
            ).children[0].children[0].children,
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
        tq = TQ()

        self.assertIs(hasattr(tq, 'lang'), True)

    @override(language='de', deactivate=True)
    def test_call_no_lang(self):
        tq = TQ()()

        self.assertEqual(tq.lang, 'de')

    def test_call_str_lang(self):
        tq = TQ()('de')

        self.assertEqual(tq.lang, 'de')

    def test_call_str_lang_invalid(self):
        with self.assertRaises(ValueError) as error:
            TQ()('xx')

        self.assertEqual(
            error.exception.args[0],
            '`xx` is not a supported language.'
        )

    def test_call_list_lang(self):
        tq = TQ()(['de', 'tr'])

        self.assertEqual(tq.lang, ['de', 'tr'])

    def test_call_list_lang_invalid(self):
        with self.assertRaises(ValueError) as error:
            TQ()(['de', 'tr', 'xx'])

        self.assertEqual(
            error.exception.args[0],
            '`xx` is not a supported language.'
        )

    def test_deepcopy_lang(self):
        tq = TQ()('de')
        tq_copy = copy.deepcopy(tq)

        self.assertEqual(tq_copy.lang, 'de')

    def test_deepcopy_type(self):
        tq = TQ()('de')
        tq_copy = copy.deepcopy(tq)

        self.assertIs(type(tq_copy), TQ)

    def test_combine_self_and_wrong_type(self):
        tq = TQ()

        with self.assertRaises(TypeError) as error:
            tq & 2

        self.assertEqual(
            error.exception.args[0],
            2
        )

    def test_combine_self_or_wrong_type(self):
        tq = TQ()

        with self.assertRaises(TypeError) as error:
            tq | 2

        self.assertEqual(
            error.exception.args[0],
            2
        )

    def test_combine_self_and_empty_other_q(self):
        tq = TQ(countries__name='Deutschland')
        other = Q()

        self.assertEqual(
            tq & other,
            tq
        )

    def test_combine_self_or_empty_other_q(self):
        tq = TQ(countries__name='Deutschland')
        other = Q()

        self.assertEqual(
            tq | other,
            tq
        )

    def test_combine_self_and_empty_other_tq(self):
        tq = TQ(countries__name='Deutschland')
        other = TQ()

        self.assertEqual(
            tq & other,
            tq
        )

    def test_combine_self_or_empty_other_tq(self):
        tq = TQ(countries__name='Deutschland')
        other = TQ()

        self.assertEqual(
            tq | other,
            tq
        )

    def test_combine_empty_self_and_other_q(self):
        tq = TQ()
        other = Q(countries__name='Deutschland')

        self.assertEqual(
            tq & other,
            other
        )

    def test_combine_empty_self_or_other_q(self):
        tq = TQ()
        other = Q(countries__name='Deutschland')

        self.assertEqual(
            tq | other,
            other
        )

    def test_combine_empty_self_and_other_tq(self):
        tq = TQ()
        other = TQ(countries__name='Deutschland')

        self.assertEqual(
            tq & other,
            other
        )

    def test_combine_empty_self_or_other_tq(self):
        tq = TQ()
        other = TQ(countries__name='Deutschland')

        self.assertEqual(
            tq | other,
            other
        )

    def test_combine_self_and_other_q(self):
        tq = TQ(countries__name='Deutschland')
        other = Q(countries__name='Germany')

        self.assertEqual(
            tq & other,
            Q(tq, other, _connector=Q.AND)
        )

    def test_combine_self_or_other_q(self):
        tq = TQ(countries__name='Deutschland')
        other = Q(countries__name='Germany')

        self.assertEqual(
            tq | other,
            Q(tq, other, _connector=Q.OR)
        )

    def test_combine_self_and_other_tq(self):
        tq = TQ(countries__name='Deutschland')
        other = TQ(countries__name='Germany')

        self.assertEqual(
            tq & other,
            Q(tq, other, _connector=Q.AND)
        )

    def test_combine_self_or_other_tq(self):
        tq = TQ(countries__name='Deutschland')
        other = TQ(countries__name='Germany')

        self.assertEqual(
            tq | other,
            Q(tq, other, _connector=Q.OR)
        )
