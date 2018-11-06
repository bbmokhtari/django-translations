import json

from django.test import TestCase
from django.urls import reverse

from sample.models import Continent

from sample.utils import create_samples


class GetContinentListTest(TestCase):
    """Tests for `get_continent_list`."""

    def test_fallback(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        continents = Continent.objects.all()
        europe = [x for x in continents if x.code == 'EU'][0]
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]
        asia = [x for x in continents if x.code == 'AS'][0]
        south_korea = asia.countries.all()[0]
        seoul = south_korea.cities.all()[0]

        response = self.client.get(
            reverse('sample:continent_list'),
            HTTP_ACCEPT_LANGUAGE='en'
        )
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(
            json.loads(response.content.decode('utf-8')),
            [
                {
                    'id': europe.id,
                    'code': 'EU',
                    'name': 'Europe',
                    'denonym': 'European',
                    'countries': [
                        {
                            'id': germany.id,
                            'code': 'DE',
                            'name': 'Germany',
                            'denonym': 'German',
                            'cities': [
                                {
                                    'id': cologne.id,
                                    'name': 'Cologne',
                                    'denonym': 'Cologner'
                                }
                            ]
                        }
                    ]
                },
                {
                    'id': asia.id,
                    'code': 'AS',
                    'name': 'Asia',
                    'denonym': 'Asian',
                    'countries': [
                        {
                            'id': south_korea.id,
                            'code': 'KR',
                            'name': 'South Korea',
                            'denonym': 'South Korean',
                            'cities': [
                                {
                                    'id': seoul.id,
                                    'name': 'Seoul',
                                    'denonym': 'Seouler'
                                }
                            ]
                        }
                    ]
                }
            ]
        )

    def test_language(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        continents = Continent.objects.all()
        europe = [x for x in continents if x.code == 'EU'][0]
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]
        asia = [x for x in continents if x.code == 'AS'][0]
        south_korea = asia.countries.all()[0]
        seoul = south_korea.cities.all()[0]

        response = self.client.get(
            reverse('sample:continent_list'),
            HTTP_ACCEPT_LANGUAGE='de'
        )
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(
            json.loads(response.content.decode('utf-8')),
            [
                {
                    'id': europe.id,
                    'code': 'EU',
                    'name': 'Europa',
                    'denonym': 'Europäisch',
                    'countries': [
                        {
                            'id': germany.id,
                            'code': 'DE',
                            'name': 'Deutschland',
                            'denonym': 'Deutsche',
                            'cities': [
                                {
                                    'id': cologne.id,
                                    'name': 'Köln',
                                    'denonym': 'Kölner'
                                }
                            ]
                        }
                    ]
                },
                {
                    'id': asia.id,
                    'code': 'AS',
                    'name': 'Asien',
                    'denonym': 'Asiatisch',
                    'countries': [
                        {
                            'id': south_korea.id,
                            'code': 'KR',
                            'name': 'Südkorea',
                            'denonym': 'Südkoreanisch',
                            'cities': [
                                {
                                    'id': seoul.id,
                                    'name': 'Seül',
                                    'denonym': 'Seüler'
                                }
                            ]
                        }
                    ]
                }
            ]
        )

    def test_accent_not_exists(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        continents = Continent.objects.all()
        europe = [x for x in continents if x.code == 'EU'][0]
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]
        asia = [x for x in continents if x.code == 'AS'][0]
        south_korea = asia.countries.all()[0]
        seoul = south_korea.cities.all()[0]

        response = self.client.get(
            reverse('sample:continent_list'),
            HTTP_ACCEPT_LANGUAGE='de-at'
        )
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(
            json.loads(response.content.decode('utf-8')),
            [
                {
                    'id': europe.id,
                    'code': 'EU',
                    'name': 'Europa',
                    'denonym': 'Europäisch',
                    'countries': [
                        {
                            'id': germany.id,
                            'code': 'DE',
                            'name': 'Deutschland',
                            'denonym': 'Deutsche',
                            'cities': [
                                {
                                    'id': cologne.id,
                                    'name': 'Köln',
                                    'denonym': 'Kölner'
                                }
                            ]
                        }
                    ]
                },
                {
                    'id': asia.id,
                    'code': 'AS',
                    'name': 'Asien',
                    'denonym': 'Asiatisch',
                    'countries': [
                        {
                            'id': south_korea.id,
                            'code': 'KR',
                            'name': 'Südkorea',
                            'denonym': 'Südkoreanisch',
                            'cities': [
                                {
                                    'id': seoul.id,
                                    'name': 'Seül',
                                    'denonym': 'Seüler'
                                }
                            ]
                        }
                    ]
                }
            ]
        )


class GetContinentDetailTest(TestCase):
    """Tests for `get_continent_detail`."""

    def test_fallback(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        europe = Continent.objects.get(code='EU')
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        response = self.client.get(
            reverse('sample:continent_detail', args=(europe.id,)),
            HTTP_ACCEPT_LANGUAGE='en'
        )
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(
            json.loads(response.content.decode('utf-8')),
            {
                'id': europe.id,
                'code': 'EU',
                'name': 'Europe',
                'denonym': 'European',
                'countries': [
                    {
                        'id': germany.id,
                        'code': 'DE',
                        'name': 'Germany',
                        'denonym': 'German',
                        'cities': [
                            {
                                'id': cologne.id,
                                'name': 'Cologne',
                                'denonym': 'Cologner'
                            }
                        ]
                    }
                ]
            }
        )

    def test_language(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        europe = Continent.objects.get(code='EU')
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        response = self.client.get(
            reverse('sample:continent_detail', args=(europe.id,)),
            HTTP_ACCEPT_LANGUAGE='de'
        )
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(
            json.loads(response.content.decode('utf-8')),
            {
                'id': europe.id,
                'code': 'EU',
                'name': 'Europa',
                'denonym': 'Europäisch',
                'countries': [
                    {
                        'id': germany.id,
                        'code': 'DE',
                        'name': 'Deutschland',
                        'denonym': 'Deutsche',
                        'cities': [
                            {
                                'id': cologne.id,
                                'name': 'Köln',
                                'denonym': 'Kölner'
                            }
                        ]
                    }
                ]
            }
        )

    def test_accent_not_exists(self):
        create_samples(
            continent_names=['europe', 'asia'],
            country_names=['germany', 'south korea'],
            city_names=['cologne', 'seoul'],
            continent_fields=['name', 'denonym'],
            country_fields=['name', 'denonym'],
            city_fields=['name', 'denonym'],
            langs=['de', 'tr']
        )

        europe = Continent.objects.get(code='EU')
        germany = europe.countries.all()[0]
        cologne = germany.cities.all()[0]

        response = self.client.get(
            reverse('sample:continent_detail', args=(europe.id,)),
            HTTP_ACCEPT_LANGUAGE='de-at'
        )
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(
            json.loads(response.content.decode('utf-8')),
            {
                'id': europe.id,
                'code': 'EU',
                'name': 'Europa',
                'denonym': 'Europäisch',
                'countries': [
                    {
                        'id': germany.id,
                        'code': 'DE',
                        'name': 'Deutschland',
                        'denonym': 'Deutsche',
                        'cities': [
                            {
                                'id': cologne.id,
                                'name': 'Köln',
                                'denonym': 'Kölner'
                            }
                        ]
                    }
                ]
            }
        )
