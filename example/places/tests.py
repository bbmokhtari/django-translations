from django.test import TestCase
from django.contrib.contenttypes.models import ContentType
from django.db import utils
from translations.models import Translation

from .models import Continent


class ContinentTest(TestCase):

    def create_continent(self):
        continent = Continent.objects.create(
            name="Europe",
            code="EU",
        )
        return continent

    def test_translation_content_type_none(self):
        continent = self.create_continent()
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

    def test_translation_object_id_none(self):
        continent = self.create_continent()
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
