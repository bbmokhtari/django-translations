from django.test import TestCase

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

    def test_fetch_all_translate_mode(self):
        create_samples(
            continent_names=['europe'],
            continent_fields=['name', 'denonym'],
            langs=['de']
        )

        continents = Continent.objects.all().apply('de')

        self.assertEqual(continents[0].name, 'Europa')
        self.assertEqual(continents[0].denonym, 'Europäisch')
