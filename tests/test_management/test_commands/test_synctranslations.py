from io import StringIO

from django.test import TestCase

from translations.management.commands.synctranslations import Command


class CommandTest(TestCase):
    """Tests for `Command`."""

    def test_execute(self):
        out = StringIO()
        command = Command(stdout=out)
        command.run_from_argv(['manage.py', 'synctranslations'])

        self.assertIs(
            hasattr(command, 'stdin'),
            True
        )

    def test_get_content_types_with_no_app_label(self):
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
