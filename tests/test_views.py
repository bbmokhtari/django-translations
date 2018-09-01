import json

from django.test import TestCase
from django.urls import reverse

from tests.sample import create_all


class GetContinentListTest(TestCase):
    """Tests for `get_continent_list`."""

    def test_get_continent_list(self):
        response = self.client.get(reverse('sample:continent_list'))
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(json.loads(response.content), [{
            "id": 1,
            "code": "EU",
            "name": "Europe",
            "denonym": "European",
            "countries": [{
                "id": 1,
                "code": "DE",
                "name": "Germany",
                "denonym": "German",
                "cities": [{
                    "id": 1,
                    "name": "Cologne",
                    "denonym": "Cologner"
                }, {
                    "id": 2,
                    "name": "Munich",
                    "denonym": "Munichian"
                }]
            }, {
                "id": 2,
                "code": "TR",
                "name": "Turkey",
                "denonym": "Turk",
                "cities": [{
                    "id": 3,
                    "name": "Istanbul",
                    "denonym": "Istanbulian"
                }, {
                    "id": 4,
                    "name": "Izmir",
                    "denonym": "Izmirian"
                }]
            }]
            }, {
            "id": 2,
            "code": "AS",
            "name": "Asia",
            "denonym": "Asian",
            "countries": [{
                "id": 3,
                "code": "KR",
                "name": "South Korea",
                "denonym": "South Korean",
                "cities": [{
                    "id": 5,
                    "name": "Seoul",
                    "denonym": "Seouler"
                }, {
                    "id": 6,
                    "name": "Ulsan",
                    "denonym": "Ulsanian"
                }]
            }, {
                "id": 4,
                "code": "IN",
                "name": "India",
                "denonym": "Indian",
                "cities": [{
                    "id": 7,
                    "name": "Mumbai",
                    "denonym": "Mumbaian"
                }, {
                    "id": 8,
                    "name": "New Delhi",
                    "denonym": "New Delhian"
                }]
            }]
            }, {
            "id": 3,
            "code": "AF",
            "name": "Africa",
            "denonym": "African",
            "countries": [{
                "id": 5,
                "code": "EG",
                "name": "Egypt",
                "denonym": "Egyptian",
                "cities": [{
                    "id": 9,
                    "name": "Cairo",
                    "denonym": "Cairoian"
                }, {
                    "id": 10,
                    "name": "Giza",
                    "denonym": "Gizean"
                }]
            }, {
                "id": 6,
                "code": "ZA",
                "name": "South Africa",
                "denonym": "South African",
                "cities": [{
                    "id": 11,
                    "name": "Cape Town",
                    "denonym": "Cape Towner"
                }, {
                    "id": 12,
                    "name": "Johannesburg",
                    "denonym": "Johannesburgian"
                }]
            }]
            }, {
            "id": 4,
            "code": "NA",
            "name": "North America",
            "denonym": "North American",
            "countries": [{
                "id": 7,
                "code": "US",
                "name": "United States of America",
                "denonym": "American",
                "cities": [{
                    "id": 13,
                    "name": "New York",
                    "denonym": "New Yorker"
                }, {
                    "id": 14,
                    "name": "New Jersey",
                    "denonym": "New Jersean"
                }]
            }, {
                "id": 8,
                "code": "MX",
                "name": "Mexico",
                "denonym": "Mexican",
                "cities": [{
                    "id": 15,
                    "name": "Mexico City",
                    "denonym": "Mexico Citian"
                }, {
                    "id": 16,
                    "name": "Cancun",
                    "denonym": "Cancunian"
                }]
            }]
            }, {
            "id": 5,
            "code": "SA",
            "name": "South America",
            "denonym": "South American",
            "countries": [{
                "id": 9,
                "code": "BR",
                "name": "Brazil",
                "denonym": "Brazilian",
                "cities": [{
                    "id": 17,
                    "name": "Sao Paulo",
                    "denonym": "Sao Paulean"
                }, {
                    "id": 18,
                    "name": "Rio de Janeiro",
                    "denonym": "Rio de Janeirean"
                }]
            }, {
                "id": 10,
                "code": "AR",
                "name": "Argentina",
                "denonym": "Argentinian",
                "cities": [{
                    "id": 19,
                    "name": "Buenos Aires",
                    "denonym": "Buenos Airesean"
                }, {
                    "id": 20,
                    "name": "Tucuman",
                    "denonym": "Tucumanian"
                }]
            }]
            }, {
            "id": 6,
            "code": "AU",
            "name": "Australia",
            "denonym": "Australian",
            "countries": [{
                "id": 11,
                "code": "ID",
                "name": "Indonesia",
                "denonym": "Indonesian",
                "cities": [{
                    "id": 21,
                    "name": "Jakarta",
                    "denonym": "Jakartean"
                }, {
                    "id": 22,
                    "name": "Surabaya",
                    "denonym": "Surabayean"
                }]
            }, {
                "id": 12,
                "code": "NZ",
                "name": "New Zealand",
                "denonym": "New Zealandian",
                "cities": [{
                    "id": 23,
                    "name": "Auckland",
                    "denonym": "Aucklandean"
                }, {
                    "id": 24,
                    "name": "Wellington",
                    "denonym": "Wellingtonian"
                }]
            }]
        }])


class GetContinentDetailTest(TestCase):
    """Tests for `get_continent_detail`."""

    def test_get_continent_detail(self):
        response = self.client.get(reverse('sample:continent_detail', args=(1,)))
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(json.loads(response.content), {
            "id": 1,
            "code": "EU",
            "name": "Europe",
            "denonym": "European",
            "countries": [{
                "id": 1,
                "code": "DE",
                "name": "Germany",
                "denonym": "German",
                "cities": [{
                    "id": 1,
                    "name": "Cologne",
                    "denonym": "Cologner"
                }, {
                    "id": 2,
                    "name": "Munich",
                    "denonym": "Munichian"
                }]
            }, {
                "id": 2,
                "code": "TR",
                "name": "Turkey",
                "denonym": "Turk",
                "cities": [{
                    "id": 3,
                    "name": "Istanbul",
                    "denonym": "Istanbulian"
                }, {
                    "id": 4,
                    "name": "Izmir",
                    "denonym": "Izmirian"
                }]
            }]
        })
