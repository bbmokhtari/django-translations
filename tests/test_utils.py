from django.test import TestCase, override_settings
from django.core.exceptions import FieldDoesNotExist
from django.contrib.contenttypes.models import ContentType

from translations.utils import _get_standard_language, \
    _get_translation_language_choices, \
    _get_reverse_relation, _get_dissected_lookup, \
    _get_translations_lookup_query, \
    _get_relations_hierarchy, _get_entity_details, \
    _get_instance_groups, _get_translations

from sample.models import Continent, Country, City

from tests.sample import create_samples


class GetStandardLanguageTest(TestCase):
    """Tests for `_get_standard_language`."""

    @override_settings(LANGUAGE_CODE='de')
    def test_active_unaccented_language(self):
        self.assertEqual(
            _get_standard_language(),
            'de'
        )

    def test_custom_unaccented_language(self):
        self.assertEqual(
            _get_standard_language('de'),
            'de'
        )

    @override_settings(LANGUAGE_CODE='de-at')
    def test_active_nonexisting_accented_language(self):
        self.assertEqual(
            _get_standard_language(),
            'de'
        )

    def test_custom_nonexisting_accented_language(self):
        self.assertEqual(
            _get_standard_language('de-at'),
            'de'
        )

    @override_settings(LANGUAGE_CODE='en-gb')
    def test_active_existing_accented_language(self):
        self.assertEqual(
            _get_standard_language(),
            'en-gb'
        )

    def test_custom_existing_accented_language(self):
        self.assertEqual(
            _get_standard_language('en-gb'),
            'en-gb'
        )

    def test_invalid_language(self):
        with self.assertRaises(ValueError) as error:
            _get_standard_language('xx')

        self.assertEqual(
            error.exception.args[0],
            'The language code `xx` is not supported.'
        )


class GetTranslationLanguageChoicesTest(TestCase):
    """Tests for `_get_translation_language_choices`."""

    @override_settings(LANGUAGE_CODE='en-us')
    def test_nonexisting_accented_default_language_code(self):
        self.assertListEqual(
            _get_translation_language_choices(),
            [
                (None, '---------'),
                ('en-gb', 'English (Great Britain)'),
                ('de', 'German'),
                ('tr', 'Turkish')
            ]
        )

    @override_settings(LANGUAGE_CODE='en-gb')
    def test_existing_accented_default_language_code(self):
        self.assertListEqual(
            _get_translation_language_choices(),
            [
                (None, '---------'),
                ('en', 'English'),
                ('de', 'German'),
                ('tr', 'Turkish')
            ]
        )

    @override_settings(LANGUAGE_CODE='xx')
    def test_invalid_default_language_code(self):
        with self.assertRaises(ValueError) as error:
            _get_translation_language_choices()

        self.assertEqual(
            error.exception.args[0],
            'The language code `xx` is not supported.'
        )


class GetReverseRelationTest(TestCase):
    """Tests for `_get_reverse_relation`."""

    def test_simple_relation(self):
        self.assertEqual(
            _get_reverse_relation(Continent, 'countries'),
            'continent'
        )

    def test_simple_reverse_relation(self):
        self.assertEqual(
            _get_reverse_relation(Country, 'continent'),
            'countries'
        )

    def test_nested_relation(self):
        self.assertEqual(
            _get_reverse_relation(Continent, 'countries__cities'),
            'country__continent'
        )

    def test_nested_reverse_relation(self):
        self.assertEqual(
            _get_reverse_relation(City, 'country__continent'),
            'countries__cities'
        )

    def test_empty_relation(self):
        with self.assertRaises(FieldDoesNotExist) as error:
            _get_reverse_relation(Continent, '')

        self.assertEqual(
            error.exception.args[0],
            "Continent has no field named ''"
        )

    def test_invalid_simple_relation(self):
        with self.assertRaises(FieldDoesNotExist) as error:
            _get_reverse_relation(Continent, 'wrong')

        self.assertEqual(
            error.exception.args[0],
            "Continent has no field named 'wrong'"
        )

    def test_invalid_nested_relation(self):
        with self.assertRaises(FieldDoesNotExist) as error:
            _get_reverse_relation(Continent, 'countries__wrong')

        self.assertEqual(
            error.exception.args[0],
            "Country has no field named 'wrong'"
        )


