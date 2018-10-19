from django.db.models import Q
from django.db.models.constants import LOOKUP_SEP

from translations.utils import _get_standard_language, _get_default_language, \
    _get_dissected_lookup


def _fetch_translations_query_getter(model, lang):
    """
    Return the translations query getter specialized for a model and some
    language.
    """
    default = _get_default_language()

    def _get_translations_query(*args, **kwargs):
        connector = kwargs.pop('_connector', None)
        negated = kwargs.pop('_negated', False)

        query = Q(_connector=connector)
        connector = query.connector  # let default connector to be set in Q

        children = list(args) + sorted(kwargs.items())

        for child in children:
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
                query = query._combine(q, connector)
            elif isinstance(child, TQ):
                getter = _fetch_translations_query_getter(model, child.lang)
                q = getter(
                    *child.children,
                    _connector=child.connector,
                    _negated=child.negated
                )

                query = query._combine(q, connector)
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
        if isinstance(lang, (list, tuple)):
            self.lang = [_get_standard_language(l) for l in lang]
        else:
            self.lang = _get_standard_language(lang)

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
