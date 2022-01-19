from django.test import TestCase
from django.contrib.contenttypes.models import ContentType
from django.db import connection, utils

from translations.models import Translation

from sample.models import Timezone, Continent, City
from sample.utils import create_samples


class TranslationTest(TestCase):
    """Tests for `Translation`."""

    def setUp(self):
        self._integrity_error_not_null = {
            "postgresql": ('null value in column "{field}" of relation ' +
                           '"{table}" violates not-null constraint'),
            "sqlite": "NOT NULL constraint_failed: {table}.{field}",
        }.get(connection.vendor)
        self._integrity_error_unique = {
            "postgresql": ('duplicate key value violates unique constraint ' +
                           '"{table}_content_type_id_object_i_82ea2ee3_uniq"'),
            "sqlite": ('UNIQUE constraint failed: {table}.content_type_id, ' +
                       '{table}.object_id, {table}.field, {table}.language'),
        }.get(connection.vendor)

    def test_content_type_none(self):
        europe = Continent.objects.create(name='Europe', code='EU')

        with self.assertRaises(utils.IntegrityError) as error:
            Translation.objects.create(
                content_type=None,
                object_id=europe.pk,
                field='name',
                language='de',
                text='Europa',
            )

        self.assertEqual(
            error.exception.args[0].split("\n")[0],
            self._integrity_error_not_null.format(
                table="translations_translation",
                field="content_type_id",
            ),
        )

    def test_object_id_none(self):
        continent_ct = ContentType.objects.get_for_model(Continent)

        with self.assertRaises(utils.IntegrityError) as error:
            Translation.objects.create(
                content_type=continent_ct,
                object_id=None,
                field='name',
                language='de',
                text='Europa',
            )

        self.assertEqual(
            error.exception.args[0].split("\n")[0],
            self._integrity_error_not_null.format(
                table="translations_translation",
                field="object_id",
            ),
        )

    def test_content_object_none(self):
        with self.assertRaises(utils.IntegrityError) as error:
            Translation.objects.create(
                content_object=None,
                field='name',
                language='de',
                text='Europa',
            )

        self.assertEqual(
            error.exception.args[0].split("\n")[0],
            self._integrity_error_not_null.format(
                table="translations_translation",
                field="object_id",
            ),
        )

    def test_field_none(self):
        europe = Continent.objects.create(name='Europe', code='EU')
        continent_ct = ContentType.objects.get_for_model(Continent)

        with self.assertRaises(utils.IntegrityError) as error:
            Translation.objects.create(
                content_type=continent_ct,
                object_id=europe.pk,
                field=None,
                language='de',
                text='Europa',
            )

        self.assertEqual(
            error.exception.args[0].split("\n")[0],
            self._integrity_error_not_null.format(
                table="translations_translation",
                field="field",
            ),
        )

    def test_language_none(self):
        europe = Continent.objects.create(name='Europe', code='EU')
        continent_ct = ContentType.objects.get_for_model(Continent)

        with self.assertRaises(utils.IntegrityError) as error:
            Translation.objects.create(
                content_type=continent_ct,
                object_id=europe.pk,
                field='name',
                language=None,
                text='Europa',
            )

        self.assertEqual(
            error.exception.args[0].split("\n")[0],
            self._integrity_error_not_null.format(
                table="translations_translation",
                field="language",
            ),
        )

    def test_text_none(self):
        europe = Continent.objects.create(name='Europe', code='EU')
        continent_ct = ContentType.objects.get_for_model(Continent)

        with self.assertRaises(utils.IntegrityError) as error:
            Translation.objects.create(
                content_type=continent_ct,
                object_id=europe.pk,
                field='name',
                language='de',
                text=None,
            )

        self.assertEqual(
            error.exception.args[0].split("\n")[0],
            self._integrity_error_not_null.format(
                table="translations_translation",
                field="text",
            ),
        )

    def test_str(self):
        europe = Continent.objects.create(name='Europe', code='EU')
        continent_ct = ContentType.objects.get_for_model(Continent)
        translation = Translation.objects.create(
            content_type=continent_ct,
            object_id=europe.pk,
            field='name',
            language='de',
            text='Europa'
        )

        self.assertEqual(
            str(translation),
            'Europe: Europa'
        )

    def test_uniqueness(self):
        europe = Continent.objects.create(name='Europe', code='EU')
        continent_ct = ContentType.objects.get_for_model(Continent)
        Translation.objects.create(
            content_type=continent_ct,
            object_id=europe.pk,
            field='name',
            language='de',
            text='Europa'
        )

        with self.assertRaises(utils.IntegrityError) as error:
            Translation.objects.create(
                content_type=continent_ct,
                object_id=europe.pk,
                field='name',
                language='de',
                text='Europa'
            )

        self.assertEqual(
            error.exception.args[0].split("\n")[0],
            self._integrity_error_unique.format(
                table="translations_translation",
            ),
        )


class TranslatableTest(TestCase):
    """Tests for `Translatable`."""

    def test_one_translations_rel(self):
        create_samples(
            continent_names=['europe'],
            continent_fields=['name', 'denonym'],
            langs=['de']
        )

        europe = Continent.objects.get(code='EU')

        self.assertQuerysetEqual(
            europe.translations.order_by('id'),
            [
                '<Translation: Europe: Europa>',
                '<Translation: European: Europäisch>',
            ]
        )

    def test_two_translations_rel(self):
        create_samples(
            continent_names=['europe', 'asia'],
            continent_fields=['name', 'denonym'],
            langs=['de']
        )

        europe = Continent.objects.get(code='EU')
        asia = Continent.objects.get(code='AS')

        self.assertQuerysetEqual(
            europe.translations.order_by('id'),
            [
                '<Translation: Europe: Europa>',
                '<Translation: European: Europäisch>',
            ]
        )
        self.assertQuerysetEqual(
            asia.translations.order_by('id'),
            [
                '<Translation: Asia: Asien>',
                '<Translation: Asian: Asiatisch>',
            ]
        )

    def test_get_translatable_fields_automatic(self):
        self.assertListEqual(
            City.get_translatable_fields(),
            [
                City._meta.get_field('name'),
                City._meta.get_field('denonym'),
            ]
        )

    def test_get_translatable_fields_empty(self):
        self.assertListEqual(
            Timezone.get_translatable_fields(),
            []
        )

    def test_get_translatable_fields_explicit(self):
        self.assertListEqual(
            Continent.get_translatable_fields(),
            [
                Continent._meta.get_field('name'),
                Continent._meta.get_field('denonym'),
            ]
        )

    def test_get_translatable_fields_names_automatic(self):
        self.assertListEqual(
            City._get_translatable_fields_names(),
            ['name', 'denonym']
        )

    def test_get_translatable_fields_names_empty(self):
        self.assertListEqual(
            Timezone._get_translatable_fields_names(),
            []
        )

    def test_get_translatable_fields_names_explicit(self):
        self.assertListEqual(
            Continent._get_translatable_fields_names(),
            ['name', 'denonym']
        )

    def test_get_translatable_fields_choices_automatic(self):
        self.assertListEqual(
            City._get_translatable_fields_choices(),
            [(None, '---------'), ('name', 'Name'), ('denonym', 'Denonym')]
        )

    def test_get_translatable_fields_choices_empty(self):
        self.assertListEqual(
            Timezone._get_translatable_fields_choices(),
            [(None, '---------')]
        )

    def test_get_translatable_fields_choices_explicit(self):
        self.assertListEqual(
            Continent._get_translatable_fields_choices(),
            [(None, '---------'), ('name', 'Name'), ('denonym', 'Denonym')]
        )
