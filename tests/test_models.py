from django.test import TestCase
from django.contrib.contenttypes.models import ContentType
from django.db import utils
from django.core.exceptions import FieldDoesNotExist
from django.utils.translation import activate

from translations.models import Translation

from sample.models import Continent, Country, City, Geo

from tests.sample import create_samples


class TranslationTest(TestCase):
    """Tests for `Translation`."""

    def test_content_type_none(self):
        europe = Continent.objects.create(name='Europe', code='EU')
        
        with self.assertRaises(utils.IntegrityError) as error:
            Translation.objects.create(
                content_type=None,
                object_id=europe.id,
                field='name',
                language='de',
                text='Europa',
            )
        
        self.assertEqual(
            error.exception.args[0],
            ('NOT NULL constraint failed: translations_translation' +
             '.content_type_id'),
        )

    def test_object_id_none(self):
        continent_ct = ContentType.objects.get_for_model(Continent)
        
        with self.assertRaises(utils.IntegrityError) as error:
            Translation.objects.create(
                content_type=continent_ct,
                object_id=None,
                field='name',
                language='de',
                text='Europa',
            )
        
        self.assertEqual(
            error.exception.args[0],
            'NOT NULL constraint failed: translations_translation.object_id',
        )

    def test_content_object_none(self):
        with self.assertRaises(utils.IntegrityError) as error:
            Translation.objects.create(
                content_object=None,
                field='name',
                language='de',
                text='Europa',
            )
        
        self.assertEqual(
            error.exception.args[0],
            'NOT NULL constraint failed: translations_translation.object_id',
        )

    def test_field_none(self):
        europe = Continent.objects.create(name='Europe', code='EU')
        continent_ct = ContentType.objects.get_for_model(Continent)
        
        with self.assertRaises(utils.IntegrityError) as error:
            Translation.objects.create(
                content_type=continent_ct,
                object_id=europe.id,
                field=None,
                language='de',
                text='Europa',
            )
        
        self.assertEqual(
            error.exception.args[0],
            'NOT NULL constraint failed: translations_translation.field',
        )

    def test_language_none(self):
        europe = Continent.objects.create(name='Europe', code='EU')
        continent_ct = ContentType.objects.get_for_model(Continent)
        
        with self.assertRaises(utils.IntegrityError) as error:
            Translation.objects.create(
                content_type=continent_ct,
                object_id=europe.id,
                field='name',
                language=None,
                text='Europa',
            )
        
        self.assertEqual(
            error.exception.args[0],
            'NOT NULL constraint failed: translations_translation.language',
        )

    def test_text_none(self):
        europe = Continent.objects.create(name='Europe', code='EU')
        continent_ct = ContentType.objects.get_for_model(Continent)
        
        with self.assertRaises(utils.IntegrityError) as error:
            Translation.objects.create(
                content_type=continent_ct,
                object_id=europe.id,
                field='name',
                language='de',
                text=None,
            )
        
        self.assertEqual(
            error.exception.args[0],
            'NOT NULL constraint failed: translations_translation.text',
        )

    def test_str(self):
        europe = Continent.objects.create(name='Europe', code='EU')
        continent_ct = ContentType.objects.get_for_model(Continent)
        translation = Translation.objects.create(
            content_type=continent_ct,
            object_id=europe.id,
            field='name',
            language='de',
            text='Europa'
        )
        self.assertEqual(str(translation), 'Europe: Europa')

    def test_uniqueness(self):
        europe = Continent.objects.create(name='Europe', code='EU')
        continent_ct = ContentType.objects.get_for_model(Continent)
        Translation.objects.create(
            content_type=continent_ct,
            object_id=europe.id,
            field='name',
            language='de',
            text='Europa'
        )
        
        with self.assertRaises(utils.IntegrityError) as error:
            Translation.objects.create(
                content_type=continent_ct,
                object_id=europe.id,
                field='name',
                language='de',
                text='Europa'
            )
        
        self.assertEqual(
            error.exception.args[0],
            ('UNIQUE constraint failed: ' +
             'translations_translation.content_type_id, ' +
             'translations_translation.object_id, ' +
             'translations_translation.field, ' +
             'translations_translation.language'),
        )


