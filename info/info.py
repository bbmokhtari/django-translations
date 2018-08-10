import os
import re
from datetime import datetime

AUTHOR = 'Behzad B. Mokhtari'
EMAIL = '35877268+perplexionist@users.noreply.github.com'
YEAR = datetime.now().year

SOURCE = 'https://github.com/perplexionist/django-translations'
TRACKER = 'https://github.com/perplexionist/django-translations/issues'
DOCS = 'https://perplexionist.github.io/django-translations'
FUND = 'https://blockchain.info/address/1FcPBamd6mVrHBNvjB5PqjbnGCBhdY7Rtm'

release_pattern = re.compile(
    r'^' +
    r'(?P<version>\d+\.\d+\.\d+)' +
    r'(?:(?P<status>a|b|rc|\.dev|\.post)(?P<status_no>\d+))?' +
    r'$'
)

# Release: 1.0.0rc2
RELEASE = os.environ['TRAVIS_TAG']
release_components = release_pattern.match(RELEASE).groupdict()

# Semantic Version: 1.0.0
VERSION = release_components['version']

# Development Status: .dev | a | b | rc | `empty string` | .post
STATUS = release_components['status']

DEV_STATUS = ''
if STATUS == '.dev':
    DEV_STATUS = '2 - Pre-Alpha'
elif STATUS == 'a':
    DEV_STATUS = '3 - Alpha'
elif STATUS == 'b':
    DEV_STATUS = '4 - Beta'
elif STATUS == 'rc':
    DEV_STATUS = '5 - Production/Stable'
elif STATUS is None or STATUS == '.post':
    DEV_STATUS = '6 - Mature'
else:
    raise Exception('Release must have a development status.')
