from django.test import TestCase
from django.core.exceptions import FieldDoesNotExist
from django.utils.translation import override

from translations.context import Context

from sample.models import Continent

from tests.sample import create_samples


class ContextTest(TestCase):
    """Tests for `Context`."""

    def test_init_instance_invalid_entity(self):
        class Person:
            def __init__(self, name):
                self.name = name

            def __str__(self):
                return self.name

            def __repr__(self):
                return self.name

        behzad = Person('Behzad')

        with self.assertRaises(TypeError) as error:
            with Context(behzad):
                pass

        self.assertEqual(
            error.exception.args[0],
            ('`Behzad` is neither a model instance nor an iterable of' +
             ' model instances.')
        )

    def test_init_instance_invalid_simple_relation(self):
        create_samples(
            continent_names=['europe'],
            continent_fields=['name', 'denonym'],
            langs=['de']
        )

        europe = Continent.objects.get(code='EU')

        with self.assertRaises(FieldDoesNotExist) as error:
            with Context(europe, 'wrong'):
                pass

        self.assertEqual(
            error.exception.args[0], "Continent has no field named 'wrong'")

    def test_init_instance_invalid_nested_relation(self):
        create_samples(
            continent_names=['europe'],
            country_names=['germany'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            langs=['de']
        )

        europe = Continent.objects.get(code='EU')

        with self.assertRaises(FieldDoesNotExist) as error:
            with Context(europe, 'countries__wrong'):
                pass

        self.assertEqual(
            error.exception.args[0], "Country has no field named 'wrong'")

    def test_init_queryset_invalid_entity(self):
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
            with Context(people):
                pass

        self.assertEqual(
            error.exception.args[0],
            ('`[Behzad, Max]` is neither a model instance nor an iterable of' +
             ' model instances.')
        )

    def test_init_queryset_invalid_simple_relation(self):
        create_samples(
            continent_names=['europe'],
            continent_fields=['name', 'denonym'],
            langs=['de']
        )

        continents = Continent.objects.all()

        with self.assertRaises(FieldDoesNotExist) as error:
            with Context(continents, 'wrong'):
                pass

        self.assertEqual(
            error.exception.args[0], "Continent has no field named 'wrong'")

    def test_init_queryset_invalid_nested_relation(self):
        create_samples(
            continent_names=['europe'],
            country_names=['germany'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            langs=['de']
        )

        continents = Continent.objects.all()

        with self.assertRaises(FieldDoesNotExist) as error:
            with Context(continents, 'countries__wrong'):
                pass

        self.assertEqual(
            error.exception.args[0], "Country has no field named 'wrong'")

    def test_get_changed_fields_instance_level_0_relation(self):
        create_samples(
            continent_names=['europe'],
            country_names=['germany'],
            city_names=['cologne'],
            langs=['de', 'tr']
        )

        europe = Continent.objects.get(code='EU')
        with Context(europe) as context:
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

            europe.name = 'Europe Name'
            europe.denonym = 'Europe Denonym'
            germany.name = 'Germany Name'
            germany.denonym = 'Germany Denonym'
            cologne.name = 'Cologne Name'
            cologne.denonym = 'Cologne Denonym'

        self.assertSetEqual(
            set(info[1] for info in context._get_changed_fields()),
            {
                'Europe Name',
                'Europe Denonym',
            }
        )

    def test_get_changed_fields_instance_level_1_relation(self):
        create_samples(
            continent_names=['europe'],
            country_names=['germany'],
            city_names=['cologne'],
            langs=['de', 'tr']
        )

        lvl_1 = ('countries',)

        europe = Continent.objects.get(code='EU')
        with Context(europe, *lvl_1) as context:
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

            europe.name = 'Europe Name'
            europe.denonym = 'Europe Denonym'
            germany.name = 'Germany Name'
            germany.denonym = 'Germany Denonym'
            cologne.name = 'Cologne Name'
            cologne.denonym = 'Cologne Denonym'

        self.assertSetEqual(
            set(info[1] for info in context._get_changed_fields()),
            {
                'Europe Name',
                'Europe Denonym',
                'Germany Name',
                'Germany Denonym',
            }
        )

    def test_get_changed_fields_instance_level_2_relation(self):
        create_samples(
            continent_names=['europe'],
            country_names=['germany'],
            city_names=['cologne'],
            langs=['de', 'tr']
        )

        lvl_2 = ('countries__cities',)

        europe = Continent.objects.get(code='EU')
        with Context(europe, *lvl_2) as context:
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

            europe.name = 'Europe Name'
            europe.denonym = 'Europe Denonym'
            germany.name = 'Germany Name'
            germany.denonym = 'Germany Denonym'
            cologne.name = 'Cologne Name'
            cologne.denonym = 'Cologne Denonym'

        self.assertSetEqual(
            set(info[1] for info in context._get_changed_fields()),
            {
                'Europe Name',
                'Europe Denonym',
                'Cologne Name',
                'Cologne Denonym',
            }
        )

    def test_get_changed_fields_instance_level_1_2_relation(self):
        create_samples(
            continent_names=['europe'],
            country_names=['germany'],
            city_names=['cologne'],
            langs=['de', 'tr']
        )

        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.get(code='EU')
        with Context(europe, *lvl_1_2) as context:
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

            europe.name = 'Europe Name'
            europe.denonym = 'Europe Denonym'
            germany.name = 'Germany Name'
            germany.denonym = 'Germany Denonym'
            cologne.name = 'Cologne Name'
            cologne.denonym = 'Cologne Denonym'

        self.assertSetEqual(
            set(info[1] for info in context._get_changed_fields()),
            {
                'Europe Name',
                'Europe Denonym',
                'Germany Name',
                'Germany Denonym',
                'Cologne Name',
                'Cologne Denonym',
            }
        )

    def test_get_changed_fields_prefetched_instance_level_0_relation(self):
        create_samples(
            continent_names=['europe'],
            country_names=['germany'],
            city_names=['cologne'],
            langs=['de', 'tr']
        )

        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code='EU')
        with Context(europe) as context:
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

            europe.name = 'Europe Name'
            europe.denonym = 'Europe Denonym'
            germany.name = 'Germany Name'
            germany.denonym = 'Germany Denonym'
            cologne.name = 'Cologne Name'
            cologne.denonym = 'Cologne Denonym'

        self.assertSetEqual(
            set(info[1] for info in context._get_changed_fields()),
            {
                'Europe Name',
                'Europe Denonym',
            }
        )

    def test_get_changed_fields_prefetched_instance_level_1_relation(self):
        create_samples(
            continent_names=['europe'],
            country_names=['germany'],
            city_names=['cologne'],
            langs=['de', 'tr']
        )

        lvl_1 = ('countries',)
        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code='EU')
        with Context(europe, *lvl_1) as context:
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

            europe.name = 'Europe Name'
            europe.denonym = 'Europe Denonym'
            germany.name = 'Germany Name'
            germany.denonym = 'Germany Denonym'
            cologne.name = 'Cologne Name'
            cologne.denonym = 'Cologne Denonym'

        self.assertSetEqual(
            set(info[1] for info in context._get_changed_fields()),
            {
                'Europe Name',
                'Europe Denonym',
                'Germany Name',
                'Germany Denonym',
            }
        )

    def test_get_changed_fields_prefetched_instance_level_2_relation(self):
        create_samples(
            continent_names=['europe'],
            country_names=['germany'],
            city_names=['cologne'],
            langs=['de', 'tr']
        )

        lvl_2 = ('countries__cities',)
        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code='EU')
        with Context(europe, *lvl_2) as context:
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

            europe.name = 'Europe Name'
            europe.denonym = 'Europe Denonym'
            germany.name = 'Germany Name'
            germany.denonym = 'Germany Denonym'
            cologne.name = 'Cologne Name'
            cologne.denonym = 'Cologne Denonym'

        self.assertSetEqual(
            set(info[1] for info in context._get_changed_fields()),
            {
                'Europe Name',
                'Europe Denonym',
                'Cologne Name',
                'Cologne Denonym',
            }
        )

    def test_get_changed_fields_prefetched_instance_level_1_2_relation(self):
        create_samples(
            continent_names=['europe'],
            country_names=['germany'],
            city_names=['cologne'],
            langs=['de', 'tr']
        )

        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code='EU')
        with Context(europe, *lvl_1_2) as context:
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

            europe.name = 'Europe Name'
            europe.denonym = 'Europe Denonym'
            germany.name = 'Germany Name'
            germany.denonym = 'Germany Denonym'
            cologne.name = 'Cologne Name'
            cologne.denonym = 'Cologne Denonym'

        self.assertSetEqual(
            set(info[1] for info in context._get_changed_fields()),
            {
                'Europe Name',
                'Europe Denonym',
                'Germany Name',
                'Germany Denonym',
                'Cologne Name',
                'Cologne Denonym',
            }
        )

    def test_get_changed_fields_queryset_level_0_relation(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            langs=['de', 'tr']
        )

        continents = Continent.objects.all()
        with Context(continents) as context:
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

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

        self.assertSetEqual(
            set(info[1] for info in context._get_changed_fields()),
            {
                'Europe Name',
                'Europe Denonym',
                'Asia Name',
                'Asia Denonym',
            }
        )

    def test_get_changed_fields_queryset_level_1_relation(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            langs=['de', 'tr']
        )

        lvl_1 = ('countries',)

        continents = Continent.objects.all()
        with Context(continents, *lvl_1) as context:
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

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

        self.assertSetEqual(
            set(info[1] for info in context._get_changed_fields()),
            {
                'Europe Name',
                'Europe Denonym',
                'Germany Name',
                'Germany Denonym',
                'Asia Name',
                'Asia Denonym',
                'South Korea Name',
                'South Korea Denonym',
            }
        )

    def test_get_changed_fields_queryset_level_2_relation(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            langs=['de', 'tr']
        )

        lvl_2 = ('countries__cities',)

        continents = Continent.objects.all()
        with Context(continents, *lvl_2) as context:
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

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

        self.assertSetEqual(
            set(info[1] for info in context._get_changed_fields()),
            {
                'Europe Name',
                'Europe Denonym',
                'Cologne Name',
                'Cologne Denonym',
                'Asia Name',
                'Asia Denonym',
                'Seoul Name',
                'Seoul Denonym',
            }
        )

    def test_get_changed_fields_queryset_level_1_2_relation(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            langs=['de', 'tr']
        )

        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.all()
        with Context(continents, *lvl_1_2) as context:
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

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

        self.assertSetEqual(
            set(info[1] for info in context._get_changed_fields()),
            {
                'Europe Name',
                'Europe Denonym',
                'Germany Name',
                'Germany Denonym',
                'Cologne Name',
                'Cologne Denonym',
                'Asia Name',
                'Asia Denonym',
                'South Korea Name',
                'South Korea Denonym',
                'Seoul Name',
                'Seoul Denonym',
            }
        )

    def test_get_changed_fields_prefetched_queryset_level_0_relation(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            langs=['de', 'tr']
        )

        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.prefetch_related(*lvl_1_2)
        with Context(continents) as context:
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

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

        self.assertSetEqual(
            set(info[1] for info in context._get_changed_fields()),
            {
                'Europe Name',
                'Europe Denonym',
                'Asia Name',
                'Asia Denonym',
            }
        )

    def test_get_changed_fields_prefetched_queryset_level_1_relation(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            langs=['de', 'tr']
        )

        lvl_1 = ('countries',)
        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.prefetch_related(*lvl_1_2)
        with Context(continents, *lvl_1) as context:
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

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

        self.assertSetEqual(
            set(info[1] for info in context._get_changed_fields()),
            {
                'Europe Name',
                'Europe Denonym',
                'Germany Name',
                'Germany Denonym',
                'Asia Name',
                'Asia Denonym',
                'South Korea Name',
                'South Korea Denonym',
            }
        )

    def test_get_changed_fields_prefetched_queryset_level_2_relation(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            langs=['de', 'tr']
        )

        lvl_2 = ('countries__cities',)
        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.prefetch_related(*lvl_1_2)
        with Context(continents, *lvl_2) as context:
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

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

        self.assertSetEqual(
            set(info[1] for info in context._get_changed_fields()),
            {
                'Europe Name',
                'Europe Denonym',
                'Cologne Name',
                'Cologne Denonym',
                'Asia Name',
                'Asia Denonym',
                'Seoul Name',
                'Seoul Denonym',
            }
        )

    def test_get_changed_fields_prefetched_queryset_level_1_2_relation(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            langs=['de', 'tr']
        )

        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.prefetch_related(*lvl_1_2)
        with Context(continents, *lvl_1_2) as context:
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

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

        self.assertSetEqual(
            set(info[1] for info in context._get_changed_fields()),
            {
                'Europe Name',
                'Europe Denonym',
                'Germany Name',
                'Germany Denonym',
                'Cologne Name',
                'Cologne Denonym',
                'Asia Name',
                'Asia Denonym',
                'South Korea Name',
                'South Korea Denonym',
                'Seoul Name',
                'Seoul Denonym',
            }
        )

    @override(language='de', deactivate=True)
    def test_create_instance_level_0_relation_no_lang(self):
        create_samples(
            continent_names=['europe'],
            country_names=['germany'],
            city_names=['cologne'],
            langs=['de', 'tr']
        )

        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.get(code='EU')
        with Context(europe) as context:
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

            europe.name = 'Europe Name'
            europe.denonym = 'Europe Denonym'
            germany.name = 'Germany Name'
            germany.denonym = 'Germany Denonym'
            cologne.name = 'Cologne Name'
            cologne.denonym = 'Cologne Denonym'

            context.create()

            europe.name = 'Europe'
            europe.denonym = 'European'
            germany.name = 'Germany'
            germany.denonym = 'German'
            cologne.name = 'Cologne'
            cologne.denonym = 'Cologner'
        with Context(europe, *lvl_1_2) as context:
            context.read()
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europe Name')
        self.assertEqual(europe.denonym, 'Europe Denonym')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')

    @override(language='de', deactivate=True)
    def test_create_instance_level_1_relation_no_lang(self):
        create_samples(
            continent_names=['europe'],
            country_names=['germany'],
            city_names=['cologne'],
            langs=['de', 'tr']
        )

        lvl_1 = ('countries',)
        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.get(code='EU')
        with Context(europe, *lvl_1) as context:
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

            europe.name = 'Europe Name'
            europe.denonym = 'Europe Denonym'
            germany.name = 'Germany Name'
            germany.denonym = 'Germany Denonym'
            cologne.name = 'Cologne Name'
            cologne.denonym = 'Cologne Denonym'

            context.create()

            europe.name = 'Europe'
            europe.denonym = 'European'
            germany.name = 'Germany'
            germany.denonym = 'German'
            cologne.name = 'Cologne'
            cologne.denonym = 'Cologner'
        with Context(europe, *lvl_1_2) as context:
            context.read()
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europe Name')
        self.assertEqual(europe.denonym, 'Europe Denonym')
        self.assertEqual(germany.name, 'Germany Name')
        self.assertEqual(germany.denonym, 'Germany Denonym')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')

    @override(language='de', deactivate=True)
    def test_create_instance_level_2_relation_no_lang(self):
        create_samples(
            continent_names=['europe'],
            country_names=['germany'],
            city_names=['cologne'],
            langs=['de', 'tr']
        )

        lvl_2 = ('countries__cities',)
        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.get(code='EU')
        with Context(europe, *lvl_2) as context:
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

            europe.name = 'Europe Name'
            europe.denonym = 'Europe Denonym'
            germany.name = 'Germany Name'
            germany.denonym = 'Germany Denonym'
            cologne.name = 'Cologne Name'
            cologne.denonym = 'Cologne Denonym'

            context.create()

            europe.name = 'Europe'
            europe.denonym = 'European'
            germany.name = 'Germany'
            germany.denonym = 'German'
            cologne.name = 'Cologne'
            cologne.denonym = 'Cologner'
        with Context(europe, *lvl_1_2) as context:
            context.read()
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europe Name')
        self.assertEqual(europe.denonym, 'Europe Denonym')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Cologne Name')
        self.assertEqual(cologne.denonym, 'Cologne Denonym')

    @override(language='de', deactivate=True)
    def test_create_instance_level_1_2_relation_no_lang(self):
        create_samples(
            continent_names=['europe'],
            country_names=['germany'],
            city_names=['cologne'],
            langs=['de', 'tr']
        )

        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.get(code='EU')
        with Context(europe, *lvl_1_2) as context:
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

            europe.name = 'Europe Name'
            europe.denonym = 'Europe Denonym'
            germany.name = 'Germany Name'
            germany.denonym = 'Germany Denonym'
            cologne.name = 'Cologne Name'
            cologne.denonym = 'Cologne Denonym'

            context.create()

            europe.name = 'Europe'
            europe.denonym = 'European'
            germany.name = 'Germany'
            germany.denonym = 'German'
            cologne.name = 'Cologne'
            cologne.denonym = 'Cologner'
        with Context(europe, *lvl_1_2) as context:
            context.read()
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europe Name')
        self.assertEqual(europe.denonym, 'Europe Denonym')
        self.assertEqual(germany.name, 'Germany Name')
        self.assertEqual(germany.denonym, 'Germany Denonym')
        self.assertEqual(cologne.name, 'Cologne Name')
        self.assertEqual(cologne.denonym, 'Cologne Denonym')

    def test_create_instance_level_0_relation_with_lang(self):
        create_samples(
            continent_names=['europe'],
            country_names=['germany'],
            city_names=['cologne'],
            langs=['de', 'tr']
        )

        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.get(code='EU')
        with Context(europe) as context:
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

            europe.name = 'Europe Name'
            europe.denonym = 'Europe Denonym'
            germany.name = 'Germany Name'
            germany.denonym = 'Germany Denonym'
            cologne.name = 'Cologne Name'
            cologne.denonym = 'Cologne Denonym'

            context.create('de')

            europe.name = 'Europe'
            europe.denonym = 'European'
            germany.name = 'Germany'
            germany.denonym = 'German'
            cologne.name = 'Cologne'
            cologne.denonym = 'Cologner'
        with Context(europe, *lvl_1_2) as context:
            context.read('de')
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europe Name')
        self.assertEqual(europe.denonym, 'Europe Denonym')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')

    def test_create_instance_level_1_relation_with_lang(self):
        create_samples(
            continent_names=['europe'],
            country_names=['germany'],
            city_names=['cologne'],
            langs=['de', 'tr']
        )

        lvl_1 = ('countries',)
        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.get(code='EU')
        with Context(europe, *lvl_1) as context:
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

            europe.name = 'Europe Name'
            europe.denonym = 'Europe Denonym'
            germany.name = 'Germany Name'
            germany.denonym = 'Germany Denonym'
            cologne.name = 'Cologne Name'
            cologne.denonym = 'Cologne Denonym'

            context.create('de')

            europe.name = 'Europe'
            europe.denonym = 'European'
            germany.name = 'Germany'
            germany.denonym = 'German'
            cologne.name = 'Cologne'
            cologne.denonym = 'Cologner'
        with Context(europe, *lvl_1_2) as context:
            context.read('de')
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europe Name')
        self.assertEqual(europe.denonym, 'Europe Denonym')
        self.assertEqual(germany.name, 'Germany Name')
        self.assertEqual(germany.denonym, 'Germany Denonym')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')

    def test_create_instance_level_2_relation_with_lang(self):
        create_samples(
            continent_names=['europe'],
            country_names=['germany'],
            city_names=['cologne'],
            langs=['de', 'tr']
        )

        lvl_2 = ('countries__cities',)
        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.get(code='EU')
        with Context(europe, *lvl_2) as context:
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

            europe.name = 'Europe Name'
            europe.denonym = 'Europe Denonym'
            germany.name = 'Germany Name'
            germany.denonym = 'Germany Denonym'
            cologne.name = 'Cologne Name'
            cologne.denonym = 'Cologne Denonym'

            context.create('de')

            europe.name = 'Europe'
            europe.denonym = 'European'
            germany.name = 'Germany'
            germany.denonym = 'German'
            cologne.name = 'Cologne'
            cologne.denonym = 'Cologner'
        with Context(europe, *lvl_1_2) as context:
            context.read('de')
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europe Name')
        self.assertEqual(europe.denonym, 'Europe Denonym')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Cologne Name')
        self.assertEqual(cologne.denonym, 'Cologne Denonym')

    def test_create_instance_level_1_2_relation_with_lang(self):
        create_samples(
            continent_names=['europe'],
            country_names=['germany'],
            city_names=['cologne'],
            langs=['de', 'tr']
        )

        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.get(code='EU')
        with Context(europe, *lvl_1_2) as context:
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

            europe.name = 'Europe Name'
            europe.denonym = 'Europe Denonym'
            germany.name = 'Germany Name'
            germany.denonym = 'Germany Denonym'
            cologne.name = 'Cologne Name'
            cologne.denonym = 'Cologne Denonym'

            context.create('de')

            europe.name = 'Europe'
            europe.denonym = 'European'
            germany.name = 'Germany'
            germany.denonym = 'German'
            cologne.name = 'Cologne'
            cologne.denonym = 'Cologner'
        with Context(europe, *lvl_1_2) as context:
            context.read('de')
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europe Name')
        self.assertEqual(europe.denonym, 'Europe Denonym')
        self.assertEqual(germany.name, 'Germany Name')
        self.assertEqual(germany.denonym, 'Germany Denonym')
        self.assertEqual(cologne.name, 'Cologne Name')
        self.assertEqual(cologne.denonym, 'Cologne Denonym')

    @override(language='de', deactivate=True)
    def test_create_prefetched_instance_level_0_relation_no_lang(self):
        create_samples(
            continent_names=['europe'],
            country_names=['germany'],
            city_names=['cologne'],
            langs=['de', 'tr']
        )

        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code='EU')
        with Context(europe) as context:
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

            europe.name = 'Europe Name'
            europe.denonym = 'Europe Denonym'
            germany.name = 'Germany Name'
            germany.denonym = 'Germany Denonym'
            cologne.name = 'Cologne Name'
            cologne.denonym = 'Cologne Denonym'

            context.create()

            europe.name = 'Europe'
            europe.denonym = 'European'
            germany.name = 'Germany'
            germany.denonym = 'German'
            cologne.name = 'Cologne'
            cologne.denonym = 'Cologner'
        with Context(europe, *lvl_1_2) as context:
            context.read()
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europe Name')
        self.assertEqual(europe.denonym, 'Europe Denonym')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')

    @override(language='de', deactivate=True)
    def test_create_prefetched_instance_level_1_relation_no_lang(self):
        create_samples(
            continent_names=['europe'],
            country_names=['germany'],
            city_names=['cologne'],
            langs=['de', 'tr']
        )

        lvl_1 = ('countries',)
        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code='EU')
        with Context(europe, *lvl_1) as context:
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

            europe.name = 'Europe Name'
            europe.denonym = 'Europe Denonym'
            germany.name = 'Germany Name'
            germany.denonym = 'Germany Denonym'
            cologne.name = 'Cologne Name'
            cologne.denonym = 'Cologne Denonym'

            context.create()

            europe.name = 'Europe'
            europe.denonym = 'European'
            germany.name = 'Germany'
            germany.denonym = 'German'
            cologne.name = 'Cologne'
            cologne.denonym = 'Cologner'
        with Context(europe, *lvl_1_2) as context:
            context.read()
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europe Name')
        self.assertEqual(europe.denonym, 'Europe Denonym')
        self.assertEqual(germany.name, 'Germany Name')
        self.assertEqual(germany.denonym, 'Germany Denonym')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')

    @override(language='de', deactivate=True)
    def test_create_prefetched_instance_level_2_relation_no_lang(self):
        create_samples(
            continent_names=['europe'],
            country_names=['germany'],
            city_names=['cologne'],
            langs=['de', 'tr']
        )

        lvl_2 = ('countries__cities',)
        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code='EU')
        with Context(europe, *lvl_2) as context:
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

            europe.name = 'Europe Name'
            europe.denonym = 'Europe Denonym'
            germany.name = 'Germany Name'
            germany.denonym = 'Germany Denonym'
            cologne.name = 'Cologne Name'
            cologne.denonym = 'Cologne Denonym'

            context.create()

            europe.name = 'Europe'
            europe.denonym = 'European'
            germany.name = 'Germany'
            germany.denonym = 'German'
            cologne.name = 'Cologne'
            cologne.denonym = 'Cologner'
        with Context(europe, *lvl_1_2) as context:
            context.read()
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europe Name')
        self.assertEqual(europe.denonym, 'Europe Denonym')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Cologne Name')
        self.assertEqual(cologne.denonym, 'Cologne Denonym')

    @override(language='de', deactivate=True)
    def test_create_prefetched_instance_level_1_2_relation_no_lang(self):
        create_samples(
            continent_names=['europe'],
            country_names=['germany'],
            city_names=['cologne'],
            langs=['de', 'tr']
        )

        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code='EU')
        with Context(europe, *lvl_1_2) as context:
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

            europe.name = 'Europe Name'
            europe.denonym = 'Europe Denonym'
            germany.name = 'Germany Name'
            germany.denonym = 'Germany Denonym'
            cologne.name = 'Cologne Name'
            cologne.denonym = 'Cologne Denonym'

            context.create()

            europe.name = 'Europe'
            europe.denonym = 'European'
            germany.name = 'Germany'
            germany.denonym = 'German'
            cologne.name = 'Cologne'
            cologne.denonym = 'Cologner'
        with Context(europe, *lvl_1_2) as context:
            context.read()
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europe Name')
        self.assertEqual(europe.denonym, 'Europe Denonym')
        self.assertEqual(germany.name, 'Germany Name')
        self.assertEqual(germany.denonym, 'Germany Denonym')
        self.assertEqual(cologne.name, 'Cologne Name')
        self.assertEqual(cologne.denonym, 'Cologne Denonym')

    def test_create_prefetched_instance_level_0_relation_with_lang(self):
        create_samples(
            continent_names=['europe'],
            country_names=['germany'],
            city_names=['cologne'],
            langs=['de', 'tr']
        )

        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code='EU')
        with Context(europe) as context:
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

            europe.name = 'Europe Name'
            europe.denonym = 'Europe Denonym'
            germany.name = 'Germany Name'
            germany.denonym = 'Germany Denonym'
            cologne.name = 'Cologne Name'
            cologne.denonym = 'Cologne Denonym'

            context.create('de')

            europe.name = 'Europe'
            europe.denonym = 'European'
            germany.name = 'Germany'
            germany.denonym = 'German'
            cologne.name = 'Cologne'
            cologne.denonym = 'Cologner'
        with Context(europe, *lvl_1_2) as context:
            context.read('de')
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europe Name')
        self.assertEqual(europe.denonym, 'Europe Denonym')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')

    def test_create_prefetched_instance_level_1_relation_with_lang(self):
        create_samples(
            continent_names=['europe'],
            country_names=['germany'],
            city_names=['cologne'],
            langs=['de', 'tr']
        )

        lvl_1 = ('countries',)
        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code='EU')
        with Context(europe, *lvl_1) as context:
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

            europe.name = 'Europe Name'
            europe.denonym = 'Europe Denonym'
            germany.name = 'Germany Name'
            germany.denonym = 'Germany Denonym'
            cologne.name = 'Cologne Name'
            cologne.denonym = 'Cologne Denonym'

            context.create('de')

            europe.name = 'Europe'
            europe.denonym = 'European'
            germany.name = 'Germany'
            germany.denonym = 'German'
            cologne.name = 'Cologne'
            cologne.denonym = 'Cologner'
        with Context(europe, *lvl_1_2) as context:
            context.read('de')
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europe Name')
        self.assertEqual(europe.denonym, 'Europe Denonym')
        self.assertEqual(germany.name, 'Germany Name')
        self.assertEqual(germany.denonym, 'Germany Denonym')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')

    def test_create_prefetched_instance_level_2_relation_with_lang(self):
        create_samples(
            continent_names=['europe'],
            country_names=['germany'],
            city_names=['cologne'],
            langs=['de', 'tr']
        )

        lvl_2 = ('countries__cities',)
        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code='EU')
        with Context(europe, *lvl_2) as context:
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

            europe.name = 'Europe Name'
            europe.denonym = 'Europe Denonym'
            germany.name = 'Germany Name'
            germany.denonym = 'Germany Denonym'
            cologne.name = 'Cologne Name'
            cologne.denonym = 'Cologne Denonym'

            context.create('de')

            europe.name = 'Europe'
            europe.denonym = 'European'
            germany.name = 'Germany'
            germany.denonym = 'German'
            cologne.name = 'Cologne'
            cologne.denonym = 'Cologner'
        with Context(europe, *lvl_1_2) as context:
            context.read('de')
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europe Name')
        self.assertEqual(europe.denonym, 'Europe Denonym')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Cologne Name')
        self.assertEqual(cologne.denonym, 'Cologne Denonym')

    def test_create_prefetched_instance_level_1_2_relation_with_lang(self):
        create_samples(
            continent_names=['europe'],
            country_names=['germany'],
            city_names=['cologne'],
            langs=['de', 'tr']
        )

        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code='EU')
        with Context(europe, *lvl_1_2) as context:
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

            europe.name = 'Europe Name'
            europe.denonym = 'Europe Denonym'
            germany.name = 'Germany Name'
            germany.denonym = 'Germany Denonym'
            cologne.name = 'Cologne Name'
            cologne.denonym = 'Cologne Denonym'

            context.create('de')

            europe.name = 'Europe'
            europe.denonym = 'European'
            germany.name = 'Germany'
            germany.denonym = 'German'
            cologne.name = 'Cologne'
            cologne.denonym = 'Cologner'
        with Context(europe, *lvl_1_2) as context:
            context.read('de')
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europe Name')
        self.assertEqual(europe.denonym, 'Europe Denonym')
        self.assertEqual(germany.name, 'Germany Name')
        self.assertEqual(germany.denonym, 'Germany Denonym')
        self.assertEqual(cologne.name, 'Cologne Name')
        self.assertEqual(cologne.denonym, 'Cologne Denonym')

    def test_create_instance_invalid_lang(self):
        create_samples(
            continent_names=['europe'],
            langs=['de']
        )

        europe = Continent.objects.get(code='EU')

        with self.assertRaises(ValueError) as error:
            with Context(europe) as context:
                context.create('xx')

        self.assertEqual(
            error.exception.args[0],
            '`xx` is not a supported language.'
        )

    @override(language='de', deactivate=True)
    def test_create_queryset_level_0_relation_no_lang(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            langs=['de', 'tr']
        )

        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.all()
        with Context(continents) as context:
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

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

            context.create()

            europe.name = 'Europe'
            europe.denonym = 'European'
            germany.name = 'Germany'
            germany.denonym = 'German'
            cologne.name = 'Cologne'
            cologne.denonym = 'Cologner'
            asia.name = 'Asia'
            asia.denonym = 'Asian'
            south_korea.name = 'South Korea'
            south_korea.denonym = 'South Korean'
            seoul.name = 'Seoul'
            seoul.denonym = 'Seouler'
        with Context(continents, *lvl_1_2) as context:
            context.read()
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

        self.assertEqual(europe.name, 'Europe Name')
        self.assertEqual(europe.denonym, 'Europe Denonym')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')
        self.assertEqual(asia.name, 'Asia Name')
        self.assertEqual(asia.denonym, 'Asia Denonym')
        self.assertEqual(south_korea.name, 'South Korea')
        self.assertEqual(south_korea.denonym, 'South Korean')
        self.assertEqual(seoul.name, 'Seoul')
        self.assertEqual(seoul.denonym, 'Seouler')

    @override(language='de', deactivate=True)
    def test_create_queryset_level_1_relation_no_lang(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            langs=['de', 'tr']
        )

        lvl_1 = ('countries',)
        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.all()
        with Context(continents, *lvl_1) as context:
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

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

            context.create()

            europe.name = 'Europe'
            europe.denonym = 'European'
            germany.name = 'Germany'
            germany.denonym = 'German'
            cologne.name = 'Cologne'
            cologne.denonym = 'Cologner'
            asia.name = 'Asia'
            asia.denonym = 'Asian'
            south_korea.name = 'South Korea'
            south_korea.denonym = 'South Korean'
            seoul.name = 'Seoul'
            seoul.denonym = 'Seouler'
        with Context(continents, *lvl_1_2) as context:
            context.read()
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

        self.assertEqual(europe.name, 'Europe Name')
        self.assertEqual(europe.denonym, 'Europe Denonym')
        self.assertEqual(germany.name, 'Germany Name')
        self.assertEqual(germany.denonym, 'Germany Denonym')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')
        self.assertEqual(asia.name, 'Asia Name')
        self.assertEqual(asia.denonym, 'Asia Denonym')
        self.assertEqual(south_korea.name, 'South Korea Name')
        self.assertEqual(south_korea.denonym, 'South Korea Denonym')
        self.assertEqual(seoul.name, 'Seoul')
        self.assertEqual(seoul.denonym, 'Seouler')

    @override(language='de', deactivate=True)
    def test_create_queryset_level_2_relation_no_lang(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            langs=['de', 'tr']
        )

        lvl_2 = ('countries__cities',)
        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.all()
        with Context(continents, *lvl_2) as context:
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

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

            context.create()

            europe.name = 'Europe'
            europe.denonym = 'European'
            germany.name = 'Germany'
            germany.denonym = 'German'
            cologne.name = 'Cologne'
            cologne.denonym = 'Cologner'
            asia.name = 'Asia'
            asia.denonym = 'Asian'
            south_korea.name = 'South Korea'
            south_korea.denonym = 'South Korean'
            seoul.name = 'Seoul'
            seoul.denonym = 'Seouler'
        with Context(continents, *lvl_1_2) as context:
            context.read()
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

        self.assertEqual(europe.name, 'Europe Name')
        self.assertEqual(europe.denonym, 'Europe Denonym')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Cologne Name')
        self.assertEqual(cologne.denonym, 'Cologne Denonym')
        self.assertEqual(asia.name, 'Asia Name')
        self.assertEqual(asia.denonym, 'Asia Denonym')
        self.assertEqual(south_korea.name, 'South Korea')
        self.assertEqual(south_korea.denonym, 'South Korean')
        self.assertEqual(seoul.name, 'Seoul Name')
        self.assertEqual(seoul.denonym, 'Seoul Denonym')

    @override(language='de', deactivate=True)
    def test_create_queryset_level_1_2_relation_no_lang(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            langs=['de', 'tr']
        )

        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.all()
        with Context(continents, *lvl_1_2) as context:
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

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

            context.create()

            europe.name = 'Europe'
            europe.denonym = 'European'
            germany.name = 'Germany'
            germany.denonym = 'German'
            cologne.name = 'Cologne'
            cologne.denonym = 'Cologner'
            asia.name = 'Asia'
            asia.denonym = 'Asian'
            south_korea.name = 'South Korea'
            south_korea.denonym = 'South Korean'
            seoul.name = 'Seoul'
            seoul.denonym = 'Seouler'
        with Context(continents, *lvl_1_2) as context:
            context.read()
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

        self.assertEqual(europe.name, 'Europe Name')
        self.assertEqual(europe.denonym, 'Europe Denonym')
        self.assertEqual(germany.name, 'Germany Name')
        self.assertEqual(germany.denonym, 'Germany Denonym')
        self.assertEqual(cologne.name, 'Cologne Name')
        self.assertEqual(cologne.denonym, 'Cologne Denonym')
        self.assertEqual(asia.name, 'Asia Name')
        self.assertEqual(asia.denonym, 'Asia Denonym')
        self.assertEqual(south_korea.name, 'South Korea Name')
        self.assertEqual(south_korea.denonym, 'South Korea Denonym')
        self.assertEqual(seoul.name, 'Seoul Name')
        self.assertEqual(seoul.denonym, 'Seoul Denonym')

    def test_create_queryset_level_0_relation_with_lang(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            langs=['de', 'tr']
        )

        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.all()
        with Context(continents) as context:
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

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

            context.create('de')

            europe.name = 'Europe'
            europe.denonym = 'European'
            germany.name = 'Germany'
            germany.denonym = 'German'
            cologne.name = 'Cologne'
            cologne.denonym = 'Cologner'
            asia.name = 'Asia'
            asia.denonym = 'Asian'
            south_korea.name = 'South Korea'
            south_korea.denonym = 'South Korean'
            seoul.name = 'Seoul'
            seoul.denonym = 'Seouler'
        with Context(continents, *lvl_1_2) as context:
            context.read('de')
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

        self.assertEqual(europe.name, 'Europe Name')
        self.assertEqual(europe.denonym, 'Europe Denonym')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')
        self.assertEqual(asia.name, 'Asia Name')
        self.assertEqual(asia.denonym, 'Asia Denonym')
        self.assertEqual(south_korea.name, 'South Korea')
        self.assertEqual(south_korea.denonym, 'South Korean')
        self.assertEqual(seoul.name, 'Seoul')
        self.assertEqual(seoul.denonym, 'Seouler')

    def test_create_queryset_level_1_relation_with_lang(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            langs=['de', 'tr']
        )

        lvl_1 = ('countries',)
        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.all()
        with Context(continents, *lvl_1) as context:
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

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

            context.create('de')

            europe.name = 'Europe'
            europe.denonym = 'European'
            germany.name = 'Germany'
            germany.denonym = 'German'
            cologne.name = 'Cologne'
            cologne.denonym = 'Cologner'
            asia.name = 'Asia'
            asia.denonym = 'Asian'
            south_korea.name = 'South Korea'
            south_korea.denonym = 'South Korean'
            seoul.name = 'Seoul'
            seoul.denonym = 'Seouler'
        with Context(continents, *lvl_1_2) as context:
            context.read('de')
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

        self.assertEqual(europe.name, 'Europe Name')
        self.assertEqual(europe.denonym, 'Europe Denonym')
        self.assertEqual(germany.name, 'Germany Name')
        self.assertEqual(germany.denonym, 'Germany Denonym')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')
        self.assertEqual(asia.name, 'Asia Name')
        self.assertEqual(asia.denonym, 'Asia Denonym')
        self.assertEqual(south_korea.name, 'South Korea Name')
        self.assertEqual(south_korea.denonym, 'South Korea Denonym')
        self.assertEqual(seoul.name, 'Seoul')
        self.assertEqual(seoul.denonym, 'Seouler')

    def test_create_queryset_level_2_relation_with_lang(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            langs=['de', 'tr']
        )

        lvl_2 = ('countries__cities',)
        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.all()
        with Context(continents, *lvl_2) as context:
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

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

            context.create('de')

            europe.name = 'Europe'
            europe.denonym = 'European'
            germany.name = 'Germany'
            germany.denonym = 'German'
            cologne.name = 'Cologne'
            cologne.denonym = 'Cologner'
            asia.name = 'Asia'
            asia.denonym = 'Asian'
            south_korea.name = 'South Korea'
            south_korea.denonym = 'South Korean'
            seoul.name = 'Seoul'
            seoul.denonym = 'Seouler'
        with Context(continents, *lvl_1_2) as context:
            context.read('de')
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

        self.assertEqual(europe.name, 'Europe Name')
        self.assertEqual(europe.denonym, 'Europe Denonym')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Cologne Name')
        self.assertEqual(cologne.denonym, 'Cologne Denonym')
        self.assertEqual(asia.name, 'Asia Name')
        self.assertEqual(asia.denonym, 'Asia Denonym')
        self.assertEqual(south_korea.name, 'South Korea')
        self.assertEqual(south_korea.denonym, 'South Korean')
        self.assertEqual(seoul.name, 'Seoul Name')
        self.assertEqual(seoul.denonym, 'Seoul Denonym')

    def test_create_queryset_level_1_2_relation_with_lang(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            langs=['de', 'tr']
        )

        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.all()
        with Context(continents, *lvl_1_2) as context:
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

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

            context.create('de')

            europe.name = 'Europe'
            europe.denonym = 'European'
            germany.name = 'Germany'
            germany.denonym = 'German'
            cologne.name = 'Cologne'
            cologne.denonym = 'Cologner'
            asia.name = 'Asia'
            asia.denonym = 'Asian'
            south_korea.name = 'South Korea'
            south_korea.denonym = 'South Korean'
            seoul.name = 'Seoul'
            seoul.denonym = 'Seouler'
        with Context(continents, *lvl_1_2) as context:
            context.read('de')
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

        self.assertEqual(europe.name, 'Europe Name')
        self.assertEqual(europe.denonym, 'Europe Denonym')
        self.assertEqual(germany.name, 'Germany Name')
        self.assertEqual(germany.denonym, 'Germany Denonym')
        self.assertEqual(cologne.name, 'Cologne Name')
        self.assertEqual(cologne.denonym, 'Cologne Denonym')
        self.assertEqual(asia.name, 'Asia Name')
        self.assertEqual(asia.denonym, 'Asia Denonym')
        self.assertEqual(south_korea.name, 'South Korea Name')
        self.assertEqual(south_korea.denonym, 'South Korea Denonym')
        self.assertEqual(seoul.name, 'Seoul Name')
        self.assertEqual(seoul.denonym, 'Seoul Denonym')

    @override(language='de', deactivate=True)
    def test_create_prefetched_queryset_level_0_relation_no_lang(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            langs=['de', 'tr']
        )

        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.prefetch_related(*lvl_1_2)
        with Context(continents) as context:
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

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

            context.create()

            europe.name = 'Europe'
            europe.denonym = 'European'
            germany.name = 'Germany'
            germany.denonym = 'German'
            cologne.name = 'Cologne'
            cologne.denonym = 'Cologner'
            asia.name = 'Asia'
            asia.denonym = 'Asian'
            south_korea.name = 'South Korea'
            south_korea.denonym = 'South Korean'
            seoul.name = 'Seoul'
            seoul.denonym = 'Seouler'
        with Context(continents, *lvl_1_2) as context:
            context.read()
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

        self.assertEqual(europe.name, 'Europe Name')
        self.assertEqual(europe.denonym, 'Europe Denonym')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')
        self.assertEqual(asia.name, 'Asia Name')
        self.assertEqual(asia.denonym, 'Asia Denonym')
        self.assertEqual(south_korea.name, 'South Korea')
        self.assertEqual(south_korea.denonym, 'South Korean')
        self.assertEqual(seoul.name, 'Seoul')
        self.assertEqual(seoul.denonym, 'Seouler')

    @override(language='de', deactivate=True)
    def test_create_prefetched_queryset_level_1_relation_no_lang(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            langs=['de', 'tr']
        )

        lvl_1 = ('countries',)
        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.prefetch_related(*lvl_1_2)
        with Context(continents, *lvl_1) as context:
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

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

            context.create()

            europe.name = 'Europe'
            europe.denonym = 'European'
            germany.name = 'Germany'
            germany.denonym = 'German'
            cologne.name = 'Cologne'
            cologne.denonym = 'Cologner'
            asia.name = 'Asia'
            asia.denonym = 'Asian'
            south_korea.name = 'South Korea'
            south_korea.denonym = 'South Korean'
            seoul.name = 'Seoul'
            seoul.denonym = 'Seouler'
        with Context(continents, *lvl_1_2) as context:
            context.read()
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

        self.assertEqual(europe.name, 'Europe Name')
        self.assertEqual(europe.denonym, 'Europe Denonym')
        self.assertEqual(germany.name, 'Germany Name')
        self.assertEqual(germany.denonym, 'Germany Denonym')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')
        self.assertEqual(asia.name, 'Asia Name')
        self.assertEqual(asia.denonym, 'Asia Denonym')
        self.assertEqual(south_korea.name, 'South Korea Name')
        self.assertEqual(south_korea.denonym, 'South Korea Denonym')
        self.assertEqual(seoul.name, 'Seoul')
        self.assertEqual(seoul.denonym, 'Seouler')

    @override(language='de', deactivate=True)
    def test_create_prefetched_queryset_level_2_relation_no_lang(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            langs=['de', 'tr']
        )

        lvl_2 = ('countries__cities',)
        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.prefetch_related(*lvl_1_2)
        with Context(continents, *lvl_2) as context:
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

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

            context.create()

            europe.name = 'Europe'
            europe.denonym = 'European'
            germany.name = 'Germany'
            germany.denonym = 'German'
            cologne.name = 'Cologne'
            cologne.denonym = 'Cologner'
            asia.name = 'Asia'
            asia.denonym = 'Asian'
            south_korea.name = 'South Korea'
            south_korea.denonym = 'South Korean'
            seoul.name = 'Seoul'
            seoul.denonym = 'Seouler'
        with Context(continents, *lvl_1_2) as context:
            context.read()
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

        self.assertEqual(europe.name, 'Europe Name')
        self.assertEqual(europe.denonym, 'Europe Denonym')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Cologne Name')
        self.assertEqual(cologne.denonym, 'Cologne Denonym')
        self.assertEqual(asia.name, 'Asia Name')
        self.assertEqual(asia.denonym, 'Asia Denonym')
        self.assertEqual(south_korea.name, 'South Korea')
        self.assertEqual(south_korea.denonym, 'South Korean')
        self.assertEqual(seoul.name, 'Seoul Name')
        self.assertEqual(seoul.denonym, 'Seoul Denonym')

    @override(language='de', deactivate=True)
    def test_create_prefetched_queryset_level_1_2_relation_no_lang(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            langs=['de', 'tr']
        )

        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.prefetch_related(*lvl_1_2)
        with Context(continents, *lvl_1_2) as context:
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

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

            context.create()

            europe.name = 'Europe'
            europe.denonym = 'European'
            germany.name = 'Germany'
            germany.denonym = 'German'
            cologne.name = 'Cologne'
            cologne.denonym = 'Cologner'
            asia.name = 'Asia'
            asia.denonym = 'Asian'
            south_korea.name = 'South Korea'
            south_korea.denonym = 'South Korean'
            seoul.name = 'Seoul'
            seoul.denonym = 'Seouler'
        with Context(continents, *lvl_1_2) as context:
            context.read()
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

        self.assertEqual(europe.name, 'Europe Name')
        self.assertEqual(europe.denonym, 'Europe Denonym')
        self.assertEqual(germany.name, 'Germany Name')
        self.assertEqual(germany.denonym, 'Germany Denonym')
        self.assertEqual(cologne.name, 'Cologne Name')
        self.assertEqual(cologne.denonym, 'Cologne Denonym')
        self.assertEqual(asia.name, 'Asia Name')
        self.assertEqual(asia.denonym, 'Asia Denonym')
        self.assertEqual(south_korea.name, 'South Korea Name')
        self.assertEqual(south_korea.denonym, 'South Korea Denonym')
        self.assertEqual(seoul.name, 'Seoul Name')
        self.assertEqual(seoul.denonym, 'Seoul Denonym')

    def test_create_prefetched_queryset_level_0_relation_with_lang(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            langs=['de', 'tr']
        )

        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.prefetch_related(*lvl_1_2)
        with Context(continents) as context:
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

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

            context.create('de')

            europe.name = 'Europe'
            europe.denonym = 'European'
            germany.name = 'Germany'
            germany.denonym = 'German'
            cologne.name = 'Cologne'
            cologne.denonym = 'Cologner'
            asia.name = 'Asia'
            asia.denonym = 'Asian'
            south_korea.name = 'South Korea'
            south_korea.denonym = 'South Korean'
            seoul.name = 'Seoul'
            seoul.denonym = 'Seouler'
        with Context(continents, *lvl_1_2) as context:
            context.read('de')
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

        self.assertEqual(europe.name, 'Europe Name')
        self.assertEqual(europe.denonym, 'Europe Denonym')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')
        self.assertEqual(asia.name, 'Asia Name')
        self.assertEqual(asia.denonym, 'Asia Denonym')
        self.assertEqual(south_korea.name, 'South Korea')
        self.assertEqual(south_korea.denonym, 'South Korean')
        self.assertEqual(seoul.name, 'Seoul')
        self.assertEqual(seoul.denonym, 'Seouler')

    def test_create_prefetched_queryset_level_1_relation_with_lang(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            langs=['de', 'tr']
        )

        lvl_1 = ('countries',)
        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.prefetch_related(*lvl_1_2)
        with Context(continents, *lvl_1) as context:
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

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

            context.create('de')

            europe.name = 'Europe'
            europe.denonym = 'European'
            germany.name = 'Germany'
            germany.denonym = 'German'
            cologne.name = 'Cologne'
            cologne.denonym = 'Cologner'
            asia.name = 'Asia'
            asia.denonym = 'Asian'
            south_korea.name = 'South Korea'
            south_korea.denonym = 'South Korean'
            seoul.name = 'Seoul'
            seoul.denonym = 'Seouler'
        with Context(continents, *lvl_1_2) as context:
            context.read('de')
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

        self.assertEqual(europe.name, 'Europe Name')
        self.assertEqual(europe.denonym, 'Europe Denonym')
        self.assertEqual(germany.name, 'Germany Name')
        self.assertEqual(germany.denonym, 'Germany Denonym')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')
        self.assertEqual(asia.name, 'Asia Name')
        self.assertEqual(asia.denonym, 'Asia Denonym')
        self.assertEqual(south_korea.name, 'South Korea Name')
        self.assertEqual(south_korea.denonym, 'South Korea Denonym')
        self.assertEqual(seoul.name, 'Seoul')
        self.assertEqual(seoul.denonym, 'Seouler')

    def test_create_prefetched_queryset_level_2_relation_with_lang(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            langs=['de', 'tr']
        )

        lvl_2 = ('countries__cities',)
        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.prefetch_related(*lvl_1_2)
        with Context(continents, *lvl_2) as context:
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

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

            context.create('de')

            europe.name = 'Europe'
            europe.denonym = 'European'
            germany.name = 'Germany'
            germany.denonym = 'German'
            cologne.name = 'Cologne'
            cologne.denonym = 'Cologner'
            asia.name = 'Asia'
            asia.denonym = 'Asian'
            south_korea.name = 'South Korea'
            south_korea.denonym = 'South Korean'
            seoul.name = 'Seoul'
            seoul.denonym = 'Seouler'
        with Context(continents, *lvl_1_2) as context:
            context.read('de')
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

        self.assertEqual(europe.name, 'Europe Name')
        self.assertEqual(europe.denonym, 'Europe Denonym')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Cologne Name')
        self.assertEqual(cologne.denonym, 'Cologne Denonym')
        self.assertEqual(asia.name, 'Asia Name')
        self.assertEqual(asia.denonym, 'Asia Denonym')
        self.assertEqual(south_korea.name, 'South Korea')
        self.assertEqual(south_korea.denonym, 'South Korean')
        self.assertEqual(seoul.name, 'Seoul Name')
        self.assertEqual(seoul.denonym, 'Seoul Denonym')

    def test_create_prefetched_queryset_level_1_2_relation_with_lang(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            langs=['de', 'tr']
        )

        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.prefetch_related(*lvl_1_2)
        with Context(continents, *lvl_1_2) as context:
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

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

            context.create('de')

            europe.name = 'Europe'
            europe.denonym = 'European'
            germany.name = 'Germany'
            germany.denonym = 'German'
            cologne.name = 'Cologne'
            cologne.denonym = 'Cologner'
            asia.name = 'Asia'
            asia.denonym = 'Asian'
            south_korea.name = 'South Korea'
            south_korea.denonym = 'South Korean'
            seoul.name = 'Seoul'
            seoul.denonym = 'Seouler'
        with Context(continents, *lvl_1_2) as context:
            context.read('de')
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

        self.assertEqual(europe.name, 'Europe Name')
        self.assertEqual(europe.denonym, 'Europe Denonym')
        self.assertEqual(germany.name, 'Germany Name')
        self.assertEqual(germany.denonym, 'Germany Denonym')
        self.assertEqual(cologne.name, 'Cologne Name')
        self.assertEqual(cologne.denonym, 'Cologne Denonym')
        self.assertEqual(asia.name, 'Asia Name')
        self.assertEqual(asia.denonym, 'Asia Denonym')
        self.assertEqual(south_korea.name, 'South Korea Name')
        self.assertEqual(south_korea.denonym, 'South Korea Denonym')
        self.assertEqual(seoul.name, 'Seoul Name')
        self.assertEqual(seoul.denonym, 'Seoul Denonym')

    def test_create_queryset_invalid_lang(self):
        create_samples(
            continent_names=['europe'],
            langs=['de']
        )

        continents = Continent.objects.all()

        with self.assertRaises(ValueError) as error:
            with Context(continents) as context:
                context.create('xx')

        self.assertEqual(
            error.exception.args[0],
            '`xx` is not a supported language.'
        )

    @override(language='de', deactivate=True)
    def test_read_instance_level_0_relation_no_lang(self):
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
        with Context(europe) as context:
            context.read()
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europa')
        self.assertEqual(europe.denonym, 'Europäisch')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')

    @override(language='de', deactivate=True)
    def test_read_instance_level_1_relation_no_lang(self):
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

        with Context(europe, *lvl_1) as context:
            context.read()
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europa')
        self.assertEqual(europe.denonym, 'Europäisch')
        self.assertEqual(germany.name, 'Deutschland')
        self.assertEqual(germany.denonym, 'Deutsche')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')

    @override(language='de', deactivate=True)
    def test_read_instance_level_2_relation_no_lang(self):
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
        with Context(europe, *lvl_2) as context:
            context.read()
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europa')
        self.assertEqual(europe.denonym, 'Europäisch')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Köln')
        self.assertEqual(cologne.denonym, 'Kölner')

    @override(language='de', deactivate=True)
    def test_read_instance_level_1_2_relation_no_lang(self):
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
        with Context(europe, *lvl_1_2) as context:
            context.read()
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europa')
        self.assertEqual(europe.denonym, 'Europäisch')
        self.assertEqual(germany.name, 'Deutschland')
        self.assertEqual(germany.denonym, 'Deutsche')
        self.assertEqual(cologne.name, 'Köln')
        self.assertEqual(cologne.denonym, 'Kölner')

    def test_read_instance_level_0_relation_with_lang(self):
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
        with Context(europe) as context:
            context.read('de')
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europa')
        self.assertEqual(europe.denonym, 'Europäisch')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')

    def test_read_instance_level_1_relation_with_lang(self):
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
        with Context(europe, *lvl_1) as context:
            context.read('de')
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europa')
        self.assertEqual(europe.denonym, 'Europäisch')
        self.assertEqual(germany.name, 'Deutschland')
        self.assertEqual(germany.denonym, 'Deutsche')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')

    def test_read_instance_level_2_relation_with_lang(self):
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
        with Context(europe, *lvl_2) as context:
            context.read('de')
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europa')
        self.assertEqual(europe.denonym, 'Europäisch')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Köln')
        self.assertEqual(cologne.denonym, 'Kölner')

    def test_read_instance_level_1_2_relation_with_lang(self):
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
        with Context(europe, *lvl_1_2) as context:
            context.read('de')
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europa')
        self.assertEqual(europe.denonym, 'Europäisch')
        self.assertEqual(germany.name, 'Deutschland')
        self.assertEqual(germany.denonym, 'Deutsche')
        self.assertEqual(cologne.name, 'Köln')
        self.assertEqual(cologne.denonym, 'Kölner')

    @override(language='de', deactivate=True)
    def test_read_prefetched_instance_level_0_relation_no_lang(self):
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
        with Context(europe) as context:
            context.read()
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europa')
        self.assertEqual(europe.denonym, 'Europäisch')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')

    @override(language='de', deactivate=True)
    def test_read_prefetched_instance_level_1_relation_no_lang(self):
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
        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code='EU')
        with Context(europe, *lvl_1) as context:
            context.read()
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europa')
        self.assertEqual(europe.denonym, 'Europäisch')
        self.assertEqual(germany.name, 'Deutschland')
        self.assertEqual(germany.denonym, 'Deutsche')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')

    @override(language='de', deactivate=True)
    def test_read_prefetched_instance_level_2_relation_no_lang(self):
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
        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code='EU')
        with Context(europe, *lvl_2) as context:
            context.read()
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europa')
        self.assertEqual(europe.denonym, 'Europäisch')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Köln')
        self.assertEqual(cologne.denonym, 'Kölner')

    @override(language='de', deactivate=True)
    def test_read_prefetched_instance_level_1_2_relation_no_lang(self):
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
        with Context(europe, *lvl_1_2) as context:
            context.read()
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europa')
        self.assertEqual(europe.denonym, 'Europäisch')
        self.assertEqual(germany.name, 'Deutschland')
        self.assertEqual(germany.denonym, 'Deutsche')
        self.assertEqual(cologne.name, 'Köln')
        self.assertEqual(cologne.denonym, 'Kölner')

    def test_read_prefetched_instance_level_0_relation_with_lang(self):
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
        with Context(europe) as context:
            context.read('de')
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europa')
        self.assertEqual(europe.denonym, 'Europäisch')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')

    def test_read_prefetched_instance_level_1_relation_with_lang(self):
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
        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code='EU')
        with Context(europe, *lvl_1) as context:
            context.read('de')
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europa')
        self.assertEqual(europe.denonym, 'Europäisch')
        self.assertEqual(germany.name, 'Deutschland')
        self.assertEqual(germany.denonym, 'Deutsche')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')

    def test_read_prefetched_instance_level_2_relation_with_lang(self):
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
        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code='EU')
        with Context(europe, *lvl_2) as context:
            context.read('de')
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europa')
        self.assertEqual(europe.denonym, 'Europäisch')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Köln')
        self.assertEqual(cologne.denonym, 'Kölner')

    def test_read_prefetched_instance_level_1_2_relation_with_lang(self):
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
        with Context(europe, *lvl_1_2) as context:
            context.read('de')
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europa')
        self.assertEqual(europe.denonym, 'Europäisch')
        self.assertEqual(germany.name, 'Deutschland')
        self.assertEqual(germany.denonym, 'Deutsche')
        self.assertEqual(cologne.name, 'Köln')
        self.assertEqual(cologne.denonym, 'Kölner')

    def test_read_instance_invalid_lang(self):
        create_samples(
            continent_names=['europe'],
            continent_fields=['name', 'denonym'],
            langs=['de']
        )

        europe = Continent.objects.get(code='EU')

        with self.assertRaises(ValueError) as error:
            with Context(europe) as context:
                context.read('xx')

        self.assertEqual(
            error.exception.args[0],
            '`xx` is not a supported language.'
        )

    @override(language='de', deactivate=True)
    def test_read_queryset_level_0_relation_no_lang(self):
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
        with Context(continents) as context:
            context.read()
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

        self.assertEqual(europe.name, 'Europa')
        self.assertEqual(europe.denonym, 'Europäisch')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')
        self.assertEqual(asia.name, 'Asien')
        self.assertEqual(asia.denonym, 'Asiatisch')
        self.assertEqual(south_korea.name, 'South Korea')
        self.assertEqual(south_korea.denonym, 'South Korean')
        self.assertEqual(seoul.name, 'Seoul')
        self.assertEqual(seoul.denonym, 'Seouler')

    @override(language='de', deactivate=True)
    def test_read_queryset_level_1_relation_no_lang(self):
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
        with Context(continents, *lvl_1) as context:
            context.read()
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

        self.assertEqual(europe.name, 'Europa')
        self.assertEqual(europe.denonym, 'Europäisch')
        self.assertEqual(germany.name, 'Deutschland')
        self.assertEqual(germany.denonym, 'Deutsche')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')
        self.assertEqual(asia.name, 'Asien')
        self.assertEqual(asia.denonym, 'Asiatisch')
        self.assertEqual(south_korea.name, 'Südkorea')
        self.assertEqual(south_korea.denonym, 'Südkoreanisch')
        self.assertEqual(seoul.name, 'Seoul')
        self.assertEqual(seoul.denonym, 'Seouler')

    @override(language='de', deactivate=True)
    def test_read_queryset_level_2_relation_no_lang(self):
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
        with Context(continents, *lvl_2) as context:
            context.read()
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

        self.assertEqual(europe.name, 'Europa')
        self.assertEqual(europe.denonym, 'Europäisch')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Köln')
        self.assertEqual(cologne.denonym, 'Kölner')
        self.assertEqual(asia.name, 'Asien')
        self.assertEqual(asia.denonym, 'Asiatisch')
        self.assertEqual(south_korea.name, 'South Korea')
        self.assertEqual(south_korea.denonym, 'South Korean')
        self.assertEqual(seoul.name, 'Seül')
        self.assertEqual(seoul.denonym, 'Seüler')

    @override(language='de', deactivate=True)
    def test_read_queryset_level_1_2_relation_no_lang(self):
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
        with Context(continents, *lvl_1_2) as context:
            context.read()
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

        self.assertEqual(europe.name, 'Europa')
        self.assertEqual(europe.denonym, 'Europäisch')
        self.assertEqual(germany.name, 'Deutschland')
        self.assertEqual(germany.denonym, 'Deutsche')
        self.assertEqual(cologne.name, 'Köln')
        self.assertEqual(cologne.denonym, 'Kölner')
        self.assertEqual(asia.name, 'Asien')
        self.assertEqual(asia.denonym, 'Asiatisch')
        self.assertEqual(south_korea.name, 'Südkorea')
        self.assertEqual(south_korea.denonym, 'Südkoreanisch')
        self.assertEqual(seoul.name, 'Seül')
        self.assertEqual(seoul.denonym, 'Seüler')

    def test_read_queryset_level_0_relation_with_lang(self):
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
        with Context(continents) as context:
            context.read('de')
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

        self.assertEqual(europe.name, 'Europa')
        self.assertEqual(europe.denonym, 'Europäisch')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')
        self.assertEqual(asia.name, 'Asien')
        self.assertEqual(asia.denonym, 'Asiatisch')
        self.assertEqual(south_korea.name, 'South Korea')
        self.assertEqual(south_korea.denonym, 'South Korean')
        self.assertEqual(seoul.name, 'Seoul')
        self.assertEqual(seoul.denonym, 'Seouler')

    def test_read_queryset_level_1_relation_with_lang(self):
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
        with Context(continents, *lvl_1) as context:
            context.read('de')
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

        self.assertEqual(europe.name, 'Europa')
        self.assertEqual(europe.denonym, 'Europäisch')
        self.assertEqual(germany.name, 'Deutschland')
        self.assertEqual(germany.denonym, 'Deutsche')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')
        self.assertEqual(asia.name, 'Asien')
        self.assertEqual(asia.denonym, 'Asiatisch')
        self.assertEqual(south_korea.name, 'Südkorea')
        self.assertEqual(south_korea.denonym, 'Südkoreanisch')
        self.assertEqual(seoul.name, 'Seoul')
        self.assertEqual(seoul.denonym, 'Seouler')

    def test_read_queryset_level_2_relation_with_lang(self):
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
        with Context(continents, *lvl_2) as context:
            context.read('de')
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

        self.assertEqual(europe.name, 'Europa')
        self.assertEqual(europe.denonym, 'Europäisch')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Köln')
        self.assertEqual(cologne.denonym, 'Kölner')
        self.assertEqual(asia.name, 'Asien')
        self.assertEqual(asia.denonym, 'Asiatisch')
        self.assertEqual(south_korea.name, 'South Korea')
        self.assertEqual(south_korea.denonym, 'South Korean')
        self.assertEqual(seoul.name, 'Seül')
        self.assertEqual(seoul.denonym, 'Seüler')

    def test_read_queryset_level_1_2_relation_with_lang(self):
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
        with Context(continents, *lvl_1_2) as context:
            context.read('de')
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

        self.assertEqual(europe.name, 'Europa')
        self.assertEqual(europe.denonym, 'Europäisch')
        self.assertEqual(germany.name, 'Deutschland')
        self.assertEqual(germany.denonym, 'Deutsche')
        self.assertEqual(cologne.name, 'Köln')
        self.assertEqual(cologne.denonym, 'Kölner')
        self.assertEqual(asia.name, 'Asien')
        self.assertEqual(asia.denonym, 'Asiatisch')
        self.assertEqual(south_korea.name, 'Südkorea')
        self.assertEqual(south_korea.denonym, 'Südkoreanisch')
        self.assertEqual(seoul.name, 'Seül')
        self.assertEqual(seoul.denonym, 'Seüler')

    @override(language='de', deactivate=True)
    def test_read_prefetched_queryset_level_0_relation_no_lang(self):
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
        with Context(continents) as context:
            context.read()
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

        self.assertEqual(europe.name, 'Europa')
        self.assertEqual(europe.denonym, 'Europäisch')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')
        self.assertEqual(asia.name, 'Asien')
        self.assertEqual(asia.denonym, 'Asiatisch')
        self.assertEqual(south_korea.name, 'South Korea')
        self.assertEqual(south_korea.denonym, 'South Korean')
        self.assertEqual(seoul.name, 'Seoul')
        self.assertEqual(seoul.denonym, 'Seouler')

    @override(language='de', deactivate=True)
    def test_read_prefetched_queryset_level_1_relation_no_lang(self):
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
        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.prefetch_related(*lvl_1_2)
        with Context(continents, *lvl_1) as context:
            context.read()
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

        self.assertEqual(europe.name, 'Europa')
        self.assertEqual(europe.denonym, 'Europäisch')
        self.assertEqual(germany.name, 'Deutschland')
        self.assertEqual(germany.denonym, 'Deutsche')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')
        self.assertEqual(asia.name, 'Asien')
        self.assertEqual(asia.denonym, 'Asiatisch')
        self.assertEqual(south_korea.name, 'Südkorea')
        self.assertEqual(south_korea.denonym, 'Südkoreanisch')
        self.assertEqual(seoul.name, 'Seoul')
        self.assertEqual(seoul.denonym, 'Seouler')

    @override(language='de', deactivate=True)
    def test_read_prefetched_queryset_level_2_relation_no_lang(self):
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
        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.prefetch_related(*lvl_1_2)
        with Context(continents, *lvl_2) as context:
            context.read()
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

        self.assertEqual(europe.name, 'Europa')
        self.assertEqual(europe.denonym, 'Europäisch')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Köln')
        self.assertEqual(cologne.denonym, 'Kölner')
        self.assertEqual(asia.name, 'Asien')
        self.assertEqual(asia.denonym, 'Asiatisch')
        self.assertEqual(south_korea.name, 'South Korea')
        self.assertEqual(south_korea.denonym, 'South Korean')
        self.assertEqual(seoul.name, 'Seül')
        self.assertEqual(seoul.denonym, 'Seüler')

    @override(language='de', deactivate=True)
    def test_read_prefetched_queryset_level_1_2_relation_no_lang(self):
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
        with Context(continents, *lvl_1_2) as context:
            context.read()
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

        self.assertEqual(europe.name, 'Europa')
        self.assertEqual(europe.denonym, 'Europäisch')
        self.assertEqual(germany.name, 'Deutschland')
        self.assertEqual(germany.denonym, 'Deutsche')
        self.assertEqual(cologne.name, 'Köln')
        self.assertEqual(cologne.denonym, 'Kölner')
        self.assertEqual(asia.name, 'Asien')
        self.assertEqual(asia.denonym, 'Asiatisch')
        self.assertEqual(south_korea.name, 'Südkorea')
        self.assertEqual(south_korea.denonym, 'Südkoreanisch')
        self.assertEqual(seoul.name, 'Seül')
        self.assertEqual(seoul.denonym, 'Seüler')

    def test_read_prefetched_queryset_level_0_relation_with_lang(self):
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
        with Context(continents) as context:
            context.read('de')
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

        self.assertEqual(europe.name, 'Europa')
        self.assertEqual(europe.denonym, 'Europäisch')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')
        self.assertEqual(asia.name, 'Asien')
        self.assertEqual(asia.denonym, 'Asiatisch')
        self.assertEqual(south_korea.name, 'South Korea')
        self.assertEqual(south_korea.denonym, 'South Korean')
        self.assertEqual(seoul.name, 'Seoul')
        self.assertEqual(seoul.denonym, 'Seouler')

    def test_read_prefetched_queryset_level_1_relation_with_lang(self):
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
        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.prefetch_related(*lvl_1_2)
        with Context(continents, *lvl_1) as context:
            context.read('de')
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

        self.assertEqual(europe.name, 'Europa')
        self.assertEqual(europe.denonym, 'Europäisch')
        self.assertEqual(germany.name, 'Deutschland')
        self.assertEqual(germany.denonym, 'Deutsche')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')
        self.assertEqual(asia.name, 'Asien')
        self.assertEqual(asia.denonym, 'Asiatisch')
        self.assertEqual(south_korea.name, 'Südkorea')
        self.assertEqual(south_korea.denonym, 'Südkoreanisch')
        self.assertEqual(seoul.name, 'Seoul')
        self.assertEqual(seoul.denonym, 'Seouler')

    def test_read_prefetched_queryset_level_2_relation_with_lang(self):
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
        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.prefetch_related(*lvl_1_2)
        with Context(continents, *lvl_2) as context:
            context.read('de')
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

        self.assertEqual(europe.name, 'Europa')
        self.assertEqual(europe.denonym, 'Europäisch')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Köln')
        self.assertEqual(cologne.denonym, 'Kölner')
        self.assertEqual(asia.name, 'Asien')
        self.assertEqual(asia.denonym, 'Asiatisch')
        self.assertEqual(south_korea.name, 'South Korea')
        self.assertEqual(south_korea.denonym, 'South Korean')
        self.assertEqual(seoul.name, 'Seül')
        self.assertEqual(seoul.denonym, 'Seüler')

    def test_read_prefetched_queryset_level_1_2_relation_with_lang(self):
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
        with Context(continents, *lvl_1_2) as context:
            context.read('de')
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

        self.assertEqual(europe.name, 'Europa')
        self.assertEqual(europe.denonym, 'Europäisch')
        self.assertEqual(germany.name, 'Deutschland')
        self.assertEqual(germany.denonym, 'Deutsche')
        self.assertEqual(cologne.name, 'Köln')
        self.assertEqual(cologne.denonym, 'Kölner')
        self.assertEqual(asia.name, 'Asien')
        self.assertEqual(asia.denonym, 'Asiatisch')
        self.assertEqual(south_korea.name, 'Südkorea')
        self.assertEqual(south_korea.denonym, 'Südkoreanisch')
        self.assertEqual(seoul.name, 'Seül')
        self.assertEqual(seoul.denonym, 'Seüler')

    def test_read_queryset_invalid_lang(self):
        create_samples(
            continent_names=['europe'],
            continent_fields=['name', 'denonym'],
            langs=['de']
        )

        continents = Continent.objects.all()

        with self.assertRaises(ValueError) as error:
            with Context(continents) as context:
                context.read('xx')

        self.assertEqual(
            error.exception.args[0],
            '`xx` is not a supported language.'
        )

    @override(language='de', deactivate=True)
    def test_update_instance_level_0_relation_no_lang(self):
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
        with Context(europe) as context:
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

            europe.name = 'Europe Name'
            europe.denonym = 'Europe Denonym'
            germany.name = 'Germany Name'
            germany.denonym = 'Germany Denonym'
            cologne.name = 'Cologne Name'
            cologne.denonym = 'Cologne Denonym'

            context.update()

            europe.name = 'Europa'
            europe.denonym = 'Europäisch'
            germany.name = 'Deutschland'
            germany.denonym = 'Deutsche'
            cologne.name = 'Köln'
            cologne.denonym = 'Kölner'
        with Context(europe, *lvl_1_2) as context:
            context.read()
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europe Name')
        self.assertEqual(europe.denonym, 'Europe Denonym')
        self.assertEqual(germany.name, 'Deutschland')
        self.assertEqual(germany.denonym, 'Deutsche')
        self.assertEqual(cologne.name, 'Köln')
        self.assertEqual(cologne.denonym, 'Kölner')

    @override(language='de', deactivate=True)
    def test_update_instance_level_1_relation_no_lang(self):
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
        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.get(code='EU')
        with Context(europe, *lvl_1) as context:
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

            europe.name = 'Europe Name'
            europe.denonym = 'Europe Denonym'
            germany.name = 'Germany Name'
            germany.denonym = 'Germany Denonym'
            cologne.name = 'Cologne Name'
            cologne.denonym = 'Cologne Denonym'

            context.update()

            europe.name = 'Europa'
            europe.denonym = 'Europäisch'
            germany.name = 'Deutschland'
            germany.denonym = 'Deutsche'
            cologne.name = 'Köln'
            cologne.denonym = 'Kölner'
        with Context(europe, *lvl_1_2) as context:
            context.read()
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europe Name')
        self.assertEqual(europe.denonym, 'Europe Denonym')
        self.assertEqual(germany.name, 'Germany Name')
        self.assertEqual(germany.denonym, 'Germany Denonym')
        self.assertEqual(cologne.name, 'Köln')
        self.assertEqual(cologne.denonym, 'Kölner')

    @override(language='de', deactivate=True)
    def test_update_instance_level_2_relation_no_lang(self):
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
        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.get(code='EU')
        with Context(europe, *lvl_2) as context:
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

            europe.name = 'Europe Name'
            europe.denonym = 'Europe Denonym'
            germany.name = 'Germany Name'
            germany.denonym = 'Germany Denonym'
            cologne.name = 'Cologne Name'
            cologne.denonym = 'Cologne Denonym'

            context.update()

            europe.name = 'Europa'
            europe.denonym = 'Europäisch'
            germany.name = 'Deutschland'
            germany.denonym = 'Deutsche'
            cologne.name = 'Köln'
            cologne.denonym = 'Kölner'
        with Context(europe, *lvl_1_2) as context:
            context.read()
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europe Name')
        self.assertEqual(europe.denonym, 'Europe Denonym')
        self.assertEqual(germany.name, 'Deutschland')
        self.assertEqual(germany.denonym, 'Deutsche')
        self.assertEqual(cologne.name, 'Cologne Name')
        self.assertEqual(cologne.denonym, 'Cologne Denonym')

    @override(language='de', deactivate=True)
    def test_update_instance_level_1_2_relation_no_lang(self):
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
        with Context(europe, *lvl_1_2) as context:
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

            europe.name = 'Europe Name'
            europe.denonym = 'Europe Denonym'
            germany.name = 'Germany Name'
            germany.denonym = 'Germany Denonym'
            cologne.name = 'Cologne Name'
            cologne.denonym = 'Cologne Denonym'

            context.update()

            europe.name = 'Europa'
            europe.denonym = 'Europäisch'
            germany.name = 'Deutschland'
            germany.denonym = 'Deutsche'
            cologne.name = 'Köln'
            cologne.denonym = 'Kölner'
        with Context(europe, *lvl_1_2) as context:
            context.read()
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europe Name')
        self.assertEqual(europe.denonym, 'Europe Denonym')
        self.assertEqual(germany.name, 'Germany Name')
        self.assertEqual(germany.denonym, 'Germany Denonym')
        self.assertEqual(cologne.name, 'Cologne Name')
        self.assertEqual(cologne.denonym, 'Cologne Denonym')

    def test_update_instance_level_0_relation_with_lang(self):
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
        with Context(europe) as context:
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

            europe.name = 'Europe Name'
            europe.denonym = 'Europe Denonym'
            germany.name = 'Germany Name'
            germany.denonym = 'Germany Denonym'
            cologne.name = 'Cologne Name'
            cologne.denonym = 'Cologne Denonym'

            context.update('de')

            europe.name = 'Europa'
            europe.denonym = 'Europäisch'
            germany.name = 'Deutschland'
            germany.denonym = 'Deutsche'
            cologne.name = 'Köln'
            cologne.denonym = 'Kölner'
        with Context(europe, *lvl_1_2) as context:
            context.read('de')
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europe Name')
        self.assertEqual(europe.denonym, 'Europe Denonym')
        self.assertEqual(germany.name, 'Deutschland')
        self.assertEqual(germany.denonym, 'Deutsche')
        self.assertEqual(cologne.name, 'Köln')
        self.assertEqual(cologne.denonym, 'Kölner')

    def test_update_instance_level_1_relation_with_lang(self):
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
        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.get(code='EU')
        with Context(europe, *lvl_1) as context:
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

            europe.name = 'Europe Name'
            europe.denonym = 'Europe Denonym'
            germany.name = 'Germany Name'
            germany.denonym = 'Germany Denonym'
            cologne.name = 'Cologne Name'
            cologne.denonym = 'Cologne Denonym'

            context.update('de')

            europe.name = 'Europa'
            europe.denonym = 'Europäisch'
            germany.name = 'Deutschland'
            germany.denonym = 'Deutsche'
            cologne.name = 'Köln'
            cologne.denonym = 'Kölner'
        with Context(europe, *lvl_1_2) as context:
            context.read('de')
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europe Name')
        self.assertEqual(europe.denonym, 'Europe Denonym')
        self.assertEqual(germany.name, 'Germany Name')
        self.assertEqual(germany.denonym, 'Germany Denonym')
        self.assertEqual(cologne.name, 'Köln')
        self.assertEqual(cologne.denonym, 'Kölner')

    def test_update_instance_level_2_relation_with_lang(self):
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
        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.get(code='EU')
        with Context(europe, *lvl_2) as context:
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

            europe.name = 'Europe Name'
            europe.denonym = 'Europe Denonym'
            germany.name = 'Germany Name'
            germany.denonym = 'Germany Denonym'
            cologne.name = 'Cologne Name'
            cologne.denonym = 'Cologne Denonym'

            context.update('de')

            europe.name = 'Europa'
            europe.denonym = 'Europäisch'
            germany.name = 'Deutschland'
            germany.denonym = 'Deutsche'
            cologne.name = 'Köln'
            cologne.denonym = 'Kölner'
        with Context(europe, *lvl_1_2) as context:
            context.read('de')
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europe Name')
        self.assertEqual(europe.denonym, 'Europe Denonym')
        self.assertEqual(germany.name, 'Deutschland')
        self.assertEqual(germany.denonym, 'Deutsche')
        self.assertEqual(cologne.name, 'Cologne Name')
        self.assertEqual(cologne.denonym, 'Cologne Denonym')

    def test_update_instance_level_1_2_relation_with_lang(self):
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
        with Context(europe, *lvl_1_2) as context:
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

            europe.name = 'Europe Name'
            europe.denonym = 'Europe Denonym'
            germany.name = 'Germany Name'
            germany.denonym = 'Germany Denonym'
            cologne.name = 'Cologne Name'
            cologne.denonym = 'Cologne Denonym'

            context.update('de')

            europe.name = 'Europa'
            europe.denonym = 'Europäisch'
            germany.name = 'Deutschland'
            germany.denonym = 'Deutsche'
            cologne.name = 'Köln'
            cologne.denonym = 'Kölner'
        with Context(europe, *lvl_1_2) as context:
            context.read('de')
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europe Name')
        self.assertEqual(europe.denonym, 'Europe Denonym')
        self.assertEqual(germany.name, 'Germany Name')
        self.assertEqual(germany.denonym, 'Germany Denonym')
        self.assertEqual(cologne.name, 'Cologne Name')
        self.assertEqual(cologne.denonym, 'Cologne Denonym')

    @override(language='de', deactivate=True)
    def test_update_prefetched_instance_level_0_relation_no_lang(self):
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
        with Context(europe) as context:
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

            europe.name = 'Europe Name'
            europe.denonym = 'Europe Denonym'
            germany.name = 'Germany Name'
            germany.denonym = 'Germany Denonym'
            cologne.name = 'Cologne Name'
            cologne.denonym = 'Cologne Denonym'

            context.update()

            europe.name = 'Europa'
            europe.denonym = 'Europäisch'
            germany.name = 'Deutschland'
            germany.denonym = 'Deutsche'
            cologne.name = 'Köln'
            cologne.denonym = 'Kölner'
        with Context(europe, *lvl_1_2) as context:
            context.read()
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europe Name')
        self.assertEqual(europe.denonym, 'Europe Denonym')
        self.assertEqual(germany.name, 'Deutschland')
        self.assertEqual(germany.denonym, 'Deutsche')
        self.assertEqual(cologne.name, 'Köln')
        self.assertEqual(cologne.denonym, 'Kölner')

    @override(language='de', deactivate=True)
    def test_update_prefetched_instance_level_1_relation_no_lang(self):
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
        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code='EU')
        with Context(europe, *lvl_1) as context:
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

            europe.name = 'Europe Name'
            europe.denonym = 'Europe Denonym'
            germany.name = 'Germany Name'
            germany.denonym = 'Germany Denonym'
            cologne.name = 'Cologne Name'
            cologne.denonym = 'Cologne Denonym'

            context.update()

            europe.name = 'Europa'
            europe.denonym = 'Europäisch'
            germany.name = 'Deutschland'
            germany.denonym = 'Deutsche'
            cologne.name = 'Köln'
            cologne.denonym = 'Kölner'
        with Context(europe, *lvl_1_2) as context:
            context.read()
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europe Name')
        self.assertEqual(europe.denonym, 'Europe Denonym')
        self.assertEqual(germany.name, 'Germany Name')
        self.assertEqual(germany.denonym, 'Germany Denonym')
        self.assertEqual(cologne.name, 'Köln')
        self.assertEqual(cologne.denonym, 'Kölner')

    @override(language='de', deactivate=True)
    def test_update_prefetched_instance_level_2_relation_no_lang(self):
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
        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code='EU')
        with Context(europe, *lvl_2) as context:
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

            europe.name = 'Europe Name'
            europe.denonym = 'Europe Denonym'
            germany.name = 'Germany Name'
            germany.denonym = 'Germany Denonym'
            cologne.name = 'Cologne Name'
            cologne.denonym = 'Cologne Denonym'

            context.update()

            europe.name = 'Europa'
            europe.denonym = 'Europäisch'
            germany.name = 'Deutschland'
            germany.denonym = 'Deutsche'
            cologne.name = 'Köln'
            cologne.denonym = 'Kölner'
        with Context(europe, *lvl_1_2) as context:
            context.read()
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europe Name')
        self.assertEqual(europe.denonym, 'Europe Denonym')
        self.assertEqual(germany.name, 'Deutschland')
        self.assertEqual(germany.denonym, 'Deutsche')
        self.assertEqual(cologne.name, 'Cologne Name')
        self.assertEqual(cologne.denonym, 'Cologne Denonym')

    @override(language='de', deactivate=True)
    def test_update_prefetched_instance_level_1_2_relation_no_lang(self):
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
        with Context(europe, *lvl_1_2) as context:
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

            europe.name = 'Europe Name'
            europe.denonym = 'Europe Denonym'
            germany.name = 'Germany Name'
            germany.denonym = 'Germany Denonym'
            cologne.name = 'Cologne Name'
            cologne.denonym = 'Cologne Denonym'

            context.update()

            europe.name = 'Europa'
            europe.denonym = 'Europäisch'
            germany.name = 'Deutschland'
            germany.denonym = 'Deutsche'
            cologne.name = 'Köln'
            cologne.denonym = 'Kölner'
        with Context(europe, *lvl_1_2) as context:
            context.read()
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europe Name')
        self.assertEqual(europe.denonym, 'Europe Denonym')
        self.assertEqual(germany.name, 'Germany Name')
        self.assertEqual(germany.denonym, 'Germany Denonym')
        self.assertEqual(cologne.name, 'Cologne Name')
        self.assertEqual(cologne.denonym, 'Cologne Denonym')

    def test_update_prefetched_instance_level_0_relation_with_lang(self):
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
        with Context(europe) as context:
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

            europe.name = 'Europe Name'
            europe.denonym = 'Europe Denonym'
            germany.name = 'Germany Name'
            germany.denonym = 'Germany Denonym'
            cologne.name = 'Cologne Name'
            cologne.denonym = 'Cologne Denonym'

            context.update('de')

            europe.name = 'Europa'
            europe.denonym = 'Europäisch'
            germany.name = 'Deutschland'
            germany.denonym = 'Deutsche'
            cologne.name = 'Köln'
            cologne.denonym = 'Kölner'
        with Context(europe, *lvl_1_2) as context:
            context.read('de')
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europe Name')
        self.assertEqual(europe.denonym, 'Europe Denonym')
        self.assertEqual(germany.name, 'Deutschland')
        self.assertEqual(germany.denonym, 'Deutsche')
        self.assertEqual(cologne.name, 'Köln')
        self.assertEqual(cologne.denonym, 'Kölner')

    def test_update_prefetched_instance_level_1_relation_with_lang(self):
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
        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code='EU')
        with Context(europe, *lvl_1) as context:
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

            europe.name = 'Europe Name'
            europe.denonym = 'Europe Denonym'
            germany.name = 'Germany Name'
            germany.denonym = 'Germany Denonym'
            cologne.name = 'Cologne Name'
            cologne.denonym = 'Cologne Denonym'

            context.update('de')

            europe.name = 'Europa'
            europe.denonym = 'Europäisch'
            germany.name = 'Deutschland'
            germany.denonym = 'Deutsche'
            cologne.name = 'Köln'
            cologne.denonym = 'Kölner'
        with Context(europe, *lvl_1_2) as context:
            context.read('de')
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europe Name')
        self.assertEqual(europe.denonym, 'Europe Denonym')
        self.assertEqual(germany.name, 'Germany Name')
        self.assertEqual(germany.denonym, 'Germany Denonym')
        self.assertEqual(cologne.name, 'Köln')
        self.assertEqual(cologne.denonym, 'Kölner')

    def test_update_prefetched_instance_level_2_relation_with_lang(self):
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
        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code='EU')
        with Context(europe, *lvl_2) as context:
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

            europe.name = 'Europe Name'
            europe.denonym = 'Europe Denonym'
            germany.name = 'Germany Name'
            germany.denonym = 'Germany Denonym'
            cologne.name = 'Cologne Name'
            cologne.denonym = 'Cologne Denonym'

            context.update('de')

            europe.name = 'Europa'
            europe.denonym = 'Europäisch'
            germany.name = 'Deutschland'
            germany.denonym = 'Deutsche'
            cologne.name = 'Köln'
            cologne.denonym = 'Kölner'
        with Context(europe, *lvl_1_2) as context:
            context.read('de')
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europe Name')
        self.assertEqual(europe.denonym, 'Europe Denonym')
        self.assertEqual(germany.name, 'Deutschland')
        self.assertEqual(germany.denonym, 'Deutsche')
        self.assertEqual(cologne.name, 'Cologne Name')
        self.assertEqual(cologne.denonym, 'Cologne Denonym')

    def test_update_prefetched_instance_level_1_2_relation_with_lang(self):
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
        with Context(europe, *lvl_1_2) as context:
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

            europe.name = 'Europe Name'
            europe.denonym = 'Europe Denonym'
            germany.name = 'Germany Name'
            germany.denonym = 'Germany Denonym'
            cologne.name = 'Cologne Name'
            cologne.denonym = 'Cologne Denonym'

            context.update('de')

            europe.name = 'Europa'
            europe.denonym = 'Europäisch'
            germany.name = 'Deutschland'
            germany.denonym = 'Deutsche'
            cologne.name = 'Köln'
            cologne.denonym = 'Kölner'
        with Context(europe, *lvl_1_2) as context:
            context.read('de')
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europe Name')
        self.assertEqual(europe.denonym, 'Europe Denonym')
        self.assertEqual(germany.name, 'Germany Name')
        self.assertEqual(germany.denonym, 'Germany Denonym')
        self.assertEqual(cologne.name, 'Cologne Name')
        self.assertEqual(cologne.denonym, 'Cologne Denonym')

    def test_update_instance_invalid_lang(self):
        create_samples(
            continent_names=['europe'],
            continent_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        europe = Continent.objects.get(code='EU')

        with self.assertRaises(ValueError) as error:
            with Context(europe) as context:
                context.update('xx')

        self.assertEqual(
            error.exception.args[0],
            '`xx` is not a supported language.'
        )

    @override(language='de', deactivate=True)
    def test_update_queryset_level_0_relation_no_lang(self):
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
        with Context(continents) as context:
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

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

            context.update()

            europe.name = 'Europa'
            europe.denonym = 'Europäisch'
            germany.name = 'Deutschland'
            germany.denonym = 'Deutsche'
            cologne.name = 'Köln'
            cologne.denonym = 'Kölner'
            asia.name = 'Asien'
            asia.denonym = 'Asiatisch'
            south_korea.name = 'Südkorea'
            south_korea.denonym = 'Südkoreanisch'
            seoul.name = 'Seül'
            seoul.denonym = 'Seüler'
        with Context(continents, *lvl_1_2) as context:
            context.read()
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

        self.assertEqual(europe.name, 'Europe Name')
        self.assertEqual(europe.denonym, 'Europe Denonym')
        self.assertEqual(germany.name, 'Deutschland')
        self.assertEqual(germany.denonym, 'Deutsche')
        self.assertEqual(cologne.name, 'Köln')
        self.assertEqual(cologne.denonym, 'Kölner')
        self.assertEqual(asia.name, 'Asia Name')
        self.assertEqual(asia.denonym, 'Asia Denonym')
        self.assertEqual(south_korea.name, 'Südkorea')
        self.assertEqual(south_korea.denonym, 'Südkoreanisch')
        self.assertEqual(seoul.name, 'Seül')
        self.assertEqual(seoul.denonym, 'Seüler')

    @override(language='de', deactivate=True)
    def test_update_queryset_level_1_relation_no_lang(self):
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
        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.all()
        with Context(continents, *lvl_1) as context:
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

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

            context.update()

            europe.name = 'Europa'
            europe.denonym = 'Europäisch'
            germany.name = 'Deutschland'
            germany.denonym = 'Deutsche'
            cologne.name = 'Köln'
            cologne.denonym = 'Kölner'
            asia.name = 'Asien'
            asia.denonym = 'Asiatisch'
            south_korea.name = 'Südkorea'
            south_korea.denonym = 'Südkoreanisch'
            seoul.name = 'Seül'
            seoul.denonym = 'Seüler'
        with Context(continents, *lvl_1_2) as context:
            context.read()
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

        self.assertEqual(europe.name, 'Europe Name')
        self.assertEqual(europe.denonym, 'Europe Denonym')
        self.assertEqual(germany.name, 'Germany Name')
        self.assertEqual(germany.denonym, 'Germany Denonym')
        self.assertEqual(cologne.name, 'Köln')
        self.assertEqual(cologne.denonym, 'Kölner')
        self.assertEqual(asia.name, 'Asia Name')
        self.assertEqual(asia.denonym, 'Asia Denonym')
        self.assertEqual(south_korea.name, 'South Korea Name')
        self.assertEqual(south_korea.denonym, 'South Korea Denonym')
        self.assertEqual(seoul.name, 'Seül')
        self.assertEqual(seoul.denonym, 'Seüler')

    @override(language='de', deactivate=True)
    def test_update_queryset_level_2_relation_no_lang(self):
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
        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.all()
        with Context(continents, *lvl_2) as context:
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

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

            context.update()

            europe.name = 'Europa'
            europe.denonym = 'Europäisch'
            germany.name = 'Deutschland'
            germany.denonym = 'Deutsche'
            cologne.name = 'Köln'
            cologne.denonym = 'Kölner'
            asia.name = 'Asien'
            asia.denonym = 'Asiatisch'
            south_korea.name = 'Südkorea'
            south_korea.denonym = 'Südkoreanisch'
            seoul.name = 'Seül'
            seoul.denonym = 'Seüler'
        with Context(continents, *lvl_1_2) as context:
            context.read()
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

        self.assertEqual(europe.name, 'Europe Name')
        self.assertEqual(europe.denonym, 'Europe Denonym')
        self.assertEqual(germany.name, 'Deutschland')
        self.assertEqual(germany.denonym, 'Deutsche')
        self.assertEqual(cologne.name, 'Cologne Name')
        self.assertEqual(cologne.denonym, 'Cologne Denonym')
        self.assertEqual(asia.name, 'Asia Name')
        self.assertEqual(asia.denonym, 'Asia Denonym')
        self.assertEqual(south_korea.name, 'Südkorea')
        self.assertEqual(south_korea.denonym, 'Südkoreanisch')
        self.assertEqual(seoul.name, 'Seoul Name')
        self.assertEqual(seoul.denonym, 'Seoul Denonym')

    @override(language='de', deactivate=True)
    def test_update_queryset_level_1_2_relation_no_lang(self):
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
        with Context(continents, *lvl_1_2) as context:
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

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

            context.update()

            europe.name = 'Europa'
            europe.denonym = 'Europäisch'
            germany.name = 'Deutschland'
            germany.denonym = 'Deutsche'
            cologne.name = 'Köln'
            cologne.denonym = 'Kölner'
            asia.name = 'Asien'
            asia.denonym = 'Asiatisch'
            south_korea.name = 'Südkorea'
            south_korea.denonym = 'Südkoreanisch'
            seoul.name = 'Seül'
            seoul.denonym = 'Seüler'
        with Context(continents, *lvl_1_2) as context:
            context.read()
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

        self.assertEqual(europe.name, 'Europe Name')
        self.assertEqual(europe.denonym, 'Europe Denonym')
        self.assertEqual(germany.name, 'Germany Name')
        self.assertEqual(germany.denonym, 'Germany Denonym')
        self.assertEqual(cologne.name, 'Cologne Name')
        self.assertEqual(cologne.denonym, 'Cologne Denonym')
        self.assertEqual(asia.name, 'Asia Name')
        self.assertEqual(asia.denonym, 'Asia Denonym')
        self.assertEqual(south_korea.name, 'South Korea Name')
        self.assertEqual(south_korea.denonym, 'South Korea Denonym')
        self.assertEqual(seoul.name, 'Seoul Name')
        self.assertEqual(seoul.denonym, 'Seoul Denonym')

    def test_update_queryset_level_0_relation_with_lang(self):
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
        with Context(continents) as context:
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

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

            context.update('de')

            europe.name = 'Europa'
            europe.denonym = 'Europäisch'
            germany.name = 'Deutschland'
            germany.denonym = 'Deutsche'
            cologne.name = 'Köln'
            cologne.denonym = 'Kölner'
            asia.name = 'Asien'
            asia.denonym = 'Asiatisch'
            south_korea.name = 'Südkorea'
            south_korea.denonym = 'Südkoreanisch'
            seoul.name = 'Seül'
            seoul.denonym = 'Seüler'
        with Context(continents, *lvl_1_2) as context:
            context.read('de')
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

        self.assertEqual(europe.name, 'Europe Name')
        self.assertEqual(europe.denonym, 'Europe Denonym')
        self.assertEqual(germany.name, 'Deutschland')
        self.assertEqual(germany.denonym, 'Deutsche')
        self.assertEqual(cologne.name, 'Köln')
        self.assertEqual(cologne.denonym, 'Kölner')
        self.assertEqual(asia.name, 'Asia Name')
        self.assertEqual(asia.denonym, 'Asia Denonym')
        self.assertEqual(south_korea.name, 'Südkorea')
        self.assertEqual(south_korea.denonym, 'Südkoreanisch')
        self.assertEqual(seoul.name, 'Seül')
        self.assertEqual(seoul.denonym, 'Seüler')

    def test_update_queryset_level_1_relation_with_lang(self):
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
        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.all()
        with Context(continents, *lvl_1) as context:
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

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

            context.update('de')

            europe.name = 'Europa'
            europe.denonym = 'Europäisch'
            germany.name = 'Deutschland'
            germany.denonym = 'Deutsche'
            cologne.name = 'Köln'
            cologne.denonym = 'Kölner'
            asia.name = 'Asien'
            asia.denonym = 'Asiatisch'
            south_korea.name = 'Südkorea'
            south_korea.denonym = 'Südkoreanisch'
            seoul.name = 'Seül'
            seoul.denonym = 'Seüler'
        with Context(continents, *lvl_1_2) as context:
            context.read('de')
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

        self.assertEqual(europe.name, 'Europe Name')
        self.assertEqual(europe.denonym, 'Europe Denonym')
        self.assertEqual(germany.name, 'Germany Name')
        self.assertEqual(germany.denonym, 'Germany Denonym')
        self.assertEqual(cologne.name, 'Köln')
        self.assertEqual(cologne.denonym, 'Kölner')
        self.assertEqual(asia.name, 'Asia Name')
        self.assertEqual(asia.denonym, 'Asia Denonym')
        self.assertEqual(south_korea.name, 'South Korea Name')
        self.assertEqual(south_korea.denonym, 'South Korea Denonym')
        self.assertEqual(seoul.name, 'Seül')
        self.assertEqual(seoul.denonym, 'Seüler')

    def test_update_queryset_level_2_relation_with_lang(self):
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
        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.all()
        with Context(continents, *lvl_2) as context:
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

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

            context.update('de')

            europe.name = 'Europa'
            europe.denonym = 'Europäisch'
            germany.name = 'Deutschland'
            germany.denonym = 'Deutsche'
            cologne.name = 'Köln'
            cologne.denonym = 'Kölner'
            asia.name = 'Asien'
            asia.denonym = 'Asiatisch'
            south_korea.name = 'Südkorea'
            south_korea.denonym = 'Südkoreanisch'
            seoul.name = 'Seül'
            seoul.denonym = 'Seüler'
        with Context(continents, *lvl_1_2) as context:
            context.read('de')
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

        self.assertEqual(europe.name, 'Europe Name')
        self.assertEqual(europe.denonym, 'Europe Denonym')
        self.assertEqual(germany.name, 'Deutschland')
        self.assertEqual(germany.denonym, 'Deutsche')
        self.assertEqual(cologne.name, 'Cologne Name')
        self.assertEqual(cologne.denonym, 'Cologne Denonym')
        self.assertEqual(asia.name, 'Asia Name')
        self.assertEqual(asia.denonym, 'Asia Denonym')
        self.assertEqual(south_korea.name, 'Südkorea')
        self.assertEqual(south_korea.denonym, 'Südkoreanisch')
        self.assertEqual(seoul.name, 'Seoul Name')
        self.assertEqual(seoul.denonym, 'Seoul Denonym')

    def test_update_queryset_level_1_2_relation_with_lang(self):
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
        with Context(continents, *lvl_1_2) as context:
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

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

            context.update('de')

            europe.name = 'Europa'
            europe.denonym = 'Europäisch'
            germany.name = 'Deutschland'
            germany.denonym = 'Deutsche'
            cologne.name = 'Köln'
            cologne.denonym = 'Kölner'
            asia.name = 'Asien'
            asia.denonym = 'Asiatisch'
            south_korea.name = 'Südkorea'
            south_korea.denonym = 'Südkoreanisch'
            seoul.name = 'Seül'
            seoul.denonym = 'Seüler'
        with Context(continents, *lvl_1_2) as context:
            context.read('de')
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

        self.assertEqual(europe.name, 'Europe Name')
        self.assertEqual(europe.denonym, 'Europe Denonym')
        self.assertEqual(germany.name, 'Germany Name')
        self.assertEqual(germany.denonym, 'Germany Denonym')
        self.assertEqual(cologne.name, 'Cologne Name')
        self.assertEqual(cologne.denonym, 'Cologne Denonym')
        self.assertEqual(asia.name, 'Asia Name')
        self.assertEqual(asia.denonym, 'Asia Denonym')
        self.assertEqual(south_korea.name, 'South Korea Name')
        self.assertEqual(south_korea.denonym, 'South Korea Denonym')
        self.assertEqual(seoul.name, 'Seoul Name')
        self.assertEqual(seoul.denonym, 'Seoul Denonym')

    @override(language='de', deactivate=True)
    def test_update_prefetched_queryset_level_0_relation_no_lang(self):
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
        with Context(continents) as context:
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

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

            context.update()

            europe.name = 'Europa'
            europe.denonym = 'Europäisch'
            germany.name = 'Deutschland'
            germany.denonym = 'Deutsche'
            cologne.name = 'Köln'
            cologne.denonym = 'Kölner'
            asia.name = 'Asien'
            asia.denonym = 'Asiatisch'
            south_korea.name = 'Südkorea'
            south_korea.denonym = 'Südkoreanisch'
            seoul.name = 'Seül'
            seoul.denonym = 'Seüler'
        with Context(continents, *lvl_1_2) as context:
            context.read()
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

        self.assertEqual(europe.name, 'Europe Name')
        self.assertEqual(europe.denonym, 'Europe Denonym')
        self.assertEqual(germany.name, 'Deutschland')
        self.assertEqual(germany.denonym, 'Deutsche')
        self.assertEqual(cologne.name, 'Köln')
        self.assertEqual(cologne.denonym, 'Kölner')
        self.assertEqual(asia.name, 'Asia Name')
        self.assertEqual(asia.denonym, 'Asia Denonym')
        self.assertEqual(south_korea.name, 'Südkorea')
        self.assertEqual(south_korea.denonym, 'Südkoreanisch')
        self.assertEqual(seoul.name, 'Seül')
        self.assertEqual(seoul.denonym, 'Seüler')

    @override(language='de', deactivate=True)
    def test_update_prefetched_queryset_level_1_relation_no_lang(self):
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
        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.prefetch_related(*lvl_1_2)
        with Context(continents, *lvl_1) as context:
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

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

            context.update()

            europe.name = 'Europa'
            europe.denonym = 'Europäisch'
            germany.name = 'Deutschland'
            germany.denonym = 'Deutsche'
            cologne.name = 'Köln'
            cologne.denonym = 'Kölner'
            asia.name = 'Asien'
            asia.denonym = 'Asiatisch'
            south_korea.name = 'Südkorea'
            south_korea.denonym = 'Südkoreanisch'
            seoul.name = 'Seül'
            seoul.denonym = 'Seüler'
        with Context(continents, *lvl_1_2) as context:
            context.read()
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

        self.assertEqual(europe.name, 'Europe Name')
        self.assertEqual(europe.denonym, 'Europe Denonym')
        self.assertEqual(germany.name, 'Germany Name')
        self.assertEqual(germany.denonym, 'Germany Denonym')
        self.assertEqual(cologne.name, 'Köln')
        self.assertEqual(cologne.denonym, 'Kölner')
        self.assertEqual(asia.name, 'Asia Name')
        self.assertEqual(asia.denonym, 'Asia Denonym')
        self.assertEqual(south_korea.name, 'South Korea Name')
        self.assertEqual(south_korea.denonym, 'South Korea Denonym')
        self.assertEqual(seoul.name, 'Seül')
        self.assertEqual(seoul.denonym, 'Seüler')

    @override(language='de', deactivate=True)
    def test_update_prefetched_queryset_level_2_relation_no_lang(self):
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
        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.prefetch_related(*lvl_1_2)
        with Context(continents, *lvl_2) as context:
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

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

            context.update()

            europe.name = 'Europa'
            europe.denonym = 'Europäisch'
            germany.name = 'Deutschland'
            germany.denonym = 'Deutsche'
            cologne.name = 'Köln'
            cologne.denonym = 'Kölner'
            asia.name = 'Asien'
            asia.denonym = 'Asiatisch'
            south_korea.name = 'Südkorea'
            south_korea.denonym = 'Südkoreanisch'
            seoul.name = 'Seül'
            seoul.denonym = 'Seüler'
        with Context(continents, *lvl_1_2) as context:
            context.read()
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

        self.assertEqual(europe.name, 'Europe Name')
        self.assertEqual(europe.denonym, 'Europe Denonym')
        self.assertEqual(germany.name, 'Deutschland')
        self.assertEqual(germany.denonym, 'Deutsche')
        self.assertEqual(cologne.name, 'Cologne Name')
        self.assertEqual(cologne.denonym, 'Cologne Denonym')
        self.assertEqual(asia.name, 'Asia Name')
        self.assertEqual(asia.denonym, 'Asia Denonym')
        self.assertEqual(south_korea.name, 'Südkorea')
        self.assertEqual(south_korea.denonym, 'Südkoreanisch')
        self.assertEqual(seoul.name, 'Seoul Name')
        self.assertEqual(seoul.denonym, 'Seoul Denonym')

    @override(language='de', deactivate=True)
    def test_update_prefetched_queryset_level_1_2_relation_no_lang(self):
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
        with Context(continents, *lvl_1_2) as context:
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

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

            context.update()

            europe.name = 'Europa'
            europe.denonym = 'Europäisch'
            germany.name = 'Deutschland'
            germany.denonym = 'Deutsche'
            cologne.name = 'Köln'
            cologne.denonym = 'Kölner'
            asia.name = 'Asien'
            asia.denonym = 'Asiatisch'
            south_korea.name = 'Südkorea'
            south_korea.denonym = 'Südkoreanisch'
            seoul.name = 'Seül'
            seoul.denonym = 'Seüler'
        with Context(continents, *lvl_1_2) as context:
            context.read()
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

        self.assertEqual(europe.name, 'Europe Name')
        self.assertEqual(europe.denonym, 'Europe Denonym')
        self.assertEqual(germany.name, 'Germany Name')
        self.assertEqual(germany.denonym, 'Germany Denonym')
        self.assertEqual(cologne.name, 'Cologne Name')
        self.assertEqual(cologne.denonym, 'Cologne Denonym')
        self.assertEqual(asia.name, 'Asia Name')
        self.assertEqual(asia.denonym, 'Asia Denonym')
        self.assertEqual(south_korea.name, 'South Korea Name')
        self.assertEqual(south_korea.denonym, 'South Korea Denonym')
        self.assertEqual(seoul.name, 'Seoul Name')
        self.assertEqual(seoul.denonym, 'Seoul Denonym')

    def test_update_prefetched_queryset_level_0_relation_with_lang(self):
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
        with Context(continents) as context:
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

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

            context.update('de')

            europe.name = 'Europa'
            europe.denonym = 'Europäisch'
            germany.name = 'Deutschland'
            germany.denonym = 'Deutsche'
            cologne.name = 'Köln'
            cologne.denonym = 'Kölner'
            asia.name = 'Asien'
            asia.denonym = 'Asiatisch'
            south_korea.name = 'Südkorea'
            south_korea.denonym = 'Südkoreanisch'
            seoul.name = 'Seül'
            seoul.denonym = 'Seüler'
        with Context(continents, *lvl_1_2) as context:
            context.read('de')
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

        self.assertEqual(europe.name, 'Europe Name')
        self.assertEqual(europe.denonym, 'Europe Denonym')
        self.assertEqual(germany.name, 'Deutschland')
        self.assertEqual(germany.denonym, 'Deutsche')
        self.assertEqual(cologne.name, 'Köln')
        self.assertEqual(cologne.denonym, 'Kölner')
        self.assertEqual(asia.name, 'Asia Name')
        self.assertEqual(asia.denonym, 'Asia Denonym')
        self.assertEqual(south_korea.name, 'Südkorea')
        self.assertEqual(south_korea.denonym, 'Südkoreanisch')
        self.assertEqual(seoul.name, 'Seül')
        self.assertEqual(seoul.denonym, 'Seüler')

    def test_update_prefetched_queryset_level_1_relation_with_lang(self):
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
        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.prefetch_related(*lvl_1_2)
        with Context(continents, *lvl_1) as context:
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

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

            context.update('de')

            europe.name = 'Europa'
            europe.denonym = 'Europäisch'
            germany.name = 'Deutschland'
            germany.denonym = 'Deutsche'
            cologne.name = 'Köln'
            cologne.denonym = 'Kölner'
            asia.name = 'Asien'
            asia.denonym = 'Asiatisch'
            south_korea.name = 'Südkorea'
            south_korea.denonym = 'Südkoreanisch'
            seoul.name = 'Seül'
            seoul.denonym = 'Seüler'
        with Context(continents, *lvl_1_2) as context:
            context.read('de')
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

        self.assertEqual(europe.name, 'Europe Name')
        self.assertEqual(europe.denonym, 'Europe Denonym')
        self.assertEqual(germany.name, 'Germany Name')
        self.assertEqual(germany.denonym, 'Germany Denonym')
        self.assertEqual(cologne.name, 'Köln')
        self.assertEqual(cologne.denonym, 'Kölner')
        self.assertEqual(asia.name, 'Asia Name')
        self.assertEqual(asia.denonym, 'Asia Denonym')
        self.assertEqual(south_korea.name, 'South Korea Name')
        self.assertEqual(south_korea.denonym, 'South Korea Denonym')
        self.assertEqual(seoul.name, 'Seül')
        self.assertEqual(seoul.denonym, 'Seüler')

    def test_update_prefetched_queryset_level_2_relation_with_lang(self):
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
        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.prefetch_related(*lvl_1_2)
        with Context(continents, *lvl_2) as context:
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

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

            context.update('de')

            europe.name = 'Europa'
            europe.denonym = 'Europäisch'
            germany.name = 'Deutschland'
            germany.denonym = 'Deutsche'
            cologne.name = 'Köln'
            cologne.denonym = 'Kölner'
            asia.name = 'Asien'
            asia.denonym = 'Asiatisch'
            south_korea.name = 'Südkorea'
            south_korea.denonym = 'Südkoreanisch'
            seoul.name = 'Seül'
            seoul.denonym = 'Seüler'
        with Context(continents, *lvl_1_2) as context:
            context.read('de')
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

        self.assertEqual(europe.name, 'Europe Name')
        self.assertEqual(europe.denonym, 'Europe Denonym')
        self.assertEqual(germany.name, 'Deutschland')
        self.assertEqual(germany.denonym, 'Deutsche')
        self.assertEqual(cologne.name, 'Cologne Name')
        self.assertEqual(cologne.denonym, 'Cologne Denonym')
        self.assertEqual(asia.name, 'Asia Name')
        self.assertEqual(asia.denonym, 'Asia Denonym')
        self.assertEqual(south_korea.name, 'Südkorea')
        self.assertEqual(south_korea.denonym, 'Südkoreanisch')
        self.assertEqual(seoul.name, 'Seoul Name')
        self.assertEqual(seoul.denonym, 'Seoul Denonym')

    def test_update_prefetched_queryset_level_1_2_relation_with_lang(self):
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
        with Context(continents, *lvl_1_2) as context:
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

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

            context.update('de')

            europe.name = 'Europa'
            europe.denonym = 'Europäisch'
            germany.name = 'Deutschland'
            germany.denonym = 'Deutsche'
            cologne.name = 'Köln'
            cologne.denonym = 'Kölner'
            asia.name = 'Asien'
            asia.denonym = 'Asiatisch'
            south_korea.name = 'Südkorea'
            south_korea.denonym = 'Südkoreanisch'
            seoul.name = 'Seül'
            seoul.denonym = 'Seüler'
        with Context(continents, *lvl_1_2) as context:
            context.read('de')
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

        self.assertEqual(europe.name, 'Europe Name')
        self.assertEqual(europe.denonym, 'Europe Denonym')
        self.assertEqual(germany.name, 'Germany Name')
        self.assertEqual(germany.denonym, 'Germany Denonym')
        self.assertEqual(cologne.name, 'Cologne Name')
        self.assertEqual(cologne.denonym, 'Cologne Denonym')
        self.assertEqual(asia.name, 'Asia Name')
        self.assertEqual(asia.denonym, 'Asia Denonym')
        self.assertEqual(south_korea.name, 'South Korea Name')
        self.assertEqual(south_korea.denonym, 'South Korea Denonym')
        self.assertEqual(seoul.name, 'Seoul Name')
        self.assertEqual(seoul.denonym, 'Seoul Denonym')

    def test_update_queryset_invalid_lang(self):
        create_samples(
            continent_names=['europe'],
            continent_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        continents = Continent.objects.all()

        with self.assertRaises(ValueError) as error:
            with Context(continents) as context:
                context.update('xx')

        self.assertEqual(
            error.exception.args[0],
            '`xx` is not a supported language.'
        )

    @override(language='de', deactivate=True)
    def test_delete_instance_level_0_relation_no_lang(self):
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
        with Context(europe) as context:
            context.delete()
        with Context(europe, *lvl_1_2) as context:
            context.read()
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europe')
        self.assertEqual(europe.denonym, 'European')
        self.assertEqual(germany.name, 'Deutschland')
        self.assertEqual(germany.denonym, 'Deutsche')
        self.assertEqual(cologne.name, 'Köln')
        self.assertEqual(cologne.denonym, 'Kölner')

    @override(language='de', deactivate=True)
    def test_delete_instance_level_1_relation_no_lang(self):
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
        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.get(code='EU')
        with Context(europe, *lvl_1) as context:
            context.delete()
        with Context(europe, *lvl_1_2) as context:
            context.read()
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europe')
        self.assertEqual(europe.denonym, 'European')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Köln')
        self.assertEqual(cologne.denonym, 'Kölner')

    @override(language='de', deactivate=True)
    def test_delete_instance_level_2_relation_no_lang(self):
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
        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.get(code='EU')
        with Context(europe, *lvl_2) as context:
            context.delete()
        with Context(europe, *lvl_1_2) as context:
            context.read()
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europe')
        self.assertEqual(europe.denonym, 'European')
        self.assertEqual(germany.name, 'Deutschland')
        self.assertEqual(germany.denonym, 'Deutsche')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')

    @override(language='de', deactivate=True)
    def test_delete_instance_level_1_2_relation_no_lang(self):
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
        with Context(europe, *lvl_1_2) as context:
            context.delete()
        with Context(europe, *lvl_1_2) as context:
            context.read()
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europe')
        self.assertEqual(europe.denonym, 'European')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')

    def test_delete_instance_level_0_relation_with_lang(self):
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
        with Context(europe) as context:
            context.delete('de')
        with Context(europe, *lvl_1_2) as context:
            context.read('de')
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europe')
        self.assertEqual(europe.denonym, 'European')
        self.assertEqual(germany.name, 'Deutschland')
        self.assertEqual(germany.denonym, 'Deutsche')
        self.assertEqual(cologne.name, 'Köln')
        self.assertEqual(cologne.denonym, 'Kölner')

    def test_delete_instance_level_1_relation_with_lang(self):
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
        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.get(code='EU')
        with Context(europe, *lvl_1) as context:
            context.delete('de')
        with Context(europe, *lvl_1_2) as context:
            context.read('de')
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europe')
        self.assertEqual(europe.denonym, 'European')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Köln')
        self.assertEqual(cologne.denonym, 'Kölner')

    def test_delete_instance_level_2_relation_with_lang(self):
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
        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.get(code='EU')
        with Context(europe, *lvl_2) as context:
            context.delete('de')
        with Context(europe, *lvl_1_2) as context:
            context.read('de')
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europe')
        self.assertEqual(europe.denonym, 'European')
        self.assertEqual(germany.name, 'Deutschland')
        self.assertEqual(germany.denonym, 'Deutsche')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')

    def test_delete_instance_level_1_2_relation_with_lang(self):
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
        with Context(europe, *lvl_1_2) as context:
            context.delete('de')
        with Context(europe, *lvl_1_2) as context:
            context.read('de')
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europe')
        self.assertEqual(europe.denonym, 'European')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')

    @override(language='de', deactivate=True)
    def test_delete_prefetched_instance_level_0_relation_no_lang(self):
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
        with Context(europe) as context:
            context.delete()
        with Context(europe, *lvl_1_2) as context:
            context.read()
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europe')
        self.assertEqual(europe.denonym, 'European')
        self.assertEqual(germany.name, 'Deutschland')
        self.assertEqual(germany.denonym, 'Deutsche')
        self.assertEqual(cologne.name, 'Köln')
        self.assertEqual(cologne.denonym, 'Kölner')

    @override(language='de', deactivate=True)
    def test_delete_prefetched_instance_level_1_relation_no_lang(self):
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
        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code='EU')
        with Context(europe, *lvl_1) as context:
            context.delete()
        with Context(europe, *lvl_1_2) as context:
            context.read()
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europe')
        self.assertEqual(europe.denonym, 'European')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Köln')
        self.assertEqual(cologne.denonym, 'Kölner')

    @override(language='de', deactivate=True)
    def test_delete_prefetched_instance_level_2_relation_no_lang(self):
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
        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code='EU')
        with Context(europe, *lvl_2) as context:
            context.delete()
        with Context(europe, *lvl_1_2) as context:
            context.read()
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europe')
        self.assertEqual(europe.denonym, 'European')
        self.assertEqual(germany.name, 'Deutschland')
        self.assertEqual(germany.denonym, 'Deutsche')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')

    @override(language='de', deactivate=True)
    def test_delete_prefetched_instance_level_1_2_relation_no_lang(self):
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
        with Context(europe, *lvl_1_2) as context:
            context.delete()
        with Context(europe, *lvl_1_2) as context:
            context.read()
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europe')
        self.assertEqual(europe.denonym, 'European')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')

    def test_delete_prefetched_instance_level_0_relation_with_lang(self):
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
        with Context(europe) as context:
            context.delete('de')
        with Context(europe, *lvl_1_2) as context:
            context.read('de')
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europe')
        self.assertEqual(europe.denonym, 'European')
        self.assertEqual(germany.name, 'Deutschland')
        self.assertEqual(germany.denonym, 'Deutsche')
        self.assertEqual(cologne.name, 'Köln')
        self.assertEqual(cologne.denonym, 'Kölner')

    def test_delete_prefetched_instance_level_1_relation_with_lang(self):
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
        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code='EU')
        with Context(europe, *lvl_1) as context:
            context.delete('de')
        with Context(europe, *lvl_1_2) as context:
            context.read('de')
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europe')
        self.assertEqual(europe.denonym, 'European')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Köln')
        self.assertEqual(cologne.denonym, 'Kölner')

    def test_delete_prefetched_instance_level_2_relation_with_lang(self):
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
        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code='EU')
        with Context(europe, *lvl_2) as context:
            context.delete('de')
        with Context(europe, *lvl_1_2) as context:
            context.read('de')
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europe')
        self.assertEqual(europe.denonym, 'European')
        self.assertEqual(germany.name, 'Deutschland')
        self.assertEqual(germany.denonym, 'Deutsche')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')

    def test_delete_prefetched_instance_level_1_2_relation_with_lang(self):
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
        with Context(europe, *lvl_1_2) as context:
            context.delete('de')
        with Context(europe, *lvl_1_2) as context:
            context.read('de')
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europe')
        self.assertEqual(europe.denonym, 'European')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')

    def test_delete_instance_invalid_lang(self):
        create_samples(
            continent_names=['europe'],
            continent_fields=['name', 'denonym'],
            langs=['de']
        )

        europe = Continent.objects.get(code='EU')

        with self.assertRaises(ValueError) as error:
            with Context(europe) as context:
                context.update('xx')

        self.assertEqual(
            error.exception.args[0],
            '`xx` is not a supported language.'
        )

    @override(language='de', deactivate=True)
    def test_delete_queryset_level_0_relation_no_lang(self):
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
        with Context(continents) as context:
            context.delete()
        with Context(continents, *lvl_1_2) as context:
            context.read()
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

        self.assertEqual(europe.name, 'Europe')
        self.assertEqual(europe.denonym, 'European')
        self.assertEqual(germany.name, 'Deutschland')
        self.assertEqual(germany.denonym, 'Deutsche')
        self.assertEqual(cologne.name, 'Köln')
        self.assertEqual(cologne.denonym, 'Kölner')
        self.assertEqual(asia.name, 'Asia')
        self.assertEqual(asia.denonym, 'Asian')
        self.assertEqual(south_korea.name, 'Südkorea')
        self.assertEqual(south_korea.denonym, 'Südkoreanisch')
        self.assertEqual(seoul.name, 'Seül')
        self.assertEqual(seoul.denonym, 'Seüler')

    @override(language='de', deactivate=True)
    def test_delete_queryset_level_1_relation_no_lang(self):
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
        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.all()
        with Context(continents, *lvl_1) as context:
            context.delete()
        with Context(continents, *lvl_1_2) as context:
            context.read()
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

        self.assertEqual(europe.name, 'Europe')
        self.assertEqual(europe.denonym, 'European')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Köln')
        self.assertEqual(cologne.denonym, 'Kölner')
        self.assertEqual(asia.name, 'Asia')
        self.assertEqual(asia.denonym, 'Asian')
        self.assertEqual(south_korea.name, 'South Korea')
        self.assertEqual(south_korea.denonym, 'South Korean')
        self.assertEqual(seoul.name, 'Seül')
        self.assertEqual(seoul.denonym, 'Seüler')

    @override(language='de', deactivate=True)
    def test_delete_queryset_level_2_relation_no_lang(self):
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
        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.all()
        with Context(continents, *lvl_2) as context:
            context.delete()
        with Context(continents, *lvl_1_2) as context:
            context.read()
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

        self.assertEqual(europe.name, 'Europe')
        self.assertEqual(europe.denonym, 'European')
        self.assertEqual(germany.name, 'Deutschland')
        self.assertEqual(germany.denonym, 'Deutsche')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')
        self.assertEqual(asia.name, 'Asia')
        self.assertEqual(asia.denonym, 'Asian')
        self.assertEqual(south_korea.name, 'Südkorea')
        self.assertEqual(south_korea.denonym, 'Südkoreanisch')
        self.assertEqual(seoul.name, 'Seoul')
        self.assertEqual(seoul.denonym, 'Seouler')

    @override(language='de', deactivate=True)
    def test_delete_queryset_level_1_2_relation_no_lang(self):
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
        with Context(continents, *lvl_1_2) as context:
            context.delete()
        with Context(continents, *lvl_1_2) as context:
            context.read()
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

        self.assertEqual(europe.name, 'Europe')
        self.assertEqual(europe.denonym, 'European')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')
        self.assertEqual(asia.name, 'Asia')
        self.assertEqual(asia.denonym, 'Asian')
        self.assertEqual(south_korea.name, 'South Korea')
        self.assertEqual(south_korea.denonym, 'South Korean')
        self.assertEqual(seoul.name, 'Seoul')
        self.assertEqual(seoul.denonym, 'Seouler')

    def test_delete_queryset_level_0_relation_with_lang(self):
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
        with Context(continents) as context:
            context.delete('de')
        with Context(continents, *lvl_1_2) as context:
            context.read('de')
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

        self.assertEqual(europe.name, 'Europe')
        self.assertEqual(europe.denonym, 'European')
        self.assertEqual(germany.name, 'Deutschland')
        self.assertEqual(germany.denonym, 'Deutsche')
        self.assertEqual(cologne.name, 'Köln')
        self.assertEqual(cologne.denonym, 'Kölner')
        self.assertEqual(asia.name, 'Asia')
        self.assertEqual(asia.denonym, 'Asian')
        self.assertEqual(south_korea.name, 'Südkorea')
        self.assertEqual(south_korea.denonym, 'Südkoreanisch')
        self.assertEqual(seoul.name, 'Seül')
        self.assertEqual(seoul.denonym, 'Seüler')

    def test_delete_queryset_level_1_relation_with_lang(self):
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
        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.all()
        with Context(continents, *lvl_1) as context:
            context.delete('de')
        with Context(continents, *lvl_1_2) as context:
            context.read('de')
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

        self.assertEqual(europe.name, 'Europe')
        self.assertEqual(europe.denonym, 'European')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Köln')
        self.assertEqual(cologne.denonym, 'Kölner')
        self.assertEqual(asia.name, 'Asia')
        self.assertEqual(asia.denonym, 'Asian')
        self.assertEqual(south_korea.name, 'South Korea')
        self.assertEqual(south_korea.denonym, 'South Korean')
        self.assertEqual(seoul.name, 'Seül')
        self.assertEqual(seoul.denonym, 'Seüler')

    def test_delete_queryset_level_2_relation_with_lang(self):
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
        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.all()
        with Context(continents, *lvl_2) as context:
            context.delete('de')
        with Context(continents, *lvl_1_2) as context:
            context.read('de')
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

        self.assertEqual(europe.name, 'Europe')
        self.assertEqual(europe.denonym, 'European')
        self.assertEqual(germany.name, 'Deutschland')
        self.assertEqual(germany.denonym, 'Deutsche')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')
        self.assertEqual(asia.name, 'Asia')
        self.assertEqual(asia.denonym, 'Asian')
        self.assertEqual(south_korea.name, 'Südkorea')
        self.assertEqual(south_korea.denonym, 'Südkoreanisch')
        self.assertEqual(seoul.name, 'Seoul')
        self.assertEqual(seoul.denonym, 'Seouler')

    def test_delete_queryset_level_1_2_relation_with_lang(self):
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
        with Context(continents, *lvl_1_2) as context:
            context.delete('de')
        with Context(continents, *lvl_1_2) as context:
            context.read('de')
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

        self.assertEqual(europe.name, 'Europe')
        self.assertEqual(europe.denonym, 'European')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')
        self.assertEqual(asia.name, 'Asia')
        self.assertEqual(asia.denonym, 'Asian')
        self.assertEqual(south_korea.name, 'South Korea')
        self.assertEqual(south_korea.denonym, 'South Korean')
        self.assertEqual(seoul.name, 'Seoul')
        self.assertEqual(seoul.denonym, 'Seouler')

    @override(language='de', deactivate=True)
    def test_delete_prefetched_queryset_level_0_relation_no_lang(self):
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
        with Context(continents) as context:
            context.delete()
        with Context(continents, *lvl_1_2) as context:
            context.read()
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

        self.assertEqual(europe.name, 'Europe')
        self.assertEqual(europe.denonym, 'European')
        self.assertEqual(germany.name, 'Deutschland')
        self.assertEqual(germany.denonym, 'Deutsche')
        self.assertEqual(cologne.name, 'Köln')
        self.assertEqual(cologne.denonym, 'Kölner')
        self.assertEqual(asia.name, 'Asia')
        self.assertEqual(asia.denonym, 'Asian')
        self.assertEqual(south_korea.name, 'Südkorea')
        self.assertEqual(south_korea.denonym, 'Südkoreanisch')
        self.assertEqual(seoul.name, 'Seül')
        self.assertEqual(seoul.denonym, 'Seüler')

    @override(language='de', deactivate=True)
    def test_delete_prefetched_queryset_level_1_relation_no_lang(self):
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
        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.prefetch_related(*lvl_1_2)
        with Context(continents, *lvl_1) as context:
            context.delete()
        with Context(continents, *lvl_1_2) as context:
            context.read()
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

        self.assertEqual(europe.name, 'Europe')
        self.assertEqual(europe.denonym, 'European')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Köln')
        self.assertEqual(cologne.denonym, 'Kölner')
        self.assertEqual(asia.name, 'Asia')
        self.assertEqual(asia.denonym, 'Asian')
        self.assertEqual(south_korea.name, 'South Korea')
        self.assertEqual(south_korea.denonym, 'South Korean')
        self.assertEqual(seoul.name, 'Seül')
        self.assertEqual(seoul.denonym, 'Seüler')

    @override(language='de', deactivate=True)
    def test_delete_prefetched_queryset_level_2_relation_no_lang(self):
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
        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.prefetch_related(*lvl_1_2)
        with Context(continents, *lvl_2) as context:
            context.delete()
        with Context(continents, *lvl_1_2) as context:
            context.read()
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

        self.assertEqual(europe.name, 'Europe')
        self.assertEqual(europe.denonym, 'European')
        self.assertEqual(germany.name, 'Deutschland')
        self.assertEqual(germany.denonym, 'Deutsche')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')
        self.assertEqual(asia.name, 'Asia')
        self.assertEqual(asia.denonym, 'Asian')
        self.assertEqual(south_korea.name, 'Südkorea')
        self.assertEqual(south_korea.denonym, 'Südkoreanisch')
        self.assertEqual(seoul.name, 'Seoul')
        self.assertEqual(seoul.denonym, 'Seouler')

    @override(language='de', deactivate=True)
    def test_delete_prefetched_queryset_level_1_2_relation_no_lang(self):
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
        with Context(continents, *lvl_1_2) as context:
            context.delete()
        with Context(continents, *lvl_1_2) as context:
            context.read()
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

        self.assertEqual(europe.name, 'Europe')
        self.assertEqual(europe.denonym, 'European')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')
        self.assertEqual(asia.name, 'Asia')
        self.assertEqual(asia.denonym, 'Asian')
        self.assertEqual(south_korea.name, 'South Korea')
        self.assertEqual(south_korea.denonym, 'South Korean')
        self.assertEqual(seoul.name, 'Seoul')
        self.assertEqual(seoul.denonym, 'Seouler')

    def test_delete_prefetched_queryset_level_0_relation_with_lang(self):
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
        with Context(continents) as context:
            context.delete('de')
        with Context(continents, *lvl_1_2) as context:
            context.read('de')
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

        self.assertEqual(europe.name, 'Europe')
        self.assertEqual(europe.denonym, 'European')
        self.assertEqual(germany.name, 'Deutschland')
        self.assertEqual(germany.denonym, 'Deutsche')
        self.assertEqual(cologne.name, 'Köln')
        self.assertEqual(cologne.denonym, 'Kölner')
        self.assertEqual(asia.name, 'Asia')
        self.assertEqual(asia.denonym, 'Asian')
        self.assertEqual(south_korea.name, 'Südkorea')
        self.assertEqual(south_korea.denonym, 'Südkoreanisch')
        self.assertEqual(seoul.name, 'Seül')
        self.assertEqual(seoul.denonym, 'Seüler')

    def test_delete_prefetched_queryset_level_1_relation_with_lang(self):
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
        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.prefetch_related(*lvl_1_2)
        with Context(continents, *lvl_1) as context:
            context.delete('de')
        with Context(continents, *lvl_1_2) as context:
            context.read('de')
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

        self.assertEqual(europe.name, 'Europe')
        self.assertEqual(europe.denonym, 'European')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Köln')
        self.assertEqual(cologne.denonym, 'Kölner')
        self.assertEqual(asia.name, 'Asia')
        self.assertEqual(asia.denonym, 'Asian')
        self.assertEqual(south_korea.name, 'South Korea')
        self.assertEqual(south_korea.denonym, 'South Korean')
        self.assertEqual(seoul.name, 'Seül')
        self.assertEqual(seoul.denonym, 'Seüler')

    def test_delete_prefetched_queryset_level_2_relation_with_lang(self):
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
        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.prefetch_related(*lvl_1_2)
        with Context(continents, *lvl_2) as context:
            context.delete('de')
        with Context(continents, *lvl_1_2) as context:
            context.read('de')
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

        self.assertEqual(europe.name, 'Europe')
        self.assertEqual(europe.denonym, 'European')
        self.assertEqual(germany.name, 'Deutschland')
        self.assertEqual(germany.denonym, 'Deutsche')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')
        self.assertEqual(asia.name, 'Asia')
        self.assertEqual(asia.denonym, 'Asian')
        self.assertEqual(south_korea.name, 'Südkorea')
        self.assertEqual(south_korea.denonym, 'Südkoreanisch')
        self.assertEqual(seoul.name, 'Seoul')
        self.assertEqual(seoul.denonym, 'Seouler')

    def test_delete_prefetched_queryset_level_1_2_relation_with_lang(self):
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
        with Context(continents, *lvl_1_2) as context:
            context.delete('de')
        with Context(continents, *lvl_1_2) as context:
            context.read('de')
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]

        self.assertEqual(europe.name, 'Europe')
        self.assertEqual(europe.denonym, 'European')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')
        self.assertEqual(asia.name, 'Asia')
        self.assertEqual(asia.denonym, 'Asian')
        self.assertEqual(south_korea.name, 'South Korea')
        self.assertEqual(south_korea.denonym, 'South Korean')
        self.assertEqual(seoul.name, 'Seoul')
        self.assertEqual(seoul.denonym, 'Seouler')

    def test_delete_queryset_invalid_lang(self):
        create_samples(
            continent_names=['europe'],
            continent_fields=['name', 'denonym'],
            langs=['de']
        )

        continents = Continent.objects.all()

        with self.assertRaises(ValueError) as error:
            with Context(continents) as context:
                context.update('xx')

        self.assertEqual(
            error.exception.args[0],
            '`xx` is not a supported language.'
        )

    @override(language='de', deactivate=True)
    def test_reset_instance_level_0_relation_no_lang(self):
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
        with Context(europe) as context:
            context.read()
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            context.reset()

        self.assertEqual(europe.name, 'Europe')
        self.assertEqual(europe.denonym, 'European')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')

    @override(language='de', deactivate=True)
    def test_reset_instance_level_1_relation_no_lang(self):
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

        with Context(europe, *lvl_1) as context:
            context.read()
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            context.reset()

        self.assertEqual(europe.name, 'Europe')
        self.assertEqual(europe.denonym, 'European')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')

    @override(language='de', deactivate=True)
    def test_reset_instance_level_2_relation_no_lang(self):
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
        with Context(europe, *lvl_2) as context:
            context.read()
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            context.reset()

        self.assertEqual(europe.name, 'Europe')
        self.assertEqual(europe.denonym, 'European')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')

    @override(language='de', deactivate=True)
    def test_reset_instance_level_1_2_relation_no_lang(self):
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
        with Context(europe, *lvl_1_2) as context:
            context.read()
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            context.reset()

        self.assertEqual(europe.name, 'Europe')
        self.assertEqual(europe.denonym, 'European')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')

    def test_reset_instance_level_0_relation_with_lang(self):
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
        with Context(europe) as context:
            context.read('de')
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            context.reset()

        self.assertEqual(europe.name, 'Europe')
        self.assertEqual(europe.denonym, 'European')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')

    def test_reset_instance_level_1_relation_with_lang(self):
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
        with Context(europe, *lvl_1) as context:
            context.read('de')
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            context.reset()

        self.assertEqual(europe.name, 'Europe')
        self.assertEqual(europe.denonym, 'European')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')

    def test_reset_instance_level_2_relation_with_lang(self):
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
        with Context(europe, *lvl_2) as context:
            context.read('de')
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            context.reset()

        self.assertEqual(europe.name, 'Europe')
        self.assertEqual(europe.denonym, 'European')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')

    def test_reset_instance_level_1_2_relation_with_lang(self):
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
        with Context(europe, *lvl_1_2) as context:
            context.read('de')
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            context.reset()

        self.assertEqual(europe.name, 'Europe')
        self.assertEqual(europe.denonym, 'European')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')

    @override(language='de', deactivate=True)
    def test_reset_prefetched_instance_level_0_relation_no_lang(self):
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
        with Context(europe) as context:
            context.read()
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            context.reset()

        self.assertEqual(europe.name, 'Europe')
        self.assertEqual(europe.denonym, 'European')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')

    @override(language='de', deactivate=True)
    def test_reset_prefetched_instance_level_1_relation_no_lang(self):
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
        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code='EU')
        with Context(europe, *lvl_1) as context:
            context.read()
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            context.reset()

        self.assertEqual(europe.name, 'Europe')
        self.assertEqual(europe.denonym, 'European')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')

    @override(language='de', deactivate=True)
    def test_reset_prefetched_instance_level_2_relation_no_lang(self):
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
        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code='EU')
        with Context(europe, *lvl_2) as context:
            context.read()
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            context.reset()

        self.assertEqual(europe.name, 'Europe')
        self.assertEqual(europe.denonym, 'European')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')

    @override(language='de', deactivate=True)
    def test_reset_prefetched_instance_level_1_2_relation_no_lang(self):
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
        with Context(europe, *lvl_1_2) as context:
            context.read()
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            context.reset()

        self.assertEqual(europe.name, 'Europe')
        self.assertEqual(europe.denonym, 'European')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')

    def test_reset_prefetched_instance_level_0_relation_with_lang(self):
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
        with Context(europe) as context:
            context.read('de')
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            context.reset()

        self.assertEqual(europe.name, 'Europe')
        self.assertEqual(europe.denonym, 'European')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')

    def test_reset_prefetched_instance_level_1_relation_with_lang(self):
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
        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code='EU')
        with Context(europe, *lvl_1) as context:
            context.read('de')
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            context.reset()

        self.assertEqual(europe.name, 'Europe')
        self.assertEqual(europe.denonym, 'European')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')

    def test_reset_prefetched_instance_level_2_relation_with_lang(self):
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
        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code='EU')
        with Context(europe, *lvl_2) as context:
            context.read('de')
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            context.reset()

        self.assertEqual(europe.name, 'Europe')
        self.assertEqual(europe.denonym, 'European')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')

    def test_reset_prefetched_instance_level_1_2_relation_with_lang(self):
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
        with Context(europe, *lvl_1_2) as context:
            context.read('de')
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            context.reset()

        self.assertEqual(europe.name, 'Europe')
        self.assertEqual(europe.denonym, 'European')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')

    @override(language='de', deactivate=True)
    def test_reset_queryset_level_0_relation_no_lang(self):
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
        with Context(continents) as context:
            context.read()
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]
            context.reset()

        self.assertEqual(europe.name, 'Europe')
        self.assertEqual(europe.denonym, 'European')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')
        self.assertEqual(asia.name, 'Asia')
        self.assertEqual(asia.denonym, 'Asian')
        self.assertEqual(south_korea.name, 'South Korea')
        self.assertEqual(south_korea.denonym, 'South Korean')
        self.assertEqual(seoul.name, 'Seoul')
        self.assertEqual(seoul.denonym, 'Seouler')

    @override(language='de', deactivate=True)
    def test_reset_queryset_level_1_relation_no_lang(self):
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
        with Context(continents, *lvl_1) as context:
            context.read()
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]
            context.reset()

        self.assertEqual(europe.name, 'Europe')
        self.assertEqual(europe.denonym, 'European')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')
        self.assertEqual(asia.name, 'Asia')
        self.assertEqual(asia.denonym, 'Asian')
        self.assertEqual(south_korea.name, 'South Korea')
        self.assertEqual(south_korea.denonym, 'South Korean')
        self.assertEqual(seoul.name, 'Seoul')
        self.assertEqual(seoul.denonym, 'Seouler')

    @override(language='de', deactivate=True)
    def test_reset_queryset_level_2_relation_no_lang(self):
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
        with Context(continents, *lvl_2) as context:
            context.read()
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]
            context.reset()

        self.assertEqual(europe.name, 'Europe')
        self.assertEqual(europe.denonym, 'European')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')
        self.assertEqual(asia.name, 'Asia')
        self.assertEqual(asia.denonym, 'Asian')
        self.assertEqual(south_korea.name, 'South Korea')
        self.assertEqual(south_korea.denonym, 'South Korean')
        self.assertEqual(seoul.name, 'Seoul')
        self.assertEqual(seoul.denonym, 'Seouler')

    @override(language='de', deactivate=True)
    def test_reset_queryset_level_1_2_relation_no_lang(self):
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
        with Context(continents, *lvl_1_2) as context:
            context.read()
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]
            context.reset()

        self.assertEqual(europe.name, 'Europe')
        self.assertEqual(europe.denonym, 'European')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')
        self.assertEqual(asia.name, 'Asia')
        self.assertEqual(asia.denonym, 'Asian')
        self.assertEqual(south_korea.name, 'South Korea')
        self.assertEqual(south_korea.denonym, 'South Korean')
        self.assertEqual(seoul.name, 'Seoul')
        self.assertEqual(seoul.denonym, 'Seouler')

    def test_reset_queryset_level_0_relation_with_lang(self):
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
        with Context(continents) as context:
            context.read('de')
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]
            context.reset()

        self.assertEqual(europe.name, 'Europe')
        self.assertEqual(europe.denonym, 'European')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')
        self.assertEqual(asia.name, 'Asia')
        self.assertEqual(asia.denonym, 'Asian')
        self.assertEqual(south_korea.name, 'South Korea')
        self.assertEqual(south_korea.denonym, 'South Korean')
        self.assertEqual(seoul.name, 'Seoul')
        self.assertEqual(seoul.denonym, 'Seouler')

    def test_reset_queryset_level_1_relation_with_lang(self):
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
        with Context(continents, *lvl_1) as context:
            context.read('de')
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]
            context.reset()

        self.assertEqual(europe.name, 'Europe')
        self.assertEqual(europe.denonym, 'European')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')
        self.assertEqual(asia.name, 'Asia')
        self.assertEqual(asia.denonym, 'Asian')
        self.assertEqual(south_korea.name, 'South Korea')
        self.assertEqual(south_korea.denonym, 'South Korean')
        self.assertEqual(seoul.name, 'Seoul')
        self.assertEqual(seoul.denonym, 'Seouler')

    def test_reset_queryset_level_2_relation_with_lang(self):
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
        with Context(continents, *lvl_2) as context:
            context.read('de')
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]
            context.reset()

        self.assertEqual(europe.name, 'Europe')
        self.assertEqual(europe.denonym, 'European')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')
        self.assertEqual(asia.name, 'Asia')
        self.assertEqual(asia.denonym, 'Asian')
        self.assertEqual(south_korea.name, 'South Korea')
        self.assertEqual(south_korea.denonym, 'South Korean')
        self.assertEqual(seoul.name, 'Seoul')
        self.assertEqual(seoul.denonym, 'Seouler')

    def test_reset_queryset_level_1_2_relation_with_lang(self):
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
        with Context(continents, *lvl_1_2) as context:
            context.read('de')
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]
            context.reset()

        self.assertEqual(europe.name, 'Europe')
        self.assertEqual(europe.denonym, 'European')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')
        self.assertEqual(asia.name, 'Asia')
        self.assertEqual(asia.denonym, 'Asian')
        self.assertEqual(south_korea.name, 'South Korea')
        self.assertEqual(south_korea.denonym, 'South Korean')
        self.assertEqual(seoul.name, 'Seoul')
        self.assertEqual(seoul.denonym, 'Seouler')

    @override(language='de', deactivate=True)
    def test_reset_prefetched_queryset_level_0_relation_no_lang(self):
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
        with Context(continents) as context:
            context.read()
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]
            context.reset()

        self.assertEqual(europe.name, 'Europe')
        self.assertEqual(europe.denonym, 'European')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')
        self.assertEqual(asia.name, 'Asia')
        self.assertEqual(asia.denonym, 'Asian')
        self.assertEqual(south_korea.name, 'South Korea')
        self.assertEqual(south_korea.denonym, 'South Korean')
        self.assertEqual(seoul.name, 'Seoul')
        self.assertEqual(seoul.denonym, 'Seouler')

    @override(language='de', deactivate=True)
    def test_reset_prefetched_queryset_level_1_relation_no_lang(self):
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
        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.prefetch_related(*lvl_1_2)
        with Context(continents, *lvl_1) as context:
            context.read()
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]
            context.reset()

        self.assertEqual(europe.name, 'Europe')
        self.assertEqual(europe.denonym, 'European')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')
        self.assertEqual(asia.name, 'Asia')
        self.assertEqual(asia.denonym, 'Asian')
        self.assertEqual(south_korea.name, 'South Korea')
        self.assertEqual(south_korea.denonym, 'South Korean')
        self.assertEqual(seoul.name, 'Seoul')
        self.assertEqual(seoul.denonym, 'Seouler')

    @override(language='de', deactivate=True)
    def test_reset_prefetched_queryset_level_2_relation_no_lang(self):
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
        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.prefetch_related(*lvl_1_2)
        with Context(continents, *lvl_2) as context:
            context.read()
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]
            context.reset()

        self.assertEqual(europe.name, 'Europe')
        self.assertEqual(europe.denonym, 'European')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')
        self.assertEqual(asia.name, 'Asia')
        self.assertEqual(asia.denonym, 'Asian')
        self.assertEqual(south_korea.name, 'South Korea')
        self.assertEqual(south_korea.denonym, 'South Korean')
        self.assertEqual(seoul.name, 'Seoul')
        self.assertEqual(seoul.denonym, 'Seouler')

    @override(language='de', deactivate=True)
    def test_reset_prefetched_queryset_level_1_2_relation_no_lang(self):
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
        with Context(continents, *lvl_1_2) as context:
            context.read()
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]
            context.reset()

        self.assertEqual(europe.name, 'Europe')
        self.assertEqual(europe.denonym, 'European')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')
        self.assertEqual(asia.name, 'Asia')
        self.assertEqual(asia.denonym, 'Asian')
        self.assertEqual(south_korea.name, 'South Korea')
        self.assertEqual(south_korea.denonym, 'South Korean')
        self.assertEqual(seoul.name, 'Seoul')
        self.assertEqual(seoul.denonym, 'Seouler')

    def test_reset_prefetched_queryset_level_0_relation_with_lang(self):
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
        with Context(continents) as context:
            context.read('de')
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]
            context.reset()

        self.assertEqual(europe.name, 'Europe')
        self.assertEqual(europe.denonym, 'European')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')
        self.assertEqual(asia.name, 'Asia')
        self.assertEqual(asia.denonym, 'Asian')
        self.assertEqual(south_korea.name, 'South Korea')
        self.assertEqual(south_korea.denonym, 'South Korean')
        self.assertEqual(seoul.name, 'Seoul')
        self.assertEqual(seoul.denonym, 'Seouler')

    def test_reset_prefetched_queryset_level_1_relation_with_lang(self):
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
        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.prefetch_related(*lvl_1_2)
        with Context(continents, *lvl_1) as context:
            context.read('de')
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]
            context.reset()

        self.assertEqual(europe.name, 'Europe')
        self.assertEqual(europe.denonym, 'European')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')
        self.assertEqual(asia.name, 'Asia')
        self.assertEqual(asia.denonym, 'Asian')
        self.assertEqual(south_korea.name, 'South Korea')
        self.assertEqual(south_korea.denonym, 'South Korean')
        self.assertEqual(seoul.name, 'Seoul')
        self.assertEqual(seoul.denonym, 'Seouler')

    def test_reset_prefetched_queryset_level_2_relation_with_lang(self):
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
        lvl_1_2 = ('countries', 'countries__cities',)

        continents = Continent.objects.prefetch_related(*lvl_1_2)
        with Context(continents, *lvl_2) as context:
            context.read('de')
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]
            context.reset()

        self.assertEqual(europe.name, 'Europe')
        self.assertEqual(europe.denonym, 'European')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')
        self.assertEqual(asia.name, 'Asia')
        self.assertEqual(asia.denonym, 'Asian')
        self.assertEqual(south_korea.name, 'South Korea')
        self.assertEqual(south_korea.denonym, 'South Korean')
        self.assertEqual(seoul.name, 'Seoul')
        self.assertEqual(seoul.denonym, 'Seouler')

    def test_reset_prefetched_queryset_level_1_2_relation_with_lang(self):
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
        with Context(continents, *lvl_1_2) as context:
            context.read('de')
            europe = [x for x in continents if x.code == 'EU'][0]
            germany = europe.countries.all()[0]
            cologne = germany.cities.all()[0]
            asia = [x for x in continents if x.code == 'AS'][0]
            south_korea = asia.countries.all()[0]
            seoul = south_korea.cities.all()[0]
            context.reset()

        self.assertEqual(europe.name, 'Europe')
        self.assertEqual(europe.denonym, 'European')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')
        self.assertEqual(asia.name, 'Asia')
        self.assertEqual(asia.denonym, 'Asian')
        self.assertEqual(south_korea.name, 'South Korea')
        self.assertEqual(south_korea.denonym, 'South Korean')
        self.assertEqual(seoul.name, 'Seoul')
        self.assertEqual(seoul.denonym, 'Seouler')
