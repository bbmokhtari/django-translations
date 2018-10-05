import json

from django.http import HttpResponse

from translations.context import Context

from .models import Continent


def _get_json(obj, *fields):
    content = {}
    for field in fields:
        content[field] = getattr(obj, field)
    return content


def get_continent_list(request):
    relations = ('countries', 'countries__cities',)

    continents = Continent.objects.prefetch_related(*relations)

    with Context(continents, *relations) as translations:
        translations.read()

        continent_list = []
        for continent in continents:
            continent_detail = _get_json(
                continent, 'id', 'code', 'name', 'denonym')
            country_list = []
            for country in continent.countries.all():
                country_detail = _get_json(
                    country, 'id', 'code', 'name', 'denonym')
                city_list = []
                for city in country.cities.all():
                    city_detail = _get_json(
                        city, 'id', 'name', 'denonym')
                    city_list.append(city_detail)
                country_detail['cities'] = city_list
                country_list.append(country_detail)
            continent_detail['countries'] = country_list
            continent_list.append(continent_detail)

        return HttpResponse(
            json.dumps(continent_list),
            content_type='application/json',
            charset='utf-8'
        )


def get_continent_detail(request, pk):
    relations = ('countries', 'countries__cities',)

    continent = Continent.objects.prefetch_related(*relations).get(id=pk)

    with Context(continent, *relations) as translations:
        translations.read()

        continent_detail = _get_json(
            continent, 'id', 'code', 'name', 'denonym')
        country_list = []
        for country in continent.countries.all():
            country_detail = _get_json(
                country, 'id', 'code', 'name', 'denonym')
            city_list = []
            for city in country.cities.all():
                city_detail = _get_json(
                    city, 'id', 'name', 'denonym')
                city_list.append(city_detail)
            country_detail['cities'] = city_list
            country_list.append(country_detail)
        continent_detail['countries'] = country_list

        return HttpResponse(
            json.dumps(continent_detail),
            content_type='application/json',
            charset='utf-8'
        )
