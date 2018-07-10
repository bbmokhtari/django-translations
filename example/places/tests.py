from django.test import TestCase
from django.contrib.contenttypes.models import ContentType
from django.db import utils
from translations.models import Translation

from .models import Continent, Country, City


class TranslationTest(TestCase):

    def test_content_type_none(self):
        """Make sure `content_type` can not be null."""
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
        """Make sure `object_id` can not be null."""
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
        """Make sure `content_object` can not be null."""
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
        """Make sure `field` can not be null."""
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
        """Make sure `language` can not be null."""
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
        """Make sure text can not be null."""
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
        """Make sure `__str__` returns source and translation."""
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
        """Make sure `content_type`, `object_id`, `field` and `language` combination is unique."""
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
        """Make sure `translations` rel works."""
        europe = Continent.objects.create(name="Europe", code="EU")
        europe.translations.create(field="name", language="fr", text="L'Europe")
        self.assertQuerysetEqual(europe.translations.all(), ["<Translation: Europe: L'Europe>"])

    def test_two_different_translations(self):
        """Make sure `translations` for distinct objects are different."""
        europe = Continent.objects.create(name="Europe", code="EU")
        europe.translations.create(field="name", language="fr", text="L'Europe")

        asia = Continent.objects.create(name="Asia", code="AS")
        asia.translations.create(field="name", language="fr", text="Asie")

        self.assertQuerysetEqual(europe.translations.all(), ["<Translation: Europe: L'Europe>"])
        self.assertQuerysetEqual(asia.translations.all(), ["<Translation: Asia: Asie>"])

    def test_fields(self):
        """Make sure `TranslatableMeta.fields` works."""
        self.assertListEqual(Continent.get_translatable_fields(), [Continent._meta.get_field("name")])

    def test_get_translations_for_object(self):
        """Make sure `get_translations` works."""
        europe = Continent.objects.create(name="Europe", code="EU")
        europe.translations.create(field="name", language="fr", text="L'Europe")
        self.assertQuerysetEqual(europe.get_translations(lang="fr"), ["<Translation: Europe: L'Europe>"])

    def test_get_translations_for_two_objects(self):
        """Make sure `get_translations` works for two distinct objects."""
        europe = Continent.objects.create(name="Europe", code="EU")
        europe.translations.create(field="name", language="fr", text="L'Europe")

        asia = Continent.objects.create(name="Asia")
        asia.translations.create(field="name", language="fr", text="Asie")

        self.assertQuerysetEqual(europe.get_translations(lang="fr"), ["<Translation: Europe: L'Europe>"])
        self.assertQuerysetEqual(asia.get_translations(lang="fr"), ["<Translation: Asia: Asie>"])

    def test_get_translations_for_object_and_relations(self):
        """Make sure `get_translations` works with `relations` argument."""
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

    def test_get_translations_for_two_objects_and_relations(self):
        """Make sure `get_translations` works with `relations` argument for two distinct objects."""
        europe = Continent.objects.create(name="Europe", code="EU")
        europe.translations.create(field="name", language="fr", text="L'Europe")

        asia = Continent.objects.create(name="Asia", code="AS")
        asia.translations.create(field="name", language="fr", text="Asie")

        france = europe.countries.create(name="France", code="FR")
        france.translations.create(field="name", language="fr", text="France")

        japan = asia.countries.create(name="Japan", code="JP")
        japan.translations.create(field="name", language="fr", text="Japon")

        paris = france.cities.create(name="Paris")
        paris.translations.create(field="name", language="fr", text="Paris")
        marseille = france.cities.create(name="Marseille")
        marseille.translations.create(field="name", language="fr", text="Marseille")

        tokio = japan.cities.create(name="Tokio")
        tokio.translations.create(field="name", language="fr", text="Tokio")

        kioto = japan.cities.create(name="Kioto")
        kioto.translations.create(field="name", language="fr", text="Kioto")

        self.assertQuerysetEqual(
            france.get_translations('continent', 'cities', lang="fr").order_by('text'),
            [
                "<Translation: France: France>",
                "<Translation: Europe: L'Europe>",
                "<Translation: Marseille: Marseille>",
                "<Translation: Paris: Paris>",
            ]
        )

        self.assertQuerysetEqual(
            japan.get_translations('continent', 'cities', lang="fr").order_by('text'),
            [
                "<Translation: Asia: Asie>",
                "<Translation: Japan: Japon>",
                "<Translation: Kioto: Kioto>",
                "<Translation: Tokio: Tokio>",
            ]
        )

    def test_translate_for_object(self):
        """Make sure `translate` works."""
        europe = Continent.objects.create(name="Europe", code="EU")
        europe.translations.create(field="name", language="fr", text="L'Europe")
        europe.translate(lang="fr")
        self.assertEqual(europe.name, "L'Europe")

    def test_translate_for_two_objects(self):
        """Make sure `translate` works for two distinct objects."""
        europe = Continent.objects.create(name="Europe", code="EU")
        europe.translations.create(field="name", language="fr", text="L'Europe")

        asia = Continent.objects.create(name="Asia")
        asia.translations.create(field="name", language="fr", text="Asie")

        europe.translate(lang="fr")
        asia.translate(lang="fr")

        self.assertEqual(europe.name, "L'Europe")
        self.assertEqual(asia.name, "Asie")

    def test_translate_for_object_and_relations(self):
        """Make sure `translate` works with `relations` argument."""
        europe = Continent.objects.create(name="Europe", code="EU")
        europe.translations.create(field="name", language="fr", text="L'Europe")

        france = europe.countries.create(name="France", code="FR")
        france.translations.create(field="name", language="fr", text="France")

        paris = france.cities.create(name="Paris")
        paris.translations.create(field="name", language="fr", text="Paris")
        marseille = france.cities.create(name="Marseille")
        marseille.translations.create(field="name", language="fr", text="Marseille")

        france.translate("continent", "cities", lang="fr")

        self.assertEqual(france.name, "France")
        self.assertEqual(france.continent.name, "L'Europe")
        for city in france.cities.all():
            self.assertIn(city.name, ["Marseille", "Paris"])

    def test_translate_for_two_objects_and_relations(self):
        """Make sure `translate` works with `relations` argument for two distinct objects."""
        europe = Continent.objects.create(name="Europe", code="EU")
        europe.translations.create(field="name", language="fr", text="L'Europe")

        asia = Continent.objects.create(name="Asia", code="AS")
        asia.translations.create(field="name", language="fr", text="Asie")

        france = europe.countries.create(name="France", code="FR")
        france.translations.create(field="name", language="fr", text="France")

        japan = asia.countries.create(name="Japan", code="JP")
        japan.translations.create(field="name", language="fr", text="Japon")

        paris = france.cities.create(name="Paris")
        paris.translations.create(field="name", language="fr", text="Paris")
        marseille = france.cities.create(name="Marseille")
        marseille.translations.create(field="name", language="fr", text="Marseille")

        tokio = japan.cities.create(name="Tokio")
        tokio.translations.create(field="name", language="fr", text="Tokio")

        kioto = japan.cities.create(name="Kioto")
        kioto.translations.create(field="name", language="fr", text="Kioto")

        france.translate("continent", "cities", lang="fr")
        japan.translate("continent", "cities", lang="fr")

        self.assertEqual(france.name, "France")
        self.assertEqual(france.continent.name, "L'Europe")
        for city in france.cities.all():
            self.assertIn(city.name, ["Marseille", "Paris"])

        self.assertEqual(japan.name, "Japon")
        self.assertEqual(japan.continent.name, "Asie")
        for city in japan.cities.all():
            self.assertIn(city.name, ["Kioto", "Tokio"])
