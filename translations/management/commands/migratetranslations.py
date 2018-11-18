from django.core.management.base import (
    BaseCommand, CommandError, no_translations,
)
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType

from translations.models import Translation, Translatable


class Command(BaseCommand):
    help = "Updates translations for apps."

    def add_arguments(self, parser):
        parser.add_argument(
            'app_label', nargs='?',
            help='App label of an application to synchronize the state.',
        )
        parser.add_argument(
            '--noinput', '--no-input', action='store_false', dest='interactive',
            help='Tells Django to NOT prompt the user for input of any kind.',
        )

    @no_translations
    def handle(self, *args, **options):
        verbosity = options['verbosity']
        interactive = options['interactive']
        app_label = options['app_label']

        if app_label:
            content_types = ContentType.objects.filter(app_label=app_label)
        else:
            content_types = ContentType.objects.all()

        query = Q()
        for content_type in content_types:
            model = content_type.model_class()
            if issubclass(model, Translatable):
                translatable_fields = model._get_translatable_fields_names()
                new_query = Q(
                    Q(content_type=content_type)
                    &
                    ~Q(field__in=translatable_fields)
                )
                query |= new_query

        self.stdout.write(self.style.NOTICE('query: {}'.format(query)))

        queryset = Translation.objects.filter(query)

        self.stdout.write(self.style.NOTICE('queryset: {}'.format(queryset)))
