############
Installation
############

1. Install the Translations app using pip:

   .. code:: bash

      $ pip install django-translations

2. Add ``translations`` to the ``INSTALLED_APPS`` in the settings of your
   project:

   .. code:: python

      INSTALLED_APPS += [
          'translations',
      ]

3. Run ``migrate``:

   .. code:: bash

      $ python manage.py migrate

4. Make sure Django Translations settings are set correctly:

   .. code:: python

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

   Please note that these settings are for Django itself.
