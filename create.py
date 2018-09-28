import os
import shutil
import django


settings = """

# Set the root directory of the repo as the search path
import sys
sys.path.insert(0, os.path.dirname(BASE_DIR))


# Install translations app, and sample app to test it
INSTALLED_APPS += [
    'translations.apps.TranslationsConfig',
    'sample.apps.SampleConfig',
    'tests.apps.TestsConfig',
]

MIDDLEWARE += [
    'django.middleware.locale.LocaleMiddleware',
]

LANGUAGES = (
    ('en', 'English'),
    ('en-gb', 'English (Great Britain)'),
    ('de', 'German'),
    ('tr', 'Turkish'),
)


# Read DB configuration from environment variables
DEFAULT_ENGINE = 'sqlite3'
DEFAULT_NAME = os.path.join(BASE_DIR, 'db.sqlite3')

ENGINE = os.environ.get('EXAMPLE_ENGINE', DEFAULT_ENGINE)
NAME = os.environ.get('EXAMPLE_NAME', DEFAULT_NAME)
HOST = os.environ.get('EXAMPLE_HOST', None)
PORT = os.environ.get('EXAMPLE_PORT', None)
USER = os.environ.get('EXAMPLE_USER', None)
PASSWORD = os.environ.get('EXAMPLE_PASSWORD', None)


def get_database_conf():
    conf = {}

    conf['ENGINE'] = 'django.db.backends.{}'.format(ENGINE)
    conf['NAME'] = NAME

    if HOST:
        conf['HOST'] = HOST
    if PORT:
        conf['PORT'] = PORT
    if USER:
        conf['USER'] = USER
    if PASSWORD:
        conf['PASSWORD'] = PASSWORD

    return conf


DATABASES = {
    'default': get_database_conf()
}


# Read logging configuration from environment variables
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': LOG_LEVEL,
        },
        'django.db': {
            'handlers': ['console'],
            'level': LOG_LEVEL,
        },
    },
}
"""

urls_1 = """

from django.conf.urls import include

urlpatterns += [
    url('sample/', include('sample.urls'))
]
"""

urls_2 = """

from django.urls import include

urlpatterns += [
    path('sample/', include('sample.urls'))
]
"""

if __name__ == '__main__':
    # remove the old project
    try:
        shutil.rmtree('project')
    except FileNotFoundError:
        pass

    # create a new project
    os.system('django-admin startproject project')

    # configure settings
    with open(os.path.join('project', 'project', 'settings.py'), 'a') as fh:
        fh.write(settings)

    # configure urls
    with open(os.path.join('project', 'project', 'urls.py'), 'a') as fh:
        if int(django.get_version().split('.')[0]) == 2:
            fh.write(urls_2)
        else:
            fh.write(urls_1)
