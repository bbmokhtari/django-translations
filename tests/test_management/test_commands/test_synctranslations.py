from io import StringIO
from contextlib import ContextDecorator
from unittest.mock import patch

from django.test import TestCase
from django.core.management import call_command
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

from translations.management.commands.synctranslations import Command
from translations.models import Translation

from sample.models import Continent, Country, City
from sample.utils import create_samples


class PsudeoTTY:
    def isatty(self):
        return True


def get_raiser(error):
    def _raiser(*args, **kwargs):
        raise error
    return _raiser


def override_execute_with_not_tty(self, *args, **options):
    self.stdin = StringIO()
    return super(Command, self).execute(*args, **options)


def override_execute_with_tty(self, *args, **options):
    self.stdin = PsudeoTTY()
    return super(Command, self).execute(*args, **options)


class override_tmeta(ContextDecorator):
    """Override the TranslatableMeta for testing."""

    def __init__(self, model, fields=None):
        self.model = model
        if fields is None:
            self.fields = []
        else:
            self.fields = fields

    def __enter__(self):
        self.old_tmeta = getattr(self.model, 'TranslatableMeta')

        class new_tmeta:
            fields = self.fields

        setattr(self.model, 'TranslatableMeta', new_tmeta)

        if hasattr(self.model, '_cached_translatable_fields'):
            delattr(self.model, '_cached_translatable_fields')
        if hasattr(self.model, '_cached_translatable_fields_names'):
            delattr(self.model, '_cached_translatable_fields_names')

    def __exit__(self, exc_type, exc_value, traceback):
        setattr(self.model, 'TranslatableMeta', self.old_tmeta)

        if hasattr(self.model, '_cached_translatable_fields'):
            delattr(self.model, '_cached_translatable_fields')
        if hasattr(self.model, '_cached_translatable_fields_names'):
            delattr(self.model, '_cached_translatable_fields_names')