class GetDissectedLookupTest(TestCase):
    """Tests for `_get_dissected_lookup`."""

    def test_no_rel_with_field_not_translatable_no_lookup(self):
        self.assertDictEqual(
            _get_dissected_lookup(Continent, 'code'),
            {
                'relation': [],
                'field': 'code',
                'lookup': '',
                'translatable': False,
            }
        )

    def test_no_rel_with_field_translatable_no_lookup(self):
        self.assertDictEqual(
            _get_dissected_lookup(Continent, 'name'),
            {
                'relation': [],
                'field': 'name',
                'lookup': '',
                'translatable': True,
            }
        )

    def test_no_rel_with_field_not_translatable_with_lookup(self):
        self.assertDictEqual(
            _get_dissected_lookup(Continent, 'code__icontains'),
            {
                'relation': [],
                'field': 'code',
                'lookup': 'icontains',
                'translatable': False,
            }
        )

    def test_no_rel_with_field_translatable_with_lookup(self):
        self.assertDictEqual(
            _get_dissected_lookup(Continent, 'name__icontains'),
            {
                'relation': [],
                'field': 'name',
                'lookup': 'icontains',
                'translatable': True,
            }
        )

    def test_with_rel_no_field_no_lookup(self):
        self.assertDictEqual(
            _get_dissected_lookup(Continent, 'countries'),
            {
                'relation': ['countries'],
                'field': '',
                'lookup': '',
                'translatable': False,
            }
        )

    def test_with_rel_no_field_with_lookup(self):
        self.assertDictEqual(
            _get_dissected_lookup(Continent, 'countries__gt'),
            {
                'relation': ['countries'],
                'field': '',
                'lookup': 'gt',
                'translatable': False,
            }
        )

    def test_with_rel_with_field_not_translatable_no_lookup(self):
        self.assertDictEqual(
            _get_dissected_lookup(Continent, 'countries__code'),
            {
                'relation': ['countries'],
                'field': 'code',
                'lookup': '',
                'translatable': False,
            }
        )

    def test_with_rel_with_field_translatable_no_lookup(self):
        self.assertDictEqual(
            _get_dissected_lookup(Continent, 'countries__name'),
            {
                'relation': ['countries'],
                'field': 'name',
                'lookup': '',
                'translatable': True,
            }
        )

    def test_with_rel_with_field_not_translatable_with_lookup(self):
        self.assertDictEqual(
            _get_dissected_lookup(Continent, 'countries__code__icontains'),
            {
                'relation': ['countries'],
                'field': 'code',
                'lookup': 'icontains',
                'translatable': False,
            }
        )

    def test_with_rel_with_field_translatable_with_lookup(self):
        self.assertDictEqual(
            _get_dissected_lookup(Continent, 'countries__name__icontains'),
            {
                'relation': ['countries'],
                'field': 'name',
                'lookup': 'icontains',
                'translatable': True,
            }
        )

    def test_with_nested_rel_with_field_not_translatable_no_lookup(self):
        self.assertDictEqual(
            _get_dissected_lookup(Continent, 'countries__cities__id'),
            {
                'relation': ['countries', 'cities'],
                'field': 'id',
                'lookup': '',
                'translatable': False,
            }
        )

    def test_with_nested_rel_with_field_translatable_no_lookup(self):
        self.assertDictEqual(
            _get_dissected_lookup(Continent, 'countries__cities__name'),
            {
                'relation': ['countries', 'cities'],
                'field': 'name',
                'lookup': '',
                'translatable': True,
            }
        )

    def test_with_nested_rel_with_field_not_translatable_with_lookup(self):
        self.assertDictEqual(
            _get_dissected_lookup(Continent, 'countries__cities__id__gt'),
            {
                'relation': ['countries', 'cities'],
                'field': 'id',
                'lookup': 'gt',
                'translatable': False,
            }
        )

    def test_with_nested_rel_with_field_translatable_with_lookup(self):
        self.assertDictEqual(
            _get_dissected_lookup(
                Continent,
                'countries__cities__name__icontains'
            ),
            {
                'relation': ['countries', 'cities'],
                'field': 'name',
                'lookup': 'icontains',
                'translatable': True,
            }
        )


