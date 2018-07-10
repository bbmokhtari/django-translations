from django.test import TestCase
from django.contrib.contenttypes.models import ContentType
from django.db import utils
from translations.models import Translation

from .models import Continent, Country, City


class TranslationTest(TestCase):

    def test_content_type_none(self):
        europe = Continent.objects.create(name="Europe", code="EU")
        with self.assertRaises(utils.IntegrityError) as error:
            Translation.objects.create(
                content_type=None,
                object_id=europe.id,
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

    def test_content_object_none(self):
        with self.assertRaises(utils.IntegrityError) as error:
            Translation.objects.create(
                content_object=None,
                field="name",
                language="fr",
                text="L'Europe",
            )
        self.assertEqual(
            error.exception.args[0],
            "NOT NULL constraint failed: translations_translation.object_id",
        )

    def test_field_none(self):
        europe = Continent.objects.create(name="Europe", code="EU")
        continent_ct = ContentType.objects.get_for_model(Continent)
        with self.assertRaises(utils.IntegrityError) as error:
            Translation.objects.create(
                content_type=continent_ct,
                object_id=europe.id,
                field=None,
                language="fr",
                text="L'Europe",
            )
        self.assertEqual(
            error.exception.args[0],
            "NOT NULL constraint failed: translations_translation.field",
        )

    def test_language_none(self):
        europe = Continent.objects.create(name="Europe", code="EU")
        continent_ct = ContentType.objects.get_for_model(Continent)
        with self.assertRaises(utils.IntegrityError) as error:
            Translation.objects.create(
                content_type=continent_ct,
                object_id=europe.id,
                field="name",
                language=None,
                text="L'Europe",
            )
        self.assertEqual(
            error.exception.args[0],
            "NOT NULL constraint failed: translations_translation.language",
        )

    def test_text_none(self):
        europe = Continent.objects.create(name="Europe", code="EU")
        continent_ct = ContentType.objects.get_for_model(Continent)
        with self.assertRaises(utils.IntegrityError) as error:
            Translation.objects.create(
                content_type=continent_ct,
                object_id=europe.id,
                field="name",
                language="fr",
                text=None,
            )
        self.assertEqual(
            error.exception.args[0],
            "NOT NULL constraint failed: translations_translation.text",
        )

    def test_str(self):
        europe = Continent.objects.create(name="Europe", code="EU")
        continent_ct = ContentType.objects.get_for_model(Continent)
        translation = Translation.objects.create(
            content_type=continent_ct,
            object_id=europe.id,
            field="name",
            language="fr",
            text="L'Europe"
        )
        self.assertEqual(str(translation), "Europe: L'Europe")

    def test_uniqueness(self):
        europe = Continent.objects.create(name="Europe", code="EU")
        continent_ct = ContentType.objects.get_for_model(Continent)
        Translation.objects.create(
            content_type=continent_ct,
            object_id=europe.id,
            field="name",
            language="fr",
            text="L'Europe"
        )
        with self.assertRaises(utils.IntegrityError) as error:
            Translation.objects.create(
                content_type=continent_ct,
                object_id=europe.id,
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
        europe = Continent.objects.create(name="Europe", code="EU")
        europe.translations.create(field="name", language="fr", text="L'Europe")
        self.assertQuerysetEqual(europe.translations.all(), ["<Translation: Europe: L'Europe>"])

    def test_two_different_translations(self):
        europe = Continent.objects.create(name="Europe", code="EU")
        europe.translations.create(field="name", language="fr", text="L'Europe")

        asia = Continent.objects.create(name="Asia", code="AS")
        asia.translations.create(field="name", language="fr", text="Asie")

        self.assertQuerysetEqual(europe.translations.all(), ["<Translation: Europe: L'Europe>"])
        self.assertQuerysetEqual(asia.translations.all(), ["<Translation: Asia: Asie>"])

    def test_fields(self):
        self.assertListEqual(Continent.get_translatable_fields(), [Continent._meta.get_field("name")])

    def test_get_translations_for_object(self):
        europe = Continent.objects.create(name="Europe", code="EU")
        europe.translations.create(field="name", language="fr", text="L'Europe")
        self.assertQuerysetEqual(europe.get_translations(lang="fr"), ["<Translation: Europe: L'Europe>"])

    def test_get_translations_for_two_objects(self):
        europe = Continent.objects.create(name="Europe", code="EU")
        europe.translations.create(field="name", language="fr", text="L'Europe")

        asia = Continent.objects.create(name="Asia")
        asia.translations.create(field="name", language="fr", text="Asie")

        self.assertQuerysetEqual(europe.get_translations(lang="fr"), ["<Translation: Europe: L'Europe>"])
        self.assertQuerysetEqual(asia.get_translations(lang="fr"), ["<Translation: Asia: Asie>"])

    def test_get_translations_for_object_and_relations(self):
        europe = Continent.objects.create(name="Europe", code="EU")
        europe.translations.create(field="name", language="fr", text="L'Europe")

        france = europe.countries.create(name="France", code="FR")
        france.translations.create(field="name", language="fr", text="France")

        paris = france.cities.create(name="Paris")
        paris.translations.create(field="name", language="fr", text="Paris")
        marseille = france.cities.create(name="Marseille")
        marseille.translations.create(field="name", language="fr", text="Marseille")

        self.assertQuerysetEqual(
            france.get_translations('continent', 'cities', lang="fr").order_by('text'),
            [
                "<Translation: France: France>",
                "<Translation: Europe: L'Europe>",
                "<Translation: Marseille: Marseille>",
                "<Translation: Paris: Paris>",
            ]
        )
