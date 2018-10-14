from django.db.models import Q, QuerySet

from translations.models import TranslatableQuerySet


def output(obj):
    return output_any(obj, base='', first=False)

def output_any(obj, base, first):
    if isinstance(obj, dict):
        return output_iter(
            obj, base, first,
            '{', '}', dict_iterator
        )
    elif isinstance(obj, list):
        return output_iter(
            obj, base, first,
            '[', ']', list_iterator
        )
    elif isinstance(obj, Q):
        return output_iter(
            obj, base, first,
            '({}:'.format(obj.connector), ')', q_iterator
        )
    elif isinstance(obj, TranslatableQuerySet):
        return output_iter(
            obj, base, first,
            '<TranslatableQuerySet [', ']>', queryset_iterator
        )
    elif isinstance(obj, QuerySet):
        return output_iter(
            obj, base, first,
            '<QuerySet [', ']>', queryset_iterator
        )
    else:
        return repr(obj)

def dict_iterator(obj, outputter):
    return sorted(['{}: {}'.format(
        outputter(key), outputter(value)) for key, value in obj.items()])

def list_iterator(obj, outputter):
    return [outputter(value) for value in obj]

def q_iterator(obj, outputter):
    return sorted([outputter(value) for value in obj.children])

def queryset_iterator(obj, outputter):
    obj = obj.order_by('pk')
    return [outputter(value) for value in obj]

def output_iter(obj, base, first, opener, closer, iterator):
    result = []

    # opener
    result.append((base + opener) if first else opener)

    # items
    indent = base + (4 * ' ')
    def outputter(value):
        return output_any(value, indent, False)
    for item in iterator(obj, outputter):
        result.append(indent + item + ',')

    # closer
    result.append(base + closer)

    return '\n'.join(result)
