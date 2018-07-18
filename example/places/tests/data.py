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


def create_continent(code, fields, langs):
    for continent in CONTINENTS:
        if code == continent["code"]:
            translations = continent.pop("translations")
            continent = Continent.objects.create(**continent)
            break
    else:
        raise ValueError("No continent coded `{}`.".format(code))

    for translation in translations:
        if translation["field"] in fields and translation["language"] in langs:
            continent.translations.create(**translation)

    return continent
