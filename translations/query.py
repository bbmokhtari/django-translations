"""This module contains the query utilities for the Translations app."""

import copy

from django.db.models import Q
from django.db.models.constants import LOOKUP_SEP

from translations.languages import _get_default_language, _get_probe_language
from translations.utils import _get_dissected_lookup


__docformat__ = 'restructuredtext'


def _fetch_translations_query_getter(model, lang):
    """
    Return the translations query getter specialized for a model and some
    language(s).
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
                    if isinstance(lang, (list, tuple)):
                        query_languages = []
                        for x in lang:
                            if x == default:
                                query_default = True
                            else:
                                query_languages.append(x)
                    else:
                        if lang == default:
                            query_default = True
                            query_languages = None
                        else:
                            query_default = False
                            query_languages = lang

                    q = Q()

                    if query_default:
                        q |= Q(**{child[0]: child[1]})

                    if query_languages:
                        relation = LOOKUP_SEP.join(
                            dissected['relation'] + ['translations'])
                        field_supp = (LOOKUP_SEP + dissected['supplement']) \
                            if dissected['supplement'] else ''
                        lang_supp = (LOOKUP_SEP + 'in') \
                            if isinstance(query_languages, (list, tuple)) \
                            else ''

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
                if child.lang:
                    getter = _fetch_translations_query_getter(
                        model,
                        child.lang
                    )
                    q = getter(
                        *child.children,
                        _connector=child.connector,
                        _negated=child.negated
                    )
                else:
                    q = _get_translations_query(
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
    Encapsulate translation queries as objects that can then be combined
    logically (using `&` and `|`).
    """

    def __init__(self, *args, **kwargs):
        """Initialize a `TQ` with `Q` arguments."""
        super(TQ, self).__init__(*args, **kwargs)
        self.lang = None

    def __deepcopy__(self, memodict):
        """Return a copy of the `TQ` object."""
        obj = super(TQ, self).__deepcopy__(memodict)
        obj.lang = self.lang
        return obj

    def __call__(self, lang=None):
        """Specialize the `TQ` for some language(s)."""
        obj = copy.deepcopy(self)
        obj.lang = _get_probe_language(lang)
        return obj

    def _combine(self, other, conn):
        """Return the result of logical combination with another `Q` object."""
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