class GetTranslationsLookupQueryTest(TestCase):
    """Tests for `_get_translations_lookup_query`."""

    def test_no_rel_with_field_not_translatable_no_lookup(self):
        self.assertDictEqual(
            dict(_get_translations_lookup_query(
                Continent, 'code', 'EU', 'de'
            ).children),
            {
                'code': 'EU',
            }
        )

    def test_no_rel_with_field_translatable_no_lookup(self):
        self.assertDictEqual(
            dict(_get_translations_lookup_query(
                Continent, 'name', 'Europa', 'de'
            ).children),
            {
                'translations__field': 'name',
                'translations__language': 'de',
                'translations__text': 'Europa',
            }
        )

    def test_no_rel_with_field_not_translatable_with_lookup(self):
        self.assertDictEqual(
            dict(_get_translations_lookup_query(
                Continent, 'code__icontains', 'EU', 'de'
            ).children),
            {
                'code__icontains': 'EU',
            },
        )

    def test_no_rel_with_field_translatable_with_lookup(self):
        self.assertDictEqual(
            dict(_get_translations_lookup_query(
                Continent, 'name__icontains', 'Europa', 'de'
            ).children),
            {
                'translations__field': 'name',
                'translations__language': 'de',
                'translations__text__icontains': 'Europa',
            }
        )

    def test_with_rel_no_field_no_lookup(self):
        self.assertDictEqual(
            dict(_get_translations_lookup_query(
                Continent, 'countries', 1, 'de'
            ).children),
            {
                'countries': 1,
            }
        )

    def test_with_rel_no_field_with_lookup(self):
        self.assertDictEqual(
            dict(_get_translations_lookup_query(
                Continent, 'countries__gt', 1, 'de'
            ).children),
            {
                'countries__gt': 1,
            }
        )

    def test_with_rel_with_field_not_translatable_no_lookup(self):
        self.assertDictEqual(
            dict(_get_translations_lookup_query(
                Continent, 'countries__code', 'DE', 'de'
            ).children),
            {
                'countries__code': 'DE',
            }
        )

    def test_with_rel_with_field_translatable_no_lookup(self):
        self.assertDictEqual(
            dict(_get_translations_lookup_query(
                Continent, 'countries__name', 'Deutschland', 'de'
            ).children),
            {
                'countries__translations__field': 'name',
                'countries__translations__language': 'de',
                'countries__translations__text': 'Deutschland',
            }
        )

    def test_with_rel_with_field_not_translatable_with_lookup(self):
        self.assertDictEqual(
            dict(_get_translations_lookup_query(
                Continent, 'countries__code__icontains', 'DE', 'de'
            ).children),
            {
                'countries__code__icontains': 'DE',
            }
        )

    def test_with_rel_with_field_translatable_with_lookup(self):
        self.assertDictEqual(
            dict(_get_translations_lookup_query(
                Continent, 'countries__name__icontains', 'Deutsch', 'de'
            ).children),
            {
                'countries__translations__field': 'name',
                'countries__translations__language': 'de',
                'countries__translations__text__icontains': 'Deutsch',
            }
        )

    def test_with_nested_rel_with_field_not_translatable_no_lookup(self):
        self.assertDictEqual(
            dict(_get_translations_lookup_query(
                Continent, 'countries__cities__id', 1, 'de'
            ).children),
            {
                'countries__cities__id': 1,
            }
        )

    def test_with_nested_rel_with_field_translatable_no_lookup(self):
        self.assertDictEqual(
            dict(_get_translations_lookup_query(
                Continent, 'countries__cities__name', 'Köln', 'de'
            ).children),
            {
                'countries__cities__translations__field': 'name',
                'countries__cities__translations__language': 'de',
                'countries__cities__translations__text': 'Köln',
            }
        )

    def test_with_nested_rel_with_field_not_translatable_with_lookup(self):
        self.assertDictEqual(
            dict(_get_translations_lookup_query(
                Continent, 'countries__cities__id__gt', 1, 'de'
            ).children),
            {
                'countries__cities__id__gt': 1,
            }
        )

    def test_with_nested_rel_with_field_translatable_with_lookup(self):
        self.assertDictEqual(
            dict(_get_translations_lookup_query(
                Continent, 'countries__cities__name__icontains', 'Kö', 'de'
            ).children),
            {
                'countries__cities__translations__field': 'name',
                'countries__cities__translations__language': 'de',
                'countries__cities__translations__text__icontains': 'Kö',
            }
        )


