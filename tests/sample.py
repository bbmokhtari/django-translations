from translations.utils import _get_reverse_relation

from sample.models import Continent, Country, City


# -------------------------------------------------------------------- samples


# Some translation spellings are written wrong on purpose to be able to
# test them
SAMPLES = {
    'europe': {
        'code': 'EU',
        'name': 'Europe',
        'denonym': 'European',
        'translations': {
            'de': {
                'name': 'Europa',
                'denonym': 'Europäisch'
            },
            'tr': {
                'name': 'Avrupa',
                'denonym': 'Avrupalı'
            }
        },
        'countries': {
            'germany': {
                'code': 'DE',
                'name': 'Germany',
                'denonym': 'German',
                'translations': {
                    'de': {
                        'name': 'Deutschland',
                        'denonym': 'Deutsche'
                    },
                    'tr': {
                        'name': 'Almanya',
                        'denonym': 'Almanca'
                    }
                },
                'cities': {
                    'cologne': {
                        'name': 'Cologne',
                        'denonym': 'Cologner',
                        'translations': {
                            'de': {
                                'name': 'Köln',
                                'denonym': 'Kölner'
                            },
                            'tr': {
                                'name': 'Koln',
                                'denonym': 'Kolnlı'
                            }
                        }
                    },
                    'munich': {
                        'name': 'Munich',
                        'denonym': 'Munichian',
                        'translations': {
                            'de': {
                                'name': 'München',
                                'denonym': 'Münchner'
                            },
                            'tr': {
                                'name': 'Münih',
                                'denonym': 'Münihlı'
                            }
                        }
                    },
                },
            },
            'turkey': {
                'code': 'TR',
                'name': 'Turkey',
                'denonym': 'Turk',
                'translations': {
                    'de': {
                        'name': 'Türkei',
                        'denonym': 'Türke'
                    },
                    'tr': {
                        'name': 'Türkiye',
                        'denonym': 'Türk'
                    }
                },
                'cities': {
                    'istanbul': {
                        'name': 'Istanbul',
                        'denonym': 'Istanbulian',
                        'translations': {
                            'de': {
                                'name': 'Ïstanbul',
                                'denonym': 'Ïstanbulisch'
                            },
                            'tr': {
                                'name': 'İstanbul',
                                'denonym': 'İstanbullı'
                            }
                        }
                    },
                    'izmir': {
                        'name': 'Izmir',
                        'denonym': 'Izmirian',
                        'translations': {
                            'de': {
                                'name': 'Ïzmir',
                                'denonym': 'Ïzmirisch'
                            },
                            'tr': {
                                'name': 'İzmir',
                                'denonym': 'İzmirlı'
                            }
                        }
                    },
                },
            },
        },
    },
    'asia': {
        'code': 'AS',
        'name': 'Asia',
        'denonym': 'Asian',
        'translations': {
            'de': {
                'name': 'Asien',
                'denonym': 'Asiatisch'
            },
            'tr': {
                'name': 'Asya',
                'denonym': 'Asyalı'
            }
        },
        'countries': {
            'south korea': {
                'code': 'KR',
                'name': 'South Korea',
                'denonym': 'South Korean',
                'translations': {
                    'de': {
                        'name': 'Südkorea',
                        'denonym': 'Südkoreanisch'
                    },
                    'tr': {
                        'name': 'Güney Kore',
                        'denonym': 'Güney Korelı'
                    }
                },
                'cities': {
                    'seoul': {
                        'name': 'Seoul',
                        'denonym': 'Seouler',
                        'translations': {
                            'de': {
                                'name': 'Seül',
                                'denonym': 'Seüler'
                            },
                            'tr': {
                                'name': 'Seul',
                                'denonym': 'Seullı'
                            }
                        }
                    },
                    'ulsan': {
                        'name': 'Ulsan',
                        'denonym': 'Ulsanian',
                        'translations': {
                            'de': {
                                'name': 'Ulsän',
                                'denonym': 'Ulsänisch'
                            },
                            'tr': {
                                'name': 'Ülsan',
                                'denonym': 'Ülsanlı'
                            }
                        }
                    },
                },
            },
            'india': {
                'code': 'IN',
                'name': 'India',
                'denonym': 'Indian',
                'translations': {
                    'de': {
                        'name': 'Indien',
                        'denonym': 'Indisch'
                    },
                    'tr': {
                        'name': 'Hindistan',
                        'denonym': 'Hintlı'
                    }
                },
                'cities': {
                    'mumbai': {
                        'name': 'Mumbai',
                        'denonym': 'Mumbaian',
                        'translations': {
                            'de': {
                                'name': 'Mumbaï',
                                'denonym': 'Mumbäisch'
                            },
                            'tr': {
                                'name': 'Bombay',
                                'denonym': 'Bombaylı'
                            }
                        }
                    },
                    'new delhi': {
                        'name': 'New Delhi',
                        'denonym': 'New Delhian',
                        'translations': {
                            'de': {
                                'name': 'Neu-Delhi',
                                'denonym': 'Neu-Delhisch'
                            },
                            'tr': {
                                'name': 'Yeni Delhi',
                                'denonym': 'Yeni Delhilı'
                            }
                        }
                    },
                },
            },
        },
    },
    'africa': {
        'code': 'AF',
        'name': 'Africa',
        'denonym': 'African',
        'translations': {
            'de': {
                'name': 'Afrika',
                'denonym': 'Afrikanisch'
            },
            'tr': {
                'name': 'Àfrika',
                'denonym': 'Àfrikalı'
            }
        },
        'countries': {
            'egypt': {
                'code': 'EG',
                'name': 'Egypt',
                'denonym': 'Egyptian',
                'translations': {
                    'de': {
                        'name': 'Ägypten',
                        'denonym': 'Ägyptisch'
                    },
                    'tr': {
                        'name': 'Mısır',
                        'denonym': 'Mısırlı'
                    }
                },
                'cities': {
                    'cairo': {
                        'name': 'Cairo',
                        'denonym': 'Cairoian',
                        'translations': {
                            'de': {
                                'name': 'Kairo',
                                'denonym': 'Kairoisch'
                            },
                            'tr': {
                                'name': 'Kahire',
                                'denonym': 'Kahirelı'
                            }
                        }
                    },
                    'giza': {
                        'name': 'Giza',
                        'denonym': 'Gizean',
                        'translations': {
                            'de': {
                                'name': 'Gizeh',
                                'denonym': 'Gizisch'
                            },
                            'tr': {
                                'name': 'Çizeh',
                                'denonym': 'Çizehlı'
                            }
                        }
                    },
                },
            },
            'south africa': {
                'code': 'ZA',
                'name': 'South Africa',
                'denonym': 'South African',
                'translations': {
                    'de': {
                        'name': 'Südafrika',
                        'denonym': 'Südafrikanisch'
                    },
                    'tr': {
                        'name': 'Güney Afrika',
                        'denonym': 'Güney Afrikalı'
                    }
                },
                'cities': {
                    'cape town': {
                        'name': 'Cape Town',
                        'denonym': 'Cape Towner',
                        'translations': {
                            'de': {
                                'name': 'Kapstadt',
                                'denonym': 'Kapstadtisch'
                            },
                            'tr': {
                                'name': 'Kap Şehri',
                                'denonym': 'Kap Şehrilı'
                            }
                        }
                    },
                    'johannesburg': {
                        'name': 'Johannesburg',
                        'denonym': 'Johannesburgian',
                        'translations': {
                            'de': {
                                'name': 'Johannesbürg',
                                'denonym': 'Johannesbürgisch'
                            },
                            'tr': {
                                'name': 'Yohannesburg',
                                'denonym': 'Yohannesburglı'
                            }
                        }
                    },
                },
            },
        },
    },
    'north america': {
        'code': 'NA',
        'name': 'North America',
        'denonym': 'North American',
        'translations': {
            'de': {
                'name': 'Nordamerika',
                'denonym': 'Nordamerikanisch'
            },
            'tr': {
                'name': 'Kuzey Amerika',
                'denonym': 'Kuzey Amerikalı'
            }
        },
        'countries': {
            'united states of america': {
                'code': 'US',
                'name': 'United States of America',
                'denonym': 'American',
                'translations': {
                    'de': {
                        'name': 'Vereinigte Staaten von Amerika',
                        'denonym': 'Amerikanisch'
                    },
                    'tr': {
                        'name': 'Amerika Birleşik Devletleri',
                        'denonym': 'Amerikalı'
                    }
                },
                'cities': {
                    'new york': {
                        'name': 'New York',
                        'denonym': 'New Yorker',
                        'translations': {
                            'de': {
                                'name': 'Neu York',
                                'denonym': 'Neu Yorkisch'
                            },
                            'tr': {
                                'name': 'Yeni York',
                                'denonym': 'Yeni Yorklı'
                            }
                        }
                    },
                    'new jersey': {
                        'name': 'New Jersey',
                        'denonym': 'New Jersean',
                        'translations': {
                            'de': {
                                'name': 'Neu Jersey',
                                'denonym': 'Neu Jersisch'
                            },
                            'tr': {
                                'name': 'Yeni Jersey',
                                'denonym': 'Yeni Jerseylı'
                            }
                        }
                    },
                },
            },
            'mexico': {
                'code': 'MX',
                'name': 'Mexico',
                'denonym': 'Mexican',
                'translations': {
                    'de': {
                        'name': 'Mexiko',
                        'denonym': 'Mexikaner'
                    },
                    'tr': {
                        'name': 'Meksika',
                        'denonym': 'Meksikalı'
                    }
                },
                'cities': {
                    'mexico city': {
                        'name': 'Mexico City',
                        'denonym': 'Mexico Citian',
                        'translations': {
                            'de': {
                                'name': 'Mexiko Stadt',
                                'denonym': 'Mexiko Stadtisch'
                            },
                            'tr': {
                                'name': 'Meksika şehri',
                                'denonym': 'Meksika şehrilı'
                            }
                        }
                    },
                    'cancun': {
                        'name': 'Cancun',
                        'denonym': 'Cancunian',
                        'translations': {
                            'de': {
                                'name': 'Cancún',
                                'denonym': 'Cancúnisch'
                            },
                            'tr': {
                                'name': 'Cancün',
                                'denonym': 'Cancünlı'
                            }
                        }
                    },
                },
            },
        },
    },
    'south america': {
        'code': 'SA',
        'name': 'South America',
        'denonym': 'South American',
        'translations': {
            'de': {
                'name': 'Südamerika',
                'denonym': 'Südamerikanisch'
            },
            'tr': {
                'name': 'Güney Amerika',
                'denonym': 'Güney Amerikalı'
            }
        },
        'countries': {
            'brazil': {
                'code': 'BR',
                'name': 'Brazil',
                'denonym': 'Brazilian',
                'translations': {
                    'de': {
                        'name': 'Brasilien',
                        'denonym': 'Brasilianisch'
                    },
                    'tr': {
                        'name': 'Brezilya',
                        'denonym': 'Brezilyalı'
                    }
                },
                'cities': {
                    'sao paulo': {
                        'name': 'Sao Paulo',
                        'denonym': 'Sao Paulean',
                        'translations': {
                            'de': {
                                'name': 'São Paulo',
                                'denonym': 'São Paulisch'
                            },
                            'tr': {
                                'name': 'Sao Paülo',
                                'denonym': 'Sao Paülolı'
                            }
                        }
                    },
                    'rio de janeiro': {
                        'name': 'Rio de Janeiro',
                        'denonym': 'Rio de Janeirean',
                        'translations': {
                            'de': {
                                'name': 'Rio von Janeiro',
                                'denonym': 'Rio von Janeirisch'
                            },
                            'tr': {
                                'name': 'Rio de Janeirü',
                                'denonym': 'Rio de Janeirülı'
                            }
                        }
                    },
                },
            },
            'argentina': {
                'code': 'AR',
                'name': 'Argentina',
                'denonym': 'Argentinian',
                'translations': {
                    'de': {
                        'name': 'Argentinien',
                        'denonym': 'Argentinisch'
                    },
                    'tr': {
                        'name': 'Arjantin',
                        'denonym': 'Arjantinlı'
                    }
                },
                'cities': {
                    'buenos aires': {
                        'name': 'Buenos Aires',
                        'denonym': 'Buenos Airesean',
                        'translations': {
                            'de': {
                                'name': 'Büenos Äires',
                                'denonym': 'Büenos Äiresisch'
                            },
                            'tr': {
                                'name': 'Büenos Aires',
                                'denonym': 'Büenos Aireslı'
                            }
                        }
                    },
                    'tucuman': {
                        'name': 'Tucuman',
                        'denonym': 'Tucumanian',
                        'translations': {
                            'de': {
                                'name': 'Tucumán',
                                'denonym': 'Tucumánisch'
                            },
                            'tr': {
                                'name': 'Tucüman',
                                'denonym': 'Tucümanlı'
                            }
                        }
                    },
                },
            },
        },
    },
    'australia': {
        'code': 'AU',
        'name': 'Australia',
        'denonym': 'Australian',
        'translations': {
            'de': {
                'name': 'Australien',
                'denonym': 'Australisch'
            },
            'tr': {
                'name': 'Avustralya',
                'denonym': 'Avustralyalı'
            }
        },
        'countries': {
            'indonesia': {
                'code': 'ID',
                'name': 'Indonesia',
                'denonym': 'Indonesian',
                'translations': {
                    'de': {
                        'name': 'Indonesien',
                        'denonym': 'Indonesier'
                    },
                    'tr': {
                        'name': 'Endonezya',
                        'denonym': 'Endonezyalı'
                    }
                },
                'cities': {
                    'jakarta': {
                        'name': 'Jakarta',
                        'denonym': 'Jakartean',
                        'translations': {
                            'de': {
                                'name': 'Jäkarta',
                                'denonym': 'Jäkartaisch'
                            },
                            'tr': {
                                'name': 'Jákarta',
                                'denonym': 'Jákartalı'
                            }
                        }
                    },
                    'surabaya': {
                        'name': 'Surabaya',
                        'denonym': 'Surabayean',
                        'translations': {
                            'de': {
                                'name': 'Suräbaya',
                                'denonym': 'Suräbayisch'
                            },
                            'tr': {
                                'name': 'Suràbaya',
                                'denonym': 'Suràbayalı'
                            }
                        }
                    },
                },
            },
            'new zealand': {
                'code': 'NZ',
                'name': 'New Zealand',
                'denonym': 'New Zealandian',
                'translations': {
                    'de': {
                        'name': 'Neuseeland',
                        'denonym': 'Neuseeländisch'
                    },
                    'tr': {
                        'name': 'Yeni Zelanda',
                        'denonym': 'Yeni Zelandalı'
                    }
                },
                'cities': {
                    'auckland': {
                        'name': 'Auckland',
                        'denonym': 'Aucklandean',
                        'translations': {
                            'de': {
                                'name': 'Äuckland',
                                'denonym': 'Äucklandisch'
                            },
                            'tr': {
                                'name': 'Akland',
                                'denonym': 'Aklandlı'
                            }
                        }
                    },
                    'wellington': {
                        'name': 'Wellington',
                        'denonym': 'Wellingtonian',
                        'translations': {
                            'de': {
                                'name': 'Wellingtön',
                                'denonym': 'Wellingtönisch'
                            },
                            'tr': {
                                'name': 'Velington',
                                'denonym': 'Velingtonlı'
                            }
                        }
                    }
                },
            }
        },
    }
}


