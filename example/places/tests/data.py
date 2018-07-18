from places.models import Continent, Country, City


CONTINENTS = [
    {
        "code": "EU",
        "name": "Europe",
        "denonym": "European",
        "translations": [
            # de
            {
                "field": "name",
                "language": "de",
                "text": "Europa",
            },
            {
                "field": "denonym",
                "language": "de",
                "text": "Europäisch",
            },
            # tr
            {
                "field": "name",
                "language": "tr",
                "text": "Avrupa",
            },
            {
                "field": "denonym",
                "language": "tr",
                "text": "Avrupalı",
            },
        ],
    },
    {
        "code": "AS",
        "name": "Asia",
        "denonym": "Asian",
        "translations": [
            # de
            {
                "field": "name",
                "language": "de",
                "text": "Asien",
            },
            {
                "field": "denonym",
                "language": "de",
                "text": "Asiatisch",
            },
            # tr
            {
                "field": "name",
                "language": "tr",
                "text": "Asya",
            },
            {
                "field": "denonym",
                "language": "tr",
                "text": "Asyalı",
            },
        ],
    },
    {
        "code": "AF",
        "name": "Africa",
        "denonym": "African",
        "translations": [
            # de
            {
                "field": "name",
                "language": "de",
                "text": "Afrika",
            },
            {
                "field": "denonym",
                "language": "de",
                "text": "Afrikanisch",
            },
            # tr
            {
                "field": "name",
                "language": "tr",
                "text": "Afrika",
            },
            {
                "field": "denonym",
                "language": "tr",
                "text": "Afrikalı",
            },
        ],
    },
    {
        "code": "NA",
        "name": "North America",
        "denonym": "North American",
        "translations": [
            # de
            {
                "field": "name",
                "language": "de",
                "text": "Nordamerika",
            },
            {
                "field": "denonym",
                "language": "de",
                "text": "Nordamerikanisch",
            },
            # tr
            {
                "field": "name",
                "language": "tr",
                "text": "Kuzey Amerika",
            },
            {
                "field": "denonym",
                "language": "tr",
                "text": "Kuzey Amerikalı",
            },
        ],
    },
    {
        "code": "SA",
        "name": "South America",
        "denonym": "South American",
        "translations": [
            # de
            {
                "field": "name",
                "language": "de",
                "text": "Südamerika",
            },
            {
                "field": "denonym",
                "language": "de",
                "text": "Südamerikanisch",
            },
            # tr
            {
                "field": "name",
                "language": "tr",
                "text": "Güney Amerika",
            },
            {
                "field": "denonym",
                "language": "tr",
                "text": "Güney Amerikalı",
            },
        ],
    },
    {
        "code": "AU",
        "name": "Australia",
        "denonym": "Australian",
        "translations": [
            # de
            {
                "field": "name",
                "language": "de",
                "text": "Australien",
            },
            {
                "field": "denonym",
                "language": "de",
                "text": "Australisch",
            },
            # tr
            {
                "field": "name",
                "language": "tr",
                "text": "Avustralya",
            },
            {
                "field": "denonym",
                "language": "tr",
                "text": "Avustralyalı",
            },
        ],
    },
]

