import os
import re
import json


# ------------------------------------------------------------- Static Content

# project
name = 'Django Translations'
dist = 'django-translations'
description = 'A Django app which provides support for model translation.'

# author
author = 'Behzad B. Mokhtari'
email = '35877268+perplexionist@users.noreply.github.com'

# urls
source = 'https://github.com/perplexionist/django-translations'
tracker = 'https://github.com/perplexionist/django-translations/issues'
documentation = 'https://perplexionist.github.io/django-translations'
funding = 'https://blockchain.info/address/1FcPBamd6mVrHBNvjB5PqjbnGCBhdY7Rtm'

# search optimization
keywords = ['django', 'internationalization']

# ------------------------------------------------------------ Dynamic Content

# all releases/tags must follow this convention
release_pattern = re.compile(
    r'^' +
    r'(?P<version>\d+\.\d+\.\d+)' +
    r'(?:(?P<status>a|b|rc|\.dev|\.post)(?P<status_no>\d+))?' +
    r'$'
)

# Release, e.g. `1.0.0rc2`
release = os.environ.get('TRAVIS_TAG', '')

# Semantic Version, e.g. `1.0.0` in case of `1.0.0rc2`
version = ''

# Status, e.g. `rc` in case of `1.0.0rc2`
status = ''

# Development Status, e.g. `5 - Production/Stable` in case of `1.0.0rc2`
verbose_status = ''

if release:
    release_components = release_pattern.match(release).groupdict()
    version = release_components['version']
    status = release_components['status']

    if status == '.dev':
        verbose_status = '2 - Pre-Alpha'
    elif status == 'a':
        verbose_status = '3 - Alpha'
    elif status == 'b':
        verbose_status = '4 - Beta'
    elif status == 'rc':
        verbose_status = '5 - Production/Stable'
    elif status is None or status == '.post':
        verbose_status = '6 - Mature'
    else:
        raise Exception('Release must have a development status.')


# --------------------------------------------------------------------- Output

# Export to config.json
if __name__ == '__main__':
    with open('config.json', 'w') as fh:
        json.dump({
            'name': name,
            'dist': dist,
            'description': description,
            'author': author,
            'email': email,
            'source': source,
            'tracker': tracker,
            'documentation': documentation,
            'funding': funding,
            'keywords': keywords,
            'release': release,
            'version': version,
            'status': status,
            'verbose_status': verbose_status
        }, fh)
