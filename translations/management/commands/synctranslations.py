"""
This module contains the synctranslations command for the Translations app.
"""

import sys

from django.core.management.base import (
    BaseCommand, CommandError,
)
from django.apps import apps
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType

from translations.models import Translation, Translatable


__docformat__ = 'restructuredtext'


class Command(BaseCommand):
    """
    The command which synchronizes the translations with
    the apps models configurations.
    """

    help = 'Synchronize the translations with the apps models configurations.'

    def execute(self, *args, **options):
        """Execute the `Command` with `BaseCommand` arguments."""
        self.stdin = options.get('stdin', sys.stdin)  # Used for testing
        return super(Command, self).execute(*args, **options)

    def add_arguments(self, parser):
        """
        Add the arguments that the `Command` accepts on an `ArgumentParser`.
        """
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

    def get_content_types(self, *app_labels):
        r"""Return the `ContentType`\ s in some apps or all of them."""
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

    def get_obsolete_translations(self, content_types):
        r"""Return the obsolete translations of some `ContentType`\ s."""
        if content_types:
            query = Q()
            for content_type in content_types:
                model = content_type.model_class()
                if issubclass(model, Translatable):
                    trans_fields = model._get_translatable_fields_names()
                    model_query = (
                        Q(content_type=content_type)
                        &
                        ~Q(field__in=trans_fields)
                    )
                else:
                    model_query = Q(content_type=content_type)
                query |= model_query
            obsolete_translations = Translation.objects.filter(query)
        else:
            obsolete_translations = Translation.objects.none()
        return obsolete_translations

    def log_obsolete_translations(self, obsolete_translations):
        """Log the details of some obsolete translations."""
        if self.verbosity >= 1:
            self.stdout.write('Looking for obsolete translations...')

            if obsolete_translations:
                changes = {}
                for translation in obsolete_translations:
                    app = apps.get_app_config(
                        translation.content_type.app_label
                    )
                    app_name = app.name
                    model = translation.content_type.model_class()
                    model_name = model.__name__

                    changes.setdefault(app_name, {})
                    changes[app_name].setdefault(model_name, set())
                    changes[app_name][model_name].add(translation.field)

                self.stdout.write(
                    'Obsolete translations found for the specified fields:'
                )

                for app_name, models in sorted(
                        changes.items(),
                        key=lambda x: x[0]):
                    self.stdout.write('- App: {}'.format(app_name))
                    for model_name, fields in sorted(
                            models.items(),
                            key=lambda x: x[0]):
                        self.stdout.write('  - Model: {}'.format(model_name))
                        for field in sorted(
                                fields,
                                key=lambda x: x[0]):
                            self.stdout.write('    - Field: {}'.format(field))

                self.stdout.write(
                    self.style.WARNING(
                        'Obsolete translations will be deleted in the '
                        'synchronization process.'
                    )
                )
            else:
                self.stdout.write('No obsolete translations found.')

    def ask_yes_no(self, message, default=None):
        """Ask the user for yes or no with a message and a default value."""
        answer = None
        while answer is None:
            value = input(message)

            # default
            if default is not None and value == '':
                value = default

            # yes or no?
            value = value.lower()
            if value in ['y', 'yes', True]:
                answer = True
            elif value in ['n', 'no', False]:
                answer = False
            else:
                answer = None
        return answer

    def should_run_synchronization(self):
        """Return whether to run the synchronization or not."""
        run = None
        if self.interactive:
            if hasattr(self.stdin, 'isatty') and not self.stdin.isatty():
                self.stderr.write(
                    "Synchronization failed due to not running in a TTY."
                )
                self.stderr.write(
                    "If you are sure about synchronization you can run "
                    "it with the '--no-input' flag."
                )
                sys.exit(1)
            else:
                try:
                    run = self.ask_yes_no(
                        (
                            'Are you sure you want to synchronize the '
                            'translations? [Y/n] '
                        ),
                        default='Y'
                    )
                except KeyboardInterrupt:
                    self.stdout.write('\n')  # move to the next line of stdin
                    self.stdout.write('\n')  # move another line for division
                    self.stderr.write("Operation cancelled.")
                    sys.exit(1)
        else:
            run = True

        return run

    def handle(self, *app_labels, **options):
        """Run the `Command` with the configured arguments."""
        # get arguments
        self.verbosity = options['verbosity']
        self.interactive = options['interactive']

        # collect all the models which will be affected
        content_types = self.get_content_types(*app_labels)

        # handle obsolete translations
        obsolete_translations = self.get_obsolete_translations(content_types)
        self.log_obsolete_translations(obsolete_translations)

        # divide initializing synchronization with asking for synchronization
        self.stdout.write('\n')

        if obsolete_translations:
            # ask user if they are sure that they want to synchronize
            run_synchronization = self.should_run_synchronization()

            # divide asking for synchronization with actual synchronization
            self.stdout.write('\n')

            if run_synchronization:
                obsolete_translations.delete()
            else:
                self.stdout.write(
                    'Synchronization cancelled.'
                )
                return

        self.stdout.write(
            self.style.SUCCESS(
                'Synchronization successful.'
            )
        )
