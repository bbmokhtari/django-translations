from django.test import TestCase
from django.contrib.contenttypes.models import ContentType
from django.db import utils
from translations.models import Translation

from .models import Continent, Country, City


class TranslationTest(TestCase):

    def test_content_type_none(self):
        continent = Continent.objects.create(name="Europe", code="EU")
        with self.assertRaises(utils.IntegrityError) as error:
            Translation.objects.create(
                content_type=None,
                object_id=continent.id,
                field="name",
                language="fr",
                text="L'Europe",
            )
        self.assertEqual(
            error.exception.args[0],
            "NOT NULL constraint failed: translations_translation.content_type_id",
        )

    def test_object_id_none(self):
        continent_ct = ContentType.objects.get_for_model(Continent)
        with self.assertRaises(utils.IntegrityError) as error:
            Translation.objects.create(
                content_type=continent_ct,
                object_id=None,
                field="name",
                language="fr",
                text="L'Europe",
            )
        self.assertEqual(
            error.exception.args[0],
            "NOT NULL constraint failed: translations_translation.object_id",
        )

    def test_field_none(self):
        continent = Continent.objects.create(name="Europe", code="EU")
        continent_ct = ContentType.objects.get_for_model(Continent)
        with self.assertRaises(utils.IntegrityError) as error:
            Translation.objects.create(
                content_type=continent_ct,
                object_id=continent.id,
                field=None,
                language="fr",
                text="L'Europe",
            )
        self.assertEqual(
            error.exception.args[0],
            "NOT NULL constraint failed: translations_translation.field",
        )

    def test_language_none(self):
        continent = Continent.objects.create(name="Europe", code="EU")
        continent_ct = ContentType.objects.get_for_model(Continent)
        with self.assertRaises(utils.IntegrityError) as error:
            Translation.objects.create(
                content_type=continent_ct,
                object_id=continent.id,
                field="name",
                language=None,
                text="L'Europe",
            )
        self.assertEqual(
            error.exception.args[0],
            "NOT NULL constraint failed: translations_translation.language",
        )

    def test_text_none(self):
        continent = Continent.objects.create(name="Europe", code="EU")
        continent_ct = ContentType.objects.get_for_model(Continent)
        with self.assertRaises(utils.IntegrityError) as error:
            Translation.objects.create(
                content_type=continent_ct,
                object_id=continent.id,
                field="name",
                language="fr",
                text=None,
            )
        self.assertEqual(
            error.exception.args[0],
            "NOT NULL constraint failed: translations_translation.text",
        )

    def test_str(self):
        continent = Continent.objects.create(name="Europe", code="EU")
        continent_ct = ContentType.objects.get_for_model(Continent)
        translation = Translation.objects.create(
            content_type=continent_ct,
            object_id=continent.id,
            field="name",
            language="fr",
            text="L'Europe"
        )
        self.assertEqual(str(translation), "Europe: L'Europe")

    def test_uniqueness(self):
        continent = Continent.objects.create(name="Europe", code="EU")
        continent_ct = ContentType.objects.get_for_model(Continent)
        Translation.objects.create(
            content_type=continent_ct,
            object_id=continent.id,
            field="name",
            language="fr",
            text="L'Europe"
        )
        with self.assertRaises(utils.IntegrityError) as error:
            Translation.objects.create(
                content_type=continent_ct,
                object_id=continent.id,
                field="name",
                language="fr",
                text="Europe"
            )
        self.assertEqual(
            error.exception.args[0],
            "UNIQUE constraint failed: translations_translation.content_type_id, translations_translation.object_id, translations_translation.field, translations_translation.language",
        )


class TranslatableTest(TestCase):

    def test_translations(self):
        continent_eu = Continent.objects.create(name="Europe", code="EU")
        continent_eu.translations.create(field="name", language="fr", text="L'Europe")
        self.assertQuerysetEqual(continent_eu.translations.all(), ["<Translation: Europe: L'Europe>"])

    def test_two_different_translations(self):
        continent_eu = Continent.objects.create(name="Europe", code="EU")
        continent_as = Continent.objects.create(name="Asia", code="AS")
        continent_eu.translations.create(field="name", language="fr", text="L'Europe")
        continent_as.translations.create(field="name", language="fr", text="Asie")
        self.assertQuerysetEqual(continent_eu.translations.all(), ["<Translation: Europe: L'Europe>"])
        self.assertQuerysetEqual(continent_as.translations.all(), ["<Translation: Asia: Asie>"])

    def test_fields(self):
        self.assertListEqual(Continent.get_translatable_fields(), [Continent._meta.get_field("name")])

    def test_get_translations_for_object(self):
        continent = Continent.objects.create(name="Europe", code="EU")
        country = Country.objects.create(name="France", code="FR", continent=continent)
        country.translations.create(field="name", language="fr", text="France")
        self.assertQuerysetEqual(country.get_translations(lang="fr"), ["<Translation: France: France>"])

    def test_get_translations_for_object_and_relations(self):
        continent = Continent.objects.create(name="Europe", code="EU")
        country = continent.countries.create(name="France", code="FR")
        paris = country.cities.create(name="Paris")
        marseille = country.cities.create(name="Marseille")
        continent.translations.create(field="name", language="fr", text="L'Europe")
        country.translations.create(field="name", language="fr", text="France")
        paris.translations.create(field="name", language="fr", text="Paris")
        marseille.translations.create(field="name", language="fr", text="Marseille")
        self.assertQuerysetEqual(
            country.get_translations('continent', 'cities', lang="fr").order_by('text'),
            [
                "<Translation: France: France>",
                "<Translation: Europe: L'Europe>",
                "<Translation: Marseille: Marseille>",
                "<Translation: Paris: Paris>",
            ]
        )
