from tests.test_case import TranslationTestCase
from django.contrib.admin import site

from sample.models import Timezone, Continent, City
from sample.admin import TimezoneAdmin, ContinentAdmin, CityAdmin


class MockRequest:
    pass


class MockSuperUser:
    def has_perm(self, perm):
        return True


request = MockRequest()
request.user = MockSuperUser()


class TranslatableAdminMixinTest(TranslationTestCase):
    """Tests for `TranslatableAdminMixin`."""

    def test_prepare_translation_inlines_fields_automatic(self):
        admin = CityAdmin(City, site)
        inlines = admin.get_inline_instances(request, obj=None)
        self.assertListEqual(
            inlines[0].form.base_fields['field'].choices,
            [(None, '---------'), ('name', 'Name'), ('denonym', 'Denonym')]
        )

    def test_prepare_translation_inlines_fields_empty(self):
        admin = TimezoneAdmin(Timezone, site)
        inlines = admin.get_inline_instances(request, obj=None)
        self.assertListEqual(
            inlines,
            []
        )

    def test_prepare_translation_inlines_fields_explicit(self):
        admin = ContinentAdmin(Continent, site)
        inlines = admin.get_inline_instances(request, obj=None)
        self.assertEqual(
            inlines[0].form.base_fields['field'].choices,
            [(None, '---------'), ('name', 'Name'), ('denonym', 'Denonym')]
        )

    def test_prepare_translation_inlines_languages(self):
        admin = ContinentAdmin(City, site)
        inlines = admin.get_inline_instances(request, obj=None)
        self.assertListEqual(
            inlines[0].form.base_fields['language'].choices,
            [
                (None, '---------'),
                ('en-gb', 'English (Great Britain)'),
                ('de', 'German'),
                ('tr', 'Turkish')
            ]
        )
