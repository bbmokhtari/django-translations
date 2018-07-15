"""
This module contains the validators for the Translations app.

.. rubric:: Functions:

:func:`validate_language`
    Validate the given language code.
:func:`validate_context`
    Validate the given context.
"""

from django.core.exceptions import ValidationError
from django.conf import settings
from django.db import models


__docformat__ = 'restructuredtext'


def validate_language(lang):
    """
    Validate the given language code.

    :param lang: The language code to validate
    :type lang: str
    :raise ~django.core.exceptions.ValidationError: If the language code is
        not included in the :data:`~django.conf.settings.LANGUAGES` settings

    >>> validate_language('de')
    >>> validate_language('xx')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    django.core.exceptions.ValidationError: ['The language code `xx` is not supported.']
    """
    if lang not in [language[0] for language in settings.LANGUAGES]:
        raise ValidationError(
            "The language code `{}` is not supported.".format(lang)
        )


def validate_context(context):
    """
    Validate the given context.

    :param context: The context to validate
    :type context: ~django.db.models.Model or
        ~collections.Iterable(~django.db.models.Model)
    :raise ~django.core.exceptions.ValidationError: If the context is
        neither a model instance nor an iterable of model instances

    >>> continents = Continent.objects.all()
    >>> validate_context(continents)
    >>> eu = Continent.objects.get(code="EU")
    >>> validate_context(eu)
    >>> validate_context([])
    >>> validate_context(123)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    django.core.exceptions.ValidationError: ['`123` is neither a model instance nor an iterable of model instances.']
    """
    error_message = '`{}` is neither {} nor {}.'.format(
        context,
        'a model instance',
        'an iterable of model instances'
    )
    if hasattr(context, '__iter__'):
        if len(context) > 0 and not isinstance(context[0], models.Model):
            raise ValidationError(error_message)
    else:
        if not isinstance(context, models.Model):
            raise ValidationError(error_message)
