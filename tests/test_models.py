from django.test import TestCase
from django.contrib.contenttypes.models import ContentType
from django.db import utils

from translations.models import Translation

from sample.models import Continent, Country, City


class TranslationTest(TestCase):

    def test_content_type_none(self):
        """Make sure `content_type` can not be null."""
        europe = Continent.objects.create(name="Europe", code="EU")
        with self.assertRaises(utils.IntegrityError) as error:
            Translation.objects.create(
                content_type=None,
                object_id=europe.id,
                field="name",
                language="de",
                text="Europa",
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
                language="de",
                text="Europa",
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
                language="de",
                text="Europa",
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
                language="de",
                text="Europa",
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
                text="Europa",
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
                language="de",
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
            language="de",
            text="Europa"
        )
        self.assertEqual(str(translation), "Europe: Europa")

    def test_uniqueness(self):
        """
        Make sure `content_type`, `object_id`, `field` and `language`
        combination is unique.
        """
        europe = Continent.objects.create(name="Europe", code="EU")
        continent_ct = ContentType.objects.get_for_model(Continent)
        Translation.objects.create(
            content_type=continent_ct,
            object_id=europe.id,
            field="name",
            language="de",
            text="Europa"
        )
        with self.assertRaises(utils.IntegrityError) as error:
            Translation.objects.create(
                content_type=continent_ct,
                object_id=europe.id,
                field="name",
                language="de",
                text="Europa"
            )
        self.assertEqual(
            error.exception.args[0],
            "UNIQUE constraint failed: translations_translation.content_type_id, translations_translation.object_id, translations_translation.field, translations_translation.language",
        )


# class TranslatableTest(TestCase):

#     def test_translations(self):
#         """Make sure `translations` rel works."""
#         europe = Continent.objects.create(name="Europe", code="EU")
#         europe.translations.create(field="name", language="de", text="Europa")
#         self.assertQuerysetEqual(europe.translations.all(), ["<Translation: Europe: Europa>"])

#     def test_two_different_translations(self):
#         """Make sure `translations` for distinct objects are different."""
#         europe = Continent.objects.create(name="Europe", code="EU")
#         europe.translations.create(field="name", language="de", text="Europa")

#         asia = Continent.objects.create(name="Asia", code="AS")
#         asia.translations.create(field="name", language="de", text="Asien")

#         self.assertQuerysetEqual(europe.translations.all(), ["<Translation: Europe: Europa>"])
#         self.assertQuerysetEqual(asia.translations.all(), ["<Translation: Asia: Asien>"])

#     def test_fields(self):
#         """Make sure `TranslatableMeta.fields` works."""
#         self.assertListEqual(Continent.get_translatable_fields(), [Continent._meta.get_field("name")])

#     def test_get_translations_for_object(self):
#         """Make sure `get_translations` works."""
#         europe = Continent.objects.create(name="Europe", code="EU")
#         europe.translations.create(field="name", language="de", text="Europa")
#         self.assertQuerysetEqual(europe.get_translations(lang="de"), ["<Translation: Europe: Europa>"])

#     def test_get_translations_for_two_objects(self):
#         """Make sure `get_translations` works for two distinct objects."""
#         europe = Continent.objects.create(name="Europe", code="EU")
#         europe.translations.create(field="name", language="de", text="Europa")

#         asia = Continent.objects.create(name="Asia")
#         asia.translations.create(field="name", language="de", text="Asien")

#         self.assertQuerysetEqual(europe.get_translations(lang="de"), ["<Translation: Europe: Europa>"])
#         self.assertQuerysetEqual(asia.get_translations(lang="de"), ["<Translation: Asia: Asien>"])

#     def test_get_translations_for_object_and_relations(self):
#         """Make sure `get_translations` works with `relations` argument."""
#         europe = Continent.objects.create(name="Europe", code="EU")
#         europe.translations.create(field="name", language="de", text="Europa")

#         germany = europe.countries.create(name="Germany", code="DE")
#         germany.translations.create(field="name", language="de", text="Deutschland")

#         cologne = germany.cities.create(name="Cologne")
#         cologne.translations.create(field="name", language="de", text="Köln")
#         munich = germany.cities.create(name="Munich")
#         munich.translations.create(field="name", language="de", text="München")

#         self.assertQuerysetEqual(
#             germany.get_translations('continent', 'cities', lang="de").order_by('text'),
#             [
#                 "<Translation: Germany: Deutschland>",
#                 "<Translation: Europe: Europa>",
#                 "<Translation: Cologne: Köln>",
#                 "<Translation: Munich: München>",
#             ]
#         )

#     def test_get_translations_for_two_objects_and_relations(self):
#         """Make sure `get_translations` works with `relations` argument for two distinct objects."""
#         europe = Continent.objects.create(name="Europe", code="EU")
#         europe.translations.create(field="name", language="de", text="Europa")

