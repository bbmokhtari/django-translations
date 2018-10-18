

def _get_translations_query(model, lang):
    """Return the translations query of a query."""

    def _get_lookups(**kwargs):
        connector = kwargs.pop('_connector', None)
        negated = kwargs.pop('_negated', False)

        children = []
        for lookup, value in kwargs.items():
            dissected = _get_dissected_lookup(model, lookup)
            if dissected['translatable']:
                relation = LOOKUP_SEP.join(
                    dissected['relation'] + ['translations'])
                supplement = (LOOKUP_SEP + dissected['supplement']) \
                    if dissected['supplement'] else ''
                children.append(
                    models.Q(**{
                            '{}__field'.format(relation): dissected['field'],
                            '{}__language'.format(relation): lang,
                            '{}__text{}'.format(relation, supplement): value
                        }
                    )
                )
            else:
                children.append((lookup, value))
        return models.Q(
            *children,
            _connector=connector,
            _negated=negated
        )

    def _get_queries(*args, **kwargs):
        connector = kwargs.pop('_connector', None)
        negated = kwargs.pop('_negated', False)

        children = []
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
            children.append(
                _get_lookups_and_queries(
                    *queries,
                    **dict(lookups),
                    _connector=arg.connector,
                    _negated=arg.negated
                )
            )
        return models.Q(
            *children,
            _connector=connector,
            _negated=negated
        )

    def _get_lookups_and_queries(*args, **kwargs):
        connector = kwargs.pop('_connector', None)
        negated = kwargs.pop('_negated', False)

        children = [
            _get_queries(
                *args,
                _connector=connector,
                _negated=negated
            ),
            _get_lookups(
                **kwargs,
                _connector=connector,
                _negated=negated
            )
        ]

        return models.Q(
            *children,
            _connector=connector,
            _negated=negated
        )

    return _get_lookups_and_queries
