from translations.utils import _get_supported_language, \
    _get_default_language, _get_active_language, _get_preferred_language, \
    _get_all_languages


DEFAULT = 'L:D'
ACTIVE  = 'L:A'
LOOSE   = 'L:O'
ALL     = 'L:L'


def _get_lang_intention(lang):
    if lang == DEFAULT:
        lang = _get_default_language()
    elif lang == ACTIVE:
        lang = _get_active_language()
    elif lang == LOOSE:
        lang = [_get_default_language(), _get_active_language()]
    elif lang == ALL:
        lang = _get_all_languages()
    elif isinstance(lang, (list, tuple)):
        lang = [_get_supported_language(l) for l in lang]
    else:
        lang = _get_preferred_language(lang)
    return lang
