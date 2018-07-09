from django.test import TestCase
from django.contrib.contenttypes.models import ContentType
from django.db import utils
from translations.models import Translation

from .models import Continent


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
        continent = Continent.objects.create(name="Europe", code="EU")
        continent.translations.create(field="name", language="fr", text="L'Europe")
        self.assertQuerysetEqual(continent.translations.all(), ["<Translation: Europe: L'Europe>"])
