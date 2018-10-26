from django.test import TestCase, override_settings
from django.db.models import Q
from django.utils.translation import override

from translations.querysets import TranslatableQuerySet

from sample.models import Continent

from tests.sample import create_samples


class TranslatableQuerySetTest(TestCase):
    """Tests for `TranslatableQuerySet`."""

    @override_settings(LANGUAGE_CODE='en-us')
    def test_init_nonexisting_accented_default_language_code(self):
        continents = Continent.objects.all()

        self.assertEqual(continents._trans_lang, 'en')
        self.assertTupleEqual(continents._trans_rels, ())
        self.assertEqual(continents._trans_cache, False)

    @override_settings(LANGUAGE_CODE='en-gb')
    def test_init_existing_accented_default_language_code(self):
        continents = Continent.objects.all()

        self.assertEqual(continents._trans_lang, 'en-gb')
        self.assertTupleEqual(continents._trans_rels, ())
        self.assertEqual(continents._trans_cache, False)

    def test_chain(self):
        continents = Continent.objects.all()

        continents._trans_lang = 'de'
        continents._trans_rels = ('countries', 'countries__cities',)
        continents._trans_cache = True

        continents = continents._chain()

        self.assertEqual(continents._trans_lang, 'de')
        self.assertTupleEqual(continents._trans_rels, ('countries', 'countries__cities',))
        self.assertEqual(continents._trans_cache, False)

    def test_fetch_all_normal_mode(self):
        create_samples(
            continent_names=['europe'],
            continent_fields=['name', 'denonym'],
            langs=['de']
        )

        continents = Continent.objects.all()

        self.assertEqual(continents[0].name, 'Europe')
        self.assertEqual(continents[0].denonym, 'European')

    @override(language='de', deactivate=True)
    def test_fetch_all_get_level_0_relation_no_lang(self):
        create_samples(
            continent_names=['europe'],
            country_names=['germany'],
            city_names=['cologne'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        europe = Continent.objects.translate().get(code='EU')
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europa')
        self.assertEqual(europe.denonym, 'Europäisch')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')

    @override(language='de', deactivate=True)
    def test_fetch_all_get_level_1_relation_no_lang(self):
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

        europe = Continent.objects.translate().translate_related(*lvl_1).get(code='EU')
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europa')
        self.assertEqual(europe.denonym, 'Europäisch')
        self.assertEqual(germany.name, 'Deutschland')
        self.assertEqual(germany.denonym, 'Deutsche')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')

    @override(language='de', deactivate=True)
    def test_fetch_all_get_level_2_relation_no_lang(self):
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

        europe = Continent.objects.translate().translate_related(*lvl_2).get(code='EU')
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europa')
        self.assertEqual(europe.denonym, 'Europäisch')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Köln')
        self.assertEqual(cologne.denonym, 'Kölner')

    @override(language='de', deactivate=True)
    def test_fetch_all_get_level_1_2_relation_no_lang(self):
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

        europe = Continent.objects.translate().translate_related(*lvl_1_2).get(code='EU')
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europa')
        self.assertEqual(europe.denonym, 'Europäisch')
        self.assertEqual(germany.name, 'Deutschland')
        self.assertEqual(germany.denonym, 'Deutsche')
        self.assertEqual(cologne.name, 'Köln')
        self.assertEqual(cologne.denonym, 'Kölner')

    def test_fetch_all_get_level_0_relation_with_lang(self):
        create_samples(
            continent_names=['europe'],
            country_names=['germany'],
            city_names=['cologne'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        europe = Continent.objects.translate('de').get(code='EU')
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europa')
        self.assertEqual(europe.denonym, 'Europäisch')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')

    def test_fetch_all_get_level_1_relation_with_lang(self):
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

        europe = Continent.objects.translate('de').translate_related(*lvl_1).get(code='EU')
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europa')
        self.assertEqual(europe.denonym, 'Europäisch')
        self.assertEqual(germany.name, 'Deutschland')
        self.assertEqual(germany.denonym, 'Deutsche')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')

    def test_fetch_all_get_level_2_relation_with_lang(self):
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

        europe = Continent.objects.translate('de').translate_related(*lvl_2).get(code='EU')
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europa')
        self.assertEqual(europe.denonym, 'Europäisch')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Köln')
        self.assertEqual(cologne.denonym, 'Kölner')

    def test_fetch_all_get_level_1_2_relation_with_lang(self):
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

        europe = Continent.objects.translate('de').translate_related(*lvl_1_2).get(code='EU')
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europa')
        self.assertEqual(europe.denonym, 'Europäisch')
        self.assertEqual(germany.name, 'Deutschland')
        self.assertEqual(germany.denonym, 'Deutsche')
        self.assertEqual(cologne.name, 'Köln')
        self.assertEqual(cologne.denonym, 'Kölner')

    @override(language='de', deactivate=True)
    def test_fetch_all_prefetched_get_level_0_relation_no_lang(self):
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

        europe = Continent.objects.prefetch_related(*lvl_1_2).translate().get(code='EU')
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europa')
        self.assertEqual(europe.denonym, 'Europäisch')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')

    @override(language='de', deactivate=True)
    def test_fetch_all_prefetched_get_level_1_relation_no_lang(self):
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

        europe = Continent.objects.prefetch_related(*lvl_1_2).translate().translate_related(*lvl_1).get(code='EU')
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europa')
        self.assertEqual(europe.denonym, 'Europäisch')
        self.assertEqual(germany.name, 'Deutschland')
        self.assertEqual(germany.denonym, 'Deutsche')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')

    @override(language='de', deactivate=True)
    def test_fetch_all_prefetched_get_level_2_relation_no_lang(self):
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

        europe = Continent.objects.prefetch_related(*lvl_1_2).translate().translate_related(*lvl_2).get(code='EU')
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europa')
        self.assertEqual(europe.denonym, 'Europäisch')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Köln')
        self.assertEqual(cologne.denonym, 'Kölner')

    @override(language='de', deactivate=True)
    def test_fetch_all_prefetched_get_level_1_2_relation_no_lang(self):
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

        europe = Continent.objects.prefetch_related(*lvl_1_2).translate().translate_related(*lvl_1_2).get(code='EU')
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europa')
        self.assertEqual(europe.denonym, 'Europäisch')
        self.assertEqual(germany.name, 'Deutschland')
        self.assertEqual(germany.denonym, 'Deutsche')
        self.assertEqual(cologne.name, 'Köln')
        self.assertEqual(cologne.denonym, 'Kölner')

    def test_fetch_all_prefetched_get_level_0_relation_with_lang(self):
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

        europe = Continent.objects.prefetch_related(*lvl_1_2).translate('de').get(code='EU')
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europa')
        self.assertEqual(europe.denonym, 'Europäisch')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')

    def test_fetch_all_prefetched_get_level_1_relation_with_lang(self):
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

        europe = Continent.objects.prefetch_related(*lvl_1_2).translate('de').translate_related(*lvl_1).get(code='EU')
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europa')
        self.assertEqual(europe.denonym, 'Europäisch')
        self.assertEqual(germany.name, 'Deutschland')
        self.assertEqual(germany.denonym, 'Deutsche')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')

    def test_fetch_all_prefetched_get_level_2_relation_with_lang(self):
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

        europe = Continent.objects.prefetch_related(*lvl_1_2).translate('de').translate_related(*lvl_2).get(code='EU')
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europa')
        self.assertEqual(europe.denonym, 'Europäisch')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Köln')
        self.assertEqual(cologne.denonym, 'Kölner')

    def test_fetch_all_prefetched_get_level_1_2_relation_with_lang(self):
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

        europe = Continent.objects.prefetch_related(*lvl_1_2).translate('de').translate_related(*lvl_1_2).get(code='EU')
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europa')
        self.assertEqual(europe.denonym, 'Europäisch')
        self.assertEqual(germany.name, 'Deutschland')
        self.assertEqual(germany.denonym, 'Deutsche')
        self.assertEqual(cologne.name, 'Köln')
        self.assertEqual(cologne.denonym, 'Kölner')

    @override(language='de', deactivate=True)
    def test_fetch_all_all_level_0_relation_no_lang(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        continents = Continent.objects.translate()
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
    def test_fetch_all_all_level_1_relation_no_lang(self):
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

        continents = Continent.objects.translate().translate_related(*lvl_1)
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
    def test_fetch_all_all_level_2_relation_no_lang(self):
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

        continents = Continent.objects.translate().translate_related(*lvl_2)
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
    def test_fetch_all_all_level_1_2_relation_no_lang(self):
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

        continents = Continent.objects.translate().translate_related(*lvl_1_2)
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

    def test_fetch_all_all_level_0_relation_with_lang(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        continents = Continent.objects.translate('de')
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

    def test_fetch_all_all_level_1_relation_with_lang(self):
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

        continents = Continent.objects.translate('de').translate_related(*lvl_1)
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

    def test_fetch_all_all_level_2_relation_with_lang(self):
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

        continents = Continent.objects.translate('de').translate_related(*lvl_2)
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

    def test_fetch_all_all_level_1_2_relation_with_lang(self):
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

        continents = Continent.objects.translate('de').translate_related(*lvl_1_2)
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
    def test_fetch_all_prefetched_all_level_0_relation_no_lang(self):
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

        continents = Continent.objects.prefetch_related(*lvl_1_2).translate()
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
    def test_fetch_all_prefetched_all_level_1_relation_no_lang(self):
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

        continents = Continent.objects.prefetch_related(*lvl_1_2).translate().translate_related(*lvl_1)
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
    def test_fetch_all_prefetched_all_level_2_relation_no_lang(self):
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

        continents = Continent.objects.prefetch_related(*lvl_1_2).translate().translate_related(*lvl_2)
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
    def test_fetch_all_prefetched_all_level_1_2_relation_no_lang(self):
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

        continents = Continent.objects.prefetch_related(*lvl_1_2).translate().translate_related(*lvl_1_2)
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

    def test_fetch_all_prefetched_all_level_0_relation_with_lang(self):
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

        continents = Continent.objects.prefetch_related(*lvl_1_2).translate('de')
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

    def test_fetch_all_prefetched_all_level_1_relation_with_lang(self):
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

        continents = Continent.objects.prefetch_related(*lvl_1_2).translate('de').translate_related(*lvl_1)
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

    def test_fetch_all_prefetched_all_level_2_relation_with_lang(self):
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

        continents = Continent.objects.prefetch_related(*lvl_1_2).translate('de').translate_related(*lvl_2)
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

    def test_fetch_all_prefetched_all_level_1_2_relation_with_lang(self):
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

        continents = Continent.objects.prefetch_related(*lvl_1_2).translate('de').translate_related(*lvl_1_2)
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
    def test_fetch_all_filter_level_0_relation_no_lang(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        continents = Continent.objects.probe().filter(Q(name='Europa') | Q(name='Asien'))
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
    def test_fetch_all_filter_level_1_relation_no_lang(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        continents = Continent.objects.probe().filter(Q(countries__name='Deutschland') | Q(countries__name='Südkorea'))
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
    def test_fetch_all_filter_level_2_relation_no_lang(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        continents = Continent.objects.probe().filter(Q(countries__cities__name='Köln') | Q(countries__cities__name='Seül'))
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
    def test_fetch_all_filter_level_1_2_relation_no_lang(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        continents = Continent.objects.probe().filter(Q(countries__name='Deutschland', countries__cities__name='Köln') | Q(countries__name='Südkorea', countries__cities__name='Seül'))
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

    def test_fetch_all_filter_level_0_relation_with_lang(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        continents = Continent.objects.probe('de').filter(Q(name='Europa') | Q(name='Asien'))
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

    def test_fetch_all_filter_level_1_relation_with_lang(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        continents = Continent.objects.probe('de').filter(Q(countries__name='Deutschland') | Q(countries__name='Südkorea'))
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

    def test_fetch_all_filter_level_2_relation_with_lang(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        continents = Continent.objects.probe('de').filter(Q(countries__cities__name='Köln') | Q(countries__cities__name='Seül'))
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

    def test_fetch_all_filter_level_1_2_relation_with_lang(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        continents = Continent.objects.probe('de').filter(Q(countries__name='Deutschland', countries__cities__name='Köln') | Q(countries__name='Südkorea', countries__cities__name='Seül'))
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
    def test_fetch_all_exclude_level_0_relation_no_lang(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        continents = Continent.objects.probe().exclude(Q(name='Afrika') | Q(name='Nordamerika'))
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
    def test_fetch_all_exclude_level_1_relation_no_lang(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        continents = Continent.objects.probe().exclude(Q(countries__name='Ägypten') | Q(countries__name='Mexiko'))
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
    def test_fetch_all_exclude_level_2_relation_no_lang(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        continents = Continent.objects.probe().exclude(Q(countries__cities__name='Cairo') | Q(countries__cities__name='Mexiko Stadtisch'))
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
    def test_fetch_all_exclude_level_1_2_relation_no_lang(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        continents = Continent.objects.probe().exclude(Q(countries__name='Ägypten', countries__cities__name='Cairo') | Q(countries__name='Mexiko', countries__cities__name='Mexiko Stadtisch'))
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

    def test_fetch_all_exclude_level_0_relation_with_lang(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        continents = Continent.objects.probe('de').exclude(Q(name='Afrika') | Q(name='Nordamerika'))
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

    def test_fetch_all_exclude_level_1_relation_with_lang(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        continents = Continent.objects.probe('de').exclude(Q(countries__name='Ägypten') | Q(countries__name='Mexiko'))
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

    def test_fetch_all_exclude_level_2_relation_with_lang(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        continents = Continent.objects.probe('de').exclude(Q(countries__cities__name='Cairo') | Q(countries__cities__name='Mexiko Stadtisch'))
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

    def test_fetch_all_exclude_level_1_2_relation_with_lang(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        continents = Continent.objects.probe('de').exclude(Q(countries__name='Ägypten', countries__cities__name='Cairo') | Q(countries__name='Mexiko', countries__cities__name='Mexiko Stadtisch'))
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
    def test_fetch_all_decipher_level_0_relation_no_lang(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        continents = Continent.objects.translate().translate('en-us')
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
    def test_fetch_all_decipher_level_1_relation_no_lang(self):
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

        continents = Continent.objects.translate().translate_related(*lvl_1).translate('en-us')
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
    def test_fetch_all_decipher_level_2_relation_no_lang(self):
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

        continents = Continent.objects.translate().translate_related(*lvl_2).translate('en-us')
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
    def test_fetch_all_decipher_level_1_2_relation_no_lang(self):
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

        continents = Continent.objects.translate().translate_related(*lvl_1_2).translate('en-us')
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

    def test_fetch_all_decipher_level_0_relation_with_lang(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        continents = Continent.objects.translate('de').translate('en-us')
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

    def test_fetch_all_decipher_level_1_relation_with_lang(self):
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

        continents = Continent.objects.translate('de').translate_related(*lvl_1).translate('en-us')
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

    def test_fetch_all_decipher_level_2_relation_with_lang(self):
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

        continents = Continent.objects.translate('de').translate_related(*lvl_2).translate('en-us')
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

    def test_fetch_all_decipher_level_1_2_relation_with_lang(self):
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

        continents = Continent.objects.translate('de').translate_related(*lvl_1_2).translate('en-us')
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
    def test_fetch_all_prefetched_decipher_level_0_relation_no_lang(self):
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

        continents = Continent.objects.prefetch_related(*lvl_1_2).translate().translate('en-us')
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
    def test_fetch_all_prefetched_decipher_level_1_relation_no_lang(self):
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

        continents = Continent.objects.prefetch_related(*lvl_1_2).translate().translate_related(*lvl_1).translate('en-us')
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
    def test_fetch_all_prefetched_decipher_level_2_relation_no_lang(self):
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

        continents = Continent.objects.prefetch_related(*lvl_1_2).translate().translate_related(*lvl_2).translate('en-us')
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
    def test_fetch_all_prefetched_decipher_level_1_2_relation_no_lang(self):
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

        continents = Continent.objects.prefetch_related(*lvl_1_2).translate().translate_related(*lvl_1_2).translate('en-us')
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

    def test_fetch_all_prefetched_decipher_level_0_relation_with_lang(self):
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

        continents = Continent.objects.prefetch_related(*lvl_1_2).translate('de').translate('en-us')
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

    def test_fetch_all_prefetched_decipher_level_1_relation_with_lang(self):
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

        continents = Continent.objects.prefetch_related(*lvl_1_2).translate('de').translate_related(*lvl_1).translate('en-us')
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

    def test_fetch_all_prefetched_decipher_level_2_relation_with_lang(self):
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

        continents = Continent.objects.prefetch_related(*lvl_1_2).translate('de').translate_related(*lvl_2).translate('en-us')
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

    def test_fetch_all_prefetched_decipher_level_1_2_relation_with_lang(self):
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

        continents = Continent.objects.prefetch_related(*lvl_1_2).translate('de').translate_related(*lvl_1_2).translate('en-us')
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

    def test_translate(self):
        continents = Continent.objects.translate('de')

        self.assertEqual(continents._trans_lang, 'de')

    @override(language='de', deactivate=True)
    def test_translate_no_lang(self):
        continents = Continent.objects.translate()

        self.assertEqual(continents._trans_lang, 'de')

    def test_translate_invalid_lang(self):
        with self.assertRaises(ValueError) as error:
            Continent.objects.translate('xx')

        self.assertEqual(
            error.exception.args[0],
            '`xx` is not a supported language.'
        )

    def test_translate_related(self):
        continents = Continent.objects.translate_related(
            'countries', 'countries__cities')

        self.assertTupleEqual(
            continents._trans_rels,
            ('countries', 'countries__cities',)
        )

    def test_probe(self):
        continents = Continent.objects.probe('de')

        self.assertEqual(continents._trans_prob, 'de')

    @override(language='de', deactivate=True)
    def test_probe_no_lang(self):
        continents = Continent.objects.probe()

        self.assertEqual(continents._trans_prob, 'de')

    def test_probe_invalid_lang(self):
        with self.assertRaises(ValueError) as error:
            Continent.objects.probe('xx')

        self.assertEqual(
            error.exception.args[0],
            '`xx` is not a supported language.'
        )
