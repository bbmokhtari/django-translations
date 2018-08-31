Translations
============

.. image:: https://travis-ci.com/perplexionist/django-translations.svg?branch=master
    :target: https://travis-ci.com/perplexionist/django-translations

Translations app provides an *easy*, *efficient* and *modular* way of
translating django models.

Requirements
------------

* Python (>=3.5)
* Django (1.11, >=2.0)

Installation
------------

1. Install Translations using PIP (use ``--pre``, still in development)::

   $ pip install --pre django-translations

2. Add ``'translations'`` to ``INSTALLED_APPS`` in the settings of your Django
   project::

       INSTALLED_APPS = [
           ...
           'translations',
           ...
       ]

3. Run ``migrate``::

   $ python manage.py migrate

Basic Usage
-----------

Model
~~~~~

Inherit ``Translatable`` in any model you want translated::

    from translations.models import Translatable

    class Continent(Translatable):
        ...

    class Country(Translatable):
        ...

    class City(Translatable):
        ...

**No Migrations** needed afterwards!

Query
~~~~~

Use the queryset extensions::

    >>> continents = Continent.objects.prefetch_related(
    ...     'countries',
    ...     'countries__cities',
    ... ).apply_translations(
    ...     'countries',
    ...     'countries__cities',
    ...     lang='de'
    ... )
    >>> continents[0].name
    Europa
    >>> continents[0].countries.all()[0].name
    Deutschland

This does **Only One Query** for the queryset and relations translations!

Admin
~~~~~

Use the admin extensions::

    from django.contrib import admin
    from translations.admin import TranslatableAdmin, TranslationInline

    from .models import Continent

    class ContinentAdmin(TranslatableAdmin):
        inlines = [TranslationInline,]

    admin.site.register(Continent, ContinentAdmin)

This provides admin inlines for the translations of the model.

Documentation
-------------

For more interesting capabilities browse through the `documentation`_.

.. _documentation: http://perplexionist.github.io/django-translations
