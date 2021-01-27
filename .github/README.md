# Django Translations

[![build](https://travis-ci.com/bbmokhtari/django-translations.svg?branch=master)](https://travis-ci.com/bbmokhtari/django-translations)
[![python](https://img.shields.io/badge/python-%3E%3D3.6%2C%20%3C4-0073b7)](https://pypi.org/project/django-translations/)
[![django](https://img.shields.io/badge/django-%3E%3D2.0%2C%20%3C4-0C4B33)](https://pypi.org/project/django-translations/)

Django model translation for perfectionists with deadlines.

## Goal

There are two types of content, each of which has its own challenges for translation:

- Static content: This is the content which is defined in the code.
  _e.g. "Please enter a valid email address."_

  Django already provides a
  [solution](https://docs.djangoproject.com/en/2.1/topics/i18n/translation/)
  for translating static content.

- Dynamic content: This is the content which is stored in the database.
  _(We can't know it beforehand!)_

  Django Translations provides a solution
  for translating dynamic content.

## Compatibility

Currently, this project is incompatible with PostgreSQL.

## Requirements

- Python (\>=3.6, \<4)
- Django (\>=2.0, \<4)

## Installation

1.  Install Django Translations using pip:
    
    ``` bash
    $ pip install django-translations
    ```

2.  Add `translations` to the `INSTALLED_APPS` in the settings of your
    project:
    
    ``` python
    INSTALLED_APPS += [
        'translations',
    ]
    ```

3.  Run `migrate`:
    
    ``` bash
    $ python manage.py migrate
    ```

4.  Configure Django internationalization and localization settings:
    
    ``` python
    USE_I18N = True          # use internationalization
    USE_L10N = True          # use localization
    
    MIDDLEWARE += [          # locale middleware
        'django.middleware.locale.LocaleMiddleware',
    ]
    
    LANGUAGE_CODE = 'en-us'  # default (fallback) language
    LANGUAGES = (            # supported languages
        ('en', 'English'),
        ('en-gb', 'English (Great Britain)'),
        ('de', 'German'),
        ('tr', 'Turkish'),
    )
    ```
    
    Please note that these settings are for Django itself.

## Basic Usage

### Model

Inherit `Translatable` in any model you want translated:

``` python
from translations.models import Translatable

class Continent(Translatable):
    code = models.Charfield(...)
    name = models.Charfield(...)
    denonym = models.Charfield(...)

    class TranslatableMeta:
        fields = ['name', 'denonym']
```

No migrations needed afterwards.

### Admin

Use the admin extensions:

``` python
from translations.admin import TranslatableAdmin, TranslationInline

class ContinentAdmin(TranslatableAdmin):
    inlines = [TranslationInline,]
```

This provides specialized translation inlines for the model.

![image](https://raw.githubusercontent.com/bbmokhtari/django-translations/master/docs/_static/admin.png)

## QuerySet

Use the queryset extensions:

``` python
>>> from sample.models import Continent
>>> continents = Continent.objects.all(
... ).distinct(           # familiar distinct
... ).probe(['en', 'de']  # probe (filter, exclude, etc.) in English and German
... ).filter(             # familiar filtering
...     countries__cities__name__startswith='Köln'
... ).translate('de'      # translate the results in German
... ).translate_related(  # translate these relations as well
...     'countries', 'countries__cities',
... )
>>> print(continents)
<TranslatableQuerySet [
    <Continent: Europa>,
]>
>>> print(continents[0].countries.all())
<TranslatableQuerySet [
    <Country: Deutschland>,
]>
>>> print(continents[0].countries.all()[0].cities.all())
<TranslatableQuerySet [
    <City: Köln>,
]>
```

This provides a powerful yet familiar interface to work with the querysets.

## Context

Use the translation context:

``` python
>>> from translations.context import Context
>>> from sample.models import Continent
>>> continents = Continent.objects.all()
>>> relations = ('countries', 'countries__cities',)
>>> with Context(continents, *relations) as context:
...     context.read('de')    # read the translations onto the context
...     print(':')            # use the objects like before
...     print(continents)
...     print(continents[0].countries.all())
...     print(continents[0].countries.all()[0].cities.all())
... 
...     continents[0].countries.all()[0].name = 'Change the name'
...     context.update('de')  # update the translations from the context
... 
...     context.delete('de')  # delete the translations of the context
... 
...     context.reset()       # reset the translations of the context
...     print(':')            # use the objects like before
...     print(continents)
...     print(continents[0].countries.all())
...     print(continents[0].countries.all()[0].cities.all())
:
<TranslatableQuerySet [
    <Continent: Asien>,
    <Continent: Europa>,
]>
<TranslatableQuerySet [
    <Country: Deutschland>,
]>
<TranslatableQuerySet [
    <City: Köln>,
]>
:
<TranslatableQuerySet [
    <Continent: Asia>,
    <Continent: Europe>,
]>
<TranslatableQuerySet [
    <Country: Germany>,
]>
<TranslatableQuerySet [
    <City: Cologne>,
]>
```

This can CRUD the translations of any objects (instance, queryset, list) and their relations.

## Documentation

For more interesting capabilities browse through the
[documentation](http://bbmokhtari.github.io/django-translations).

## Support the project

To support the project you can:
- ⭐️: [Star](http://github.com/bbmokhtari/django-translations/) it on GitHub.
- 💻: [Contribute](https://bbmokhtari.github.io/django-translations/contribution.html) to the code base.
- ☕️: [Buy](https://bbmokhtari.github.io/django-translations/donation.html) the maintainers coffee.