COUNTRIES = [
    {
        "code": "DE",
        "name": "Germany",
        "denonym": "German",
        "translations": [
            # de
            {
                "field": "name",
                "language": "de",
                "text": "Deutschland",
            },
            {
                "field": "denonym",
                "language": "de",
                "text": "Deutsche",
            },
            # tr
            {
                "field": "name",
                "language": "tr",
                "text": "Almanya",
            },
            {
                "field": "denonym",
                "language": "tr",
                "text": "Almanca",
            },
        ],
    },
    {
        "code": "TR",
        "name": "Turkey",
        "denonym": "Turk",
        "translations": [
            # de
            {
                "field": "name",
                "language": "de",
                "text": "Türkei",
            },
            {
                "field": "denonym",
                "language": "de",
                "text": "Türke",
            },
            # tr
            {
                "field": "name",
                "language": "tr",
                "text": "Türkiye",
            },
            {
                "field": "denonym",
                "language": "tr",
                "text": "Türk",
            },
        ],
    },
    {
        "code": "KR",
        "name": "South Korea",
        "denonym": "South Korean",
        "translations": [
            # de
            {
                "field": "name",
                "language": "de",
                "text": "Südkorea",
            },
            {
                "field": "denonym",
                "language": "de",
                "text": "Südkoreanisch",
            },
            # tr
            {
                "field": "name",
                "language": "tr",
                "text": "Güney Kore",
            },
            {
                "field": "denonym",
                "language": "tr",
                "text": "güney Koreli",
            },
        ],
    },
    {
        "code": "IN",
        "name": "India",
        "denonym": "Indian",
        "translations": [
            # de
            {
                "field": "name",
                "language": "de",
                "text": "Indien",
            },
            {
                "field": "denonym",
                "language": "de",
                "text": "Indisch",
            },
            # tr
            {
                "field": "name",
                "language": "tr",
                "text": "Hindistan",
            },
            {
                "field": "denonym",
                "language": "tr",
                "text": "Hintli",
            },
        ],
    },
    {
        "code": "EG",
        "name": "Egypt",
        "denonym": "Egyptian",
        "translations": [
            # de
            {
                "field": "name",
                "language": "de",
                "text": "Ägypten",
            },
            {
                "field": "denonym",
                "language": "de",
                "text": "Ägyptisch",
            },
            # tr
            {
                "field": "name",
                "language": "tr",
                "text": "Mısır",
            },
            {
                "field": "denonym",
                "language": "tr",
                "text": "Mısırli",
            },
        ],
    },
    {
        "code": "ZA",
        "name": "South Africa",
        "denonym": "South African",
        "translations": [
            # de
            {
                "field": "name",
                "language": "de",
                "text": "Südafrika",
            },
            {
                "field": "denonym",
                "language": "de",
                "text": "Südafrikanisch",
            },
            # tr
            {
                "field": "name",
                "language": "tr",
                "text": "Güney Afrika",
            },
            {
                "field": "denonym",
                "language": "tr",
                "text": "Güney Afrikalı",
            },
        ],
    },
    {
        "code": "US",
        "name": "United States of America",
        "denonym": "American",
        "translations": [
            # de
            {
                "field": "name",
                "language": "de",
                "text": "Vereinigte Staaten von Amerika",
            },
            {
                "field": "denonym",
                "language": "de",
                "text": "Amerikanisch",
            },
            # tr
            {
                "field": "name",
                "language": "tr",
                "text": "Amerika Birleşik Devletleri",
            },
            {
                "field": "denonym",
                "language": "tr",
                "text": "Amerikalı",
            },
        ],
    },
    {
        "code": "MX",
        "name": "Mexico",
        "denonym": "Mexican",
        "translations": [
            # de
            {
                "field": "name",
                "language": "de",
                "text": "Mexiko",
            },
            {
                "field": "denonym",
                "language": "de",
                "text": "Mexikaner",
            },
            # tr
            {
                "field": "name",
                "language": "tr",
                "text": "Meksika",
            },
            {
                "field": "denonym",
                "language": "tr",
                "text": "Meksikalı",
            },
        ],
    },
    {
        "code": "BR",
        "name": "Brazil",
        "denonym": "Brazilian",
        "translations": [
            # de
            {
                "field": "name",
                "language": "de",
                "text": "Brasilien",
            },
            {
                "field": "denonym",
                "language": "de",
                "text": "Brasilianisch",
            },
            # tr
            {
                "field": "name",
                "language": "tr",
                "text": "Brezilya",
            },
            {
                "field": "denonym",
                "language": "tr",
                "text": "Brezilyalı",
            },
        ],
    },
    {
        "code": "AR",
        "name": "Argentina",
        "denonym": "Argentinian",
        "translations": [
            # de
            {
                "field": "name",
                "language": "de",
                "text": "Argentinien",
            },
            {
                "field": "denonym",
                "language": "de",
                "text": "Argentinisch",
            },
            # tr
            {
                "field": "name",
                "language": "tr",
                "text": "Arjantin",
            },
            {
                "field": "denonym",
                "language": "tr",
                "text": "Arjantinlı",
            },
        ],
    },
    {
        "code": "ID",
        "name": "Indonesia",
        "denonym": "Indonesian",
        "translations": [
            # de
            {
                "field": "name",
                "language": "de",
                "text": "Indonesien",
            },
            {
                "field": "denonym",
                "language": "de",
                "text": "Indonesier",
            },
            # tr
            {
                "field": "name",
                "language": "tr",
                "text": "Endonezya",
            },
            {
                "field": "denonym",
                "language": "tr",
                "text": "Endonezyalı",
            },
        ],
    },
    {
        "code": "NZ",
        "name": "New Zealand",
        "denonym": "New Zealandian",
        "translations": [
            # de
            {
                "field": "name",
                "language": "de",
                "text": "Neuseeland",
            },
            {
                "field": "denonym",
                "language": "de",
                "text": "Neuseeländisch",
            },
            # tr
            {
                "field": "name",
                "language": "tr",
                "text": "Yeni Zelanda",
            },
            {
                "field": "denonym",
                "language": "tr",
                "text": "Yeni Zelandalı",
            },
        ],
    },
]

CITIES = [
    {
        "name": "Cologne",
        "denonym": "Cologner",
        "translations": [
            # de
            {
                "field": "name",
                "language": "de",
                "text": "Köln",
            },
            {
                "field": "denonym",
                "language": "de",
                "text": "Kölner",
            },
            # tr
            {
                "field": "name",
                "language": "tr",
                "text": "Koln",
            },
            {
                "field": "denonym",
                "language": "tr",
                "text": "Kolnlı",
            },
        ],
    },
    {
        "name": "Munich",
        "denonym": "Munichian",
        "translations": [
            # de
            {
                "field": "name",
                "language": "de",
                "text": "München",
            },
            {
                "field": "denonym",
                "language": "de",
                "text": "Münchner",
            },
            # tr
            {
                "field": "name",
                "language": "tr",
                "text": "Münih",
            },
            {
                "field": "denonym",
                "language": "tr",
                "text": "Münihlı",
            },
        ],
    },
]


def create_continent(name, fields, langs):
    for continent in CONTINENTS:
        if name == continent["name"]:
            translations = continent.pop("translations")
            continent = Continent.objects.create(**continent)
            break
    else:
        raise ValueError("No continent named `{}`.".format(name))

    for translation in translations:
        if translation["field"] in fields and translation["language"] in langs:
            continent.translations.create(**translation)

    return continent