class GetRelationsHierarchyTest(TestCase):
    """Tests for `_get_relations_hierarchy`."""

    def test_level_0_relation(self):
        self.assertDictEqual(
            _get_relations_hierarchy(),
            {}
        )

    def test_one_level_1_relation(self):
        self.assertEqual(
            _get_relations_hierarchy(
                'countries'
            ),
            {
                'countries': {
                    'included': True,
                    'relations': {}
                }
            }
        )

    def test_many_level_1_relations(self):
        self.assertEqual(
            _get_relations_hierarchy(
                'countries',
                'unions'
            ),
            {
                'countries': {
                    'included': True,
                    'relations': {}
                },
                'unions': {
                    'included': True,
                    'relations': {}
                },
            }
        )

    def test_one_unincluded_level_1_and_one_nested_level_2_relation(self):
        self.assertEqual(
            _get_relations_hierarchy(
                'countries__cities'
            ),
            {
                'countries': {
                    'included': False,
                    'relations': {
                        'cities': {
                            'included': True,
                            'relations': {}
                        }
                    }
                }
            }
        )

    def test_many_unincluded_level_1_and_one_nested_level_2_relation(self):
        self.assertEqual(
            _get_relations_hierarchy(
                'countries__cities',
                'unions__projects',
            ),
            {
                'countries': {
                    'included': False,
                    'relations': {
                        'cities': {
                            'included': True,
                            'relations': {}
                        }
                    }
                },
                'unions': {
                    'included': False,
                    'relations': {
                        'projects': {
                            'included': True,
                            'relations': {}
                        }
                    }
                }
            }
        )

    def test_one_unincluded_level_1_and_many_nested_level_2_relations(self):
        self.assertEqual(
            _get_relations_hierarchy(
                'countries__cities',
                'countries__currency'
            ),
            {
                'countries': {
                    'included': False,
                    'relations': {
                        'cities': {
                            'included': True,
                            'relations': {}
                        },
                        'currency': {
                            'included': True,
                            'relations': {}
                        }
                    }
                }
            }
        )

    def test_many_unincluded_level_1_and_many_nested_level_2_relations(self):
        self.assertEqual(
            _get_relations_hierarchy(
                'countries__cities',
                'countries__currency',
                'unions__projects',
                'unions__currency'
            ),
            {
                'countries': {
                    'included': False,
                    'relations': {
                        'cities': {
                            'included': True,
                            'relations': {}
                        },
                        'currency': {
                            'included': True,
                            'relations': {}
                        }
                    }
                },
                'unions': {
                    'included': False,
                    'relations': {
                        'projects': {
                            'included': True,
                            'relations': {}
                        },
                        'currency': {
                            'included': True,
                            'relations': {}
                        }
                    }
                }
            }
        )

    def test_one_included_level_1_and_one_nested_level_2_relation(self):
        self.assertEqual(
            _get_relations_hierarchy(
                'countries',
                'countries__cities'
            ),
            {
                'countries': {
                    'included': True,
                    'relations': {
                        'cities': {
                            'included': True,
                            'relations': {}
                        }
                    }
                }
            }
        )

    def test_many_included_level_1_and_one_nested_level_2_relation(self):
        self.assertEqual(
            _get_relations_hierarchy(
                'countries',
                'countries__cities',
                'unions',
                'unions__projects'
            ),
            {
                'countries': {
                    'included': True,
                    'relations': {
                        'cities': {
                            'included': True,
                            'relations': {}
                        }
                    }
                },
                'unions': {
                    'included': True,
                    'relations': {
                        'projects': {
                            'included': True,
                            'relations': {}
                        }
                    }
                },
            }
        )

    def test_one_included_level_1_and_many_nested_level_2_relations(self):
        self.assertEqual(
            _get_relations_hierarchy(
                'countries',
                'countries__cities',
                'countries__currency'
            ),
            {
                'countries': {
                    'included': True,
                    'relations': {
                        'cities': {
                            'included': True,
                            'relations': {}
                        },
                        'currency': {
                            'included': True,
                            'relations': {}
                        }
                    }
                }
            }
        )

    def test_many_included_level_1_and_many_nested_level_2_relations(self):
        self.assertEqual(
            _get_relations_hierarchy(
                'countries',
                'countries__cities',
                'countries__currency',
                'unions',
                'unions__projects',
                'unions__currency'
            ),
            {
                'countries': {
                    'included': True,
                    'relations': {
                        'cities': {
                            'included': True,
                            'relations': {}
                        },
                        'currency': {
                            'included': True,
                            'relations': {}
                        }
                    }
                },
                'unions': {
                    'included': True,
                    'relations': {
                        'projects': {
                            'included': True,
                            'relations': {}
                        },
                        'currency': {
                            'included': True,
                            'relations': {}
                        }
                    }
                },
            }
        )


class GetEntityDetailsTest(TestCase):
    """Tests for `_get_entity_details`."""

    def test_iterable(self):
        create_samples(continent_names=['europe', 'asia'])

        continents = list(Continent.objects.all())

        self.assertEqual(
            _get_entity_details(continents),
            (True, Continent)
        )

    def test_queryset(self):
        create_samples(continent_names=['europe', 'asia'])

        continents = Continent.objects.all()

        self.assertEqual(
            _get_entity_details(continents),
            (True, Continent)
        )

    def test_instance(self):
        create_samples(continent_names=['europe'])

        europe = Continent.objects.get(code='EU')

        self.assertEqual(
            _get_entity_details(europe),
            (False, Continent)
        )

    def test_empty_iterable(self):
        self.assertEqual(
            _get_entity_details([]),
            (True, None)
        )

    def test_empty_queryset(self):
        continents = Continent.objects.none()

        self.assertEqual(
            _get_entity_details(continents),
            (True, None)
        )

    def test_invalid_instance(self):
        class Person:
            def __init__(self, name):
                self.name = name

            def __str__(self):
                return self.name

            def __repr__(self):
                return self.name

        behzad = Person('Behzad')

        with self.assertRaises(TypeError) as error:
            _get_entity_details(behzad)

        self.assertEqual(
            error.exception.args[0],
            ('`Behzad` is neither a model instance nor an iterable' +
             ' of model instances.')
        )

    def test_invalid_iterable(self):
        class Person:
            def __init__(self, name):
                self.name = name

            def __str__(self):
                return self.name

            def __repr__(self):
                return self.name

        people = []
        people.append(Person('Behzad'))
        people.append(Person('Max'))

        with self.assertRaises(TypeError) as error:
            _get_entity_details(people)

        self.assertEqual(
            error.exception.args[0],
            ('`[Behzad, Max]` is neither a model instance nor an iterable' +
             ' of model instances.')
        )


