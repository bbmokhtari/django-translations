import json

from django.test import TestCase
from django.urls import reverse

from sample.models import Continent
from sample.utils import create_samples


class GetContinentListTest(TestCase):
    """Tests for `get_continent_list`."""

    def test_fallback(self):
        """
        Test for fallback

        Args:
            self: (todo): write your description
        """
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
                }
            ]
        )

    def test_language(self):
        """
        This function returns the language.

        Args:
            self: (todo): write your description
        """
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
                }
            ]
        )

    def test_accent_not_exists(self):
        """
        Test if the existence exists.

        Args:
            self: (todo): write your description
        """
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
                }
            ]
        )


class GetContinentDetailTest(TestCase):
    """Tests for `get_continent_detail`."""

    def test_fallback(self):
        """
        Test for fallback

        Args:
            self: (todo): write your description
        """
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
        """
        This function to see if the language

        Args:
            self: (todo): write your description
        """
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
        """
        Test if a user has not in - test.

        Args:
            self: (todo): write your description
        """
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