#         asia = Continent.objects.create(name="Asia", code="AS")
#         asia.translations.create(field="name", language="de", text="Asien")

#         germany = europe.countries.create(name="Germany", code="DE")
#         germany.translations.create(field="name", language="de", text="Deutschland")

#         persia = asia.countries.create(name="Persia", code="IR")
#         persia.translations.create(field="name", language="de", text="Persien")

#         cologne = germany.cities.create(name="Cologne")
#         cologne.translations.create(field="name", language="de", text="Köln")
#         munich = germany.cities.create(name="Munich")
#         munich.translations.create(field="name", language="de", text="München")

#         tehran = persia.cities.create(name="Tehran")
#         tehran.translations.create(field="name", language="de", text="Teheran")
#         shiraz = persia.cities.create(name="Shiraz")
#         shiraz.translations.create(field="name", language="de", text="Schiras")

#         self.assertQuerysetEqual(
#             germany.get_translations('continent', 'cities', lang="de").order_by('text'),
#             [
#                 "<Translation: Germany: Deutschland>",
#                 "<Translation: Europe: Europa>",
#                 "<Translation: Cologne: Köln>",
#                 "<Translation: Munich: München>",
#             ]
#         )

#         self.assertQuerysetEqual(
#             persia.get_translations('continent', 'cities', lang="de").order_by('text'),
#             [
#                 "<Translation: Asia: Asien>",
#                 "<Translation: Persia: Persien>",
#                 "<Translation: Shiraz: Schiras>",
#                 "<Translation: Tehran: Teheran>",
#             ]
#         )

#     def test_translate_for_object(self):
#         """Make sure `translate` works."""
#         europe = Continent.objects.create(name="Europe", code="EU")
#         europe.translations.create(field="name", language="de", text="Europa")
#         europe.translate(lang="de")
#         self.assertEqual(europe.name, "Europa")

#     def test_translate_for_two_objects(self):
#         """Make sure `translate` works for two distinct objects."""
#         europe = Continent.objects.create(name="Europe", code="EU")
#         europe.translations.create(field="name", language="de", text="Europa")

#         asia = Continent.objects.create(name="Asia")
#         asia.translations.create(field="name", language="de", text="Asien")

#         europe.translate(lang="de")
#         asia.translate(lang="de")

#         self.assertEqual(europe.name, "Europa")
#         self.assertEqual(asia.name, "Asien")

#     def test_translate_for_object_and_relations(self):
#         """Make sure `translate` works with `relations` argument."""
#         europe = Continent.objects.create(name="Europe", code="EU")
#         europe.translations.create(field="name", language="de", text="Europa")

#         germany = europe.countries.create(name="Germany", code="DE")
#         germany.translations.create(field="name", language="de", text="Deutschland")

#         cologne = germany.cities.create(name="Cologne")
#         cologne.translations.create(field="name", language="de", text="Köln")
#         munich = germany.cities.create(name="Munich")
#         munich.translations.create(field="name", language="de", text="München")

#         germany.translate("continent", "cities", lang="de")

#         self.assertEqual(germany.name, "Deutschland")
#         self.assertEqual(germany.continent.name, "Europa")
#         for city in germany.cities.all():
#             self.assertIn(city.name, ["Köln", "München"])

#     def test_translate_for_two_objects_and_relations(self):
#         """Make sure `translate` works with `relations` argument for two distinct objects."""
#         europe = Continent.objects.create(name="Europe", code="EU")
#         europe.translations.create(field="name", language="de", text="Europa")

#         asia = Continent.objects.create(name="Asia", code="AS")
#         asia.translations.create(field="name", language="de", text="Asien")

#         germany = europe.countries.create(name="Germany", code="DE")
#         germany.translations.create(field="name", language="de", text="Deutschland")

#         persia = asia.countries.create(name="Persia", code="IR")
#         persia.translations.create(field="name", language="de", text="Persien")

#         cologne = germany.cities.create(name="Cologne")
#         cologne.translations.create(field="name", language="de", text="Köln")
#         munich = germany.cities.create(name="Munich")
#         munich.translations.create(field="name", language="de", text="München")

#         tehran = persia.cities.create(name="Tehran")
#         tehran.translations.create(field="name", language="de", text="Teheran")
#         shiraz = persia.cities.create(name="Shiraz")
#         shiraz.translations.create(field="name", language="de", text="Schiras")

#         germany.translate("continent", "cities", lang="de")
#         persia.translate("continent", "cities", lang="de")

#         self.assertEqual(germany.name, "Deutschland")
#         self.assertEqual(germany.continent.name, "Europa")
#         for city in germany.cities.all():
#             self.assertIn(city.name, ["Köln", "München"])

#         self.assertEqual(persia.name, "Persien")
#         self.assertEqual(persia.continent.name, "Asien")
#         for city in persia.cities.all():
#             self.assertIn(city.name, ["Teheran", "Schiras"])
