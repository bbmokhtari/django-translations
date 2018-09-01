import json

from django.http import HttpResponse

from .models import Continent


def _get_json(obj, *fields):
    content = {}
    for field in fields:
        content[field] = getattr(obj, field)
    return content


def get_continent_list(request):
    continents = Continent.objects.all().apply_translations()

    content = []
    for continent in continents:
        content.append(_get_json(continent, 'id', 'code', 'name', 'denonym'))

    return HttpResponse(
        json.dumps(content),
        content_type='application/json',
        charset='utf-8'
    )
