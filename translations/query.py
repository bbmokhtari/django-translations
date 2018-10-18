from django.db import models
from django.db.models.constants import LOOKUP_SEP

from translations.utils import _get_dissected_lookup


def _get_translations_query_fetcher(model, lang):
    """Return the translations query."""

    def _get_translations_query(*args, **kwargs):
        connector = kwargs.pop('_connector', None)
        negated = kwargs.pop('_negated', False)

        query = models.Q(_connector=connector)
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
                    q = models.Q(**{
                            '{}__field'.format(relation): dissected['field'],
                            '{}__language'.format(relation): lang,
                            '{}__text{}'.format(relation, supplement): child[1]
                        }
                    )
                else:
                    q = models.Q(**{child[0]: child[1]})
            elif isinstance(child, models.Q):
                queries = []
                lookups = []
                for index, nested in enumerate(child.children):
                    if isinstance(nested, models.Q):
                        queries.append(nested)
                    elif isinstance(nested, tuple):
                        lookups.append(nested)
                    else:
                        raise ValueError("Unsupported query {}".format(child))
                q = _get_translations_query(
                    *queries,
                    *lookups,
                    _connector=child.connector,
                    _negated=child.negated
                )

                query = query._combine(q, connector)

        if negated:
            query = ~query

        return query

    return _get_translations_query
