from django.test import TestCase
from django.db import models
from django.core.exceptions import FieldDoesNotExist
from django.utils.translation import activate, deactivate
from django.contrib.contenttypes.models import ContentType

from translations.utils import _get_translation_language, \
    _get_entity_details, _get_reverse_relation,  _get_relations_hierarchy, \
    _get_entity_groups, _get_translations, \
    apply_translations, update_translations

from translations.models import Translation

from sample.models import Continent, Country, City

from .sample import create_samples


class GetTranslationLanguageTest(TestCase):
    """Tests for `_get_translation_language`."""

    def test_active_lang(self):
        """Make sure it works with an active language."""
        activate('en')
        self.assertEqual(
            _get_translation_language(),
            'en'
        )

    def test_custom_lang(self):
        """Make sure it works with a valid language code."""
        self.assertEqual(
            _get_translation_language('de'),
            'de'
        )

    def test_invalid_lang(self):
        """Make sure it raises on an invalid language code."""
        with self.assertRaises(ValueError) as error:
            _get_translation_language('xx')
        self.assertEqual(
            error.exception.args[0],
            "The language code `xx` is not supported."
        )


class GetEntityDetailsTest(TestCase):
    """Tests for `_get_entity_details`."""

    def test_iterable(self):
        """Make sure it works with a model iterable."""
        create_samples(continent_names=["europe", "asia"])

        continents = list(Continent.objects.all())
        self.assertEqual(
            _get_entity_details(continents),
            (True, Continent)
        )

    def test_queryset(self):
        """Make sure it works with a model queryset."""
        create_samples(continent_names=["europe", "asia"])

        continents = Continent.objects.all()
        self.assertEqual(
            _get_entity_details(continents),
            (True, Continent)
        )

    def test_instance(self):
        """Make sure it works with a model instance."""
        create_samples(continent_names=["europe"])

        europe = Continent.objects.get(code="EU")

        self.assertEqual(
            _get_entity_details(europe),
            (False, Continent)
        )

    def test_empty_iterable(self):
        """Make sure it works with an empty list."""
        self.assertEqual(
            _get_entity_details([]),
            (True, None)
        )

    def test_empty_queryset(self):
        """Make sure it works with an empty queryset."""
        continents = Continent.objects.none()
        self.assertEqual(
            _get_entity_details(continents),
            (True, None)
        )

    def test_invalid_iterable(self):
        """Make sure it raises on invalid iterable."""
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
            "`[Behzad, Max]` is neither a model instance nor an iterable of model instances."
        )

    def test_invalid_instance(self):
        """Make sure it raises on invalid instance."""
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
            "`Behzad` is neither a model instance nor an iterable of model instances."
        )


class GetReverseRelationTest(TestCase):
    """Tests for `_get_reverse_relation`."""

    def test_simple_relation(self):
        """Make sure it works with a simple relation."""
        self.assertEqual(
            _get_reverse_relation(Continent, 'countries'),
            'continent'
        )

    def test_simple_reverse_relation(self):
        """Make sure it works with a simple relation in reverse."""
        self.assertEqual(
            _get_reverse_relation(Country, 'continent'),
            'countries'
        )

    def test_nested_relation(self):
        """Make sure it works with a nested relation."""
        self.assertEqual(
            _get_reverse_relation(Continent, 'countries__cities'),
            'country__continent'
        )

    def test_nested_reverse_relation(self):
        """Make sure it works with a nested relation in reverse."""
        self.assertEqual(
            _get_reverse_relation(City, 'country__continent'),
            'countries__cities'
        )

    def test_empty_relation(self):
        """Make sure it raises on an empty relation."""
        with self.assertRaises(FieldDoesNotExist) as error:
            _get_reverse_relation(
                Continent,
                ''
            )
        self.assertEqual(
            error.exception.args[0],
            "Continent has no field named ''"
        )

    def test_invalid_simple_relation(self):
        """Make sure it raises on an invalid simple relation."""
        with self.assertRaises(FieldDoesNotExist) as error:
            _get_reverse_relation(
                Continent,
                'wrong'
            )
        self.assertEqual(
            error.exception.args[0],
            "Continent has no field named 'wrong'"
        )

    def test_invalid_nested_relation(self):
        """Make sure it raises on an invalid nested relation."""
        with self.assertRaises(FieldDoesNotExist) as error:
            _get_reverse_relation(
                Continent,
                'countries__wrong'
            )
        self.assertEqual(
            error.exception.args[0],
            "Country has no field named 'wrong'"
        )


class GetRelationsHierarchyTest(TestCase):
    """Tests for `_get_relations_hierarchy`."""

    def test_no_relations(self):
        self.assertDictEqual(
            _get_relations_hierarchy(),
            {}
        )

    def test_one_included_no_nested_relations(self):
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

    def test_many_included_no_nested_relations(self):
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

    def test_one_unincluded_one_nested_relation(self):
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

    def test_many_unincluded_one_nested_relation(self):
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

    def test_one_uincluded_many_nested_relations(self):
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

    def test_many_uincluded_many_nested_relations(self):
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

    def test_one_included_one_nested_relations(self):
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

    def test_many_included_one_nested_relations(self):
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

    def test_one_included_many_nested_relations(self):
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

    def test_many_included_many_nested_relations(self):
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


