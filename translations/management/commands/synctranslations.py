import sys

from django.core.management.base import (
    BaseCommand, CommandError, no_translations,
)
from django.apps import apps
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType

from translations.models import Translation, Translatable


class Command(BaseCommand):
    help = 'Synchronize the translations for apps.'

    def add_arguments(self, parser):
        parser.add_argument(
            'args',
            metavar='app_label',
            nargs='*',
            help=(
                'Specify the app label(s) to synchronize the translations for.'
            ),
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

        # get arguments
        self.verbosity = options['verbosity']
        self.interactive = options['interactive']

        # collect all the models which will be affected
        content_types = self.get_content_types(*app_labels)

        # handle obsolete translations
        obsolete_translations = self.get_obsolete_translations(*content_types)
        self.log_obsolete_translations(obsolete_translations)

        # divide initializing synchronization with asking for synchronization
        self.stdout.write('\n')

        # quit if there's nothing to do
        if not obsolete_translations:
            self.stdout.write('Nothing to synchronize.')
            return

        # ask user if they are sure that they want to synchronize
        run_synchronization = self.get_run_synchronization()

        # divide asking for synchronization with actual synchronization
        self.stdout.write('\n')

        if run_synchronization:
            obsolete_translations.delete()
            self.stdout.write(
                self.style.SUCCESS(
                    'Successfully synchronized translations.'
                )
            )
        else:
            self.stdout.write(
                'Cancelled synchronizing translations.'
            )

    def get_content_types(self, *app_labels):
        """Return the content types of some apps or all of them."""
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
        """Return the obsolete translations of some content types."""
        if content_types:
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
            obsolete_translations = Translation.objects.filter(query)
        else:
            obsolete_translations = Translation.objects.none()
        return obsolete_translations

    def log_obsolete_translations(self, obsolete_translations):
        """Log the obsolete translations."""
        if self.verbosity >= 1:
            self.stdout.write('Looking for obsolete translations...')

            if obsolete_translations:
                changes = {}
                for translation in obsolete_translations:
                    app = apps.get_app_config(translation.content_type.app_label)
                    app_name = app.name
                    model = translation.content_type.model_class()
                    model_name = model.__name__

                    changes.setdefault(app_name, {})
                    changes[app_name].setdefault(model_name, set())
                    changes[app_name][model_name].add(translation.field)

                self.stdout.write(
                    'Obsolete translations found for the specified fields:'
                )

                for app_name, models in changes.items():
                    self.stdout.write('- App: {}'.format(app_name))
                    for model_name, fields in models.items():
                        self.stdout.write('  - Model: {}'.format(model_name))
                        for field in fields:
                            self.stdout.write('    - Field: {}'.format(field))
            else:
                self.stdout.write('No obsolete translations found.')

    def get_run_synchronization(self):
        """Return whether to run synchronization or not."""
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
                            'Are you sure you want to synchronize the '
                            'translations? [Y/n] '
                        ),
                        default='Y'
                    )
                except KeyboardInterrupt:
                    run = False
                    self.stderr.write('\n')  # move to the next line of stdin
        else:
            run = True

        return run

    def get_yes_no(self, message, default=None):
        """Ask user for yes or no with a message and a default value."""
        answer = None
        while answer is None:
            raw_value = input(message)

            # default
            if default is not None and raw_value == '':
                raw_value = default

            # yes or no?
            raw_value = raw_value.lower()
            if raw_value in ['y', 'yes', True]:
                answer = True
            elif raw_value in ['n', 'no', False]:
                answer = False
            else:
                answer = None
        return answer
