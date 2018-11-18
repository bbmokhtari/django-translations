import sys

from django.core.management.base import (
    BaseCommand, CommandError, no_translations,
)
from django.apps import apps
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType

from translations.models import Translation, Translatable


class Command(BaseCommand):
    help = "Synchronize the translations."

    def add_arguments(self, parser):
        parser.add_argument(
            'args',
            metavar='app_label',
            nargs='*',
            help='Specify the app label(s) to synchronize translations for.',
        )
        parser.add_argument(
            '--noinput', '--no-input',
            action='store_false',
            dest='interactive',
            help='Tells Django to NOT prompt the user for input of any kind.',
        )

    def execute(self, *args, **options):
        self.stdin = options.get('stdin', sys.stdin)  # Used for testing
        return super().execute(*args, **options)

    @no_translations
    def handle(self, *app_labels, **options):

        self.verbosity = options['verbosity']
        self.interactive = options['interactive']

        content_types = self.get_content_types(*app_labels)

        obsolete_translations = self.get_obsolete_translations(*content_types)
        self.log_obsolete_translations(obsolete_translations)

        run_synchronization = self.get_run_synchronization()
        if run_synchronization:
            obsolete_translations.delete()
            self.stdout.write(
                self.style.SUCCESS(
                    '\nSuccessfully synchronized translations.'
                )
            )
        else:
            self.stdout.write(
                '\nCancelled synchronizing translations.'
            )

    def get_content_types(self, *app_labels):
        if app_labels:
            query = Q()
            for app_label in app_labels:
                try:
                    apps.get_app_config(app_label)
                except LookupError:
                    raise CommandError(
                        "App '{}' is not found.".format(app_label)
                    )
                else:
                    query |= Q(app_label=app_label)
            content_types = ContentType.objects.filter(query)
        else:
            content_types = ContentType.objects.all()
        return content_types

    def get_obsolete_translations(self, *content_types):
        query = Q()
        for content_type in content_types:
            model = content_type.model_class()
            if issubclass(model, Translatable):
                translatable_fields = model._get_translatable_fields_names()
                model_query = (
                    Q(content_type=content_type)
                    &
                    ~Q(field__in=translatable_fields)
                )
            else:
                model_query = Q(content_type=content_type)
            query |= model_query
        return Translation.objects.filter(query)

    def log_obsolete_translations(self, obsolete_translations):
        if obsolete_translations and self.verbosity >= 1:
            self.stdout.write(
                'The translations for the following fields will be deleted:'
            )

            changes = {}
            for translation in obsolete_translations:
                app = apps.get_app_config(translation.content_type.app_label)
                app_name = app.name
                model = translation.content_type.model_class()
                model_name = model.__name__

                changes.setdefault(app_name, {})
                changes[app_name].setdefault(model_name, set())
                changes[app_name][model_name].add(translation.field)

            for app_name, models in changes.items():
                self.stdout.write('- App: {}'.format(app_name))
                for model_name, fields in models.items():
                    self.stdout.write('  - Model: {}'.format(model_name))
                    for field in sorted(fields):
                        self.stdout.write('    - Field: {}'.format(field))

    def get_run_synchronization(self):
        run = None
        if self.interactive:
            if hasattr(self.stdin, 'isatty') and not self.stdin.isatty():
                run = False
                self.stdout.write(
                    "Synchronizing translations skipped due to not running in "
                    "a TTY. "
                )
            else:
                try:
                    run = self.get_yes_no(
                        (
                            'Are you sure you want to synchronize translations? '
                            '[Y/n] '
                        ),
                        default='Y'
                    )
                except KeyboardInterrupt:
                    self.stderr.write("\nOperation cancelled.")
                    sys.exit(1)
        else:
            run = True

        return run

    def get_yes_no(self, message, default=None):
        if default is not None:
            valid_default = ['y', 'yes', 'n', 'no']
            if str(default).lower() not in valid_default:
                raise ValueError(
                    "default must be one of: {}".format(valid_default))

        answer = None
        while answer is None:
            raw_value = input(message)

            # default
            if default and raw_value == '':
                raw_value = default

            # yes or no?
            raw_value = raw_value.lower()
            if raw_value in ['y', 'yes']:
                answer = True
            elif raw_value in ['n', 'no']:
                answer = False
            else:
                answer = None
        return answer
