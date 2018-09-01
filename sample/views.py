import json

from django.http import HttpResponse
from django.utils.translation import get_language

from .models import Continent


def _get_json(obj, *fields):
    content = {}
    for field in fields:
        content[field] = getattr(obj, field)
    return content


def get_continent_list(request):
    print("LANG: " + get_language())
    continents = Continent.objects.all().apply_translations()

    content = []
    for continent in continents:
        content.append(_get_json(continent, 'id', 'code', 'name', 'denonym'))

    return HttpResponse(
        json.dumps(content),
        content_type='application/json',
        charset='utf-8'
    )
