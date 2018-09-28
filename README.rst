Translations
============

|build| |python| |pypi| |django| |flake8|

.. |build| image:: https://travis-ci.com/perplexionist/django-translations.svg?branch=master
           :target: https://travis-ci.com/perplexionist/django-translations

.. |python| image:: https://img.shields.io/badge/python-3.5%7C3.6-0073b7.svg
            :target: https://pypi.org/project/django-translations/

.. |pypi| image:: https://img.shields.io/badge/pypi-1.0.0-f9d35f.svg
          :target: https://pypi.org/project/django-translations/

.. |django| image:: https://img.shields.io/badge/django-1.11%7C2.0%7C2.1-0C4B33.svg
            :target: https://pypi.org/project/django-translations/

.. |flake8| image:: https://img.shields.io/badge/flake8-linted-green.svg
            :target: https://travis-ci.com/perplexionist/django-translations

Translations app provides an *easy*, *efficient* and *modular* way of
translating Django *models*.

Requirements
------------

* Python (>=3.5)
* Django (1.11, >=2.0)

Installation
------------

1. Install Translations using PIP (use ``--pre``, still in development):

   .. code:: bash

      $ pip install --pre django-translations

2. Add ``'translations'`` to ``INSTALLED_APPS`` in the settings of your Django
   project:

   .. code:: python

      INSTALLED_APPS += [
          'translations',
      ]

3. Run ``migrate``:

   .. code:: bash

      $ python manage.py migrate

4. Make sure django internationalization settings are set correctly:

   .. code:: python

      USE_I18N = True          # use internationalization
      USE_L10N = True          # use localization

      MIDDLEWARE += [          # locale middleware
          'django.middleware.locale.LocaleMiddleware',
      ]

      LANGUAGE_CODE = 'en-us'  # fallback language
      LANGUAGES = (            # supported languages
          ('en', 'English'), 
          ('de', 'German'),
      )

Basic Usage
-----------

Model
~~~~~

Inherit ``Translatable`` in any model you want translated:

.. code:: python

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

Use the queryset extensions:

.. code:: python

   >>> # 1. query the database
   >>> continents = Continent.objects.prefetch_related(
   ...     'countries',
   ...     'countries__cities'
   ... )
   >>> # 2. apply the translations (in place)
   >>> continents.apply_translations(
   ...     'countries',
   ...     'countries__cities',
   ...     lang='de'
   ... )
   >>> # 3. use it like before
   >>> continents[0].name
   Europa
   >>> continents[0].countries.all()[0].name
   Deutschland

This does **Only One Query** for the translations of the queryset and the
specified relations!

Admin
~~~~~

Use the admin extensions:

.. code:: python

   from translations.admin import TranslatableAdmin, TranslationInline

   class ContinentAdmin(TranslatableAdmin):
       inlines = [TranslationInline,]

This provides specialized translation inlines for the model.

Documentation
-------------

For more interesting capabilities browse through the `documentation`_.

.. _documentation: http://perplexionist.github.io/django-translations
