from django.db import models
from django.db.models.constants import LOOKUP_SEP

from translations.utils import _get_dissected_lookup


def _get_translations_query(model, lang):
    """Return the translations query."""

    def _get_lookups_and_queries(*args, **kwargs):
        connector = kwargs.pop('_connector', None)
        negated = kwargs.pop('_negated', False)

        query = models.Q(_connector=connector)
        connector = query.connector

        for lookup, value in kwargs.items():
            dissected = _get_dissected_lookup(model, lookup)
            if dissected['translatable']:
                relation = LOOKUP_SEP.join(
                    dissected['relation'] + ['translations'])
                supplement = (LOOKUP_SEP + dissected['supplement']) \
                    if dissected['supplement'] else ''
                q = models.Q(**{
                        '{}__field'.format(relation): dissected['field'],
                        '{}__language'.format(relation): lang,
                        '{}__text{}'.format(relation, supplement): value
                    }
                )
            else:
                q = models.Q(**{lookup: value})

            query = query._combine(q, connector)

        for arg in args:
            queries = []
            lookups = []
            for index, child in enumerate(arg.children):
                if isinstance(child, models.Q):
                    queries.append(child)
                elif isinstance(child, tuple):
                    lookups.append(child)
                else:
                    raise ValueError("Unsupported query {}".format(child))
            q = _get_lookups_and_queries(
                *queries,
                **dict(lookups),
                _connector=arg.connector,
                _negated=arg.negated
            )

            query = query._combine(q, connector)

        if negated:
            query = ~query

        return query

    return _get_lookups_and_queries
