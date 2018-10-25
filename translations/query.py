"""This module contains the query utilities for the Translations app."""
import copy

from django.db.models import Q
from django.db.models.constants import LOOKUP_SEP

from translations.languages import _get_probe_language
from translations.utils import _get_dissected_lookup


__docformat__ = 'restructuredtext'


def _fetch_translations_query_getter(model, lang=None):
    """
    Return the translations query getter specialized for a model and some
    language.
    """
    lang, is_default, is_iter = _get_probe_language(lang)

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
                    if is_iter:
                        query_default = is_default
                        query_languages = lang
                    else:
                        if is_default:
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

    def __init__(self, *args, **kwargs):
        """Initialize a `TQ`."""
        lang = kwargs.pop('_lang', None)
        super(TQ, self).__init__(*args, **kwargs)
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