class CommandTest(TestCase):
    """Tests for `Command`."""

    def test_execute(self):
        stdout = StringIO()
        command = Command(stdout=stdout)
        command.run_from_argv(['manage.py', 'synctranslations'])

        self.assertIs(
            hasattr(command, 'stdin'),
            True
        )

    def test_get_content_types_no_app_labels(self):
        command = Command()
        content_types = command.get_content_types()

        self.assertListEqual(
            sorted(
                list(content_types.values_list('app_label', 'model')),
                key=lambda x: (x[0], x[1])
            ),
            [
                ('admin', 'logentry'),
                ('auth', 'group'),
                ('auth', 'permission'),
                ('auth', 'user'),
                ('contenttypes', 'contenttype'),
                ('sample', 'city'),
                ('sample', 'continent'),
                ('sample', 'country'),
                ('sample', 'timezone'),
                ('sessions', 'session'),
                ('translations', 'translation'),
            ]
        )

    def test_get_content_types_one_app_label(self):
        command = Command()
        content_types = command.get_content_types('sample')

        self.assertListEqual(
            sorted(
                list(content_types.values_list('app_label', 'model')),
                key=lambda x: (x[0], x[1])
            ),
            [
                ('sample', 'city'),
                ('sample', 'continent'),
                ('sample', 'country'),
                ('sample', 'timezone'),
            ]
        )

    def test_get_content_types_two_app_labels(self):
        command = Command()
        content_types = command.get_content_types('sample', 'translations')

        self.assertListEqual(
            sorted(
                list(content_types.values_list('app_label', 'model')),
                key=lambda x: (x[0], x[1])
            ),
            [
                ('sample', 'city'),
                ('sample', 'continent'),
                ('sample', 'country'),
                ('sample', 'timezone'),
                ('translations', 'translation'),
            ]
        )

    def test_get_content_types_all_app_labels(self):
        command = Command()
        content_types = command.get_content_types(
            'admin', 'auth', 'contenttypes', 'sessions',
            'sample', 'translations'
        )

        self.assertListEqual(
            sorted(
                list(content_types.values_list('app_label', 'model')),
                key=lambda x: (x[0], x[1])
            ),
            [
                ('admin', 'logentry'),
                ('auth', 'group'),
                ('auth', 'permission'),
                ('auth', 'user'),
                ('contenttypes', 'contenttype'),
                ('sample', 'city'),
                ('sample', 'continent'),
                ('sample', 'country'),
                ('sample', 'timezone'),
                ('sessions', 'session'),
                ('translations', 'translation'),
            ]
        )

    def test_get_obsolete_translations_no_content_types_no_fields(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        command = Command()
        obsolete_translations = command.get_obsolete_translations(
            ContentType.objects.none()
        )

        self.assertQuerysetEqual(
            obsolete_translations.order_by('id'),
            []
        )

    def test_get_obsolete_translations_one_content_type_no_fields(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        command = Command()
        obsolete_translations = command.get_obsolete_translations(
            ContentType.objects.get_for_models(Continent).values()
        )

        self.assertQuerysetEqual(
            obsolete_translations.order_by('id'),
            []
        )

    def test_get_obsolete_translations_two_content_types_no_fields(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        command = Command()
        obsolete_translations = command.get_obsolete_translations(
            ContentType.objects.get_for_models(Continent, Country).values()
        )

        self.assertQuerysetEqual(
            obsolete_translations.order_by('id'),
            []
        )

    def test_get_obsolete_translations_all_content_types_no_fields(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        command = Command()
        obsolete_translations = command.get_obsolete_translations(
            ContentType.objects.all()
        )

        self.assertQuerysetEqual(
            obsolete_translations.order_by('id'),
            []
        )

    @override_tmeta(Continent, fields=['name'])
    @override_tmeta(Country, fields=['name'])
    @override_tmeta(City, fields=['name'])
    def test_get_obsolete_translations_no_content_types_one_field(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        command = Command()
        obsolete_translations = command.get_obsolete_translations(
            ContentType.objects.none()
        )

        self.assertQuerysetEqual(
            obsolete_translations.order_by('id'),
            []
        )

    @override_tmeta(Continent, fields=['name'])
    @override_tmeta(Country, fields=['name'])
    @override_tmeta(City, fields=['name'])
    def test_get_obsolete_translations_one_content_type_one_field(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        command = Command()
        obsolete_translations = command.get_obsolete_translations(
            ContentType.objects.get_for_models(Continent).values()
        )

        self.assertQuerysetEqual(
            obsolete_translations.order_by('id'),
            [
                '<Translation: European: Europäisch>',
                '<Translation: European: Avrupalı>',
                '<Translation: Asian: Asiatisch>',
                '<Translation: Asian: Asyalı>'
            ]
        )

    @override_tmeta(Continent, fields=['name'])
    @override_tmeta(Country, fields=['name'])
    @override_tmeta(City, fields=['name'])
    def test_get_obsolete_translations_two_content_types_one_field(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        command = Command()
        obsolete_translations = command.get_obsolete_translations(
            ContentType.objects.get_for_models(Continent, Country).values()
        )

        self.assertQuerysetEqual(
            obsolete_translations.order_by('id'),
            [
                '<Translation: European: Europäisch>',
                '<Translation: European: Avrupalı>',
                '<Translation: German: Deutsche>',
                '<Translation: German: Almanca>',
                '<Translation: Asian: Asiatisch>',
                '<Translation: Asian: Asyalı>',
                '<Translation: South Korean: Südkoreanisch>',
                '<Translation: South Korean: Güney Korelı>'
            ]
        )

    @override_tmeta(Continent, fields=['name'])
    @override_tmeta(Country, fields=['name'])
    @override_tmeta(City, fields=['name'])
    def test_get_obsolete_translations_all_content_types_one_field(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        command = Command()
        obsolete_translations = command.get_obsolete_translations(
            ContentType.objects.all()
        )

        self.assertQuerysetEqual(
            obsolete_translations.order_by('id'),
            [
                '<Translation: European: Europäisch>',
                '<Translation: European: Avrupalı>',
                '<Translation: German: Deutsche>',
                '<Translation: German: Almanca>',
                '<Translation: Cologner: Kölner>',
                '<Translation: Cologner: Kolnlı>',
                '<Translation: Asian: Asiatisch>',
                '<Translation: Asian: Asyalı>',
                '<Translation: South Korean: Südkoreanisch>',
                '<Translation: South Korean: Güney Korelı>',
                '<Translation: Seouler: Seüler>',
                '<Translation: Seouler: Seullı>'
            ]
        )

    @override_tmeta(Continent, fields=[])
    @override_tmeta(Country, fields=[])
    @override_tmeta(City, fields=[])
    def test_get_obsolete_translations_no_content_types_two_fields(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        command = Command()
        obsolete_translations = command.get_obsolete_translations(
            ContentType.objects.none()
        )

        self.assertQuerysetEqual(
            obsolete_translations.order_by('id'),
            []
        )

    @override_tmeta(Continent, fields=[])
    @override_tmeta(Country, fields=[])
    @override_tmeta(City, fields=[])
    def test_get_obsolete_translations_one_content_type_two_fields(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        command = Command()
        obsolete_translations = command.get_obsolete_translations(
            ContentType.objects.get_for_models(Continent).values()
        )

        self.assertQuerysetEqual(
            obsolete_translations.order_by('id'),
            [
                '<Translation: Europe: Europa>',
                '<Translation: European: Europäisch>',
                '<Translation: Europe: Avrupa>',
                '<Translation: European: Avrupalı>',
                '<Translation: Asia: Asien>',
                '<Translation: Asian: Asiatisch>',
                '<Translation: Asia: Asya>',
                '<Translation: Asian: Asyalı>'
            ]
        )

    @override_tmeta(Continent, fields=[])
    @override_tmeta(Country, fields=[])
    @override_tmeta(City, fields=[])
    def test_get_obsolete_translations_two_content_types_two_fields(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        command = Command()
        obsolete_translations = command.get_obsolete_translations(
            ContentType.objects.get_for_models(Continent, Country).values()
        )

        self.assertQuerysetEqual(
            obsolete_translations.order_by('id'),
            [
                '<Translation: Europe: Europa>',
                '<Translation: European: Europäisch>',
                '<Translation: Europe: Avrupa>',
                '<Translation: European: Avrupalı>',
                '<Translation: Germany: Deutschland>',
                '<Translation: German: Deutsche>',
                '<Translation: Germany: Almanya>',
                '<Translation: German: Almanca>',
                '<Translation: Asia: Asien>',
                '<Translation: Asian: Asiatisch>',
                '<Translation: Asia: Asya>',
                '<Translation: Asian: Asyalı>',
                '<Translation: South Korea: Südkorea>',
                '<Translation: South Korean: Südkoreanisch>',
                '<Translation: South Korea: Güney Kore>',
                '<Translation: South Korean: Güney Korelı>'
            ]
        )

    @override_tmeta(Continent, fields=[])
    @override_tmeta(Country, fields=[])
    @override_tmeta(City, fields=[])
    def test_get_obsolete_translations_all_content_types_two_fields(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        command = Command()
        obsolete_translations = command.get_obsolete_translations(
            ContentType.objects.all()
        )

        self.assertQuerysetEqual(
            obsolete_translations.order_by('id'),
            [
                '<Translation: Europe: Europa>',
                '<Translation: European: Europäisch>',
                '<Translation: Europe: Avrupa>',
                '<Translation: European: Avrupalı>',
                '<Translation: Germany: Deutschland>',
                '<Translation: German: Deutsche>',
                '<Translation: Germany: Almanya>',
                '<Translation: German: Almanca>',
                '<Translation: Cologne: Köln>',
                '<Translation: Cologner: Kölner>',
                '<Translation: Cologne: Koln>',
                '<Translation: Cologner: Kolnlı>',
                '<Translation: Asia: Asien>',
                '<Translation: Asian: Asiatisch>',
                '<Translation: Asia: Asya>',
                '<Translation: Asian: Asyalı>',
                '<Translation: South Korea: Südkorea>',
                '<Translation: South Korean: Südkoreanisch>',
                '<Translation: South Korea: Güney Kore>',
                '<Translation: South Korean: Güney Korelı>',
                '<Translation: Seoul: Seül>',
                '<Translation: Seouler: Seüler>',
                '<Translation: Seoul: Seul>',
                '<Translation: Seouler: Seullı>'
            ]
        )

    def test_get_obsolete_translations_one_content_type_not_trans(self):
        user = User.objects.create_user('behzad')

        Translation.objects.create(
            content_object=user,
            field='username',
            language='de',
            text='behzad',
        )

        command = Command()
        obsolete_translations = command.get_obsolete_translations(
            ContentType.objects.get_for_models(User).values()
        )

        self.assertQuerysetEqual(
            obsolete_translations.order_by('id'),
            [
                '<Translation: behzad: behzad>',
            ]
        )

    def test_get_obsolete_translations_all_content_types_not_trans(self):
        user = User.objects.create_user('behzad')

        Translation.objects.create(
            content_object=user,
            field='username',
            language='de',
            text='behzad',
        )

        command = Command()
        obsolete_translations = command.get_obsolete_translations(
            ContentType.objects.all()
        )

        self.assertQuerysetEqual(
            obsolete_translations.order_by('id'),
            [
                '<Translation: behzad: behzad>',
            ]
        )

    def test_log_obsolete_translations_no_content_types_no_fields(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        stdout = StringIO()
        command = Command(stdout=stdout)
        obsolete_translations = command.get_obsolete_translations(
            ContentType.objects.none()
        )
        command.verbosity = 1
        command.log_obsolete_translations(obsolete_translations)

        self.assertEqual(
            stdout.getvalue(),
            'Looking for obsolete translations...\n'
            'No obsolete translations found.\n'
        )

    def test_log_obsolete_translations_one_content_type_no_fields(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        stdout = StringIO()
        command = Command(stdout=stdout)
        obsolete_translations = command.get_obsolete_translations(
            ContentType.objects.get_for_models(Continent).values()
        )
        command.verbosity = 1
        command.log_obsolete_translations(obsolete_translations)

        self.assertEqual(
            stdout.getvalue(),
            'Looking for obsolete translations...\n'
            'No obsolete translations found.\n'
        )

    def test_log_obsolete_translations_two_content_types_no_fields(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        stdout = StringIO()
        command = Command(stdout=stdout)
        obsolete_translations = command.get_obsolete_translations(
            ContentType.objects.get_for_models(Continent, Country).values()
        )
        command.verbosity = 1
        command.log_obsolete_translations(obsolete_translations)

        self.assertEqual(
            stdout.getvalue(),
            'Looking for obsolete translations...\n'
            'No obsolete translations found.\n'
        )

    def test_log_obsolete_translations_all_content_types_no_fields(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        stdout = StringIO()
        command = Command(stdout=stdout)
        obsolete_translations = command.get_obsolete_translations(
            ContentType.objects.all()
        )
        command.verbosity = 1
        command.log_obsolete_translations(obsolete_translations)

        self.assertEqual(
            stdout.getvalue(),
            'Looking for obsolete translations...\n'
            'No obsolete translations found.\n'
        )

    @override_tmeta(Continent, fields=['name'])
    @override_tmeta(Country, fields=['name'])
    @override_tmeta(City, fields=['name'])
    def test_log_obsolete_translations_no_content_types_one_field(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        stdout = StringIO()
        command = Command(stdout=stdout)
        obsolete_translations = command.get_obsolete_translations(
            ContentType.objects.none()
        )
        command.verbosity = 1
        command.log_obsolete_translations(obsolete_translations)

        self.assertEqual(
            stdout.getvalue(),
            'Looking for obsolete translations...\n'
            'No obsolete translations found.\n'
        )

    @override_tmeta(Continent, fields=['name'])
    @override_tmeta(Country, fields=['name'])
    @override_tmeta(City, fields=['name'])
    def test_log_obsolete_translations_one_content_type_one_field(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        stdout = StringIO()
        command = Command(stdout=stdout)
        obsolete_translations = command.get_obsolete_translations(
            ContentType.objects.get_for_models(Continent).values()
        )
        command.verbosity = 1
        command.log_obsolete_translations(obsolete_translations)

        self.assertEqual(
            stdout.getvalue(),
            'Looking for obsolete translations...\n'
            'Obsolete translations found for the specified fields:\n'
            '- App: sample\n'
            '  - Model: Continent\n'
            '    - Field: denonym\n'
            +
            command.style.WARNING(
                'Obsolete translations will be deleted in the '
                'synchronization process.'
            ) + '\n'
        )

    @override_tmeta(Continent, fields=['name'])
    @override_tmeta(Country, fields=['name'])
    @override_tmeta(City, fields=['name'])
    def test_log_obsolete_translations_two_content_types_one_field(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        stdout = StringIO()
        command = Command(stdout=stdout)
        obsolete_translations = command.get_obsolete_translations(
            ContentType.objects.get_for_models(Continent, Country).values()
        )
        command.verbosity = 1
        command.log_obsolete_translations(obsolete_translations)

        self.assertEqual(
            stdout.getvalue(),
            'Looking for obsolete translations...\n'
            'Obsolete translations found for the specified fields:\n'
            '- App: sample\n'
            '  - Model: Continent\n'
            '    - Field: denonym\n'
            '  - Model: Country\n'
            '    - Field: denonym\n'
            +
            command.style.WARNING(
                'Obsolete translations will be deleted in the '
                'synchronization process.'
            ) + '\n'
        )

    @override_tmeta(Continent, fields=['name'])
    @override_tmeta(Country, fields=['name'])
    @override_tmeta(City, fields=['name'])
    def test_log_obsolete_translations_all_content_types_one_field(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        stdout = StringIO()
        command = Command(stdout=stdout)
        obsolete_translations = command.get_obsolete_translations(
            ContentType.objects.all()
        )
        command.verbosity = 1
        command.log_obsolete_translations(obsolete_translations)

        self.assertEqual(
            stdout.getvalue(),
            'Looking for obsolete translations...\n'
            'Obsolete translations found for the specified fields:\n'
            '- App: sample\n'
            '  - Model: City\n'
            '    - Field: denonym\n'
            '  - Model: Continent\n'
            '    - Field: denonym\n'
            '  - Model: Country\n'
            '    - Field: denonym\n'
            +
            command.style.WARNING(
                'Obsolete translations will be deleted in the '
                'synchronization process.'
            ) + '\n'
        )

    @override_tmeta(Continent, fields=[])
    @override_tmeta(Country, fields=[])
    @override_tmeta(City, fields=[])
    def test_log_obsolete_translations_no_content_types_two_fields(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        stdout = StringIO()
        command = Command(stdout=stdout)
        obsolete_translations = command.get_obsolete_translations(
            ContentType.objects.none()
        )
        command.verbosity = 1
        command.log_obsolete_translations(obsolete_translations)

        self.assertEqual(
            stdout.getvalue(),
            'Looking for obsolete translations...\n'
            'No obsolete translations found.\n'
        )

    @override_tmeta(Continent, fields=[])
    @override_tmeta(Country, fields=[])
    @override_tmeta(City, fields=[])
    def test_log_obsolete_translations_one_content_type_two_fields(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        stdout = StringIO()
        command = Command(stdout=stdout)
        obsolete_translations = command.get_obsolete_translations(
            ContentType.objects.get_for_models(Continent).values()
        )
        command.verbosity = 1
        command.log_obsolete_translations(obsolete_translations)

        self.assertEqual(
            stdout.getvalue(),
            'Looking for obsolete translations...\n'
            'Obsolete translations found for the specified fields:\n'
            '- App: sample\n'
            '  - Model: Continent\n'
            '    - Field: denonym\n'
            '    - Field: name\n'
            +
            command.style.WARNING(
                'Obsolete translations will be deleted in the '
                'synchronization process.'
            ) + '\n'
        )

    @override_tmeta(Continent, fields=[])
    @override_tmeta(Country, fields=[])
    @override_tmeta(City, fields=[])
    def test_log_obsolete_translations_two_content_types_two_fields(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        stdout = StringIO()
        command = Command(stdout=stdout)
        obsolete_translations = command.get_obsolete_translations(
            ContentType.objects.get_for_models(Continent, Country).values()
        )
        command.verbosity = 1
        command.log_obsolete_translations(obsolete_translations)

        self.assertEqual(
            stdout.getvalue(),
            'Looking for obsolete translations...\n'
            'Obsolete translations found for the specified fields:\n'
            '- App: sample\n'
            '  - Model: Continent\n'
            '    - Field: denonym\n'
            '    - Field: name\n'
            '  - Model: Country\n'
            '    - Field: denonym\n'
            '    - Field: name\n'
            +
            command.style.WARNING(
                'Obsolete translations will be deleted in the '
                'synchronization process.'
            ) + '\n'
        )

    @override_tmeta(Continent, fields=[])
    @override_tmeta(Country, fields=[])
    @override_tmeta(City, fields=[])
    def test_log_obsolete_translations_all_content_types_two_fields(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        stdout = StringIO()
        command = Command(stdout=stdout)
        obsolete_translations = command.get_obsolete_translations(
            ContentType.objects.all()
        )
        command.verbosity = 1
        command.log_obsolete_translations(obsolete_translations)

        self.assertEqual(
            stdout.getvalue(),
            'Looking for obsolete translations...\n'
            'Obsolete translations found for the specified fields:\n'
            '- App: sample\n'
            '  - Model: City\n'
            '    - Field: denonym\n'
            '    - Field: name\n'
            '  - Model: Continent\n'
            '    - Field: denonym\n'
            '    - Field: name\n'
            '  - Model: Country\n'
            '    - Field: denonym\n'
            '    - Field: name\n'
            +
            command.style.WARNING(
                'Obsolete translations will be deleted in the '
                'synchronization process.'
            ) + '\n'
        )

    def test_log_obsolete_translations_one_content_type_not_trans(self):
        user = User.objects.create_user('behzad')

        Translation.objects.create(
            content_object=user,
            field='username',
            language='de',
            text='behzad',
        )

        stdout = StringIO()
        command = Command(stdout=stdout)
        obsolete_translations = command.get_obsolete_translations(
            ContentType.objects.get_for_models(User).values()
        )
        command.verbosity = 1
        command.log_obsolete_translations(obsolete_translations)

        self.assertEqual(
            stdout.getvalue(),
            'Looking for obsolete translations...\n'
            'Obsolete translations found for the specified fields:\n'
            '- App: django.contrib.auth\n'
            '  - Model: User\n'
            '    - Field: username\n'
            +
            command.style.WARNING(
                'Obsolete translations will be deleted in the '
                'synchronization process.'
            ) + '\n'
        )

    def test_log_obsolete_translations_all_content_types_not_trans(self):
        user = User.objects.create_user('behzad')

        Translation.objects.create(
            content_object=user,
            field='username',
            language='de',
            text='behzad',
        )

        stdout = StringIO()
        command = Command(stdout=stdout)
        obsolete_translations = command.get_obsolete_translations(
            ContentType.objects.all()
        )
        command.verbosity = 1
        command.log_obsolete_translations(obsolete_translations)

        self.assertEqual(
            stdout.getvalue(),
            'Looking for obsolete translations...\n'
            'Obsolete translations found for the specified fields:\n'
            '- App: django.contrib.auth\n'
            '  - Model: User\n'
            '    - Field: username\n'
            +
            command.style.WARNING(
                'Obsolete translations will be deleted in the '
                'synchronization process.'
            ) + '\n'
        )

    @patch('builtins.input', new=lambda *args: 'yes')
    def test_ask_yes_no_input_yes(self):
        command = Command()

        self.assertEqual(
            command.ask_yes_no('message'),
            True
        )

    @patch('builtins.input', new=lambda *args: 'no')
    def test_ask_yes_no_input_no(self):
        command = Command()

        self.assertEqual(
            command.ask_yes_no('message'),
            False
        )

    @patch('builtins.input', new=lambda *args: 'y')
    def test_ask_yes_no_input_y(self):
        command = Command()

        self.assertEqual(
            command.ask_yes_no('message'),
            True
        )

    @patch('builtins.input', new=lambda *args: 'n')
    def test_ask_yes_no_input_n(self):
        command = Command()

        self.assertEqual(
            command.ask_yes_no('message'),
            False
        )

    def test_should_run_synchronization_not_interactive(self):
        command = Command()
        command.interactive = False

        self.assertEqual(
            command.should_run_synchronization(),
            True
        )

    def test_should_run_synchronization_interactive_not_tty(self):
        stdin = StringIO()
        stdout = StringIO()
        stderr = StringIO()
        command = Command(stdout=stdout, stderr=stderr)
        command.interactive = True
        command.stdin = stdin

        with self.assertRaises(SystemExit) as error:
            command.should_run_synchronization()

        self.assertEqual(
            error.exception.code,
            1
        )
        self.assertEqual(
            stderr.getvalue(),
            "Synchronization failed due to not running in a TTY.\n"
            "If you are sure about synchronization you can run "
            "it with the '--no-input' flag.\n"
        )

    @patch(
        'translations.management.commands.synctranslations.Command.ask_yes_no',
        new=lambda *args, **kwargs: True
    )
    def test_should_run_synchronization_interactive_tty_yes(self):
        stdin = PsudeoTTY()
        stdout = StringIO()
        command = Command(stdout=stdout)
        command.interactive = True
        command.stdin = stdin

        self.assertEqual(
            command.should_run_synchronization(),
            True
        )

    @patch(
        'translations.management.commands.synctranslations.Command.ask_yes_no',
        new=lambda *args, **kwargs: False
    )
    def test_should_run_synchronization_interactive_tty_no(self):
        stdin = PsudeoTTY()
        stdout = StringIO()
        command = Command(stdout=stdout)
        command.interactive = True
        command.stdin = stdin

        self.assertEqual(
            command.should_run_synchronization(),
            False
        )

    @patch(
        'translations.management.commands.synctranslations.Command.ask_yes_no',
        new=get_raiser(KeyboardInterrupt)
    )
    def test_should_run_synchronization_interactive_tty_interrupt(self):
        stdin = PsudeoTTY()
        stdout = StringIO()
        stderr = StringIO()
        command = Command(stdout=stdout, stderr=stderr)
        command.interactive = True
        command.stdin = stdin

        with self.assertRaises(SystemExit) as error:
            command.should_run_synchronization()

        self.assertEqual(
            error.exception.code,
            1
        )
        self.assertEqual(
            stderr.getvalue(),
            "Operation cancelled.\n"
        )

    @patch(
        'translations.management.commands.synctranslations.Command.execute',
        new=override_execute_with_not_tty
    )
    def test_handle_no_app_labels_no_fields(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        stdout = StringIO()
        call_command(
            'synctranslations',
            stdout=stdout
        )

        self.assertEqual(
            stdout.getvalue(),
            'Looking for obsolete translations...\n'
            'No obsolete translations found.\n'
            '\n'
            +
            Command().style.SUCCESS(
                'Synchronization successful.'
            ) + '\n'
        )

    @patch(
        'translations.management.commands.synctranslations.Command.execute',
        new=override_execute_with_not_tty
    )
    def test_handle_one_app_label_no_fields(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        stdout = StringIO()
        call_command(
            'synctranslations',
            'sample',
            stdout=stdout
        )

        self.assertEqual(
            stdout.getvalue(),
            'Looking for obsolete translations...\n'
            'No obsolete translations found.\n'
            '\n'
            +
            Command().style.SUCCESS(
                'Synchronization successful.'
            ) + '\n'
        )

    @patch(
        'translations.management.commands.synctranslations.Command.execute',
        new=override_execute_with_not_tty
    )
    def test_handle_two_app_labels_no_fields(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        stdout = StringIO()
        call_command(
            'synctranslations',
            'sample', 'translations',
            stdout=stdout
        )

        self.assertEqual(
            stdout.getvalue(),
            'Looking for obsolete translations...\n'
            'No obsolete translations found.\n'
            '\n'
            +
            Command().style.SUCCESS(
                'Synchronization successful.'
            ) + '\n'
        )

    @patch(
        'translations.management.commands.synctranslations.Command.execute',
        new=override_execute_with_not_tty
    )
    def test_handle_all_app_labels_no_fields(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        stdout = StringIO()
        call_command(
            'synctranslations',
            'admin', 'auth', 'contenttypes', 'sessions',
            'sample', 'translations',
            stdout=stdout
        )

        self.assertEqual(
            stdout.getvalue(),
            'Looking for obsolete translations...\n'
            'No obsolete translations found.\n'
            '\n'
            +
            Command().style.SUCCESS(
                'Synchronization successful.'
            ) + '\n'
        )

    @patch(
        'translations.management.commands.synctranslations.Command.execute',
        new=override_execute_with_tty
    )
    @patch('builtins.input', new=lambda *args: 'y')
    @override_tmeta(Continent, fields=['name'])
    @override_tmeta(Country, fields=['name'])
    @override_tmeta(City, fields=['name'])
    def test_handle_no_app_labels_one_field_input_yes(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        stdout = StringIO()
        call_command(
            'synctranslations',
            stdout=stdout
        )

        self.assertEqual(
            stdout.getvalue(),
            'Looking for obsolete translations...\n'
            'Obsolete translations found for the specified fields:\n'
            '- App: sample\n'
            '  - Model: City\n'
            '    - Field: denonym\n'
            '  - Model: Continent\n'
            '    - Field: denonym\n'
            '  - Model: Country\n'
            '    - Field: denonym\n'
            +
            Command().style.WARNING(
                'Obsolete translations will be deleted in the '
                'synchronization process.'
            ) + '\n'
            '\n'
            '\n'
            +
            Command().style.SUCCESS(
                'Synchronization successful.'
            ) + '\n'
        )

    @patch(
        'translations.management.commands.synctranslations.Command.execute',
        new=override_execute_with_tty
    )
    @patch('builtins.input', new=lambda *args: 'y')
    @override_tmeta(Continent, fields=['name'])
    @override_tmeta(Country, fields=['name'])
    @override_tmeta(City, fields=['name'])
    def test_handle_one_app_label_one_field_input_yes(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        stdout = StringIO()
        call_command(
            'synctranslations',
            'sample',
            stdout=stdout
        )

        self.assertEqual(
            stdout.getvalue(),
            'Looking for obsolete translations...\n'
            'Obsolete translations found for the specified fields:\n'
            '- App: sample\n'
            '  - Model: City\n'
            '    - Field: denonym\n'
            '  - Model: Continent\n'
            '    - Field: denonym\n'
            '  - Model: Country\n'
            '    - Field: denonym\n'
            +
            Command().style.WARNING(
                'Obsolete translations will be deleted in the '
                'synchronization process.'
            ) + '\n'
            '\n'
            '\n'
            +
            Command().style.SUCCESS(
                'Synchronization successful.'
            ) + '\n'
        )

    @patch(
        'translations.management.commands.synctranslations.Command.execute',
        new=override_execute_with_tty
    )
    @patch('builtins.input', new=lambda *args: 'y')
    @override_tmeta(Continent, fields=['name'])
    @override_tmeta(Country, fields=['name'])
    @override_tmeta(City, fields=['name'])
    def test_handle_two_app_labels_one_field_input_yes(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        stdout = StringIO()
        call_command(
            'synctranslations',
            'sample', 'translations',
            stdout=stdout
        )

        self.assertEqual(
            stdout.getvalue(),
            'Looking for obsolete translations...\n'
            'Obsolete translations found for the specified fields:\n'
            '- App: sample\n'
            '  - Model: City\n'
            '    - Field: denonym\n'
            '  - Model: Continent\n'
            '    - Field: denonym\n'
            '  - Model: Country\n'
            '    - Field: denonym\n'
            +
            Command().style.WARNING(
                'Obsolete translations will be deleted in the '
                'synchronization process.'
            ) + '\n'
            '\n'
            '\n'
            +
            Command().style.SUCCESS(
                'Synchronization successful.'
            ) + '\n'
        )

    @patch(
        'translations.management.commands.synctranslations.Command.execute',
        new=override_execute_with_tty
    )
    @patch('builtins.input', new=lambda *args: 'y')
    @override_tmeta(Continent, fields=['name'])
    @override_tmeta(Country, fields=['name'])
    @override_tmeta(City, fields=['name'])
    def test_handle_all_app_labels_one_field_input_yes(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        stdout = StringIO()
        call_command(
            'synctranslations',
            'admin', 'auth', 'contenttypes', 'sessions',
            'sample', 'translations',
            stdout=stdout
        )

        self.assertEqual(
            stdout.getvalue(),
            'Looking for obsolete translations...\n'
            'Obsolete translations found for the specified fields:\n'
            '- App: sample\n'
            '  - Model: City\n'
            '    - Field: denonym\n'
            '  - Model: Continent\n'
            '    - Field: denonym\n'
            '  - Model: Country\n'
            '    - Field: denonym\n'
            +
            Command().style.WARNING(
                'Obsolete translations will be deleted in the '
                'synchronization process.'
            ) + '\n'
            '\n'
            '\n'
            +
            Command().style.SUCCESS(
                'Synchronization successful.'
            ) + '\n'
        )

    @patch(
        'translations.management.commands.synctranslations.Command.execute',
        new=override_execute_with_tty
    )
    @patch('builtins.input', new=lambda *args: 'n')
    @override_tmeta(Continent, fields=['name'])
    @override_tmeta(Country, fields=['name'])
    @override_tmeta(City, fields=['name'])
    def test_handle_no_app_labels_one_field_input_no(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        stdout = StringIO()
        call_command(
            'synctranslations',
            stdout=stdout
        )

        self.assertEqual(
            stdout.getvalue(),
            'Looking for obsolete translations...\n'
            'Obsolete translations found for the specified fields:\n'
            '- App: sample\n'
            '  - Model: City\n'
            '    - Field: denonym\n'
            '  - Model: Continent\n'
            '    - Field: denonym\n'
            '  - Model: Country\n'
            '    - Field: denonym\n'
            +
            Command().style.WARNING(
                'Obsolete translations will be deleted in the '
                'synchronization process.'
            ) + '\n'
            '\n'
            '\n'
            'Synchronization cancelled.\n'
        )

    @patch(
        'translations.management.commands.synctranslations.Command.execute',
        new=override_execute_with_tty
    )
    @patch('builtins.input', new=lambda *args: 'n')
    @override_tmeta(Continent, fields=['name'])
    @override_tmeta(Country, fields=['name'])
    @override_tmeta(City, fields=['name'])
    def test_handle_one_app_label_one_field_input_no(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        stdout = StringIO()
        call_command(
            'synctranslations',
            'sample',
            stdout=stdout
        )

        self.assertEqual(
            stdout.getvalue(),
            'Looking for obsolete translations...\n'
            'Obsolete translations found for the specified fields:\n'
            '- App: sample\n'
            '  - Model: City\n'
            '    - Field: denonym\n'
            '  - Model: Continent\n'
            '    - Field: denonym\n'
            '  - Model: Country\n'
            '    - Field: denonym\n'
            +
            Command().style.WARNING(
                'Obsolete translations will be deleted in the '
                'synchronization process.'
            ) + '\n'
            '\n'
            '\n'
            'Synchronization cancelled.\n'
        )

    @patch(
        'translations.management.commands.synctranslations.Command.execute',
        new=override_execute_with_tty
    )
    @patch('builtins.input', new=lambda *args: 'n')
    @override_tmeta(Continent, fields=['name'])
    @override_tmeta(Country, fields=['name'])
    @override_tmeta(City, fields=['name'])
    def test_handle_two_app_labels_one_field_input_no(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        stdout = StringIO()
        call_command(
            'synctranslations',
            'sample', 'translations',
            stdout=stdout
        )

        self.assertEqual(
            stdout.getvalue(),
            'Looking for obsolete translations...\n'
            'Obsolete translations found for the specified fields:\n'
            '- App: sample\n'
            '  - Model: City\n'
            '    - Field: denonym\n'
            '  - Model: Continent\n'
            '    - Field: denonym\n'
            '  - Model: Country\n'
            '    - Field: denonym\n'
            +
            Command().style.WARNING(
                'Obsolete translations will be deleted in the '
                'synchronization process.'
            ) + '\n'
            '\n'
            '\n'
            'Synchronization cancelled.\n'
        )

    @patch(
        'translations.management.commands.synctranslations.Command.execute',
        new=override_execute_with_tty
    )
    @patch('builtins.input', new=lambda *args: 'n')
    @override_tmeta(Continent, fields=['name'])
    @override_tmeta(Country, fields=['name'])
    @override_tmeta(City, fields=['name'])
    def test_handle_all_app_labels_one_field_input_no(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        stdout = StringIO()
        call_command(
            'synctranslations',
            'admin', 'auth', 'contenttypes', 'sessions',
            'sample', 'translations',
            stdout=stdout
        )

        self.assertEqual(
            stdout.getvalue(),
            'Looking for obsolete translations...\n'
            'Obsolete translations found for the specified fields:\n'
            '- App: sample\n'
            '  - Model: City\n'
            '    - Field: denonym\n'
            '  - Model: Continent\n'
            '    - Field: denonym\n'
            '  - Model: Country\n'
            '    - Field: denonym\n'
            +
            Command().style.WARNING(
                'Obsolete translations will be deleted in the '
                'synchronization process.'
            ) + '\n'
            '\n'
            '\n'
            'Synchronization cancelled.\n'
        )

    @patch(
        'translations.management.commands.synctranslations.Command.execute',
        new=override_execute_with_tty
    )
    @patch(
        'translations.management.commands.synctranslations.Command.ask_yes_no',
        new=get_raiser(KeyboardInterrupt)
    )
    @override_tmeta(Continent, fields=['name'])
    @override_tmeta(Country, fields=['name'])
    @override_tmeta(City, fields=['name'])
    def test_handle_no_app_labels_one_field_input_interrupt(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        stdout = StringIO()
        stderr = StringIO()
        with self.assertRaises(SystemExit) as error:
            call_command(
                'synctranslations',
                stdout=stdout, stderr=stderr
            )

        self.assertEqual(
            error.exception.code,
            1
        )
        self.assertEqual(
            stdout.getvalue(),
            'Looking for obsolete translations...\n'
            'Obsolete translations found for the specified fields:\n'
            '- App: sample\n'
            '  - Model: City\n'
            '    - Field: denonym\n'
            '  - Model: Continent\n'
            '    - Field: denonym\n'
            '  - Model: Country\n'
            '    - Field: denonym\n'
            +
            Command().style.WARNING(
                'Obsolete translations will be deleted in the '
                'synchronization process.'
            ) + '\n'
            '\n'
            '\n'
            '\n'
        )
        self.assertEqual(
            stderr.getvalue(),
            'Operation cancelled.\n'
        )

    @patch(
        'translations.management.commands.synctranslations.Command.execute',
        new=override_execute_with_tty
    )
    @patch(
        'translations.management.commands.synctranslations.Command.ask_yes_no',
        new=get_raiser(KeyboardInterrupt)
    )
    @override_tmeta(Continent, fields=['name'])
    @override_tmeta(Country, fields=['name'])
    @override_tmeta(City, fields=['name'])
    def test_handle_one_app_label_one_field_input_interrupt(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        stdout = StringIO()
        stderr = StringIO()
        with self.assertRaises(SystemExit) as error:
            call_command(
                'synctranslations',
                'sample',
                stdout=stdout, stderr=stderr
            )

        self.assertEqual(
            error.exception.code,
            1
        )
        self.assertEqual(
            stdout.getvalue(),
            'Looking for obsolete translations...\n'
            'Obsolete translations found for the specified fields:\n'
            '- App: sample\n'
            '  - Model: City\n'
            '    - Field: denonym\n'
            '  - Model: Continent\n'
            '    - Field: denonym\n'
            '  - Model: Country\n'
            '    - Field: denonym\n'
            +
            Command().style.WARNING(
                'Obsolete translations will be deleted in the '
                'synchronization process.'
            ) + '\n'
            '\n'
            '\n'
            '\n'
        )
        self.assertEqual(
            stderr.getvalue(),
            'Operation cancelled.\n'
        )

    @patch(
        'translations.management.commands.synctranslations.Command.execute',
        new=override_execute_with_tty
    )
    @patch(
        'translations.management.commands.synctranslations.Command.ask_yes_no',
        new=get_raiser(KeyboardInterrupt)
    )
    @override_tmeta(Continent, fields=['name'])
    @override_tmeta(Country, fields=['name'])
    @override_tmeta(City, fields=['name'])
    def test_handle_two_app_labels_one_field_input_interrupt(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        stdout = StringIO()
        stderr = StringIO()
        with self.assertRaises(SystemExit) as error:
            call_command(
                'synctranslations',
                'sample', 'translations',
                stdout=stdout, stderr=stderr
            )

        self.assertEqual(
            error.exception.code,
            1
        )
        self.assertEqual(
            stdout.getvalue(),
            'Looking for obsolete translations...\n'
            'Obsolete translations found for the specified fields:\n'
            '- App: sample\n'
            '  - Model: City\n'
            '    - Field: denonym\n'
            '  - Model: Continent\n'
            '    - Field: denonym\n'
            '  - Model: Country\n'
            '    - Field: denonym\n'
            +
            Command().style.WARNING(
                'Obsolete translations will be deleted in the '
                'synchronization process.'
            ) + '\n'
            '\n'
            '\n'
            '\n'
        )
        self.assertEqual(
            stderr.getvalue(),
            'Operation cancelled.\n'
        )

    @patch(
        'translations.management.commands.synctranslations.Command.execute',
        new=override_execute_with_tty
    )
    @patch(
        'translations.management.commands.synctranslations.Command.ask_yes_no',
        new=get_raiser(KeyboardInterrupt)
    )
    @override_tmeta(Continent, fields=['name'])
    @override_tmeta(Country, fields=['name'])
    @override_tmeta(City, fields=['name'])
    def test_handle_all_app_labels_one_field_input_interrupt(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        stdout = StringIO()
        stderr = StringIO()
        with self.assertRaises(SystemExit) as error:
            call_command(
                'synctranslations',
                'admin', 'auth', 'contenttypes', 'sessions',
                'sample', 'translations',
                stdout=stdout, stderr=stderr
            )

        self.assertEqual(
            error.exception.code,
            1
        )
        self.assertEqual(
            stdout.getvalue(),
            'Looking for obsolete translations...\n'
            'Obsolete translations found for the specified fields:\n'
            '- App: sample\n'
            '  - Model: City\n'
            '    - Field: denonym\n'
            '  - Model: Continent\n'
            '    - Field: denonym\n'
            '  - Model: Country\n'
            '    - Field: denonym\n'
            +
            Command().style.WARNING(
                'Obsolete translations will be deleted in the '
                'synchronization process.'
            ) + '\n'
            '\n'
            '\n'
            '\n'
        )
        self.assertEqual(
            stderr.getvalue(),
            'Operation cancelled.\n'
        )

    @patch(
        'translations.management.commands.synctranslations.Command.execute',
        new=override_execute_with_not_tty
    )
    @override_tmeta(Continent, fields=['name'])
    @override_tmeta(Country, fields=['name'])
    @override_tmeta(City, fields=['name'])
    def test_handle_no_app_labels_one_field_input_not_tty(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        stdout = StringIO()
        stderr = StringIO()
        with self.assertRaises(SystemExit) as error:
            call_command(
                'synctranslations',
                stdout=stdout, stderr=stderr
            )

        self.assertEqual(
            error.exception.code,
            1
        )
        self.assertEqual(
            stdout.getvalue(),
            'Looking for obsolete translations...\n'
            'Obsolete translations found for the specified fields:\n'
            '- App: sample\n'
            '  - Model: City\n'
            '    - Field: denonym\n'
            '  - Model: Continent\n'
            '    - Field: denonym\n'
            '  - Model: Country\n'
            '    - Field: denonym\n'
            +
            Command().style.WARNING(
                'Obsolete translations will be deleted in the '
                'synchronization process.'
            ) + '\n'
            '\n'
        )
        self.assertEqual(
            stderr.getvalue(),
            "Synchronization failed due to not running in a TTY.\n"
            "If you are sure about synchronization you can run "
            "it with the '--no-input' flag.\n"
        )

    @patch(
        'translations.management.commands.synctranslations.Command.execute',
        new=override_execute_with_not_tty
    )
    @override_tmeta(Continent, fields=['name'])
    @override_tmeta(Country, fields=['name'])
    @override_tmeta(City, fields=['name'])
    def test_handle_one_app_label_one_field_input_not_tty(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        stdout = StringIO()
        stderr = StringIO()
        with self.assertRaises(SystemExit) as error:
            call_command(
                'synctranslations',
                'sample',
                stdout=stdout, stderr=stderr
            )

        self.assertEqual(
            error.exception.code,
            1
        )
        self.assertEqual(
            stdout.getvalue(),
            'Looking for obsolete translations...\n'
            'Obsolete translations found for the specified fields:\n'
            '- App: sample\n'
            '  - Model: City\n'
            '    - Field: denonym\n'
            '  - Model: Continent\n'
            '    - Field: denonym\n'
            '  - Model: Country\n'
            '    - Field: denonym\n'
            +
            Command().style.WARNING(
                'Obsolete translations will be deleted in the '
                'synchronization process.'
            ) + '\n'
            '\n'
        )
        self.assertEqual(
            stderr.getvalue(),
            "Synchronization failed due to not running in a TTY.\n"
            "If you are sure about synchronization you can run "
            "it with the '--no-input' flag.\n"
        )

    @patch(
        'translations.management.commands.synctranslations.Command.execute',
        new=override_execute_with_not_tty
    )
    @override_tmeta(Continent, fields=['name'])
    @override_tmeta(Country, fields=['name'])
    @override_tmeta(City, fields=['name'])
    def test_handle_two_app_labels_one_field_input_not_tty(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        stdout = StringIO()
        stderr = StringIO()
        with self.assertRaises(SystemExit) as error:
            call_command(
                'synctranslations',
                'sample', 'translations',
                stdout=stdout, stderr=stderr
            )

        self.assertEqual(
            error.exception.code,
            1
        )
        self.assertEqual(
            stdout.getvalue(),
            'Looking for obsolete translations...\n'
            'Obsolete translations found for the specified fields:\n'
            '- App: sample\n'
            '  - Model: City\n'
            '    - Field: denonym\n'
            '  - Model: Continent\n'
            '    - Field: denonym\n'
            '  - Model: Country\n'
            '    - Field: denonym\n'
            +
            Command().style.WARNING(
                'Obsolete translations will be deleted in the '
                'synchronization process.'
            ) + '\n'
            '\n'
        )
        self.assertEqual(
            stderr.getvalue(),
            "Synchronization failed due to not running in a TTY.\n"
            "If you are sure about synchronization you can run "
            "it with the '--no-input' flag.\n"
        )

    @patch(
        'translations.management.commands.synctranslations.Command.execute',
        new=override_execute_with_not_tty
    )
    @override_tmeta(Continent, fields=['name'])
    @override_tmeta(Country, fields=['name'])
    @override_tmeta(City, fields=['name'])
    def test_handle_all_app_labels_one_field_input_not_tty(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        stdout = StringIO()
        stderr = StringIO()
        with self.assertRaises(SystemExit) as error:
            call_command(
                'synctranslations',
                'admin', 'auth', 'contenttypes', 'sessions',
                'sample', 'translations',
                stdout=stdout, stderr=stderr
            )

        self.assertEqual(
            error.exception.code,
            1
        )
        self.assertEqual(
            stdout.getvalue(),
            'Looking for obsolete translations...\n'
            'Obsolete translations found for the specified fields:\n'
            '- App: sample\n'
            '  - Model: City\n'
            '    - Field: denonym\n'
            '  - Model: Continent\n'
            '    - Field: denonym\n'
            '  - Model: Country\n'
            '    - Field: denonym\n'
            +
            Command().style.WARNING(
                'Obsolete translations will be deleted in the '
                'synchronization process.'
            ) + '\n'
            '\n'
        )
        self.assertEqual(
            stderr.getvalue(),
            "Synchronization failed due to not running in a TTY.\n"
            "If you are sure about synchronization you can run "
            "it with the '--no-input' flag.\n"
        )

    @patch(
        'translations.management.commands.synctranslations.Command.execute',
        new=override_execute_with_tty
    )
    @patch('builtins.input', new=lambda *args: 'y')
    @override_tmeta(Continent, fields=[])
    @override_tmeta(Country, fields=[])
    @override_tmeta(City, fields=[])
    def test_handle_no_app_labels_two_fields_input_yes(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        stdout = StringIO()
        call_command(
            'synctranslations',
            stdout=stdout
        )

        self.assertEqual(
            stdout.getvalue(),
            'Looking for obsolete translations...\n'
            'Obsolete translations found for the specified fields:\n'
            '- App: sample\n'
            '  - Model: City\n'
            '    - Field: denonym\n'
            '    - Field: name\n'
            '  - Model: Continent\n'
            '    - Field: denonym\n'
            '    - Field: name\n'
            '  - Model: Country\n'
            '    - Field: denonym\n'
            '    - Field: name\n'
            +
            Command().style.WARNING(
                'Obsolete translations will be deleted in the '
                'synchronization process.'
            ) + '\n'
            '\n'
            '\n'
            +
            Command().style.SUCCESS(
                'Synchronization successful.'
            ) + '\n'
        )

    @patch(
        'translations.management.commands.synctranslations.Command.execute',
        new=override_execute_with_tty
    )
    @patch('builtins.input', new=lambda *args: 'y')
    @override_tmeta(Continent, fields=[])
    @override_tmeta(Country, fields=[])
    @override_tmeta(City, fields=[])
    def test_handle_one_app_label_two_fields_input_yes(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        stdout = StringIO()
        call_command(
            'synctranslations',
            'sample',
            stdout=stdout
        )

        self.assertEqual(
            stdout.getvalue(),
            'Looking for obsolete translations...\n'
            'Obsolete translations found for the specified fields:\n'
            '- App: sample\n'
            '  - Model: City\n'
            '    - Field: denonym\n'
            '    - Field: name\n'
            '  - Model: Continent\n'
            '    - Field: denonym\n'
            '    - Field: name\n'
            '  - Model: Country\n'
            '    - Field: denonym\n'
            '    - Field: name\n'
            +
            Command().style.WARNING(
                'Obsolete translations will be deleted in the '
                'synchronization process.'
            ) + '\n'
            '\n'
            '\n'
            +
            Command().style.SUCCESS(
                'Synchronization successful.'
            ) + '\n'
        )

    @patch(
        'translations.management.commands.synctranslations.Command.execute',
        new=override_execute_with_tty
    )
    @patch('builtins.input', new=lambda *args: 'y')
    @override_tmeta(Continent, fields=[])
    @override_tmeta(Country, fields=[])
    @override_tmeta(City, fields=[])
    def test_handle_two_app_labels_two_fields_input_yes(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        stdout = StringIO()
        call_command(
            'synctranslations',
            'sample', 'translations',
            stdout=stdout
        )

        self.assertEqual(
            stdout.getvalue(),
            'Looking for obsolete translations...\n'
            'Obsolete translations found for the specified fields:\n'
            '- App: sample\n'
            '  - Model: City\n'
            '    - Field: denonym\n'
            '    - Field: name\n'
            '  - Model: Continent\n'
            '    - Field: denonym\n'
            '    - Field: name\n'
            '  - Model: Country\n'
            '    - Field: denonym\n'
            '    - Field: name\n'
            +
            Command().style.WARNING(
                'Obsolete translations will be deleted in the '
                'synchronization process.'
            ) + '\n'
            '\n'
            '\n'
            +
            Command().style.SUCCESS(
                'Synchronization successful.'
            ) + '\n'
        )

    @patch(
        'translations.management.commands.synctranslations.Command.execute',
        new=override_execute_with_tty
    )
    @patch('builtins.input', new=lambda *args: 'y')
    @override_tmeta(Continent, fields=[])
    @override_tmeta(Country, fields=[])
    @override_tmeta(City, fields=[])
    def test_handle_all_app_labels_two_fields_input_yes(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        stdout = StringIO()
        call_command(
            'synctranslations',
            'admin', 'auth', 'contenttypes', 'sessions',
            'sample', 'translations',
            stdout=stdout
        )

        self.assertEqual(
            stdout.getvalue(),
            'Looking for obsolete translations...\n'
            'Obsolete translations found for the specified fields:\n'
            '- App: sample\n'
            '  - Model: City\n'
            '    - Field: denonym\n'
            '    - Field: name\n'
            '  - Model: Continent\n'
            '    - Field: denonym\n'
            '    - Field: name\n'
            '  - Model: Country\n'
            '    - Field: denonym\n'
            '    - Field: name\n'
            +
            Command().style.WARNING(
                'Obsolete translations will be deleted in the '
                'synchronization process.'
            ) + '\n'
            '\n'
            '\n'
            +
            Command().style.SUCCESS(
                'Synchronization successful.'
            ) + '\n'
        )

    @patch(
        'translations.management.commands.synctranslations.Command.execute',
        new=override_execute_with_tty
    )
    @patch('builtins.input', new=lambda *args: 'n')
    @override_tmeta(Continent, fields=[])
    @override_tmeta(Country, fields=[])
    @override_tmeta(City, fields=[])
    def test_handle_no_app_labels_two_fields_input_no(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        stdout = StringIO()
        call_command(
            'synctranslations',
            stdout=stdout
        )

        self.assertEqual(
            stdout.getvalue(),
            'Looking for obsolete translations...\n'
            'Obsolete translations found for the specified fields:\n'
            '- App: sample\n'
            '  - Model: City\n'
            '    - Field: denonym\n'
            '    - Field: name\n'
            '  - Model: Continent\n'
            '    - Field: denonym\n'
            '    - Field: name\n'
            '  - Model: Country\n'
            '    - Field: denonym\n'
            '    - Field: name\n'
            +
            Command().style.WARNING(
                'Obsolete translations will be deleted in the '
                'synchronization process.'
            ) + '\n'
            '\n'
            '\n'
            'Synchronization cancelled.\n'
        )

    @patch(
        'translations.management.commands.synctranslations.Command.execute',
        new=override_execute_with_tty
    )
    @patch('builtins.input', new=lambda *args: 'n')
    @override_tmeta(Continent, fields=[])
    @override_tmeta(Country, fields=[])
    @override_tmeta(City, fields=[])
    def test_handle_one_app_label_two_fields_input_no(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        stdout = StringIO()
        call_command(
            'synctranslations',
            'sample',
            stdout=stdout
        )

        self.assertEqual(
            stdout.getvalue(),
            'Looking for obsolete translations...\n'
            'Obsolete translations found for the specified fields:\n'
            '- App: sample\n'
            '  - Model: City\n'
            '    - Field: denonym\n'
            '    - Field: name\n'
            '  - Model: Continent\n'
            '    - Field: denonym\n'
            '    - Field: name\n'
            '  - Model: Country\n'
            '    - Field: denonym\n'
            '    - Field: name\n'
            +
            Command().style.WARNING(
                'Obsolete translations will be deleted in the '
                'synchronization process.'
            ) + '\n'
            '\n'
            '\n'
            'Synchronization cancelled.\n'
        )

    @patch(
        'translations.management.commands.synctranslations.Command.execute',
        new=override_execute_with_tty
    )
    @patch('builtins.input', new=lambda *args: 'n')
    @override_tmeta(Continent, fields=[])
    @override_tmeta(Country, fields=[])
    @override_tmeta(City, fields=[])
    def test_handle_two_app_labels_two_fields_input_no(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        stdout = StringIO()
        call_command(
            'synctranslations',
            'sample', 'translations',
            stdout=stdout
        )

        self.assertEqual(
            stdout.getvalue(),
            'Looking for obsolete translations...\n'
            'Obsolete translations found for the specified fields:\n'
            '- App: sample\n'
            '  - Model: City\n'
            '    - Field: denonym\n'
            '    - Field: name\n'
            '  - Model: Continent\n'
            '    - Field: denonym\n'
            '    - Field: name\n'
            '  - Model: Country\n'
            '    - Field: denonym\n'
            '    - Field: name\n'
            +
            Command().style.WARNING(
                'Obsolete translations will be deleted in the '
                'synchronization process.'
            ) + '\n'
            '\n'
            '\n'
            'Synchronization cancelled.\n'
        )

    @patch(
        'translations.management.commands.synctranslations.Command.execute',
        new=override_execute_with_tty
    )
    @patch('builtins.input', new=lambda *args: 'n')
    @override_tmeta(Continent, fields=[])
    @override_tmeta(Country, fields=[])
    @override_tmeta(City, fields=[])
    def test_handle_all_app_labels_two_fields_input_no(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        stdout = StringIO()
        call_command(
            'synctranslations',
            'admin', 'auth', 'contenttypes', 'sessions',
            'sample', 'translations',
            stdout=stdout
        )

        self.assertEqual(
            stdout.getvalue(),
            'Looking for obsolete translations...\n'
            'Obsolete translations found for the specified fields:\n'
            '- App: sample\n'
            '  - Model: City\n'
            '    - Field: denonym\n'
            '    - Field: name\n'
            '  - Model: Continent\n'
            '    - Field: denonym\n'
            '    - Field: name\n'
            '  - Model: Country\n'
            '    - Field: denonym\n'
            '    - Field: name\n'
            +
            Command().style.WARNING(
                'Obsolete translations will be deleted in the '
                'synchronization process.'
            ) + '\n'
            '\n'
            '\n'
            'Synchronization cancelled.\n'
        )

    @patch(
        'translations.management.commands.synctranslations.Command.execute',
        new=override_execute_with_tty
    )
    @patch(
        'translations.management.commands.synctranslations.Command.ask_yes_no',
        new=get_raiser(KeyboardInterrupt)
    )
    @override_tmeta(Continent, fields=[])
    @override_tmeta(Country, fields=[])
    @override_tmeta(City, fields=[])
    def test_handle_no_app_labels_two_fields_input_interrupt(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        stdout = StringIO()
        stderr = StringIO()
        with self.assertRaises(SystemExit) as error:
            call_command(
                'synctranslations',
                stdout=stdout, stderr=stderr
            )

        self.assertEqual(
            error.exception.code,
            1
        )
        self.assertEqual(
            stdout.getvalue(),
            'Looking for obsolete translations...\n'
            'Obsolete translations found for the specified fields:\n'
            '- App: sample\n'
            '  - Model: City\n'
            '    - Field: denonym\n'
            '    - Field: name\n'
            '  - Model: Continent\n'
            '    - Field: denonym\n'
            '    - Field: name\n'
            '  - Model: Country\n'
            '    - Field: denonym\n'
            '    - Field: name\n'
            +
            Command().style.WARNING(
                'Obsolete translations will be deleted in the '
                'synchronization process.'
            ) + '\n'
            '\n'
            '\n'
            '\n'
        )
        self.assertEqual(
            stderr.getvalue(),
            'Operation cancelled.\n'
        )

    @patch(
        'translations.management.commands.synctranslations.Command.execute',
        new=override_execute_with_tty
    )
    @patch(
        'translations.management.commands.synctranslations.Command.ask_yes_no',
        new=get_raiser(KeyboardInterrupt)
    )
    @override_tmeta(Continent, fields=[])
    @override_tmeta(Country, fields=[])
    @override_tmeta(City, fields=[])
    def test_handle_one_app_label_two_fields_input_interrupt(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        stdout = StringIO()
        stderr = StringIO()
        with self.assertRaises(SystemExit) as error:
            call_command(
                'synctranslations',
                'sample',
                stdout=stdout, stderr=stderr
            )

        self.assertEqual(
            error.exception.code,
            1
        )
        self.assertEqual(
            stdout.getvalue(),
            'Looking for obsolete translations...\n'
            'Obsolete translations found for the specified fields:\n'
            '- App: sample\n'
            '  - Model: City\n'
            '    - Field: denonym\n'
            '    - Field: name\n'
            '  - Model: Continent\n'
            '    - Field: denonym\n'
            '    - Field: name\n'
            '  - Model: Country\n'
            '    - Field: denonym\n'
            '    - Field: name\n'
            +
            Command().style.WARNING(
                'Obsolete translations will be deleted in the '
                'synchronization process.'
            ) + '\n'
            '\n'
            '\n'
            '\n'
        )
        self.assertEqual(
            stderr.getvalue(),
            'Operation cancelled.\n'
        )

    @patch(
        'translations.management.commands.synctranslations.Command.execute',
        new=override_execute_with_tty
    )
    @patch(
        'translations.management.commands.synctranslations.Command.ask_yes_no',
        new=get_raiser(KeyboardInterrupt)
    )
    @override_tmeta(Continent, fields=[])
    @override_tmeta(Country, fields=[])
    @override_tmeta(City, fields=[])
    def test_handle_two_app_labels_two_fields_input_interrupt(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        stdout = StringIO()
        stderr = StringIO()
        with self.assertRaises(SystemExit) as error:
            call_command(
                'synctranslations',
                'sample', 'translations',
                stdout=stdout, stderr=stderr
            )

        self.assertEqual(
            error.exception.code,
            1
        )
        self.assertEqual(
            stdout.getvalue(),
            'Looking for obsolete translations...\n'
            'Obsolete translations found for the specified fields:\n'
            '- App: sample\n'
            '  - Model: City\n'
            '    - Field: denonym\n'
            '    - Field: name\n'
            '  - Model: Continent\n'
            '    - Field: denonym\n'
            '    - Field: name\n'
            '  - Model: Country\n'
            '    - Field: denonym\n'
            '    - Field: name\n'
            +
            Command().style.WARNING(
                'Obsolete translations will be deleted in the '
                'synchronization process.'
            ) + '\n'
            '\n'
            '\n'
            '\n'
        )
        self.assertEqual(
            stderr.getvalue(),
            'Operation cancelled.\n'
        )

    @patch(
        'translations.management.commands.synctranslations.Command.execute',
        new=override_execute_with_tty
    )
    @patch(
        'translations.management.commands.synctranslations.Command.ask_yes_no',
        new=get_raiser(KeyboardInterrupt)
    )
    @override_tmeta(Continent, fields=[])
    @override_tmeta(Country, fields=[])
    @override_tmeta(City, fields=[])
    def test_handle_all_app_labels_two_fields_input_interrupt(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        stdout = StringIO()
        stderr = StringIO()
        with self.assertRaises(SystemExit) as error:
            call_command(
                'synctranslations',
                'admin', 'auth', 'contenttypes', 'sessions',
                'sample', 'translations',
                stdout=stdout, stderr=stderr
            )

        self.assertEqual(
            error.exception.code,
            1
        )
        self.assertEqual(
            stdout.getvalue(),
            'Looking for obsolete translations...\n'
            'Obsolete translations found for the specified fields:\n'
            '- App: sample\n'
            '  - Model: City\n'
            '    - Field: denonym\n'
            '    - Field: name\n'
            '  - Model: Continent\n'
            '    - Field: denonym\n'
            '    - Field: name\n'
            '  - Model: Country\n'
            '    - Field: denonym\n'
            '    - Field: name\n'
            +
            Command().style.WARNING(
                'Obsolete translations will be deleted in the '
                'synchronization process.'
            ) + '\n'
            '\n'
            '\n'
            '\n'
        )
        self.assertEqual(
            stderr.getvalue(),
            'Operation cancelled.\n'
        )

    @patch(
        'translations.management.commands.synctranslations.Command.execute',
        new=override_execute_with_not_tty
    )
    @override_tmeta(Continent, fields=[])
    @override_tmeta(Country, fields=[])
    @override_tmeta(City, fields=[])
    def test_handle_no_app_labels_two_fields_input_not_tty(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        stdout = StringIO()
        stderr = StringIO()
        with self.assertRaises(SystemExit) as error:
            call_command(
                'synctranslations',
                stdout=stdout, stderr=stderr
            )

        self.assertEqual(
            error.exception.code,
            1
        )
        self.assertEqual(
            stdout.getvalue(),
            'Looking for obsolete translations...\n'
            'Obsolete translations found for the specified fields:\n'
            '- App: sample\n'
            '  - Model: City\n'
            '    - Field: denonym\n'
            '    - Field: name\n'
            '  - Model: Continent\n'
            '    - Field: denonym\n'
            '    - Field: name\n'
            '  - Model: Country\n'
            '    - Field: denonym\n'
            '    - Field: name\n'
            +
            Command().style.WARNING(
                'Obsolete translations will be deleted in the '
                'synchronization process.'
            ) + '\n'
            '\n'
        )
        self.assertEqual(
            stderr.getvalue(),
            "Synchronization failed due to not running in a TTY.\n"
            "If you are sure about synchronization you can run "
            "it with the '--no-input' flag.\n"
        )

    @patch(
        'translations.management.commands.synctranslations.Command.execute',
        new=override_execute_with_not_tty
    )
    @override_tmeta(Continent, fields=[])
    @override_tmeta(Country, fields=[])
    @override_tmeta(City, fields=[])
    def test_handle_one_app_label_two_fields_input_not_tty(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        stdout = StringIO()
        stderr = StringIO()
        with self.assertRaises(SystemExit) as error:
            call_command(
                'synctranslations',
                'sample',
                stdout=stdout, stderr=stderr
            )

        self.assertEqual(
            error.exception.code,
            1
        )
        self.assertEqual(
            stdout.getvalue(),
            'Looking for obsolete translations...\n'
            'Obsolete translations found for the specified fields:\n'
            '- App: sample\n'
            '  - Model: City\n'
            '    - Field: denonym\n'
            '    - Field: name\n'
            '  - Model: Continent\n'
            '    - Field: denonym\n'
            '    - Field: name\n'
            '  - Model: Country\n'
            '    - Field: denonym\n'
            '    - Field: name\n'
            +
            Command().style.WARNING(
                'Obsolete translations will be deleted in the '
                'synchronization process.'
            ) + '\n'
            '\n'
        )
        self.assertEqual(
            stderr.getvalue(),
            "Synchronization failed due to not running in a TTY.\n"
            "If you are sure about synchronization you can run "
            "it with the '--no-input' flag.\n"
        )

    @patch(
        'translations.management.commands.synctranslations.Command.execute',
        new=override_execute_with_not_tty
    )
    @override_tmeta(Continent, fields=[])
    @override_tmeta(Country, fields=[])
    @override_tmeta(City, fields=[])
    def test_handle_two_app_labels_two_fields_input_not_tty(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        stdout = StringIO()
        stderr = StringIO()
        with self.assertRaises(SystemExit) as error:
            call_command(
                'synctranslations',
                'sample', 'translations',
                stdout=stdout, stderr=stderr
            )

        self.assertEqual(
            error.exception.code,
            1
        )
        self.assertEqual(
            stdout.getvalue(),
            'Looking for obsolete translations...\n'
            'Obsolete translations found for the specified fields:\n'
            '- App: sample\n'
            '  - Model: City\n'
            '    - Field: denonym\n'
            '    - Field: name\n'
            '  - Model: Continent\n'
            '    - Field: denonym\n'
            '    - Field: name\n'
            '  - Model: Country\n'
            '    - Field: denonym\n'
            '    - Field: name\n'
            +
            Command().style.WARNING(
                'Obsolete translations will be deleted in the '
                'synchronization process.'
            ) + '\n'
            '\n'
        )
        self.assertEqual(
            stderr.getvalue(),
            "Synchronization failed due to not running in a TTY.\n"
            "If you are sure about synchronization you can run "
            "it with the '--no-input' flag.\n"
        )

    @patch(
        'translations.management.commands.synctranslations.Command.execute',
        new=override_execute_with_not_tty
    )
    @override_tmeta(Continent, fields=[])
    @override_tmeta(Country, fields=[])
    @override_tmeta(City, fields=[])
    def test_handle_all_app_labels_two_fields_input_not_tty(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        stdout = StringIO()
        stderr = StringIO()
        with self.assertRaises(SystemExit) as error:
            call_command(
                'synctranslations',
                'admin', 'auth', 'contenttypes', 'sessions',
                'sample', 'translations',
                stdout=stdout, stderr=stderr
            )

        self.assertEqual(
            error.exception.code,
            1
        )
        self.assertEqual(
            stdout.getvalue(),
            'Looking for obsolete translations...\n'
            'Obsolete translations found for the specified fields:\n'
            '- App: sample\n'
            '  - Model: City\n'
            '    - Field: denonym\n'
            '    - Field: name\n'
            '  - Model: Continent\n'
            '    - Field: denonym\n'
            '    - Field: name\n'
            '  - Model: Country\n'
            '    - Field: denonym\n'
            '    - Field: name\n'
            +
            Command().style.WARNING(
                'Obsolete translations will be deleted in the '
                'synchronization process.'
            ) + '\n'
            '\n'
        )
        self.assertEqual(
            stderr.getvalue(),
            "Synchronization failed due to not running in a TTY.\n"
            "If you are sure about synchronization you can run "
            "it with the '--no-input' flag.\n"
        )