class GetEntityGroupsTest(TestCase):
    """Tests for `_get_entity_groups`."""

    # ---- arguments testing -------------------------------------------------

    def test_instance_level_0_relation(self):
        create_samples(
            continent_names=["europe"],
            continent_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        europe = Continent.objects.get(code="EU")

        ct_continent = ContentType.objects.get_for_model(Continent)

        hierarchy = _get_relations_hierarchy()

        self.assertDictEqual(
            _get_entity_groups(europe, hierarchy),
            {
                ct_continent.id: {
                    str(europe.id): europe
                }
            }
        )

    def test_instance_level_1_relation(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        europe = Continent.objects.get(code="EU")
        germany = europe.countries.all()[0]

        ct_continent = ContentType.objects.get_for_model(Continent)
        ct_country = ContentType.objects.get_for_model(Country)

        hierarchy = _get_relations_hierarchy('countries')

        self.assertDictEqual(
            _get_entity_groups(europe, hierarchy),
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
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        europe = Continent.objects.get(code="EU")
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        ct_continent = ContentType.objects.get_for_model(Continent)
        ct_city = ContentType.objects.get_for_model(City)

        hierarchy = _get_relations_hierarchy('countries__cities')

        self.assertDictEqual(
            _get_entity_groups(europe, hierarchy),
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
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        europe = Continent.objects.get(code="EU")
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        ct_continent = ContentType.objects.get_for_model(Continent)
        ct_country = ContentType.objects.get_for_model(Country)
        ct_city = ContentType.objects.get_for_model(City)

        hierarchy = _get_relations_hierarchy('countries', 'countries__cities')

        self.assertDictEqual(
            _get_entity_groups(europe, hierarchy),
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
            continent_names=["europe", "asia"],
            continent_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        continents = Continent.objects.all()

        europe = [x for x in continents if x.code == 'EU'][0]

        asia = [x for x in continents if x.code == 'AS'][0]

        ct_continent = ContentType.objects.get_for_model(Continent)

        hierarchy = _get_relations_hierarchy('countries',)

        self.assertDictEqual(
            _get_entity_groups(continents, hierarchy),
            {
                ct_continent.id: {
                    str(europe.id): europe,
                    str(asia.id): asia
                },
            }
        )

    def test_queryset_level_1_relation(self):
        create_samples(
            continent_names=["europe", "asia"],
            country_names=["germany", "south korea"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        continents = Continent.objects.all()

        europe = [x for x in continents if x.code == 'EU'][0]
        germany = europe.countries.all()[0]

        asia = [x for x in continents if x.code == 'AS'][0]
        south_korea = asia.countries.all()[0]

        ct_continent = ContentType.objects.get_for_model(Continent)
        ct_country = ContentType.objects.get_for_model(Country)

        hierarchy = _get_relations_hierarchy('countries',)

        self.assertDictEqual(
            _get_entity_groups(continents, hierarchy),
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
            continent_names=["europe", "asia"],
            country_names=["germany", "south korea"],
            city_names=["cologne", "seoul"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        continents = Continent.objects.all()

        europe = [x for x in continents if x.code == 'EU'][0]
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        asia = [x for x in continents if x.code == 'AS'][0]
        south_korea = asia.countries.all()[0]
        seoul = south_korea.cities.all()[0]

        ct_continent = ContentType.objects.get_for_model(Continent)
        ct_city = ContentType.objects.get_for_model(City)

        hierarchy = _get_relations_hierarchy('countries__cities',)

        self.assertDictEqual(
            _get_entity_groups(continents, hierarchy),
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
            continent_names=["europe", "asia"],
            country_names=["germany", "south korea"],
            city_names=["cologne", "seoul"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        continents = Continent.objects.all()

        europe = [x for x in continents if x.code == 'EU'][0]
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        asia = [x for x in continents if x.code == 'AS'][0]
        south_korea = asia.countries.all()[0]
        seoul = south_korea.cities.all()[0]

        ct_continent = ContentType.objects.get_for_model(Continent)
        ct_country = ContentType.objects.get_for_model(Country)
        ct_city = ContentType.objects.get_for_model(City)

        hierarchy = _get_relations_hierarchy('countries', 'countries__cities',)

        self.assertDictEqual(
            _get_entity_groups(continents, hierarchy),
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

    # ---- error testing -----------------------------------------------------

    def test_invalid_relation(self):
        create_samples(
            continent_names=["europe"],
            continent_fields=["name", "denonym"],
            langs=["de"]
        )

        europe = Continent.objects.get(code="EU")

        hierarchy = _get_relations_hierarchy('wrong')

        with self.assertRaises(FieldDoesNotExist) as error:
            _get_entity_groups(europe, hierarchy)
        self.assertEqual(
            error.exception.args[0],
            "Continent has no field named 'wrong'"
        )

    def test_invalid_entity(self):
        class Person:
            def __init__(self, name):
                self.name = name

            def __str__(self):
                return self.name

            def __repr__(self):
                return self.name

        behzad = Person('Behzad')
        with self.assertRaises(TypeError) as error:
            _get_entity_groups(behzad, {})
        self.assertEqual(
            error.exception.args[0],
            "`Behzad` is neither a model instance nor an iterable of model instances."
        )


class GetTranslationsTest(TestCase):
    """Tests for `_get_translations`."""

    # ---- arguments testing -------------------------------------------------

    def test_instance_level_0_relation_no_lang(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        europe = Continent.objects.get(code="EU")
        hierarchy = _get_relations_hierarchy()
        groups = _get_entity_groups(europe, hierarchy)

        activate("de")
        self.assertQuerysetEqual(
            _get_translations(
                groups
            ).order_by("id"),
            [
                "<Translation: Europe: Europa>",
                "<Translation: European: Europäisch>",
            ]
        )

    def test_instance_level_1_relation_no_lang(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        europe = Continent.objects.get(code="EU")
        hierarchy = _get_relations_hierarchy('countries')
        groups = _get_entity_groups(europe, hierarchy)

        activate("de")
        self.assertQuerysetEqual(
            _get_translations(
                groups
            ).order_by("id"),
            [
                "<Translation: Europe: Europa>",
                "<Translation: European: Europäisch>",
                "<Translation: Germany: Deutschland>",
                "<Translation: German: Deutsche>",
            ]
        )

    def test_instance_level_2_relation_no_lang(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        europe = Continent.objects.get(code="EU")
        hierarchy = _get_relations_hierarchy('countries__cities')
        groups = _get_entity_groups(europe, hierarchy)

        activate("de")
        self.assertQuerysetEqual(
            _get_translations(
                groups
            ).order_by("id"),
            [
                "<Translation: Europe: Europa>",
                "<Translation: European: Europäisch>",
                "<Translation: Cologne: Köln>",
                "<Translation: Cologner: Kölner>",
            ]
        )

    def test_instance_level_1_2_relation_no_lang(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        europe = Continent.objects.get(code="EU")
        hierarchy = _get_relations_hierarchy('countries', 'countries__cities')
        groups = _get_entity_groups(europe, hierarchy)

        activate("de")
        self.assertQuerysetEqual(
            _get_translations(
                groups
            ).order_by("id"),
            [
                "<Translation: Europe: Europa>",
                "<Translation: European: Europäisch>",
                "<Translation: Germany: Deutschland>",
                "<Translation: German: Deutsche>",
                "<Translation: Cologne: Köln>",
                "<Translation: Cologner: Kölner>",
            ]
        )

    def test_instance_level_0_relation_with_lang(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        europe = Continent.objects.get(code="EU")
        hierarchy = _get_relations_hierarchy()
        groups = _get_entity_groups(europe, hierarchy)

        self.assertQuerysetEqual(
            _get_translations(
                groups
            ).order_by("id"),
            [
                "<Translation: Europe: Europa>",
                "<Translation: European: Europäisch>",
            ]
        )

    def test_instance_level_1_relation_with_lang(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        europe = Continent.objects.get(code="EU")
        hierarchy = _get_relations_hierarchy('countries')
        groups = _get_entity_groups(europe, hierarchy)

        self.assertQuerysetEqual(
            _get_translations(
                groups,
                lang="de"
            ).order_by("id"),
            [
                "<Translation: Europe: Europa>",
                "<Translation: European: Europäisch>",
                "<Translation: Germany: Deutschland>",
                "<Translation: German: Deutsche>",
            ]
        )

    def test_instance_level_2_relation_with_lang(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        europe = Continent.objects.get(code="EU")
        hierarchy = _get_relations_hierarchy('countries__cities')
        groups = _get_entity_groups(europe, hierarchy)

        self.assertQuerysetEqual(
            _get_translations(
                groups,
                lang="de"
            ).order_by("id"),
            [
                "<Translation: Europe: Europa>",
                "<Translation: European: Europäisch>",
                "<Translation: Cologne: Köln>",
                "<Translation: Cologner: Kölner>",
            ]
        )

    def test_instance_level_1_2_relation_with_lang(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        europe = Continent.objects.get(code="EU")
        hierarchy = _get_relations_hierarchy('countries', 'countries__cities')
        groups = _get_entity_groups(europe, hierarchy)

        self.assertQuerysetEqual(
            _get_translations(
                groups,
                lang="de"
            ).order_by("id"),
            [
                "<Translation: Europe: Europa>",
                "<Translation: European: Europäisch>",
                "<Translation: Germany: Deutschland>",
                "<Translation: German: Deutsche>",
                "<Translation: Cologne: Köln>",
                "<Translation: Cologner: Kölner>",
            ]
        )

    def test_queryset_level_0_relation_no_lang(self):
        create_samples(
            continent_names=["europe", "asia"],
            country_names=["germany", "south korea"],
            city_names=["cologne", "seoul"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        continents = Continent.objects.all()
        hierarchy = _get_relations_hierarchy()
        groups = _get_entity_groups(continents, hierarchy)

        activate("de")
        self.assertQuerysetEqual(
            _get_translations(
                groups
            ).order_by("id"),
            [
                "<Translation: Europe: Europa>",
                "<Translation: European: Europäisch>",
                "<Translation: Asia: Asien>",
                "<Translation: Asian: Asiatisch>",
            ]
        )

    def test_queryset_level_1_relation_no_lang(self):
        create_samples(
            continent_names=["europe", "asia"],
            country_names=["germany", "south korea"],
            city_names=["cologne", "seoul"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        continents = Continent.objects.all()
        hierarchy = _get_relations_hierarchy('countries')
        groups = _get_entity_groups(continents, hierarchy)

        activate("de")
        self.assertQuerysetEqual(
            _get_translations(
                groups
            ).order_by("id"),
            [
                "<Translation: Europe: Europa>",
                "<Translation: European: Europäisch>",
                "<Translation: Germany: Deutschland>",
                "<Translation: German: Deutsche>",
                "<Translation: Asia: Asien>",
                "<Translation: Asian: Asiatisch>",
                "<Translation: South Korea: Südkorea>",
                "<Translation: South Korean: Südkoreanisch>",
            ]
        )

    def test_queryset_level_2_relation_no_lang(self):
        create_samples(
            continent_names=["europe", "asia"],
            country_names=["germany", "south korea"],
            city_names=["cologne", "seoul"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        continents = Continent.objects.all()
        hierarchy = _get_relations_hierarchy('countries__cities')
        groups = _get_entity_groups(continents, hierarchy)

        activate("de")
        self.assertQuerysetEqual(
            _get_translations(
                groups
            ).order_by("id"),
            [
                "<Translation: Europe: Europa>",
                "<Translation: European: Europäisch>",
                "<Translation: Cologne: Köln>",
                "<Translation: Cologner: Kölner>",
                "<Translation: Asia: Asien>",
                "<Translation: Asian: Asiatisch>",
                "<Translation: Seoul: Seül>",
                "<Translation: Seouler: Seüler>",
            ]
        )

    def test_queryset_level_1_2_relation_no_lang(self):
        create_samples(
            continent_names=["europe", "asia"],
            country_names=["germany", "south korea"],
            city_names=["cologne", "seoul"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        continents = Continent.objects.all()
        hierarchy = _get_relations_hierarchy('countries', 'countries__cities')
        groups = _get_entity_groups(continents, hierarchy)

        activate("de")
        self.assertQuerysetEqual(
            _get_translations(
                groups
            ).order_by("id"),
            [
                "<Translation: Europe: Europa>",
                "<Translation: European: Europäisch>",
                "<Translation: Germany: Deutschland>",
                "<Translation: German: Deutsche>",
                "<Translation: Cologne: Köln>",
                "<Translation: Cologner: Kölner>",
                "<Translation: Asia: Asien>",
                "<Translation: Asian: Asiatisch>",
                "<Translation: South Korea: Südkorea>",
                "<Translation: South Korean: Südkoreanisch>",
                "<Translation: Seoul: Seül>",
                "<Translation: Seouler: Seüler>",
            ]
        )

    def test_queryset_level_0_relation_with_lang(self):
        create_samples(
            continent_names=["europe", "asia"],
            country_names=["germany", "south korea"],
            city_names=["cologne", "seoul"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        continents = Continent.objects.all()
        hierarchy = _get_relations_hierarchy()
        groups = _get_entity_groups(continents, hierarchy)

        self.assertQuerysetEqual(
            _get_translations(
                groups,
                lang="de"
            ).order_by("id"),
            [
                "<Translation: Europe: Europa>",
                "<Translation: European: Europäisch>",
                "<Translation: Asia: Asien>",
                "<Translation: Asian: Asiatisch>",
            ]
        )

    def test_queryset_level_1_relation_with_lang(self):
        create_samples(
            continent_names=["europe", "asia"],
            country_names=["germany", "south korea"],
            city_names=["cologne", "seoul"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        continents = Continent.objects.all()
        hierarchy = _get_relations_hierarchy('countries')
        groups = _get_entity_groups(continents, hierarchy)

        self.assertQuerysetEqual(
            _get_translations(
                groups,
                lang="de"
            ).order_by("id"),
            [
                "<Translation: Europe: Europa>",
                "<Translation: European: Europäisch>",
                "<Translation: Germany: Deutschland>",
                "<Translation: German: Deutsche>",
                "<Translation: Asia: Asien>",
                "<Translation: Asian: Asiatisch>",
                "<Translation: South Korea: Südkorea>",
                "<Translation: South Korean: Südkoreanisch>",
            ]
        )

    def test_queryset_level_2_relation_with_lang(self):
        create_samples(
            continent_names=["europe", "asia"],
            country_names=["germany", "south korea"],
            city_names=["cologne", "seoul"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        continents = Continent.objects.all()
        hierarchy = _get_relations_hierarchy('countries__cities')
        groups = _get_entity_groups(continents, hierarchy)

        self.assertQuerysetEqual(
            _get_translations(
                groups,
                lang="de"
            ).order_by("id"),
            [
                "<Translation: Europe: Europa>",
                "<Translation: European: Europäisch>",
                "<Translation: Cologne: Köln>",
                "<Translation: Cologner: Kölner>",
                "<Translation: Asia: Asien>",
                "<Translation: Asian: Asiatisch>",
                "<Translation: Seoul: Seül>",
                "<Translation: Seouler: Seüler>",
            ]
        )

    def test_queryset_level_1_2_relation_with_lang(self):
        create_samples(
            continent_names=["europe", "asia"],
            country_names=["germany", "south korea"],
            city_names=["cologne", "seoul"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        continents = Continent.objects.all()
        hierarchy = _get_relations_hierarchy('countries', 'countries__cities')
        groups = _get_entity_groups(continents, hierarchy)

        self.assertQuerysetEqual(
            _get_translations(
                groups,
                lang="de"
            ).order_by("id"),
            [
                "<Translation: Europe: Europa>",
                "<Translation: European: Europäisch>",
                "<Translation: Germany: Deutschland>",
                "<Translation: German: Deutsche>",
                "<Translation: Cologne: Köln>",
                "<Translation: Cologner: Kölner>",
                "<Translation: Asia: Asien>",
                "<Translation: Asian: Asiatisch>",
                "<Translation: South Korea: Südkorea>",
                "<Translation: South Korean: Südkoreanisch>",
                "<Translation: Seoul: Seül>",
                "<Translation: Seouler: Seüler>",
            ]
        )

    # ---- error testing -----------------------------------------------------

    def test_invalid_lang(self):
        create_samples(
            continent_names=["europe"],
            continent_fields=["name", "denonym"],
            langs=["de"]
        )

        europe = Continent.objects.get(code="EU")
        hierarchy = _get_relations_hierarchy()
        groups = _get_entity_groups(europe, hierarchy)

        with self.assertRaises(ValueError) as error:
            _get_translations(
                groups,
                lang="xx"
            )
        self.assertEqual(
            error.exception.args[0],
            "The language code `xx` is not supported."
        )


class ApplyTranslationsTest(TestCase):
    """Tests for `apply_translations`."""

    # ---- arguments testing -------------------------------------------------

    def test_instance_level_0_relation_no_lang(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        activate("de")

        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code="EU")
        apply_translations(europe)
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europa'
        )
        self.assertEqual(
            europe.denonym,
            'Europäisch'
        )
        self.assertEqual(
            germany.name,
            'Germany'
        )
        self.assertEqual(
            germany.denonym,
            'German'
        )
        self.assertEqual(
            cologne.name,
            'Cologne'
        )
        self.assertEqual(
            cologne.denonym,
            'Cologner'
        )

    def test_instance_level_1_relation_no_lang(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        activate("de")

        lvl_1 = ('countries',)
        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code="EU")
        apply_translations(europe, *lvl_1)
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europa'
        )
        self.assertEqual(
            europe.denonym,
            'Europäisch'
        )
        self.assertEqual(
            germany.name,
            'Deutschland'
        )
        self.assertEqual(
            germany.denonym,
            'Deutsche'
        )
        self.assertEqual(
            cologne.name,
            'Cologne'
        )
        self.assertEqual(
            cologne.denonym,
            'Cologner'
        )

    def test_instance_level_2_relation_no_lang(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        activate("de")

        lvl_2 = ('countries__cities',)
        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code="EU")
        apply_translations(europe, *lvl_2)
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europa'
        )
        self.assertEqual(
            europe.denonym,
            'Europäisch'
        )
        self.assertEqual(
            germany.name,
            'Germany'
        )
        self.assertEqual(
            germany.denonym,
            'German'
        )
        self.assertEqual(
            cologne.name,
            'Köln'
        )
        self.assertEqual(
            cologne.denonym,
            'Kölner'
        )

    def test_instance_level_1_2_relation_no_lang(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        activate("de")

        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code="EU")
        apply_translations(europe, *lvl_1_2)
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europa'
        )
        self.assertEqual(
            europe.denonym,
            'Europäisch'
        )
        self.assertEqual(
            germany.name,
            'Deutschland'
        )
        self.assertEqual(
            germany.denonym,
            'Deutsche'
        )
        self.assertEqual(
            cologne.name,
            'Köln'
        )
        self.assertEqual(
            cologne.denonym,
            'Kölner'
        )

    def test_instance_level_0_relation_with_lang(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code="EU")
        apply_translations(europe, lang="de")
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europa'
        )
        self.assertEqual(
            europe.denonym,
            'Europäisch'
        )
        self.assertEqual(
            germany.name,
            'Germany'
        )
        self.assertEqual(
            germany.denonym,
            'German'
        )
        self.assertEqual(
            cologne.name,
            'Cologne'
        )
        self.assertEqual(
            cologne.denonym,
            'Cologner'
        )

    def test_instance_level_1_relation_with_lang(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        lvl_1 = ('countries',)
        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code="EU")
        apply_translations(europe, *lvl_1, lang="de")
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europa'
        )
        self.assertEqual(
            europe.denonym,
            'Europäisch'
        )
        self.assertEqual(
            germany.name,
            'Deutschland'
        )
        self.assertEqual(
            germany.denonym,
            'Deutsche'
        )
        self.assertEqual(
            cologne.name,
            'Cologne'
        )
        self.assertEqual(
            cologne.denonym,
            'Cologner'
        )

    def test_instance_level_2_relation_with_lang(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        lvl_2 = ('countries__cities',)
        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code="EU")
        apply_translations(europe, *lvl_2, lang="de")
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europa'
        )
        self.assertEqual(
            europe.denonym,
            'Europäisch'
        )
        self.assertEqual(
            germany.name,
            'Germany'
        )
        self.assertEqual(
            germany.denonym,
            'German'
        )
        self.assertEqual(
            cologne.name,
            'Köln'
        )
        self.assertEqual(
            cologne.denonym,
            'Kölner'
        )

    def test_instance_level_1_2_relation_with_lang(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code="EU")
        apply_translations(europe, *lvl_1_2, lang="de")
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europa'
        )
        self.assertEqual(
            europe.denonym,
            'Europäisch'
        )
        self.assertEqual(
            germany.name,
            'Deutschland'
        )
        self.assertEqual(
            germany.denonym,
            'Deutsche'
        )
        self.assertEqual(
            cologne.name,
            'Köln'
        )
        self.assertEqual(
            cologne.denonym,
            'Kölner'
        )

    def test_queryset_level_0_relation_no_lang(self):
        create_samples(
            continent_names=["europe", "asia"],
            country_names=["germany", "south korea"],
            city_names=["cologne", "seoul"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        activate("de")

        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.prefetch_related(*lvl_1_2).all()
        apply_translations(continents)
        europe = [x for x in continents if x.code == 'EU'][0]
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]
        asia = [x for x in continents if x.code == 'AS'][0]
        south_korea = asia.countries.all()[0]
        seoul = south_korea.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europa'
        )
        self.assertEqual(
            europe.denonym,
            'Europäisch'
        )
        self.assertEqual(
            germany.name,
            'Germany'
        )
        self.assertEqual(
            germany.denonym,
            'German'
        )
        self.assertEqual(
            cologne.name,
            'Cologne'
        )
        self.assertEqual(
            cologne.denonym,
            'Cologner'
        )
        self.assertEqual(
            asia.name,
            'Asien'
        )
        self.assertEqual(
            asia.denonym,
            'Asiatisch'
        )
        self.assertEqual(
            south_korea.name,
            'South Korea'
        )
        self.assertEqual(
            south_korea.denonym,
            'South Korean'
        )
        self.assertEqual(
            seoul.name,
            'Seoul'
        )
        self.assertEqual(
            seoul.denonym,
            'Seouler'
        )

    def test_queryset_level_1_relation_no_lang(self):
        create_samples(
            continent_names=["europe", "asia"],
            country_names=["germany", "south korea"],
            city_names=["cologne", "seoul"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        activate("de")

        lvl_1 = ('countries',)
        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.prefetch_related(*lvl_1_2).all()
        apply_translations(continents, *lvl_1)
        europe = [x for x in continents if x.code == 'EU'][0]
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]
        asia = [x for x in continents if x.code == 'AS'][0]
        south_korea = asia.countries.all()[0]
        seoul = south_korea.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europa'
        )
        self.assertEqual(
            europe.denonym,
            'Europäisch'
        )
        self.assertEqual(
            germany.name,
            'Deutschland'
        )
        self.assertEqual(
            germany.denonym,
            'Deutsche'
        )
        self.assertEqual(
            cologne.name,
            'Cologne'
        )
        self.assertEqual(
            cologne.denonym,
            'Cologner'
        )
        self.assertEqual(
            asia.name,
            'Asien'
        )
        self.assertEqual(
            asia.denonym,
            'Asiatisch'
        )
        self.assertEqual(
            south_korea.name,
            'Südkorea'
        )
        self.assertEqual(
            south_korea.denonym,
            'Südkoreanisch'
        )
        self.assertEqual(
            seoul.name,
            'Seoul'
        )
        self.assertEqual(
            seoul.denonym,
            'Seouler'
        )

    def test_queryset_level_2_relation_no_lang(self):
        create_samples(
            continent_names=["europe", "asia"],
            country_names=["germany", "south korea"],
            city_names=["cologne", "seoul"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        activate("de")

        lvl_2 = ('countries__cities',)
        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.prefetch_related(*lvl_1_2).all()
        apply_translations(continents, *lvl_2)
        europe = [x for x in continents if x.code == 'EU'][0]
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]
        asia = [x for x in continents if x.code == 'AS'][0]
        south_korea = asia.countries.all()[0]
        seoul = south_korea.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europa'
        )
        self.assertEqual(
            europe.denonym,
            'Europäisch'
        )
        self.assertEqual(
            germany.name,
            'Germany'
        )
        self.assertEqual(
            germany.denonym,
            'German'
        )
        self.assertEqual(
            cologne.name,
            'Köln'
        )
        self.assertEqual(
            cologne.denonym,
            'Kölner'
        )
        self.assertEqual(
            asia.name,
            'Asien'
        )
        self.assertEqual(
            asia.denonym,
            'Asiatisch'
        )
        self.assertEqual(
            south_korea.name,
            'South Korea'
        )
        self.assertEqual(
            south_korea.denonym,
            'South Korean'
        )
        self.assertEqual(
            seoul.name,
            'Seül'
        )
        self.assertEqual(
            seoul.denonym,
            'Seüler'
        )

    def test_queryset_level_1_2_relation_no_lang(self):
        create_samples(
            continent_names=["europe", "asia"],
            country_names=["germany", "south korea"],
            city_names=["cologne", "seoul"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        activate("de")

        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.prefetch_related(*lvl_1_2).all()
        apply_translations(continents, *lvl_1_2)
        europe = [x for x in continents if x.code == 'EU'][0]
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]
        asia = [x for x in continents if x.code == 'AS'][0]
        south_korea = asia.countries.all()[0]
        seoul = south_korea.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europa'
        )
        self.assertEqual(
            europe.denonym,
            'Europäisch'
        )
        self.assertEqual(
            germany.name,
            'Deutschland'
        )
        self.assertEqual(
            germany.denonym,
            'Deutsche'
        )
        self.assertEqual(
            cologne.name,
            'Köln'
        )
        self.assertEqual(
            cologne.denonym,
            'Kölner'
        )
        self.assertEqual(
            asia.name,
            'Asien'
        )
        self.assertEqual(
            asia.denonym,
            'Asiatisch'
        )
        self.assertEqual(
            south_korea.name,
            'Südkorea'
        )
        self.assertEqual(
            south_korea.denonym,
            'Südkoreanisch'
        )
        self.assertEqual(
            seoul.name,
            'Seül'
        )
        self.assertEqual(
            seoul.denonym,
            'Seüler'
        )

    def test_queryset_level_0_relation_with_lang(self):
        create_samples(
            continent_names=["europe", "asia"],
            country_names=["germany", "south korea"],
            city_names=["cologne", "seoul"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.prefetch_related(*lvl_1_2).all()
        apply_translations(continents, lang="de")
        europe = [x for x in continents if x.code == 'EU'][0]
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]
        asia = [x for x in continents if x.code == 'AS'][0]
        south_korea = asia.countries.all()[0]
        seoul = south_korea.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europa'
        )
        self.assertEqual(
            europe.denonym,
            'Europäisch'
        )
        self.assertEqual(
            germany.name,
            'Germany'
        )
        self.assertEqual(
            germany.denonym,
            'German'
        )
        self.assertEqual(
            cologne.name,
            'Cologne'
        )
        self.assertEqual(
            cologne.denonym,
            'Cologner'
        )
        self.assertEqual(
            asia.name,
            'Asien'
        )
        self.assertEqual(
            asia.denonym,
            'Asiatisch'
        )
        self.assertEqual(
            south_korea.name,
            'South Korea'
        )
        self.assertEqual(
            south_korea.denonym,
            'South Korean'
        )
        self.assertEqual(
            seoul.name,
            'Seoul'
        )
        self.assertEqual(
            seoul.denonym,
            'Seouler'
        )

    def test_queryset_level_1_relation_with_lang(self):
        create_samples(
            continent_names=["europe", "asia"],
            country_names=["germany", "south korea"],
            city_names=["cologne", "seoul"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        lvl_1 = ('countries',)
        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.prefetch_related(*lvl_1_2).all()
        apply_translations(continents, *lvl_1, lang="de")
        europe = [x for x in continents if x.code == 'EU'][0]
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]
        asia = [x for x in continents if x.code == 'AS'][0]
        south_korea = asia.countries.all()[0]
        seoul = south_korea.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europa'
        )
        self.assertEqual(
            europe.denonym,
            'Europäisch'
        )
        self.assertEqual(
            germany.name,
            'Deutschland'
        )
        self.assertEqual(
            germany.denonym,
            'Deutsche'
        )
        self.assertEqual(
            cologne.name,
            'Cologne'
        )
        self.assertEqual(
            cologne.denonym,
            'Cologner'
        )
        self.assertEqual(
            asia.name,
            'Asien'
        )
        self.assertEqual(
            asia.denonym,
            'Asiatisch'
        )
        self.assertEqual(
            south_korea.name,
            'Südkorea'
        )
        self.assertEqual(
            south_korea.denonym,
            'Südkoreanisch'
        )
        self.assertEqual(
            seoul.name,
            'Seoul'
        )
        self.assertEqual(
            seoul.denonym,
            'Seouler'
        )

    def test_queryset_level_2_relation_with_lang(self):
        create_samples(
            continent_names=["europe", "asia"],
            country_names=["germany", "south korea"],
            city_names=["cologne", "seoul"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        lvl_2 = ('countries__cities',)
        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.prefetch_related(*lvl_1_2).all()
        apply_translations(continents, *lvl_2, lang="de")
        europe = [x for x in continents if x.code == 'EU'][0]
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]
        asia = [x for x in continents if x.code == 'AS'][0]
        south_korea = asia.countries.all()[0]
        seoul = south_korea.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europa'
        )
        self.assertEqual(
            europe.denonym,
            'Europäisch'
        )
        self.assertEqual(
            germany.name,
            'Germany'
        )
        self.assertEqual(
            germany.denonym,
            'German'
        )
        self.assertEqual(
            cologne.name,
            'Köln'
        )
        self.assertEqual(
            cologne.denonym,
            'Kölner'
        )
        self.assertEqual(
            asia.name,
            'Asien'
        )
        self.assertEqual(
            asia.denonym,
            'Asiatisch'
        )
        self.assertEqual(
            south_korea.name,
            'South Korea'
        )
        self.assertEqual(
            south_korea.denonym,
            'South Korean'
        )
        self.assertEqual(
            seoul.name,
            'Seül'
        )
        self.assertEqual(
            seoul.denonym,
            'Seüler'
        )

    def test_queryset_level_1_2_relation_with_lang(self):
        create_samples(
            continent_names=["europe", "asia"],
            country_names=["germany", "south korea"],
            city_names=["cologne", "seoul"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.prefetch_related(*lvl_1_2).all()
        apply_translations(continents, *lvl_1_2, lang="de")
        europe = [x for x in continents if x.code == 'EU'][0]
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]
        asia = [x for x in continents if x.code == 'AS'][0]
        south_korea = asia.countries.all()[0]
        seoul = south_korea.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europa'
        )
        self.assertEqual(
            europe.denonym,
            'Europäisch'
        )
        self.assertEqual(
            germany.name,
            'Deutschland'
        )
        self.assertEqual(
            germany.denonym,
            'Deutsche'
        )
        self.assertEqual(
            cologne.name,
            'Köln'
        )
        self.assertEqual(
            cologne.denonym,
            'Kölner'
        )
        self.assertEqual(
            asia.name,
            'Asien'
        )
        self.assertEqual(
            asia.denonym,
            'Asiatisch'
        )
        self.assertEqual(
            south_korea.name,
            'Südkorea'
        )
        self.assertEqual(
            south_korea.denonym,
            'Südkoreanisch'
        )
        self.assertEqual(
            seoul.name,
            'Seül'
        )
        self.assertEqual(
            seoul.denonym,
            'Seüler'
        )

    # ---- error testing -----------------------------------------------------

    def test_invalid_lang(self):
        create_samples(
            continent_names=["europe"],
            continent_fields=["name", "denonym"],
            langs=["de"]
        )

        europe = Continent.objects.get(code="EU")

        with self.assertRaises(ValueError) as error:
            apply_translations(
                europe,
                lang="xx"
            )
        self.assertEqual(
            error.exception.args[0],
            "The language code `xx` is not supported."
        )

    def test_invalid_relation(self):
        create_samples(
            continent_names=["europe"],
            continent_fields=["name", "denonym"],
            langs=["de"]
        )

        europe = Continent.objects.get(code="EU")

        with self.assertRaises(FieldDoesNotExist) as error:
            apply_translations(
                europe,
                'wrong',
                lang="de"
            )
        self.assertEqual(
            error.exception.args[0],
            "Continent has no field named 'wrong'"
        )

    def test_invalid_entity(self):
        class Person:
            def __init__(self, name):
                self.name = name

            def __str__(self):
                return self.name

            def __repr__(self):
                return self.name

        behzad = Person('Behzad')
        with self.assertRaises(TypeError) as error:
            apply_translations(
                behzad,
                lang="de"
            )
        self.assertEqual(
            error.exception.args[0],
            "`Behzad` is neither a model instance nor an iterable of model instances."
        )


class UpdateTranslationsTest(TestCase):
    """Tests for `update_translations`."""

    # ---- arguments testing -------------------------------------------------

    def test_instance_level_0_relation_no_lang(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        activate("de")

        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code="EU")
        apply_translations(europe, *lvl_1_2)
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        # change
        europe.name = 'Europe Name'
        europe.denonym = 'Europe Denonym'
        germany.name = 'Germany Name'
        germany.denonym = 'Germany Denonym'
        cologne.name = 'Cologne Name'
        cologne.denonym = 'Cologne Denonym'
        update_translations(europe)

        # reapply
        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code="EU")
        apply_translations(europe, *lvl_1_2)
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europe Name'
        )
        self.assertEqual(
            europe.denonym,
            'Europe Denonym'
        )
        self.assertEqual(
            germany.name,
            'Deutschland'
        )
        self.assertEqual(
            germany.denonym,
            'Deutsche'
        )
        self.assertEqual(
            cologne.name,
            'Köln'
        )
        self.assertEqual(
            cologne.denonym,
            'Kölner'
        )

    def test_instance_level_1_relation_no_lang(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        activate("de")

        lvl_1 = ('countries',)
        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code="EU")
        apply_translations(europe, *lvl_1_2)
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        # change
        europe.name = 'Europe Name'
        europe.denonym = 'Europe Denonym'
        germany.name = 'Germany Name'
        germany.denonym = 'Germany Denonym'
        cologne.name = 'Cologne Name'
        cologne.denonym = 'Cologne Denonym'
        update_translations(europe, *lvl_1)

        # reapply
        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code="EU")
        apply_translations(europe, *lvl_1_2)
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europe Name'
        )
        self.assertEqual(
            europe.denonym,
            'Europe Denonym'
        )
        self.assertEqual(
            germany.name,
            'Germany Name'
        )
        self.assertEqual(
            germany.denonym,
            'Germany Denonym'
        )
        self.assertEqual(
            cologne.name,
            'Köln'
        )
        self.assertEqual(
            cologne.denonym,
            'Kölner'
        )

    def test_instance_level_2_relation_no_lang(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        activate("de")

        lvl_2 = ('countries__cities',)
        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code="EU")
        apply_translations(europe, *lvl_1_2)
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        # change
        europe.name = 'Europe Name'
        europe.denonym = 'Europe Denonym'
        germany.name = 'Germany Name'
        germany.denonym = 'Germany Denonym'
        cologne.name = 'Cologne Name'
        cologne.denonym = 'Cologne Denonym'
        update_translations(europe, *lvl_2)

        # reapply
        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code="EU")
        apply_translations(europe, *lvl_1_2)
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europe Name'
        )
        self.assertEqual(
            europe.denonym,
            'Europe Denonym'
        )
        self.assertEqual(
            germany.name,
            'Deutschland'
        )
        self.assertEqual(
            germany.denonym,
            'Deutsche'
        )
        self.assertEqual(
            cologne.name,
            'Cologne Name'
        )
        self.assertEqual(
            cologne.denonym,
            'Cologne Denonym'
        )

    def test_instance_level_1_2_relation_no_lang(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        activate("de")

        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code="EU")
        apply_translations(europe, *lvl_1_2)
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        # change
        europe.name = 'Europe Name'
        europe.denonym = 'Europe Denonym'
        germany.name = 'Germany Name'
        germany.denonym = 'Germany Denonym'
        cologne.name = 'Cologne Name'
        cologne.denonym = 'Cologne Denonym'
        update_translations(europe, *lvl_1_2)

        # reapply
        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code="EU")
        apply_translations(europe, *lvl_1_2)
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europe Name'
        )
        self.assertEqual(
            europe.denonym,
            'Europe Denonym'
        )
        self.assertEqual(
            germany.name,
            'Germany Name'
        )
        self.assertEqual(
            germany.denonym,
            'Germany Denonym'
        )
        self.assertEqual(
            cologne.name,
            'Cologne Name'
        )
        self.assertEqual(
            cologne.denonym,
            'Cologne Denonym'
        )

    def test_instance_level_0_relation_with_lang(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code="EU")
        apply_translations(europe, *lvl_1_2, lang="de")
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        # change
        europe.name = 'Europe Name'
        europe.denonym = 'Europe Denonym'
        germany.name = 'Germany Name'
        germany.denonym = 'Germany Denonym'
        cologne.name = 'Cologne Name'
        cologne.denonym = 'Cologne Denonym'
        update_translations(europe, lang="de")

        # reapply
        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code="EU")
        apply_translations(europe, *lvl_1_2, lang="de")
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europe Name'
        )
        self.assertEqual(
            europe.denonym,
            'Europe Denonym'
        )
        self.assertEqual(
            germany.name,
            'Deutschland'
        )
        self.assertEqual(
            germany.denonym,
            'Deutsche'
        )
        self.assertEqual(
            cologne.name,
            'Köln'
        )
        self.assertEqual(
            cologne.denonym,
            'Kölner'
        )

    def test_instance_level_1_relation_with_lang(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        lvl_1 = ('countries',)
        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code="EU")
        apply_translations(europe, *lvl_1_2, lang="de")
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        # change
        europe.name = 'Europe Name'
        europe.denonym = 'Europe Denonym'
        germany.name = 'Germany Name'
        germany.denonym = 'Germany Denonym'
        cologne.name = 'Cologne Name'
        cologne.denonym = 'Cologne Denonym'
        update_translations(europe, *lvl_1, lang="de")

        # reapply
        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code="EU")
        apply_translations(europe, *lvl_1_2, lang="de")
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europe Name'
        )
        self.assertEqual(
            europe.denonym,
            'Europe Denonym'
        )
        self.assertEqual(
            germany.name,
            'Germany Name'
        )
        self.assertEqual(
            germany.denonym,
            'Germany Denonym'
        )
        self.assertEqual(
            cologne.name,
            'Köln'
        )
        self.assertEqual(
            cologne.denonym,
            'Kölner'
        )

    def test_instance_level_2_relation_with_lang(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        lvl_2 = ('countries__cities',)
        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code="EU")
        apply_translations(europe, *lvl_1_2, lang="de")
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        # change
        europe.name = 'Europe Name'
        europe.denonym = 'Europe Denonym'
        germany.name = 'Germany Name'
        germany.denonym = 'Germany Denonym'
        cologne.name = 'Cologne Name'
        cologne.denonym = 'Cologne Denonym'
        update_translations(europe, *lvl_2, lang="de")

        # reapply
        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code="EU")
        apply_translations(europe, *lvl_1_2, lang="de")
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europe Name'
        )
        self.assertEqual(
            europe.denonym,
            'Europe Denonym'
        )
        self.assertEqual(
            germany.name,
            'Deutschland'
        )
        self.assertEqual(
            germany.denonym,
            'Deutsche'
        )
        self.assertEqual(
            cologne.name,
            'Cologne Name'
        )
        self.assertEqual(
            cologne.denonym,
            'Cologne Denonym'
        )

    def test_instance_level_1_2_relation_with_lang(self):
        create_samples(
            continent_names=["europe"],
            country_names=["germany"],
            city_names=["cologne"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code="EU")
        apply_translations(europe, *lvl_1_2, lang="de")
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        # change
        europe.name = 'Europe Name'
        europe.denonym = 'Europe Denonym'
        germany.name = 'Germany Name'
        germany.denonym = 'Germany Denonym'
        cologne.name = 'Cologne Name'
        cologne.denonym = 'Cologne Denonym'
        update_translations(europe, *lvl_1_2, lang="de")

        # reapply
        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code="EU")
        apply_translations(europe, *lvl_1_2, lang="de")
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europe Name'
        )
        self.assertEqual(
            europe.denonym,
            'Europe Denonym'
        )
        self.assertEqual(
            germany.name,
            'Germany Name'
        )
        self.assertEqual(
            germany.denonym,
            'Germany Denonym'
        )
        self.assertEqual(
            cologne.name,
            'Cologne Name'
        )
        self.assertEqual(
            cologne.denonym,
            'Cologne Denonym'
        )

    def test_queryset_level_0_relation_no_lang(self):
        create_samples(
            continent_names=["europe", "asia"],
            country_names=["germany", "south korea"],
            city_names=["cologne", "seoul"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        activate("de")

        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.prefetch_related(*lvl_1_2).all()
        apply_translations(continents, *lvl_1_2)
        europe = [x for x in continents if x.code == 'EU'][0]
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]
        asia = [x for x in continents if x.code == 'AS'][0]
        south_korea = asia.countries.all()[0]
        seoul = south_korea.cities.all()[0]

        # change
        europe.name = 'Europe Name'
        europe.denonym = 'Europe Denonym'
        germany.name = 'Germany Name'
        germany.denonym = 'Germany Denonym'
        cologne.name = 'Cologne Name'
        cologne.denonym = 'Cologne Denonym'
        asia.name = 'Asia Name'
        asia.denonym = 'Asia Denonym'
        south_korea.name = 'South Korea Name'
        south_korea.denonym = 'South Korea Denonym'
        seoul.name = 'Seoul Name'
        seoul.denonym = 'Seoul Denonym'
        update_translations(continents)

        # reapply
        continents = Continent.objects.prefetch_related(*lvl_1_2).all()
        apply_translations(continents, *lvl_1_2)
        europe = [x for x in continents if x.code == 'EU'][0]
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]
        asia = [x for x in continents if x.code == 'AS'][0]
        south_korea = asia.countries.all()[0]
        seoul = south_korea.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europe Name'
        )
        self.assertEqual(
            europe.denonym,
            'Europe Denonym'
        )
        self.assertEqual(
            germany.name,
            'Deutschland'
        )
        self.assertEqual(
            germany.denonym,
            'Deutsche'
        )
        self.assertEqual(
            cologne.name,
            'Köln'
        )
        self.assertEqual(
            cologne.denonym,
            'Kölner'
        )
        self.assertEqual(
            asia.name,
            'Asia Name'
        )
        self.assertEqual(
            asia.denonym,
            'Asia Denonym'
        )
        self.assertEqual(
            south_korea.name,
            'Südkorea'
        )
        self.assertEqual(
            south_korea.denonym,
            'Südkoreanisch'
        )
        self.assertEqual(
            seoul.name,
            'Seül'
        )
        self.assertEqual(
            seoul.denonym,
            'Seüler'
        )

    def test_queryset_level_1_relation_no_lang(self):
        create_samples(
            continent_names=["europe", "asia"],
            country_names=["germany", "south korea"],
            city_names=["cologne", "seoul"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        activate("de")

        lvl_1 = ('countries',)
        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.prefetch_related(*lvl_1_2).all()
        apply_translations(continents, *lvl_1_2)
        europe = [x for x in continents if x.code == 'EU'][0]
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]
        asia = [x for x in continents if x.code == 'AS'][0]
        south_korea = asia.countries.all()[0]
        seoul = south_korea.cities.all()[0]

        # change
        europe.name = 'Europe Name'
        europe.denonym = 'Europe Denonym'
        germany.name = 'Germany Name'
        germany.denonym = 'Germany Denonym'
        cologne.name = 'Cologne Name'
        cologne.denonym = 'Cologne Denonym'
        asia.name = 'Asia Name'
        asia.denonym = 'Asia Denonym'
        south_korea.name = 'South Korea Name'
        south_korea.denonym = 'South Korea Denonym'
        seoul.name = 'Seoul Name'
        seoul.denonym = 'Seoul Denonym'
        update_translations(continents, *lvl_1)

        # reapply
        continents = Continent.objects.prefetch_related(*lvl_1_2).all()
        apply_translations(continents, *lvl_1_2)
        europe = [x for x in continents if x.code == 'EU'][0]
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]
        asia = [x for x in continents if x.code == 'AS'][0]
        south_korea = asia.countries.all()[0]
        seoul = south_korea.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europe Name'
        )
        self.assertEqual(
            europe.denonym,
            'Europe Denonym'
        )
        self.assertEqual(
            germany.name,
            'Germany Name'
        )
        self.assertEqual(
            germany.denonym,
            'Germany Denonym'
        )
        self.assertEqual(
            cologne.name,
            'Köln'
        )
        self.assertEqual(
            cologne.denonym,
            'Kölner'
        )
        self.assertEqual(
            asia.name,
            'Asia Name'
        )
        self.assertEqual(
            asia.denonym,
            'Asia Denonym'
        )
        self.assertEqual(
            south_korea.name,
            'South Korea Name'
        )
        self.assertEqual(
            south_korea.denonym,
            'South Korea Denonym'
        )
        self.assertEqual(
            seoul.name,
            'Seül'
        )
        self.assertEqual(
            seoul.denonym,
            'Seüler'
        )

    def test_queryset_level_2_relation_no_lang(self):
        create_samples(
            continent_names=["europe", "asia"],
            country_names=["germany", "south korea"],
            city_names=["cologne", "seoul"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        activate("de")

        lvl_2 = ('countries__cities',)
        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.prefetch_related(*lvl_1_2).all()
        apply_translations(continents, *lvl_1_2)
        europe = [x for x in continents if x.code == 'EU'][0]
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]
        asia = [x for x in continents if x.code == 'AS'][0]
        south_korea = asia.countries.all()[0]
        seoul = south_korea.cities.all()[0]

        # change
        europe.name = 'Europe Name'
        europe.denonym = 'Europe Denonym'
        germany.name = 'Germany Name'
        germany.denonym = 'Germany Denonym'
        cologne.name = 'Cologne Name'
        cologne.denonym = 'Cologne Denonym'
        asia.name = 'Asia Name'
        asia.denonym = 'Asia Denonym'
        south_korea.name = 'South Korea Name'
        south_korea.denonym = 'South Korea Denonym'
        seoul.name = 'Seoul Name'
        seoul.denonym = 'Seoul Denonym'
        update_translations(continents, *lvl_2)

        # reapply
        continents = Continent.objects.prefetch_related(*lvl_1_2).all()
        apply_translations(continents, *lvl_1_2)
        europe = [x for x in continents if x.code == 'EU'][0]
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]
        asia = [x for x in continents if x.code == 'AS'][0]
        south_korea = asia.countries.all()[0]
        seoul = south_korea.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europe Name'
        )
        self.assertEqual(
            europe.denonym,
            'Europe Denonym'
        )
        self.assertEqual(
            germany.name,
            'Deutschland'
        )
        self.assertEqual(
            germany.denonym,
            'Deutsche'
        )
        self.assertEqual(
            cologne.name,
            'Cologne Name'
        )
        self.assertEqual(
            cologne.denonym,
            'Cologne Denonym'
        )
        self.assertEqual(
            asia.name,
            'Asia Name'
        )
        self.assertEqual(
            asia.denonym,
            'Asia Denonym'
        )
        self.assertEqual(
            south_korea.name,
            'Südkorea'
        )
        self.assertEqual(
            south_korea.denonym,
            'Südkoreanisch'
        )
        self.assertEqual(
            seoul.name,
            'Seoul Name'
        )
        self.assertEqual(
            seoul.denonym,
            'Seoul Denonym'
        )

    def test_queryset_level_1_2_relation_no_lang(self):
        create_samples(
            continent_names=["europe", "asia"],
            country_names=["germany", "south korea"],
            city_names=["cologne", "seoul"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        activate("de")

        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.prefetch_related(*lvl_1_2).all()
        apply_translations(continents, *lvl_1_2)
        europe = [x for x in continents if x.code == 'EU'][0]
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]
        asia = [x for x in continents if x.code == 'AS'][0]
        south_korea = asia.countries.all()[0]
        seoul = south_korea.cities.all()[0]

        # change
        europe.name = 'Europe Name'
        europe.denonym = 'Europe Denonym'
        germany.name = 'Germany Name'
        germany.denonym = 'Germany Denonym'
        cologne.name = 'Cologne Name'
        cologne.denonym = 'Cologne Denonym'
        asia.name = 'Asia Name'
        asia.denonym = 'Asia Denonym'
        south_korea.name = 'South Korea Name'
        south_korea.denonym = 'South Korea Denonym'
        seoul.name = 'Seoul Name'
        seoul.denonym = 'Seoul Denonym'
        update_translations(continents, *lvl_1_2)

        # reapply
        continents = Continent.objects.prefetch_related(*lvl_1_2).all()
        apply_translations(continents, *lvl_1_2)
        europe = [x for x in continents if x.code == 'EU'][0]
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]
        asia = [x for x in continents if x.code == 'AS'][0]
        south_korea = asia.countries.all()[0]
        seoul = south_korea.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europe Name'
        )
        self.assertEqual(
            europe.denonym,
            'Europe Denonym'
        )
        self.assertEqual(
            germany.name,
            'Germany Name'
        )
        self.assertEqual(
            germany.denonym,
            'Germany Denonym'
        )
        self.assertEqual(
            cologne.name,
            'Cologne Name'
        )
        self.assertEqual(
            cologne.denonym,
            'Cologne Denonym'
        )
        self.assertEqual(
            asia.name,
            'Asia Name'
        )
        self.assertEqual(
            asia.denonym,
            'Asia Denonym'
        )
        self.assertEqual(
            south_korea.name,
            'South Korea Name'
        )
        self.assertEqual(
            south_korea.denonym,
            'South Korea Denonym'
        )
        self.assertEqual(
            seoul.name,
            'Seoul Name'
        )
        self.assertEqual(
            seoul.denonym,
            'Seoul Denonym'
        )

    def test_queryset_level_0_relation_with_lang(self):
        create_samples(
            continent_names=["europe", "asia"],
            country_names=["germany", "south korea"],
            city_names=["cologne", "seoul"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.prefetch_related(*lvl_1_2).all()
        apply_translations(continents, *lvl_1_2, lang="de")
        europe = [x for x in continents if x.code == 'EU'][0]
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]
        asia = [x for x in continents if x.code == 'AS'][0]
        south_korea = asia.countries.all()[0]
        seoul = south_korea.cities.all()[0]

        # change
        europe.name = 'Europe Name'
        europe.denonym = 'Europe Denonym'
        germany.name = 'Germany Name'
        germany.denonym = 'Germany Denonym'
        cologne.name = 'Cologne Name'
        cologne.denonym = 'Cologne Denonym'
        asia.name = 'Asia Name'
        asia.denonym = 'Asia Denonym'
        south_korea.name = 'South Korea Name'
        south_korea.denonym = 'South Korea Denonym'
        seoul.name = 'Seoul Name'
        seoul.denonym = 'Seoul Denonym'
        update_translations(continents, lang="de")

        # reapply
        continents = Continent.objects.prefetch_related(*lvl_1_2).all()
        apply_translations(continents, *lvl_1_2, lang="de")
        europe = [x for x in continents if x.code == 'EU'][0]
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]
        asia = [x for x in continents if x.code == 'AS'][0]
        south_korea = asia.countries.all()[0]
        seoul = south_korea.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europe Name'
        )
        self.assertEqual(
            europe.denonym,
            'Europe Denonym'
        )
        self.assertEqual(
            germany.name,
            'Deutschland'
        )
        self.assertEqual(
            germany.denonym,
            'Deutsche'
        )
        self.assertEqual(
            cologne.name,
            'Köln'
        )
        self.assertEqual(
            cologne.denonym,
            'Kölner'
        )
        self.assertEqual(
            asia.name,
            'Asia Name'
        )
        self.assertEqual(
            asia.denonym,
            'Asia Denonym'
        )
        self.assertEqual(
            south_korea.name,
            'Südkorea'
        )
        self.assertEqual(
            south_korea.denonym,
            'Südkoreanisch'
        )
        self.assertEqual(
            seoul.name,
            'Seül'
        )
        self.assertEqual(
            seoul.denonym,
            'Seüler'
        )

    def test_queryset_level_1_relation_with_lang(self):
        create_samples(
            continent_names=["europe", "asia"],
            country_names=["germany", "south korea"],
            city_names=["cologne", "seoul"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        lvl_1 = ('countries',)
        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.prefetch_related(*lvl_1_2).all()
        apply_translations(continents, *lvl_1_2, lang="de")
        europe = [x for x in continents if x.code == 'EU'][0]
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]
        asia = [x for x in continents if x.code == 'AS'][0]
        south_korea = asia.countries.all()[0]
        seoul = south_korea.cities.all()[0]

        # change
        europe.name = 'Europe Name'
        europe.denonym = 'Europe Denonym'
        germany.name = 'Germany Name'
        germany.denonym = 'Germany Denonym'
        cologne.name = 'Cologne Name'
        cologne.denonym = 'Cologne Denonym'
        asia.name = 'Asia Name'
        asia.denonym = 'Asia Denonym'
        south_korea.name = 'South Korea Name'
        south_korea.denonym = 'South Korea Denonym'
        seoul.name = 'Seoul Name'
        seoul.denonym = 'Seoul Denonym'
        update_translations(continents, *lvl_1, lang="de")

        # reapply
        continents = Continent.objects.prefetch_related(*lvl_1_2).all()
        apply_translations(continents, *lvl_1_2, lang="de")
        europe = [x for x in continents if x.code == 'EU'][0]
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]
        asia = [x for x in continents if x.code == 'AS'][0]
        south_korea = asia.countries.all()[0]
        seoul = south_korea.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europe Name'
        )
        self.assertEqual(
            europe.denonym,
            'Europe Denonym'
        )
        self.assertEqual(
            germany.name,
            'Germany Name'
        )
        self.assertEqual(
            germany.denonym,
            'Germany Denonym'
        )
        self.assertEqual(
            cologne.name,
            'Köln'
        )
        self.assertEqual(
            cologne.denonym,
            'Kölner'
        )
        self.assertEqual(
            asia.name,
            'Asia Name'
        )
        self.assertEqual(
            asia.denonym,
            'Asia Denonym'
        )
        self.assertEqual(
            south_korea.name,
            'South Korea Name'
        )
        self.assertEqual(
            south_korea.denonym,
            'South Korea Denonym'
        )
        self.assertEqual(
            seoul.name,
            'Seül'
        )
        self.assertEqual(
            seoul.denonym,
            'Seüler'
        )

    def test_queryset_level_2_relation_with_lang(self):
        create_samples(
            continent_names=["europe", "asia"],
            country_names=["germany", "south korea"],
            city_names=["cologne", "seoul"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        lvl_2 = ('countries__cities',)
        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.prefetch_related(*lvl_1_2).all()
        apply_translations(continents, *lvl_1_2, lang="de")
        europe = [x for x in continents if x.code == 'EU'][0]
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]
        asia = [x for x in continents if x.code == 'AS'][0]
        south_korea = asia.countries.all()[0]
        seoul = south_korea.cities.all()[0]

        # change
        europe.name = 'Europe Name'
        europe.denonym = 'Europe Denonym'
        germany.name = 'Germany Name'
        germany.denonym = 'Germany Denonym'
        cologne.name = 'Cologne Name'
        cologne.denonym = 'Cologne Denonym'
        asia.name = 'Asia Name'
        asia.denonym = 'Asia Denonym'
        south_korea.name = 'South Korea Name'
        south_korea.denonym = 'South Korea Denonym'
        seoul.name = 'Seoul Name'
        seoul.denonym = 'Seoul Denonym'
        update_translations(continents, *lvl_2, lang="de")

        # reapply
        continents = Continent.objects.prefetch_related(*lvl_1_2).all()
        apply_translations(continents, *lvl_1_2, lang="de")
        europe = [x for x in continents if x.code == 'EU'][0]
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]
        asia = [x for x in continents if x.code == 'AS'][0]
        south_korea = asia.countries.all()[0]
        seoul = south_korea.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europe Name'
        )
        self.assertEqual(
            europe.denonym,
            'Europe Denonym'
        )
        self.assertEqual(
            germany.name,
            'Deutschland'
        )
        self.assertEqual(
            germany.denonym,
            'Deutsche'
        )
        self.assertEqual(
            cologne.name,
            'Cologne Name'
        )
        self.assertEqual(
            cologne.denonym,
            'Cologne Denonym'
        )
        self.assertEqual(
            asia.name,
            'Asia Name'
        )
        self.assertEqual(
            asia.denonym,
            'Asia Denonym'
        )
        self.assertEqual(
            south_korea.name,
            'Südkorea'
        )
        self.assertEqual(
            south_korea.denonym,
            'Südkoreanisch'
        )
        self.assertEqual(
            seoul.name,
            'Seoul Name'
        )
        self.assertEqual(
            seoul.denonym,
            'Seoul Denonym'
        )

    def test_queryset_level_1_2_relation_with_lang(self):
        create_samples(
            continent_names=["europe", "asia"],
            country_names=["germany", "south korea"],
            city_names=["cologne", "seoul"],
            continent_fields=["name", "denonym"],
            country_fields=["name", "denonym"],
            city_fields=["name", "denonym"],
            langs=["de", "tr"]
        )

        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.prefetch_related(*lvl_1_2).all()
        apply_translations(continents, *lvl_1_2, lang="de")
        europe = [x for x in continents if x.code == 'EU'][0]
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]
        asia = [x for x in continents if x.code == 'AS'][0]
        south_korea = asia.countries.all()[0]
        seoul = south_korea.cities.all()[0]

        # change
        europe.name = 'Europe Name'
        europe.denonym = 'Europe Denonym'
        germany.name = 'Germany Name'
        germany.denonym = 'Germany Denonym'
        cologne.name = 'Cologne Name'
        cologne.denonym = 'Cologne Denonym'
        asia.name = 'Asia Name'
        asia.denonym = 'Asia Denonym'
        south_korea.name = 'South Korea Name'
        south_korea.denonym = 'South Korea Denonym'
        seoul.name = 'Seoul Name'
        seoul.denonym = 'Seoul Denonym'
        update_translations(continents, *lvl_1_2, lang="de")

        # reapply
        continents = Continent.objects.prefetch_related(*lvl_1_2).all()
        apply_translations(continents, *lvl_1_2, lang="de")
        europe = [x for x in continents if x.code == 'EU'][0]
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]
        asia = [x for x in continents if x.code == 'AS'][0]
        south_korea = asia.countries.all()[0]
        seoul = south_korea.cities.all()[0]

        self.assertEqual(
            europe.name,
            'Europe Name'
        )
        self.assertEqual(
            europe.denonym,
            'Europe Denonym'
        )
        self.assertEqual(
            germany.name,
            'Germany Name'
        )
        self.assertEqual(
            germany.denonym,
            'Germany Denonym'
        )
        self.assertEqual(
            cologne.name,
            'Cologne Name'
        )
        self.assertEqual(
            cologne.denonym,
            'Cologne Denonym'
        )
        self.assertEqual(
            asia.name,
            'Asia Name'
        )
        self.assertEqual(
            asia.denonym,
            'Asia Denonym'
        )
        self.assertEqual(
            south_korea.name,
            'South Korea Name'
        )
        self.assertEqual(
            south_korea.denonym,
            'South Korea Denonym'
        )
        self.assertEqual(
            seoul.name,
            'Seoul Name'
        )
        self.assertEqual(
            seoul.denonym,
            'Seoul Denonym'
        )

    # ---- error testing -----------------------------------------------------

    def test_invalid_lang(self):
        create_samples(
            continent_names=["europe"],
            continent_fields=["name", "denonym"],
            langs=["de"]
        )

        europe = Continent.objects.get(code="EU")

        with self.assertRaises(ValueError) as error:
            apply_translations(
                europe,
                lang="xx"
            )
        self.assertEqual(
            error.exception.args[0],
            "The language code `xx` is not supported."
        )

    def test_invalid_relation(self):
        create_samples(
            continent_names=["europe"],
            continent_fields=["name", "denonym"],
            langs=["de"]
        )

        europe = Continent.objects.get(code="EU")

        with self.assertRaises(FieldDoesNotExist) as error:
            apply_translations(
                europe,
                'wrong',
                lang="de"
            )
        self.assertEqual(
            error.exception.args[0],
            "Continent has no field named 'wrong'"
        )

    def test_invalid_entity(self):
        class Person:
            def __init__(self, name):
                self.name = name

            def __str__(self):
                return self.name

            def __repr__(self):
                return self.name

        behzad = Person('Behzad')
        with self.assertRaises(TypeError) as error:
            apply_translations(
                behzad,
                lang="de"
            )
        self.assertEqual(
            error.exception.args[0],
            "`Behzad` is neither a model instance nor an iterable of model instances."
        )