# --------------------------------------------------------------- sample lists


CONTINENTS = []
COUNTRIES = []
CITIES = []

CONTINENT_FIELDS = []
COUNTRY_FIELDS = []
CITY_FIELDS = []

LANGS = []


def handle_fields_consistency(fields, excluded, consistent):
    # extract fields
    extracted_fields = []
    for field in fields:
        if field not in excluded:
            extracted_fields.append(field)

    # throw an error if `consistent` fields are not present in extracted ones
    for field in consistent:
        if field not in extracted_fields:
            raise Exception(
                'Field {} does not exist in {}'.format(
                    field,
                    consistent
                )
            )

    # add the fields that are not present in the consistent
    for field in extracted_fields:
        if field not in consistent:
            consistent.append(field)


def handle_langs_consistency(translations, lang_consistent, field_consistent):
    # extract langs
    extracted_langs = []
    for translation_lang, translation_fields in translations.items():
        extracted_langs.append(translation_lang)
        for field in translation_fields.keys():
            if field not in field_consistent:
                raise Exception(
                    'Field {} in translations is not in {}'.format(
                        field,
                        field_consistent
                    )
                )

    # throw an error if `consistent` langs are not present in extracted ones
    for lang in lang_consistent:
        if lang not in extracted_langs:
            raise Exception(
                'Language {} does not exist in {}'.format(
                    lang,
                    lang_consistent
                )
            )

    # add the langs that are not present in the consistent
    for lang in extracted_langs:
        if lang not in lang_consistent:
            lang_consistent.append(lang)


