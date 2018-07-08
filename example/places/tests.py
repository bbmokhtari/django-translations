from django.test import TestCase
from django.contrib.contenttypes.models import ContentType
from django.db import utils
from translations.models import Translation

from .models import Continent


class ContinentTest(TestCase):

    def test_translation_content_type_empty(self):
        continent = Continent.objects.create(
            name="Europe",
            code="EU",
        )
        with self.assertRaises(utils.IntegrityError) as integrityError:
            Translation.objects.create(
                content_type=None,
                object_id=continent.id,
                field="name",
                language="fr",
                text="L'Europe"
            )
        self.assertEqual(
            integrityError.exception.args[0],
            "NOT NULL constraint failed: translations_translation.content_type_id",
        )
