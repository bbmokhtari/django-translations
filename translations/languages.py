from translations.utils import _get_default_language, _get_active_language, \
    _get_all_languages


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
