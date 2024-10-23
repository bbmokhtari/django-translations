import json

from tests.test_case import TranslationTestCase
from django.urls import reverse

from sample.models import Continent
from sample.utils import create_samples


class GetContinentListTest(TranslationTestCase):
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
                    'code': 'AS',
                    'name': 'Asia',
                    'denonym': 'Asian',
                    'countries': [
                        {
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
                },
                {
                    'code': 'EU',
                    'name': 'Europe',
                    'denonym': 'European',
                    'countries': [
                        {
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
                    'code': 'AS',
                    'name': 'Asien',
                    'denonym': 'Asiatisch',
                    'countries': [
                        {
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
                },
                {
                    'code': 'EU',
                    'name': 'Europa',
                    'denonym': 'Europäisch',
                    'countries': [
                        {
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
                    'code': 'AS',
                    'name': 'Asien',
                    'denonym': 'Asiatisch',
                    'countries': [
                        {
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
                },
                {
                    'code': 'EU',
                    'name': 'Europa',
                    'denonym': 'Europäisch',
                    'countries': [
                        {
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
            ]
        )


class GetContinentDetailTest(TranslationTestCase):
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
            reverse('sample:continent_detail', args=(europe.pk,)),
            HTTP_ACCEPT_LANGUAGE='en'
        )
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(
            json.loads(response.content.decode('utf-8')),
            {
                'code': 'EU',
                'name': 'Europe',
                'denonym': 'European',
                'countries': [
                    {
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
            reverse('sample:continent_detail', args=(europe.pk,)),
            HTTP_ACCEPT_LANGUAGE='de'
        )
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(
            json.loads(response.content.decode('utf-8')),
            {
                'code': 'EU',
                'name': 'Europa',
                'denonym': 'Europäisch',
                'countries': [
                    {
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
            reverse('sample:continent_detail', args=(europe.pk,)),
            HTTP_ACCEPT_LANGUAGE='de-at'
        )
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(
            json.loads(response.content.decode('utf-8')),
            {
                'code': 'EU',
                'name': 'Europa',
                'denonym': 'Europäisch',
                'countries': [
                    {
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
