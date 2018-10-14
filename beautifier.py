from django.db.models import Q, QuerySet

from translations.models import TranslatableQuerySet


def beautify(obj, representation=True):
    return beautify_any(obj, '', True, representation)

def beautify_any(obj, base, first, representation):
    if isinstance(obj, dict):
        return beautify_iter(
            obj, base, first,
            '{', '}', dict_iterator
        )
    elif isinstance(obj, list):
        return beautify_iter(
            obj, base, first,
            '[', ']', list_iterator
        )
    elif isinstance(obj, Q):
        if representation:
            return beautify_iter(
                obj, base, first,
                '<Q: ({}:'.format(obj.connector), ')>', q_iterator
            )
        else:
            return beautify_iter(
                obj, base, first,
                '({}:'.format(obj.connector), ')', q_iterator
            )
    elif isinstance(obj, TranslatableQuerySet):
        return beautify_iter(
            obj, base, first,
            '<TranslatableQuerySet [', ']>', queryset_iterator
        )
    elif isinstance(obj, QuerySet):
        return beautify_iter(
            obj, base, first,
            '<QuerySet [', ']>', queryset_iterator
        )
    else:
        if representation:
            return repr(obj)
        else:
            return str(obj)

def dict_iterator(obj, beautifier):
    return sorted([
        '{key}: {value}'.format(key=beautifier(key), value=beautifier(value)) \
        for key, value in obj.items()
    ])

def list_iterator(obj, beautifier):
    return [beautifier(value) for value in obj]

def q_iterator(obj, beautifier):
    return sorted([
        beautifier(value, False) \
        if isinstance(value, Q) else beautifier(value) \
        for value in obj.children
    ])

def queryset_iterator(obj, beautifier):
    obj = obj.order_by('pk')
    return [beautifier(value) for value in obj]

def beautify_iter(obj, base, first, opener, closer, iterator):
    result = []

    # opener
    result.append((base + opener) if first else opener)

    # items
    indent = base + (4 * ' ')
    def beautifier(value, representation=True):
        return beautify_any(value, indent, False, representation)
    for item in iterator(obj, beautifier):
        result.append(indent + item + ',')

    # closer
    result.append(base + closer)

    return '\n'.join(result)
