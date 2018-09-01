import json

from django.http import HttpResponse

from .models import Continent


def get_continent_list(request):
    continents = Continent.objects.all().apply_translations()
    content = json.dumps(list(continents))
    return HttpResponse(content, content_type='application/json')
