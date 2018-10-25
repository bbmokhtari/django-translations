"""This module contains the languages for the Translations app."""
from django.utils.translation import get_language
from django.conf import settings


__docformat__ = 'restructuredtext'


_supported_language_cache = {}
_translation_language_choices_cache = {}


def _get_supported_language(lang):
    """Return the `supported language` code of a custom language code."""
    # check cache first
    try:
        return _supported_language_cache[lang]
    except KeyError:
        pass

    code = lang.split('-')[0]

    lang_exists = False
    code_exists = False

    # break when the lang is found but not when the code is found
    # cause the code might come before lang and we may miss an accent
    for language in settings.LANGUAGES:
        if lang == language[0]:
            lang_exists = True
            break
        if code == language[0]:
            code_exists = True

    if lang_exists:
        _supported_language_cache[lang] = lang
    elif code_exists:
        _supported_language_cache[lang] = code
    else:
        raise ValueError(
            'The language code `{}` is not supported.'.format(lang)
        )

    return _supported_language_cache[lang]


def _get_default_language():
    """Return the `supported language` code of the `default language` code."""
    return _get_supported_language(settings.LANGUAGE_CODE)


def _get_active_language():
    """Return the `supported language` code of the `active language` code."""
    return _get_supported_language(get_language())


def _get_preferred_language(lang=None):
    """Return the `supported language` code of a preferred language code."""
    if lang is None:
        return _get_active_language()
    else:
        return _get_supported_language(lang)


def _get_all_languages():
    """Return all the `supported language` codes."""
    return [language[0] for language in settings.LANGUAGES]


def _get_translation_language_choices():
    """Return the `translation language` choices."""
    default = _get_default_language()

    # check cache first
    try:
        return _translation_language_choices_cache[default]
    except KeyError:
        pass

    choices = [
        (None, '---------'),
    ]

    for language in settings.LANGUAGES:
        if language[0] != default:
            choices.append(language)

    _translation_language_choices_cache[default] = choices

    return _translation_language_choices_cache[default]


class _LANGUAGE:

    @property
    def DEFAULT(self):
        return _get_default_language()

    @property
    def ACTIVE(self):
        return _get_active_language()

    @property
    def LOOSE(self):
        return [_get_default_language(), _get_active_language()]

    @property
    def ALL(self):
        return _get_all_languages()

languages = _LANGUAGE
