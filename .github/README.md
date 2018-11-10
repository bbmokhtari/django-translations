# Translations

[![build](https://travis-ci.com/perplexionist/django-translations.svg?branch=master)](https://travis-ci.com/perplexionist/django-translations)
[![python](https://img.shields.io/badge/python-3.5%7C3.6-0073b7.svg)](https://pypi.org/project/django-translations/)
[![pypi](https://img.shields.io/badge/pypi-1.0.0-f9d35f.svg)](https://pypi.org/project/django-translations/)
[![django](https://img.shields.io/badge/django-2.0%7C2.1-0C4B33.svg)](https://pypi.org/project/django-translations/)
[![flake8](https://img.shields.io/badge/flake8-linted-green.svg)](https://travis-ci.com/perplexionist/django-translations)

Django model translation for perfectionists with deadlines.

## Requirements

- Python (\>=3.5)
- Django (\>=2.0)

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

![image](https://raw.githubusercontent.com/perplexionist/django-translations/master/docs/_static/admin.png)

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
    <Continent: Europa>,
    <Continent: Asien>,
]>
<TranslatableQuerySet [
    <Country: Deutschland>,
]>
<TranslatableQuerySet [
    <City: Köln>,
]>
:
<TranslatableQuerySet [
    <Continent: Europe>,
    <Continent: Asia>,
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
[documentation](http://perplexionist.github.io/django-translations).
