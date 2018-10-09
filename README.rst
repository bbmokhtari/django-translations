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
       code = models.Charfield(...)
       name = models.Charfield(...)
       denonym = models.Charfield(...)

       class TranslatableMeta:
           fields = ['name', 'denonym']

**NO MIGRATIONS** needed afterwards!

Query
~~~~~

Use the context:

.. code:: python

   >>> from translations.context import Context
   >>> # 1. query the database like before
   >>> continents = Continent.objects.all()
   >>> # 2. work with the translated objects
   >>> with Context(continents, 'countries', 'countries__cities',) as context:
   ...     # -------------------------------- read the context in German
   ...     context.read('de')
   ...     print(continents[0].name)
   ...     print(continents[0].countries.all()[0].name)
   ...     # -------------------------------- update the context in German
   ...     continents[0].name = 'Europa (changed)'
   ...     continents[0].countries.all()[0].name = 'Deutschland (changed)'
   ...     context.update('de')
   ...     # -------------------------------- and more capabilties
   ...     context.reset()
   ...     print(continents[0].name)
   ...     print(continents[0].countries.all()[0].name)
   Europa
   Deutschland
   Europe
   Germany

This does only **ONE QUERY** to translate any object (instance, queryset, list)
plus all its relations.

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
