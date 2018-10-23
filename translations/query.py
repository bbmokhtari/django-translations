"""This module contains the query utilities for the Translations app."""
import copy

from django.db.models import Q
from django.db.models.constants import LOOKUP_SEP

from translations.utils import _get_supported_language, \
    _get_default_language, _get_active_language, _get_preferred_language, \
    _get_all_languages, _get_dissected_lookup


__docformat__ = 'restructuredtext'


def _fetch_translations_query_getter(model, lang):
    """
    Return the translations query getter specialized for a model and some
    language.
    """
    default = _get_default_language()

    def _get_translations_query(*args, **kwargs):
        connector = kwargs.pop('_connector', None)
        negated = kwargs.pop('_negated', False)

        children = list(args) + sorted(kwargs.items())

        for index, child in enumerate(children):
            if isinstance(child, tuple):
                dissected = _get_dissected_lookup(model, child[0])
                if dissected['translatable']:
                    query_default = False
                    query_languages = None
                    if isinstance(lang, str):
                        if lang == default:
                            query_default = True
                            query_languages = None
                        else:
                            query_default = False
                            query_languages = lang
                    elif isinstance(lang, (list, tuple)):
                        query_languages = []
                        for l in lang:
                            if default == l:
                                query_default = True
                            else:
                                query_languages.append(l)
                    else:
                        raise TypeError(
                            '`lang` must be a str or a list of strs.'.format(
                                lang
                            )
                        )

                    q = Q()

                    if query_default:
                        q |= Q(**{child[0]: child[1]})

                    if query_languages:
                        relation = LOOKUP_SEP.join(
                            dissected['relation'] + ['translations'])
                        field_supp = (LOOKUP_SEP + dissected['supplement']) \
                            if dissected['supplement'] else ''
                        lang_supp = (LOOKUP_SEP + 'in') \
                            if isinstance(query_languages, (list, tuple)) else ''

                        q |= Q(**{
                            '{}__field'.format(relation): 
                                dissected['field'],
                            '{}__text{}'.format(relation, field_supp): 
                                child[1],
                            '{}__language{}'.format(relation, lang_supp):
                                query_languages
                        })
                else:
                    q = Q(**{child[0]: child[1]})
            elif isinstance(child, TQ):
                getter = _fetch_translations_query_getter(model, child.lang)
                q = getter(
                    *child.children,
                    _connector=child.connector,
                    _negated=child.negated
                )
            elif isinstance(child, Q):
                q = _get_translations_query(
                    *child.children,
                    _connector=child.connector,
                    _negated=child.negated
                )
            children[index] = q

        query = Q(*children, _connector=connector, _negated=negated)

        return query

    return _get_translations_query


class TQ(Q):
    """
    Encapsulate translation filters as objects that can then be combined
    logically (using `&` and `|`).
    """

    class LANG:
        DEFAULT = 'L:D'
        ACTIVE  = 'L:A'
        LOOSE   = 'L:O'
        ALL     = 'L:L'

    def __init__(self, *args, **kwargs):
        """Initialize a `TQ`."""
        lang = kwargs.pop('_lang', None)
        super(TQ, self).__init__(*args, **kwargs)
        if lang == self.LANG.DEFAULT:
            lang = _get_default_language()
        elif lang == self.LANG.ACTIVE:
            lang = _get_active_language()
        elif lang == self.LANG.LOOSE:
            lang = [_get_default_language(), _get_active_language()]
        elif lang == self.LANG.ALL:
            lang = _get_all_languages()
        elif isinstance(lang, (list, tuple)):
            lang = [_get_supported_language(l) for l in lang]
        else:
            lang = _get_preferred_language(lang)
        self.lang = lang

    def __deepcopy__(self, memodict):
        """Return a copy of the `TQ` object."""
        obj = super(TQ, self).__deepcopy__(memodict)
        obj.lang = self.lang
        return obj

    def _combine(self, other, conn):
        """Return the result of logical combination with another `Q`."""
        if not isinstance(other, Q):
            raise TypeError(other)

        # If the other Q() is empty, ignore it and just use `self`.
        if not other:
            return copy.deepcopy(self)
        # Or if this Q is empty, ignore it and just use `other`.
        elif not self:
            return copy.deepcopy(other)

        obj = Q(self, other, _connector=conn)
        return obj
