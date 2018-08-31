from django.test import TestCase
from django.contrib.admin import site

from sample.models import Continent, City, Geo
from sample.admin import ContinentAdmin, CityAdmin, GeoAdmin


class TranslatableAdminMixin(TestCase):

    def test_get_translation_choices_none(self):
        admin = CityAdmin(City, site)
        self.assertListEqual(
            admin._get_translation_choices(),
            [(None, '---------'), ('name', 'name'), ('denonym', 'denonym')]
        )

    def test_get_translation_choices_empty(self):
        admin = GeoAdmin(Geo, site)
        self.assertListEqual(
            admin._get_translation_choices(),
            [(None, '---------')]
        )

    def test_get_translation_choices_explicit(self):
        admin = ContinentAdmin(Continent, site)
        self.assertListEqual(
            admin._get_translation_choices(),
            [(None, '---------'), ('name', 'name'), ('denonym', 'denonym')]
        )
