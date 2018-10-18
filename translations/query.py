from django.db.models import Q
from django.db.models.constants import LOOKUP_SEP

from translations.utils import _get_dissected_lookup


def _get_translations_query_fetcher(model, lang):
    """Return the translations query."""

    def _get_translations_query(*args, **kwargs):
        connector = kwargs.pop('_connector', None)
        negated = kwargs.pop('_negated', False)

        query = Q(_connector=connector)
        connector = query.connector

        children = list(args) + sorted(kwargs.items())

        for child in children:
            if isinstance(child, tuple):
                dissected = _get_dissected_lookup(model, child[0])
                if dissected['translatable']:
                    relation = LOOKUP_SEP.join(
                        dissected['relation'] + ['translations'])
                    supplement = (LOOKUP_SEP + dissected['supplement']) \
                        if dissected['supplement'] else ''
                    q = Q(**{
                            '{}__field'.format(relation): dissected['field'],
                            '{}__language'.format(relation): lang,
                            '{}__text{}'.format(relation, supplement): child[1]
                        }
                    )
                else:
                    q = Q(**{child[0]: child[1]})
            elif isinstance(child, Q):
                q = _get_translations_query(
                    *child.children,
                    _connector=child.connector,
                    _negated=child.negated
                )

                query = query._combine(q, connector)

        if negated:
            query = ~query

        return query

    return _get_translations_query


class TQ(Q):

    def __init__(self, *args, **kwargs):
        lang = kwargs.pop('_lang', None)
        super(TQ, self).__init__(*args, **kwargs)
        self.lang = lang

    def __deepcopy__(self, memodict):
        obj = super(TQ, self).__deepcopy__(memodict)
        obj.lang = self.lang
        return obj

    def _combine(self, other, conn):
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
