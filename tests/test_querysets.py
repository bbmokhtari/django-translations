from django.test import TestCase, override_settings
from django.db.models import Q

from translations.querysets import TranslatableQuerySet

from sample.models import Continent

from tests.sample import create_samples


class TranslatableQuerySetTest(TestCase):
    """Tests for `TranslatableQuerySet`."""

    def test_init(self):
        continents = Continent.objects.all()

        self.assertEqual(continents._trans_lang, None)
        self.assertTupleEqual(continents._trans_rels, ())
        self.assertEqual(continents._trans_cipher, True)
        self.assertEqual(continents._trans_cache, False)

    def test_chain(self):
        continents = Continent.objects.all()

        continents._trans_lang = 'de'
        continents._trans_rels = ('countries', 'countries__cities',)
        continents._trans_cipher = False
        continents._trans_cache = True

        continents = continents._chain()

        self.assertEqual(continents._trans_lang, 'de')
        self.assertTupleEqual(continents._trans_rels, ('countries', 'countries__cities',))
        self.assertEqual(continents._trans_cipher, False)
        self.assertEqual(continents._trans_cache, False)

    def test_translate_mode_lang_set_cipher_set(self):
        continents = Continent.objects.all()

        continents._trans_lang = 'de'
        continents._trans_cipher = True

        self.assertEqual(continents._translate_mode(), True)

    def test_translate_mode_lang_set_cipher_unset(self):
        continents = Continent.objects.all()

        continents._trans_lang = 'de'
        continents._trans_cipher = False

        self.assertEqual(continents._translate_mode(), False)

    def test_translate_mode_lang_unset_cipher_set(self):
        continents = Continent.objects.all()

        continents._trans_lang = None
        continents._trans_cipher = True

        self.assertEqual(continents._translate_mode(), False)

    def test_translate_mode_lang_unset_cipher_unset(self):
        continents = Continent.objects.all()

        continents._trans_lang = None
        continents._trans_cipher = False

        self.assertEqual(continents._translate_mode(), False)

    def test_fetch_all_normal_mode(self):
        create_samples(
            continent_names=['europe'],
            continent_fields=['name', 'denonym'],
            langs=['de']
        )

        continents = Continent.objects.all()

        self.assertEqual(continents[0].name, 'Europe')
        self.assertEqual(continents[0].denonym, 'European')

    # TODO: MORE _fetch_all tests - START

    @override_settings(LANGUAGE_CODE='de')
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

        europe = Continent.objects.apply().get(code='EU')
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europa')
        self.assertEqual(europe.denonym, 'Europäisch')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')

    @override_settings(LANGUAGE_CODE='de')
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

        europe = Continent.objects.apply().translate_related(*lvl_1).get(code='EU')
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europa')
        self.assertEqual(europe.denonym, 'Europäisch')
        self.assertEqual(germany.name, 'Deutschland')
        self.assertEqual(germany.denonym, 'Deutsche')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')

    @override_settings(LANGUAGE_CODE='de')
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

        europe = Continent.objects.apply().translate_related(*lvl_2).get(code='EU')
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europa')
        self.assertEqual(europe.denonym, 'Europäisch')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Köln')
        self.assertEqual(cologne.denonym, 'Kölner')

    @override_settings(LANGUAGE_CODE='de')
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

        europe = Continent.objects.apply().translate_related(*lvl_1_2).get(code='EU')
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

        europe = Continent.objects.apply('de').get(code='EU')
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

        europe = Continent.objects.apply('de').translate_related(*lvl_1).get(code='EU')
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

        europe = Continent.objects.apply('de').translate_related(*lvl_2).get(code='EU')
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

        europe = Continent.objects.apply('de').translate_related(*lvl_1_2).get(code='EU')
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europa')
        self.assertEqual(europe.denonym, 'Europäisch')
        self.assertEqual(germany.name, 'Deutschland')
        self.assertEqual(germany.denonym, 'Deutsche')
        self.assertEqual(cologne.name, 'Köln')
        self.assertEqual(cologne.denonym, 'Kölner')

    @override_settings(LANGUAGE_CODE='de')
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

        europe = Continent.objects.prefetch_related(*lvl_1_2).apply().get(code='EU')
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europa')
        self.assertEqual(europe.denonym, 'Europäisch')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')

    @override_settings(LANGUAGE_CODE='de')
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

        europe = Continent.objects.prefetch_related(*lvl_1_2).apply().translate_related(*lvl_1).get(code='EU')
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europa')
        self.assertEqual(europe.denonym, 'Europäisch')
        self.assertEqual(germany.name, 'Deutschland')
        self.assertEqual(germany.denonym, 'Deutsche')
        self.assertEqual(cologne.name, 'Cologne')
        self.assertEqual(cologne.denonym, 'Cologner')

    @override_settings(LANGUAGE_CODE='de')
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

        europe = Continent.objects.prefetch_related(*lvl_1_2).apply().translate_related(*lvl_2).get(code='EU')
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europa')
        self.assertEqual(europe.denonym, 'Europäisch')
        self.assertEqual(germany.name, 'Germany')
        self.assertEqual(germany.denonym, 'German')
        self.assertEqual(cologne.name, 'Köln')
        self.assertEqual(cologne.denonym, 'Kölner')

    @override_settings(LANGUAGE_CODE='de')
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

        europe = Continent.objects.prefetch_related(*lvl_1_2).apply().translate_related(*lvl_1_2).get(code='EU')
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

        europe = Continent.objects.prefetch_related(*lvl_1_2).apply('de').get(code='EU')
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

        europe = Continent.objects.prefetch_related(*lvl_1_2).apply('de').translate_related(*lvl_1).get(code='EU')
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

        europe = Continent.objects.prefetch_related(*lvl_1_2).apply('de').translate_related(*lvl_2).get(code='EU')
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

        europe = Continent.objects.prefetch_related(*lvl_1_2).apply('de').translate_related(*lvl_1_2).get(code='EU')
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        self.assertEqual(europe.name, 'Europa')
        self.assertEqual(europe.denonym, 'Europäisch')
        self.assertEqual(germany.name, 'Deutschland')
        self.assertEqual(germany.denonym, 'Deutsche')
        self.assertEqual(cologne.name, 'Köln')
        self.assertEqual(cologne.denonym, 'Kölner')

    @override_settings(LANGUAGE_CODE='de')
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

        continents = Continent.objects.apply().all()
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

    @override_settings(LANGUAGE_CODE='de')
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

        continents = Continent.objects.apply().translate_related(*lvl_1).all()
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

    @override_settings(LANGUAGE_CODE='de')
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

        continents = Continent.objects.apply().translate_related(*lvl_2).all()
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

    @override_settings(LANGUAGE_CODE='de')
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

        continents = Continent.objects.apply().translate_related(*lvl_1_2).all()
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

        continents = Continent.objects.apply('de').all()
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

        continents = Continent.objects.apply('de').translate_related(*lvl_1).all()
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

        continents = Continent.objects.apply('de').translate_related(*lvl_2).all()
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

        continents = Continent.objects.apply('de').translate_related(*lvl_1_2).all()
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

    @override_settings(LANGUAGE_CODE='de')
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

        continents = Continent.objects.prefetch_related(*lvl_1_2).apply()
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

    @override_settings(LANGUAGE_CODE='de')
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

        continents = Continent.objects.prefetch_related(*lvl_1_2).apply().translate_related(*lvl_1)
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

    @override_settings(LANGUAGE_CODE='de')
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

        continents = Continent.objects.prefetch_related(*lvl_1_2).apply().translate_related(*lvl_2)
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

    @override_settings(LANGUAGE_CODE='de')
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

        continents = Continent.objects.prefetch_related(*lvl_1_2).apply().translate_related(*lvl_1_2)
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

        continents = Continent.objects.prefetch_related(*lvl_1_2).apply('de')
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

        continents = Continent.objects.prefetch_related(*lvl_1_2).apply('de').translate_related(*lvl_1)
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

        continents = Continent.objects.prefetch_related(*lvl_1_2).apply('de').translate_related(*lvl_2)
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

        continents = Continent.objects.prefetch_related(*lvl_1_2).apply('de').translate_related(*lvl_1_2)
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

    # TODO: MORE _fetch_all tests - END

    def test_get_translations_queries_lookup_nr_yf_nt_nl(self):
        continents = Continent.objects.apply(
            'de')._get_translations_queries(
                code='EU')

        self.assertDictEqual(
            dict(continents[0].children),
            {
                'code': 'EU',
            }
        )

    def test_get_translations_queries_lookup_nr_yf_yt_nl(self):
        continents = Continent.objects.apply(
            'de')._get_translations_queries(
                name='Europa')

        self.assertDictEqual(
            dict(continents[0].children),
            {
                'translations__field': 'name',
                'translations__language': 'de',
                'translations__text': 'Europa',
            }
        )

    def test_get_translations_queries_lookup_nr_yf_nt_yl(self):
        continents = Continent.objects.apply(
            'de')._get_translations_queries(
                code__icontains='EU')

        self.assertDictEqual(
            dict(continents[0].children),
            {
                'code__icontains': 'EU',
            },
        )

    def test_get_translations_queries_lookup_nr_yf_yt_yl(self):
        continents = Continent.objects.apply(
            'de')._get_translations_queries(
                name__icontains='Europa')

        self.assertDictEqual(
            dict(continents[0].children),
            {
                'translations__field': 'name',
                'translations__language': 'de',
                'translations__text__icontains': 'Europa',
            }
        )

    def test_get_translations_queries_lookup_yr_nf_nl(self):
        continents = Continent.objects.apply(
            'de')._get_translations_queries(
                countries=1)

        self.assertDictEqual(
            dict(continents[0].children),
            {
                'countries': 1,
            }
        )

    def test_get_translations_queries_lookup_yr_nf_yl(self):
        continents = Continent.objects.apply(
            'de')._get_translations_queries(
                countries__gt=1)

        self.assertDictEqual(
            dict(continents[0].children),
            {
                'countries__gt': 1,
            }
        )

    def test_get_translations_queries_lookup_yr_yf_nt_nl(self):
        continents = Continent.objects.apply(
            'de')._get_translations_queries(
                countries__code='DE')

        self.assertDictEqual(
            dict(continents[0].children),
            {
                'countries__code': 'DE',
            }
        )

    def test_get_translations_queries_lookup_yr_yf_yt_nl(self):
        continents = Continent.objects.apply(
            'de')._get_translations_queries(
                countries__name='Deutschland')

        self.assertDictEqual(
            dict(continents[0].children),
            {
                'countries__translations__field': 'name',
                'countries__translations__language': 'de',
                'countries__translations__text': 'Deutschland',
            }
        )

    def test_get_translations_queries_lookup_yr_yf_nt_yl(self):
        continents = Continent.objects.apply(
            'de')._get_translations_queries(
                countries__code__icontains='DE')

        self.assertDictEqual(
            dict(continents[0].children),
            {
                'countries__code__icontains': 'DE',
            }
        )

    def test_get_translations_queries_lookup_yr_yf_yt_yl(self):
        continents = Continent.objects.apply(
            'de')._get_translations_queries(
                countries__name__icontains='Deutsch')

        self.assertDictEqual(
            dict(continents[0].children),
            {
                'countries__translations__field': 'name',
                'countries__translations__language': 'de',
                'countries__translations__text__icontains': 'Deutsch',
            }
        )

    def test_get_translations_queries_lookup_yrnested_yf_nt_nl(self):
        continents = Continent.objects.apply(
            'de')._get_translations_queries(
                countries__cities__id=1)

        self.assertDictEqual(
            dict(continents[0].children),
            {
                'countries__cities__id': 1,
            }
        )

    def test_get_translations_queries_lookup_yrnested_yf_yt_nl(self):
        continents = Continent.objects.apply(
            'de')._get_translations_queries(
                countries__cities__name='Köln')

        self.assertDictEqual(
            dict(continents[0].children),
            {
                'countries__cities__translations__field': 'name',
                'countries__cities__translations__language': 'de',
                'countries__cities__translations__text': 'Köln',
            }
        )

    def test_get_translations_queries_lookup_yrnested_yf_nt_yl(self):
        continents = Continent.objects.apply(
            'de')._get_translations_queries(
                countries__cities__id__gt=1)

        self.assertDictEqual(
            dict(continents[0].children),
            {
                'countries__cities__id__gt': 1,
            }
        )

    def test_get_translations_queries_lookup_yrnested_yf_yt_yl(self):
        continents = Continent.objects.apply(
            'de')._get_translations_queries(
                countries__cities__name__icontains='Kö')

        self.assertDictEqual(
            dict(continents[0].children),
            {
                'countries__cities__translations__field': 'name',
                'countries__cities__translations__language': 'de',
                'countries__cities__translations__text__icontains': 'Kö',
            }
        )

    def test_get_translations_queries_query_nr_yf_nt_nl(self):
        continents = Continent.objects.apply(
            'de')._get_translations_queries(
                Q(code='EU'))

        self.assertDictEqual(
            dict(continents[0].children[0].children),
            {
                'code': 'EU',
            }
        )

    def test_get_translations_queries_query_nr_yf_yt_nl(self):
        continents = Continent.objects.apply(
            'de')._get_translations_queries(
                Q(name='Europa'))

        self.assertDictEqual(
            dict(continents[0].children[0].children),
            {
                'translations__field': 'name',
                'translations__language': 'de',
                'translations__text': 'Europa',
            }
        )

    def test_get_translations_queries_query_nr_yf_nt_yl(self):
        continents = Continent.objects.apply(
            'de')._get_translations_queries(
                Q(code__icontains='EU'))

        self.assertDictEqual(
            dict(continents[0].children[0].children),
            {
                'code__icontains': 'EU',
            },
        )

    def test_get_translations_queries_query_nr_yf_yt_yl(self):
        continents = Continent.objects.apply(
            'de')._get_translations_queries(
                Q(name__icontains='Europa'))

        self.assertDictEqual(
            dict(continents[0].children[0].children),
            {
                'translations__field': 'name',
                'translations__language': 'de',
                'translations__text__icontains': 'Europa',
            }
        )

    def test_get_translations_queries_query_yr_nf_nl(self):
        continents = Continent.objects.apply(
            'de')._get_translations_queries(
                Q(countries=1))

        self.assertDictEqual(
            dict(continents[0].children[0].children),
            {
                'countries': 1,
            }
        )

    def test_get_translations_queries_query_yr_nf_yl(self):
        continents = Continent.objects.apply(
            'de')._get_translations_queries(
                Q(countries__gt=1))

        self.assertDictEqual(
            dict(continents[0].children[0].children),
            {
                'countries__gt': 1,
            }
        )

    def test_get_translations_queries_query_yr_yf_nt_nl(self):
        continents = Continent.objects.apply(
            'de')._get_translations_queries(
                Q(countries__code='DE'))

        self.assertDictEqual(
            dict(continents[0].children[0].children),
            {
                'countries__code': 'DE',
            }
        )

    def test_get_translations_queries_query_yr_yf_yt_nl(self):
        continents = Continent.objects.apply(
            'de')._get_translations_queries(
                Q(countries__name='Deutschland'))

        self.assertDictEqual(
            dict(continents[0].children[0].children),
            {
                'countries__translations__field': 'name',
                'countries__translations__language': 'de',
                'countries__translations__text': 'Deutschland',
            }
        )

    def test_get_translations_queries_query_yr_yf_nt_yl(self):
        continents = Continent.objects.apply(
            'de')._get_translations_queries(
                Q(countries__code__icontains='DE'))

        self.assertDictEqual(
            dict(continents[0].children[0].children),
            {
                'countries__code__icontains': 'DE',
            }
        )

    def test_get_translations_queries_query_yr_yf_yt_yl(self):
        continents = Continent.objects.apply(
            'de')._get_translations_queries(
                Q(countries__name__icontains='Deutsch'))

        self.assertDictEqual(
            dict(continents[0].children[0].children),
            {
                'countries__translations__field': 'name',
                'countries__translations__language': 'de',
                'countries__translations__text__icontains': 'Deutsch',
            }
        )

    def test_get_translations_queries_query_yrnested_yf_nt_nl(self):
        continents = Continent.objects.apply(
            'de')._get_translations_queries(
                Q(countries__cities__id=1))

        self.assertDictEqual(
            dict(continents[0].children[0].children),
            {
                'countries__cities__id': 1,
            }
        )

    def test_get_translations_queries_query_yrnested_yf_yt_nl(self):
        continents = Continent.objects.apply(
            'de')._get_translations_queries(
                Q(countries__cities__name='Köln'))

        self.assertDictEqual(
            dict(continents[0].children[0].children),
            {
                'countries__cities__translations__field': 'name',
                'countries__cities__translations__language': 'de',
                'countries__cities__translations__text': 'Köln',
            }
        )

    def test_get_translations_queries_query_yrnested_yf_nt_yl(self):
        continents = Continent.objects.apply(
            'de')._get_translations_queries(
                Q(countries__cities__id__gt=1))

        self.assertDictEqual(
            dict(continents[0].children[0].children),
            {
                'countries__cities__id__gt': 1,
            }
        )

    def test_get_translations_queries_query_yrnested_yf_yt_yl(self):
        continents = Continent.objects.apply(
            'de')._get_translations_queries(
                Q(countries__cities__name__icontains='Kö'))

        self.assertDictEqual(
            dict(continents[0].children[0].children),
            {
                'countries__cities__translations__field': 'name',
                'countries__cities__translations__language': 'de',
                'countries__cities__translations__text__icontains': 'Kö',
            }
        )

    def test_get_translations_queries_query_nested_query(self):
        continents = Continent.objects.apply(
            'de')._get_translations_queries(
                Q(countries__cities__name__icontains='Kö'))

        self.assertDictEqual(
            dict(continents[0].children[0].children),
            {
                'countries__cities__translations__field': 'name',
                'countries__cities__translations__language': 'de',
                'countries__cities__translations__text__icontains': 'Kö',
            }
        )

    def test_apply(self):
        continents = Continent.objects.apply('de')

        self.assertEqual(continents._trans_lang, 'de')

    @override_settings(LANGUAGE_CODE='de')
    def test_apply_no_lang(self):
        continents = Continent.objects.apply()

        self.assertEqual(continents._trans_lang, 'de')

    def test_apply_invalid_lang(self):
        with self.assertRaises(ValueError) as error:
            continents = Continent.objects.apply('xx')

        self.assertEqual(
            error.exception.args[0],
            'The language code `xx` is not supported.'
        )

    def test_translate_related(self):
        continents = Continent.objects.translate_related(
            'countries', 'countries__cities')

        self.assertTupleEqual(
            continents._trans_rels,
            ('countries', 'countries__cities',)
        )

    def test_cipher(self):
        continents = Continent.objects.cipher()

        self.assertEqual(continents._trans_cipher, True)

    def test_decipher(self):
        continents = Continent.objects.decipher()

        self.assertEqual(continents._trans_cipher, False)