# fill them in using SAMPLES
for continent_k, continent_v in SAMPLES.items():
    CONTINENTS.append(continent_k)
    handle_fields_consistency(
        continent_v.keys(),
        ['countries', 'translations'],
        CONTINENT_FIELDS
    )
    handle_langs_consistency(
        continent_v['translations'],
        LANGS,
        CONTINENT_FIELDS
    )
    for country_k, country_v in continent_v['countries'].items():
        COUNTRIES.append(country_k)
        handle_fields_consistency(
            country_v.keys(),
            ['cities', 'translations'],
            COUNTRY_FIELDS
        )
        handle_langs_consistency(
            country_v['translations'],
            LANGS,
            COUNTRY_FIELDS
        )
        for city_k, city_v in country_v['cities'].items():
            CITIES.append(city_k)
            handle_fields_consistency(
                city_v.keys(),
                ['translations'],
                CITY_FIELDS
            )
            handle_langs_consistency(
                city_v['translations'],
                LANGS,
                CITY_FIELDS
            )


# ------------------------------------------------------------------ functions


def create_samples(
        continent_names=None, country_names=None, city_names=None,
        continent_fields=None, country_fields=None, city_fields=None,
        langs=None):

    # initialize areas
    continent_names = continent_names if continent_names is not None else []
    country_names = country_names if country_names is not None else []
    city_names = city_names if city_names is not None else []

    # initialize fields
    continent_fields = continent_fields if continent_fields is not None else []
    country_fields = country_fields if country_fields is not None else []
    city_fields = city_fields if city_fields is not None else []

    # initialize langs
    langs = langs if langs is not None else []

    info = {
        'model': Continent,
        'names': continent_names,
        'fields': continent_fields,
        'fields_desc': True,  # name translations is created before denonym
        'langs': langs,
        'descendant': {
            'countries': {
                'model': Country,
                'names': country_names,
                'fields': country_fields,
                'fields_desc': True,  # same reason as above
                'langs': langs,
                'descendant': {
                    'cities': {
                        'model': City,
                        'names': city_names,
                        'fields': city_fields,
                        'fields_desc': True, # same reason as above
                        'langs': langs,
                    }
                }
            }
        }
    }

    creator(**info)

    error_items = []

    if continent_names:
        error_items.append('Continents {}'.format(continent_names))

    if country_names:
        error_items.append('Countries {}'.format(country_names))

    if city_names:
        error_items.append('Cities {}'.format(city_names))

    if error_items:
        items = ', '.join(error_items)
        generated_error = '{} could not be created!'.format(items)
        raise Exception(generated_error)