class GetInstanceGroupsTest(TestCase):
    """Tests for `_get_instance_groups`."""

    def test_instance_level_0_relation(self):
        create_samples(
            continent_names=['europe'],
            continent_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        europe = Continent.objects.get(code='EU')

        hierarchy = _get_relations_hierarchy()

        ct_continent = ContentType.objects.get_for_model(Continent)

        self.assertDictEqual(
            _get_instance_groups(europe, hierarchy),
            {
                ct_continent.id: {
                    str(europe.id): europe
                }
            }
        )

    def test_instance_level_1_relation(self):
        create_samples(
            continent_names=['europe'],
            country_names=['germany'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        lvl_1 = ('countries',)

        europe = Continent.objects.get(code='EU')
        germany = europe.countries.all()[0]

        hierarchy = _get_relations_hierarchy(*lvl_1)

        ct_continent = ContentType.objects.get_for_model(Continent)
        ct_country = ContentType.objects.get_for_model(Country)

        self.assertDictEqual(
            _get_instance_groups(europe, hierarchy),
            {
                ct_continent.id: {
                    str(europe.id): europe
                },
                ct_country.id: {
                    str(germany.id): germany
                }
            }
        )

    def test_instance_level_2_relation(self):
        create_samples(
            continent_names=['europe'],
            country_names=['germany'],
            city_names=['cologne'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        lvl_2 = ('countries__cities',)

        europe = Continent.objects.get(code='EU')
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        hierarchy = _get_relations_hierarchy(*lvl_2)

        ct_continent = ContentType.objects.get_for_model(Continent)
        ct_city = ContentType.objects.get_for_model(City)

        self.assertDictEqual(
            _get_instance_groups(europe, hierarchy),
            {
                ct_continent.id: {
                    str(europe.id): europe
                },
                ct_city.id: {
                    str(cologne.id): cologne
                }
            }
        )

    def test_instance_level_1_2_relation(self):
        create_samples(
            continent_names=['europe'],
            country_names=['germany'],
            city_names=['cologne'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.get(code='EU')
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        hierarchy = _get_relations_hierarchy(*lvl_1_2)

        ct_continent = ContentType.objects.get_for_model(Continent)
        ct_country = ContentType.objects.get_for_model(Country)
        ct_city = ContentType.objects.get_for_model(City)

        self.assertDictEqual(
            _get_instance_groups(europe, hierarchy),
            {
                ct_continent.id: {
                    str(europe.id): europe
                },
                ct_country.id: {
                    str(germany.id): germany
                },
                ct_city.id: {
                    str(cologne.id): cologne
                }
            }
        )

    def test_queryset_level_0_relation(self):
        create_samples(
            continent_names=['europe', 'asia'],
            continent_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        continents = Continent.objects.all()

        europe = [x for x in continents if x.code == 'EU'][0]

        asia = [x for x in continents if x.code == 'AS'][0]

        hierarchy = _get_relations_hierarchy()

        ct_continent = ContentType.objects.get_for_model(Continent)

        self.assertDictEqual(
            _get_instance_groups(continents, hierarchy),
            {
                ct_continent.id: {
                    str(europe.id): europe,
                    str(asia.id): asia
                },
            }
        )

    def test_queryset_level_1_relation(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        lvl_1 = ('countries',)

        continents = Continent.objects.all()

        europe = [x for x in continents if x.code == 'EU'][0]
        germany = europe.countries.all()[0]

        asia = [x for x in continents if x.code == 'AS'][0]
        south_korea = asia.countries.all()[0]

        hierarchy = _get_relations_hierarchy(*lvl_1)

        ct_continent = ContentType.objects.get_for_model(Continent)
        ct_country = ContentType.objects.get_for_model(Country)

        self.assertDictEqual(
            _get_instance_groups(continents, hierarchy),
            {
                ct_continent.id: {
                    str(europe.id): europe,
                    str(asia.id): asia
                },
                ct_country.id: {
                    str(germany.id): germany,
                    str(south_korea.id): south_korea
                },
            }
        )

    def test_queryset_level_2_relation(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        lvl_2 = ('countries__cities',)

        continents = Continent.objects.all()

        europe = [x for x in continents if x.code == 'EU'][0]
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        asia = [x for x in continents if x.code == 'AS'][0]
        south_korea = asia.countries.all()[0]
        seoul = south_korea.cities.all()[0]

        hierarchy = _get_relations_hierarchy(*lvl_2)

        ct_continent = ContentType.objects.get_for_model(Continent)
        ct_city = ContentType.objects.get_for_model(City)

        self.assertDictEqual(
            _get_instance_groups(continents, hierarchy),
            {
                ct_continent.id: {
                    str(europe.id): europe,
                    str(asia.id): asia
                },
                ct_city.id: {
                    str(cologne.id): cologne,
                    str(seoul.id): seoul
                }
            }
        )

    def test_queryset_level_1_2_relation(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.all()

        europe = [x for x in continents if x.code == 'EU'][0]
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        asia = [x for x in continents if x.code == 'AS'][0]
        south_korea = asia.countries.all()[0]
        seoul = south_korea.cities.all()[0]

        hierarchy = _get_relations_hierarchy(*lvl_1_2)

        ct_continent = ContentType.objects.get_for_model(Continent)
        ct_country = ContentType.objects.get_for_model(Country)
        ct_city = ContentType.objects.get_for_model(City)

        self.assertDictEqual(
            _get_instance_groups(continents, hierarchy),
            {
                ct_continent.id: {
                    str(europe.id): europe,
                    str(asia.id): asia
                },
                ct_country.id: {
                    str(germany.id): germany,
                    str(south_korea.id): south_korea
                },
                ct_city.id: {
                    str(cologne.id): cologne,
                    str(seoul.id): seoul
                }
            }
        )

    def test_prefetched_instance_level_0_relation(self):
        create_samples(
            continent_names=['europe'],
            continent_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        europe = Continent.objects.get(code='EU')

        hierarchy = _get_relations_hierarchy()

        ct_continent = ContentType.objects.get_for_model(Continent)

        self.assertDictEqual(
            _get_instance_groups(
                europe,
                hierarchy,
            ),
            {
                ct_continent.id: {
                    str(europe.id): europe
                }
            }
        )

    def test_prefetched_instance_level_1_relation(self):
        create_samples(
            continent_names=['europe'],
            country_names=['germany'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        lvl_1 = ('countries',)

        europe = Continent.objects.prefetch_related(*lvl_1).get(code='EU')
        germany = europe.countries.all()[0]

        hierarchy = _get_relations_hierarchy(*lvl_1)

        ct_continent = ContentType.objects.get_for_model(Continent)
        ct_country = ContentType.objects.get_for_model(Country)

        self.assertDictEqual(
            _get_instance_groups(
                europe,
                hierarchy,
            ),
            {
                ct_continent.id: {
                    str(europe.id): europe
                },
                ct_country.id: {
                    str(germany.id): germany
                }
            }
        )

    def test_prefetched_instance_level_2_relation(self):
        create_samples(
            continent_names=['europe'],
            country_names=['germany'],
            city_names=['cologne'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        lvl_2 = ('countries__cities',)

        europe = Continent.objects.prefetch_related(*lvl_2).get(code='EU')
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        hierarchy = _get_relations_hierarchy(*lvl_2)

        ct_continent = ContentType.objects.get_for_model(Continent)
        ct_city = ContentType.objects.get_for_model(City)

        self.assertDictEqual(
            _get_instance_groups(
                europe,
                hierarchy,
            ),
            {
                ct_continent.id: {
                    str(europe.id): europe
                },
                ct_city.id: {
                    str(cologne.id): cologne
                }
            }
        )

    def test_prefetched_instance_level_1_2_relation(self):
        create_samples(
            continent_names=['europe'],
            country_names=['germany'],
            city_names=['cologne'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code='EU')
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        hierarchy = _get_relations_hierarchy(*lvl_1_2)

        ct_continent = ContentType.objects.get_for_model(Continent)
        ct_country = ContentType.objects.get_for_model(Country)
        ct_city = ContentType.objects.get_for_model(City)

        self.assertDictEqual(
            _get_instance_groups(
                europe,
                hierarchy,
            ),
            {
                ct_continent.id: {
                    str(europe.id): europe
                },
                ct_country.id: {
                    str(germany.id): germany
                },
                ct_city.id: {
                    str(cologne.id): cologne
                }
            }
        )

    def test_prefetched_queryset_level_0_relation(self):
        create_samples(
            continent_names=['europe', 'asia'],
            continent_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        continents = Continent.objects.all()

        europe = [x for x in continents if x.code == 'EU'][0]

        asia = [x for x in continents if x.code == 'AS'][0]

        hierarchy = _get_relations_hierarchy()

        ct_continent = ContentType.objects.get_for_model(Continent)

        self.assertDictEqual(
            _get_instance_groups(
                continents,
                hierarchy,
            ),
            {
                ct_continent.id: {
                    str(europe.id): europe,
                    str(asia.id): asia
                },
            }
        )

    def test_prefetched_queryset_level_1_relation(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        lvl_1 = ('countries',)

        continents = Continent.objects.prefetch_related(*lvl_1)

        europe = [x for x in continents if x.code == 'EU'][0]
        germany = europe.countries.all()[0]

        asia = [x for x in continents if x.code == 'AS'][0]
        south_korea = asia.countries.all()[0]

        hierarchy = _get_relations_hierarchy(*lvl_1)

        ct_continent = ContentType.objects.get_for_model(Continent)
        ct_country = ContentType.objects.get_for_model(Country)

        self.assertDictEqual(
            _get_instance_groups(
                continents,
                hierarchy,
            ),
            {
                ct_continent.id: {
                    str(europe.id): europe,
                    str(asia.id): asia
                },
                ct_country.id: {
                    str(germany.id): germany,
                    str(south_korea.id): south_korea
                },
            }
        )

    def test_prefetched_queryset_level_2_relation(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        lvl_2 = ('countries__cities',)

        continents = Continent.objects.prefetch_related(*lvl_2)

        europe = [x for x in continents if x.code == 'EU'][0]
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        asia = [x for x in continents if x.code == 'AS'][0]
        south_korea = asia.countries.all()[0]
        seoul = south_korea.cities.all()[0]

        hierarchy = _get_relations_hierarchy(*lvl_2)

        ct_continent = ContentType.objects.get_for_model(Continent)
        ct_city = ContentType.objects.get_for_model(City)

        self.assertDictEqual(
            _get_instance_groups(
                continents,
                hierarchy,
            ),
            {
                ct_continent.id: {
                    str(europe.id): europe,
                    str(asia.id): asia
                },
                ct_city.id: {
                    str(cologne.id): cologne,
                    str(seoul.id): seoul
                }
            }
        )

    def test_prefetched_queryset_level_1_2_relation(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.prefetch_related(*lvl_1_2)

        europe = [x for x in continents if x.code == 'EU'][0]
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        asia = [x for x in continents if x.code == 'AS'][0]
        south_korea = asia.countries.all()[0]
        seoul = south_korea.cities.all()[0]

        hierarchy = _get_relations_hierarchy(*lvl_1_2)

        ct_continent = ContentType.objects.get_for_model(Continent)
        ct_country = ContentType.objects.get_for_model(Country)
        ct_city = ContentType.objects.get_for_model(City)

        self.assertDictEqual(
            _get_instance_groups(
                continents,
                hierarchy,
            ),
            {
                ct_continent.id: {
                    str(europe.id): europe,
                    str(asia.id): asia
                },
                ct_country.id: {
                    str(germany.id): germany,
                    str(south_korea.id): south_korea
                },
                ct_city.id: {
                    str(cologne.id): cologne,
                    str(seoul.id): seoul
                }
            }
        )

    def test_invalid_instance(self):
        class Person:
            def __init__(self, name):
                self.name = name

            def __str__(self):
                return self.name

            def __repr__(self):
                return self.name

        behzad = Person('Behzad')

        with self.assertRaises(TypeError) as error:
            _get_instance_groups(
                behzad,
                {}
            )

        self.assertEqual(
            error.exception.args[0],
            ('`Behzad` is neither a model instance nor an iterable of' +
             ' model instances.')
        )

    def test_invalid_iterable(self):
        class Person:
            def __init__(self, name):
                self.name = name

            def __str__(self):
                return self.name

            def __repr__(self):
                return self.name

        people = []
        people.append(Person('Behzad'))
        people.append(Person('Max'))

        with self.assertRaises(TypeError) as error:
            _get_instance_groups(
                people,
                {}
            )

        self.assertEqual(
            error.exception.args[0],
            ('`[Behzad, Max]` is neither a model instance nor an iterable of' +
             ' model instances.')
        )

    def test_invalid_simple_relation(self):
        create_samples(
            continent_names=['europe'],
            continent_fields=['name', 'denonym'],
            langs=['de']
        )

        europe = Continent.objects.get(code='EU')

        hierarchy = _get_relations_hierarchy('wrong')

        with self.assertRaises(FieldDoesNotExist) as error:
            _get_instance_groups(
                europe,
                hierarchy
            )

        self.assertEqual(
            error.exception.args[0],
            "Continent has no field named 'wrong'"
        )

    def test_invalid_nested_relation(self):
        create_samples(
            continent_names=['europe'],
            country_names=['germany'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            langs=['de']
        )

        europe = Continent.objects.get(code='EU')

        hierarchy = _get_relations_hierarchy('countries__wrong')

        with self.assertRaises(FieldDoesNotExist) as error:
            _get_instance_groups(
                europe,
                hierarchy
            )

        self.assertEqual(
            error.exception.args[0],
            "Country has no field named 'wrong'"
        )


class GetTranslationsTest(TestCase):
    """Tests for `_get_translations`."""

    def test_instance_level_0_relation_with_lang(self):
        create_samples(
            continent_names=['europe'],
            country_names=['germany'],
            city_names=['cologne'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        europe = Continent.objects.get(code='EU')
        hierarchy = _get_relations_hierarchy()
        groups = _get_instance_groups(europe, hierarchy)

        self.assertQuerysetEqual(
            _get_translations(groups, lang='de').order_by('id'),
            [
                '<Translation: Europe: Europa>',
                '<Translation: European: Europäisch>',
            ]
        )

    def test_instance_level_1_relation_with_lang(self):
        create_samples(
            continent_names=['europe'],
            country_names=['germany'],
            city_names=['cologne'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        lvl_1 = ('countries',)

        europe = Continent.objects.get(code='EU')
        hierarchy = _get_relations_hierarchy(*lvl_1)
        groups = _get_instance_groups(europe, hierarchy)

        self.assertQuerysetEqual(
            _get_translations(groups, lang='de').order_by('id'),
            [
                '<Translation: Europe: Europa>',
                '<Translation: European: Europäisch>',
                '<Translation: Germany: Deutschland>',
                '<Translation: German: Deutsche>',
            ]
        )

    def test_instance_level_2_relation_with_lang(self):
        create_samples(
            continent_names=['europe'],
            country_names=['germany'],
            city_names=['cologne'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        lvl_2 = ('countries__cities',)

        europe = Continent.objects.get(code='EU')
        hierarchy = _get_relations_hierarchy(*lvl_2)
        groups = _get_instance_groups(europe, hierarchy)

        self.assertQuerysetEqual(
            _get_translations(groups, lang='de').order_by('id'),
            [
                '<Translation: Europe: Europa>',
                '<Translation: European: Europäisch>',
                '<Translation: Cologne: Köln>',
                '<Translation: Cologner: Kölner>',
            ]
        )

    def test_instance_level_1_2_relation_with_lang(self):
        create_samples(
            continent_names=['europe'],
            country_names=['germany'],
            city_names=['cologne'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.get(code='EU')
        hierarchy = _get_relations_hierarchy(*lvl_1_2)
        groups = _get_instance_groups(europe, hierarchy)

        self.assertQuerysetEqual(
            _get_translations(groups, lang='de').order_by('id'),
            [
                '<Translation: Europe: Europa>',
                '<Translation: European: Europäisch>',
                '<Translation: Germany: Deutschland>',
                '<Translation: German: Deutsche>',
                '<Translation: Cologne: Köln>',
                '<Translation: Cologner: Kölner>',
            ]
        )

    def test_queryset_level_0_relation_with_lang(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        continents = Continent.objects.all()
        hierarchy = _get_relations_hierarchy()
        groups = _get_instance_groups(continents, hierarchy)

        self.assertQuerysetEqual(
            _get_translations(groups, lang='de').order_by('id'),
            [
                '<Translation: Europe: Europa>',
                '<Translation: European: Europäisch>',
                '<Translation: Asia: Asien>',
                '<Translation: Asian: Asiatisch>',
            ]
        )

    def test_queryset_level_1_relation_with_lang(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        lvl_1 = ('countries',)

        continents = Continent.objects.all()
        hierarchy = _get_relations_hierarchy(*lvl_1)
        groups = _get_instance_groups(continents, hierarchy)

        self.assertQuerysetEqual(
            _get_translations(groups, lang='de').order_by('id'),
            [
                '<Translation: Europe: Europa>',
                '<Translation: European: Europäisch>',
                '<Translation: Germany: Deutschland>',
                '<Translation: German: Deutsche>',
                '<Translation: Asia: Asien>',
                '<Translation: Asian: Asiatisch>',
                '<Translation: South Korea: Südkorea>',
                '<Translation: South Korean: Südkoreanisch>',
            ]
        )

    def test_queryset_level_2_relation_with_lang(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        lvl_2 = ('countries__cities',)

        continents = Continent.objects.all()
        hierarchy = _get_relations_hierarchy(*lvl_2)
        groups = _get_instance_groups(continents, hierarchy)

        self.assertQuerysetEqual(
            _get_translations(groups, lang='de').order_by('id'),
            [
                '<Translation: Europe: Europa>',
                '<Translation: European: Europäisch>',
                '<Translation: Cologne: Köln>',
                '<Translation: Cologner: Kölner>',
                '<Translation: Asia: Asien>',
                '<Translation: Asian: Asiatisch>',
                '<Translation: Seoul: Seül>',
                '<Translation: Seouler: Seüler>',
            ]
        )

    def test_queryset_level_1_2_relation_with_lang(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.all()
        hierarchy = _get_relations_hierarchy(*lvl_1_2)
        groups = _get_instance_groups(continents, hierarchy)

        self.assertQuerysetEqual(
            _get_translations(groups, lang='de').order_by('id'),
            [
                '<Translation: Europe: Europa>',
                '<Translation: European: Europäisch>',
                '<Translation: Germany: Deutschland>',
                '<Translation: German: Deutsche>',
                '<Translation: Cologne: Köln>',
                '<Translation: Cologner: Kölner>',
                '<Translation: Asia: Asien>',
                '<Translation: Asian: Asiatisch>',
                '<Translation: South Korea: Südkorea>',
                '<Translation: South Korean: Südkoreanisch>',
                '<Translation: Seoul: Seül>',
                '<Translation: Seouler: Seüler>',
            ]
        )