class TranslatableTest(TestCase):
    """Tests for `Translatable`."""

    def test_one_translations_rel(self):
        create_samples(
            continent_names=['europe'],
            continent_fields=['name', 'denonym'],
            langs=['de']
        )

        europe = Continent.objects.get(code='EU')

        self.assertQuerysetEqual(
            europe.translations.order_by('id'),
            [
                '<Translation: Europe: Europa>',
                '<Translation: European: Europäisch>',
            ]
        )

    def test_two_translations_rel(self):
        create_samples(
            continent_names=['europe', 'asia'],
            continent_fields=['name', 'denonym'],
            langs=['de']
        )

        europe = Continent.objects.get(code='EU')
        asia = Continent.objects.get(code='AS')

        self.assertQuerysetEqual(
            europe.translations.order_by('id'),
            [
                '<Translation: Europe: Europa>',
                '<Translation: European: Europäisch>',
            ]
        )
        self.assertQuerysetEqual(
            asia.translations.order_by('id'),
            [
                '<Translation: Asia: Asien>',
                '<Translation: Asian: Asiatisch>',
            ]
        )

    def test_fields_none_automatic(self):
        self.assertListEqual(
            City.get_translatable_fields(),
            [
                City._meta.get_field('name'),
                City._meta.get_field('denonym'),
            ]
        )

    def test_fields_empty(self):
        self.assertListEqual(
            Geo.get_translatable_fields(),
            []
        )

    def test_fields_explicit(self):
        self.assertListEqual(
            Continent.get_translatable_fields(),
            [
                Continent._meta.get_field('name'),
                Continent._meta.get_field('denonym'),
            ]
        )

    def test_field_names_none_automatic(self):
        self.assertListEqual(
            City.get_translatable_field_names(),
            ['name', 'denonym']
        )

    def test_field_names_empty(self):
        self.assertListEqual(
            Geo.get_translatable_field_names(),
            []
        )

    def test_field_names_explicit(self):
        self.assertListEqual(
            Continent.get_translatable_field_names(),
            ['name', 'denonym']
        )

    def test_apply_translations_level_0_relation_no_lang(self):
        create_samples(
            continent_names=['europe'],
            country_names=['germany'],
            city_names=['cologne'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        activate('de')

        europe = Continent.objects.get(code='EU')
        europe.apply_translations()
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

    def test_apply_translations_level_1_relation_no_lang(self):
        create_samples(
            continent_names=['europe'],
            country_names=['germany'],
            city_names=['cologne'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        activate('de')

        lvl_1 = ('countries',)

        europe = Continent.objects.get(code='EU')
        europe.apply_translations(*lvl_1)
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

    def test_apply_translations_level_2_relation_no_lang(self):
        create_samples(
            continent_names=['europe'],
            country_names=['germany'],
            city_names=['cologne'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        activate('de')

        lvl_2 = ('countries__cities',)

        europe = Continent.objects.get(code='EU')
        europe.apply_translations(*lvl_2)
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

    def test_apply_translations_level_1_2_relation_no_lang(self):
        create_samples(
            continent_names=['europe'],
            country_names=['germany'],
            city_names=['cologne'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        activate('de')

        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.get(code='EU')
        europe.apply_translations(*lvl_1_2)
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

    def test_apply_translations_level_0_relation_with_lang(self):
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
        europe.apply_translations(lang='de')
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

    def test_apply_translations_level_1_relation_with_lang(self):
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
        europe.apply_translations(*lvl_1, lang='de')
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

    def test_apply_translations_level_2_relation_with_lang(self):
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
        europe.apply_translations(*lvl_2, lang='de')
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

    def test_apply_translations_level_1_2_relation_with_lang(self):
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
        europe.apply_translations(*lvl_1_2, lang='de')
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

    def test_apply_translations_prefetched_level_0_relation_no_lang(self):
        create_samples(
            continent_names=['europe'],
            country_names=['germany'],
            city_names=['cologne'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        activate('de')

        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code='EU')
        europe.apply_translations()
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

    def test_apply_translations_prefetched_level_1_relation_no_lang(self):
        create_samples(
            continent_names=['europe'],
            country_names=['germany'],
            city_names=['cologne'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        activate('de')

        lvl_1 = ('countries',)
        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code='EU')
        europe.apply_translations(*lvl_1)
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

    def test_apply_translations_prefetched_level_2_relation_no_lang(self):
        create_samples(
            continent_names=['europe'],
            country_names=['germany'],
            city_names=['cologne'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        activate('de')

        lvl_2 = ('countries__cities',)
        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code='EU')
        europe.apply_translations(*lvl_2)
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

    def test_apply_translations_prefetched_level_1_2_relation_no_lang(self):
        create_samples(
            continent_names=['europe'],
            country_names=['germany'],
            city_names=['cologne'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        activate('de')

        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code='EU')
        europe.apply_translations(*lvl_1_2)
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

    def test_apply_translations_prefetched_level_0_relation_with_lang(self):
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
        europe.apply_translations(lang='de')
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

    def test_apply_translations_prefetched_level_1_relation_with_lang(self):
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
        europe.apply_translations(*lvl_1, lang='de')
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

    def test_apply_translations_prefetched_level_2_relation_with_lang(self):
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
        europe.apply_translations(*lvl_2, lang='de')
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

    def test_apply_translations_prefetched_level_1_2_relation_with_lang(self):
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
        europe.apply_translations(*lvl_1_2, lang='de')
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

    def test_apply_translations_invalid_simple_relation(self):
        create_samples(
            continent_names=['europe'],
            continent_fields=['name', 'denonym'],
            langs=['de']
        )

        europe = Continent.objects.get(code='EU')

        with self.assertRaises(FieldDoesNotExist) as error:
            europe.apply_translations('wrong')

        self.assertEqual(
            error.exception.args[0],
            "Continent has no field named 'wrong'"
        )

    def test_apply_translations_invalid_nested_relation(self):
        create_samples(
            continent_names=['europe'],
            country_names=['germany'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            langs=['de']
        )

        europe = Continent.objects.get(code='EU')

        with self.assertRaises(FieldDoesNotExist) as error:
            europe.apply_translations('countries__wrong')

        self.assertEqual(
            error.exception.args[0],
            "Country has no field named 'wrong'"
        )

    def test_apply_translations_invalid_lang(self):
        create_samples(
            continent_names=['europe'],
            continent_fields=['name', 'denonym'],
            langs=['de']
        )

        europe = Continent.objects.get(code='EU')

        with self.assertRaises(ValueError) as error:
            europe.apply_translations(lang='xx')

        self.assertEqual(
            error.exception.args[0],
            'The language code `xx` is not supported.'
        )

    def test_update_translations_level_0_relation_no_lang(self):
        create_samples(
            continent_names=['europe'],
            country_names=['germany'],
            city_names=['cologne'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        activate('de')

        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code='EU')
        europe.apply_translations(*lvl_1_2)
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        # change
        europe.name = 'Europe Name'
        europe.denonym = 'Europe Denonym'
        germany.name = 'Germany Name'
        germany.denonym = 'Germany Denonym'
        cologne.name = 'Cologne Name'
        cologne.denonym = 'Cologne Denonym'
        europe.update_translations()

        # reapply
        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code='EU')
        europe.apply_translations(*lvl_1_2)
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

    def test_update_translations_level_1_relation_no_lang(self):
        create_samples(
            continent_names=['europe'],
            country_names=['germany'],
            city_names=['cologne'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        activate('de')

        lvl_1 = ('countries',)
        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code='EU')
        europe.apply_translations(*lvl_1_2)
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        # change
        europe.name = 'Europe Name'
        europe.denonym = 'Europe Denonym'
        germany.name = 'Germany Name'
        germany.denonym = 'Germany Denonym'
        cologne.name = 'Cologne Name'
        cologne.denonym = 'Cologne Denonym'
        europe.update_translations(*lvl_1)

        # reapply
        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code='EU')
        europe.apply_translations(*lvl_1_2)
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

    def test_update_translations_level_2_relation_no_lang(self):
        create_samples(
            continent_names=['europe'],
            country_names=['germany'],
            city_names=['cologne'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        activate('de')

        lvl_2 = ('countries__cities',)
        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code='EU')
        europe.apply_translations(*lvl_1_2)
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        # change
        europe.name = 'Europe Name'
        europe.denonym = 'Europe Denonym'
        germany.name = 'Germany Name'
        germany.denonym = 'Germany Denonym'
        cologne.name = 'Cologne Name'
        cologne.denonym = 'Cologne Denonym'
        europe.update_translations(*lvl_2)

        # reapply
        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code='EU')
        europe.apply_translations(*lvl_1_2)
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

    def test_update_translations_level_1_2_relation_no_lang(self):
        create_samples(
            continent_names=['europe'],
            country_names=['germany'],
            city_names=['cologne'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        activate('de')

        lvl_1_2 = ('countries', 'countries__cities',)

        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code='EU')
        europe.apply_translations(*lvl_1_2)
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        # change
        europe.name = 'Europe Name'
        europe.denonym = 'Europe Denonym'
        germany.name = 'Germany Name'
        germany.denonym = 'Germany Denonym'
        cologne.name = 'Cologne Name'
        cologne.denonym = 'Cologne Denonym'
        europe.update_translations(*lvl_1_2)

        # reapply
        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code='EU')
        europe.apply_translations(*lvl_1_2)
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

    def test_update_translations_level_0_relation_with_lang(self):
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
        europe.apply_translations(*lvl_1_2, lang='de')
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        # change
        europe.name = 'Europe Name'
        europe.denonym = 'Europe Denonym'
        germany.name = 'Germany Name'
        germany.denonym = 'Germany Denonym'
        cologne.name = 'Cologne Name'
        cologne.denonym = 'Cologne Denonym'
        europe.update_translations(lang='de')

        # reapply
        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code='EU')
        europe.apply_translations(*lvl_1_2, lang='de')
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

    def test_update_translations_level_1_relation_with_lang(self):
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
        europe.apply_translations(*lvl_1_2, lang='de')
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        # change
        europe.name = 'Europe Name'
        europe.denonym = 'Europe Denonym'
        germany.name = 'Germany Name'
        germany.denonym = 'Germany Denonym'
        cologne.name = 'Cologne Name'
        cologne.denonym = 'Cologne Denonym'
        europe.update_translations(*lvl_1, lang='de')

        # reapply
        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code='EU')
        europe.apply_translations(*lvl_1_2, lang='de')
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

    def test_update_translations_level_2_relation_with_lang(self):
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
        europe.apply_translations(*lvl_1_2, lang='de')
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        # change
        europe.name = 'Europe Name'
        europe.denonym = 'Europe Denonym'
        germany.name = 'Germany Name'
        germany.denonym = 'Germany Denonym'
        cologne.name = 'Cologne Name'
        cologne.denonym = 'Cologne Denonym'
        europe.update_translations(*lvl_2, lang='de')

        # reapply
        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code='EU')
        europe.apply_translations(*lvl_1_2, lang='de')
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

    def test_update_translations_level_1_2_relation_with_lang(self):
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
        europe.apply_translations(*lvl_1_2, lang='de')
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        # change
        europe.name = 'Europe Name'
        europe.denonym = 'Europe Denonym'
        germany.name = 'Germany Name'
        germany.denonym = 'Germany Denonym'
        cologne.name = 'Cologne Name'
        cologne.denonym = 'Cologne Denonym'
        europe.update_translations(*lvl_1_2, lang='de')

        # reapply
        europe = Continent.objects.prefetch_related(*lvl_1_2).get(code='EU')
        europe.apply_translations(*lvl_1_2, lang='de')
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

    def test_update_translations_invalid_simple_relation(self):
        create_samples(
            continent_names=['europe'],
            continent_fields=['name', 'denonym'],
            langs=['de']
        )

        europe = Continent.objects.get(code='EU')

        with self.assertRaises(FieldDoesNotExist) as error:
            europe.update_translations('wrong')

        self.assertEqual(
            error.exception.args[0],
            "Continent has no field named 'wrong'"
        )

    def test_update_translations_invalid_nested_relation(self):
        create_samples(
            continent_names=['europe'],
            country_names=['germany'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            langs=['de']
        )

        lvl_1 = ('countries',)

        europe = Continent.objects.prefetch_related(*lvl_1).get(code='EU')

        with self.assertRaises(FieldDoesNotExist) as error:
            europe.update_translations('countries__wrong')

        self.assertEqual(
            error.exception.args[0],
            "Country has no field named 'wrong'"
        )

    def test_update_translations_invalid_lang(self):
        create_samples(
            continent_names=['europe'],
            continent_fields=['name', 'denonym'],
            langs=['de']
        )

        europe = Continent.objects.get(code='EU')

        with self.assertRaises(ValueError) as error:
            europe.update_translations(lang='xx')

        self.assertEqual(
            error.exception.args[0],
            'The language code `xx` is not supported.'
        )

    def test_update_translations_invalid_prefetch_simple_relation(self):
        create_samples(
            continent_names=['europe'],
            country_names=['germany'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            langs=['de']
        )

        lvl_1 = ('countries',)

        europe = Continent.objects.get(code='EU')

        with self.assertRaises(RuntimeError) as error:
            europe.update_translations(*lvl_1)

        self.assertEqual(
            error.exception.args[0],
            ('The relation `countries` of the model `Continent` must' +
             ' be prefetched.')
        )

    def test_update_translations_invalid_prefetch_nested_relation(self):
        create_samples(
            continent_names=['europe'],
            country_names=['germany'],
            city_names=['cologne'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de']
        )

        lvl_2 = ('countries__cities',)

        europe = Continent.objects.get(code='EU')

        with self.assertRaises(RuntimeError) as error:
            europe.update_translations(*lvl_2)

        self.assertEqual(
            error.exception.args[0],
            ('The relation `countries` of the model `Continent` must' +
             ' be prefetched.')
        )

    def test_update_translations_invalid_prefetch_partial_nested_relation(self):
        create_samples(
            continent_names=['europe'],
            country_names=['germany'],
            city_names=['cologne'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de']
        )

        lvl_1 = ('countries',)
        lvl_2 = ('countries__cities',)

        europe = Continent.objects.prefetch_related(*lvl_1).get(code='EU')

        with self.assertRaises(RuntimeError) as error:
            europe.update_translations(*lvl_2)

        self.assertEqual(
            error.exception.args[0],
            ('The relation `cities` of the model `Country` must' +
             ' be prefetched.')
        )