def create_all():
    create_samples(
        continent_names=CONTINENTS,
        country_names=COUNTRIES,
        city_names=CITIES,
        continent_fields=CONTINENT_FIELDS,
        country_fields=COUNTRY_FIELDS,
        city_fields=CITY_FIELDS,
        langs=LANGS
    )


def creator(**kwargs):
    # these two are handled automatically - but needed in recursive calls
    samples = kwargs.get('samples', SAMPLES)
    parent = kwargs.get('parent', {})

    # these are the standard info to pass in
    model = kwargs.get('model', None)
    names = kwargs.get('names', [])
    fields = kwargs.get('fields', [])
    langs = kwargs.get('langs', [])
    descendant = kwargs.get('descendant', {})

    # order of creation for testing
    fields_desc = kwargs.get('fields_desc', False)
    langs_desc = kwargs.get('langs_desc', False)
    descendant_desc = kwargs.get('descendant_desc', False)

    # dict sorter function
    def sorter(x):
        return x[0]

    for name in names[:]:
        info = samples.get(name)

        if info:
            names.remove(name)
        else:
            continue

        info = info.copy()

        for descendant_key, descendant_kwargs in descendant.items():
            descendant_kwargs['samples'] = info.pop(descendant_key)

        translations = info.pop('translations')

        for parent_key, parent_value in parent.items():
            info[parent_key] = parent_value

        obj = model.objects.create(**info)

        translations_iterable = sorted(
            translations.items(),
            key=sorter,
            reverse=langs_desc
        )
        for lang, dictionary in translations_iterable:
            if lang in langs:
                dictionary_iterable = sorted(
                    dictionary.items(),
                    key=sorter,
                    reverse=fields_desc
                )
                for field, text in dictionary_iterable:
                    if field in fields:
                        obj.translations.create(
                            language=lang,
                            field=field,
                            text=text,
                        )

        descendant_iterable = sorted(
            descendant.items(),
            key=sorter,
            reverse=descendant_desc
        )
        for descendant_key, descendant_kwargs in descendant_iterable:
            parent_key = _get_reverse_relation(model, descendant_key)
            descendant_kwargs['parent'] = {
                parent_key: obj
            }
            creator(**descendant_kwargs)
