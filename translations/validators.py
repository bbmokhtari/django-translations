"""
This module contains the validators for the Translations app.

.. rubric:: Functions:

:func:`validate_language`
    Validate the given language code.

----
"""

from django.core.exceptions import ValidationError
from django.conf import settings


__docformat__ = 'restructuredtext'


def validate_language(lang):
    """
    Validate the given language code.

    :param lang: The language code to validate
    :type lang: str
    :raise ~django.core.exceptions.ValidationError: If the language code is
        not supported in the :data:`~django.conf.settings.LANGUAGES` settings.
    """
    if lang not in [language[0] for language in settings.LANGUAGES]:
        raise ValidationError(
            "The language code `{}` is not supported.".format(lang)
        )
