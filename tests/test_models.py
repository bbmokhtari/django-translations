from django.test import TestCase
from django.contrib.contenttypes.models import ContentType
from django.db import utils

from translations.models import Translation

from sample.models import Continent, Country, City, Geo

from .sample import create_samples


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


class TranslatableTest(TestCase):

    def test_one_translations_rel(self):
        """Make sure `translations` rel works."""
        create_samples(
            continent_names=["europe"],
            continent_fields=["name", "denonym"],
            langs=["de"]
        )

        europe = Continent.objects.get(code='EU')

        self.assertQuerysetEqual(
            europe.translations.all().order_by('id'),
            [
                "<Translation: Europe: Europa>",
                "<Translation: European: Europäisch>",
            ]
        )

    def test_two_translations_rel(self):
        """Make sure `translations` for distinct objects are different."""
        create_samples(
            continent_names=["europe", "asia"],
            continent_fields=["name", "denonym"],
            langs=["de"]
        )

        europe = Continent.objects.get(code='EU')
        asia = Continent.objects.get(code='AS')

        self.assertQuerysetEqual(
            europe.translations.all().order_by('id'),
            [
                "<Translation: Europe: Europa>",
                "<Translation: European: Europäisch>",
            ]
        )
        self.assertQuerysetEqual(
            asia.translations.all().order_by('id'),
            [
                "<Translation: Asia: Asien>",
                "<Translation: Asian: Asiatisch>",
            ]
        )

    def test_fields_none_automatic(self):
        """Make sure `TranslatableMeta.fields` works with ``None``."""
        self.assertListEqual(
            City.get_translatable_fields(),
            [
                City._meta.get_field("name"),
                City._meta.get_field("denonym"),
            ]
        )

    def test_fields_empty(self):
        """Make sure `TranslatableMeta.fields` works with ``None``."""
        self.assertListEqual(
            Geo.get_translatable_fields(),
            []
        )

    def test_fields_explicit(self):
        """Make sure `TranslatableMeta.fields` works with explicit fields."""
        self.assertListEqual(
            Continent.get_translatable_fields(),
            [
                Continent._meta.get_field("name"),
                Continent._meta.get_field("denonym"),
            ]
        )
