import os
import re
import json


# ------------------------------------------------------------- Static Content

# project
project = {
    'name': 'Django Translations',
    'github': 'django-translations',
    'dist': 'django-translations',
    'desc': 'Django model translation for perfectionists with deadlines.',
    'logo': 'translation.svg',
}

# author
author = {
    'name': 'Behzad B. Mokhtari',
    'email': 'behzad.public@gmail.com',
    'github': 'perplexionist',
}

# github
github = {
    'user': author['github'],
    'repo': project['github'],
}

# urls
urls = {
    'source': 'https://github.com/{user}/{repo}'.format(**github),
    'tracker': 'https://github.com/{user}/{repo}/issues'.format(**github),
    'documentation': 'https://{user}.github.io/{repo}'.format(**github),
    'funding': 'https://{user}.github.io/{repo}/donation.html'.format(
        **github),
}

# search optimization
keywords = ['django', 'translation', 'internationalization', 'localization']

# ------------------------------------------------------------ Dynamic Content

release = {
    'name': os.environ.get('TRAVIS_TAG', ''),  # e.g. `1.0.0rc2`
    'version': '',                             # e.g. `1.0.0`
    'status': '',                              # e.g. `rc`
    'classifier': '',                          # e.g. `5 - Production/Stable`
}

if release['name']:
    # all releases must follow this convention
    pattern = re.compile(
        r'^' +
        r'(?P<version>\d+\.\d+\.\d+)' +
        r'(?:(?P<status>a|b|rc|\.dev|\.post)(?P<status_no>\d+))?' +
        r'$'
    )
    components = pattern.match(release['name']).groupdict()
    release['version'] = components['version']
    release['status'] = components['status']

    if release['status'] == '.dev':
        release['classifier'] = '2 - Pre-Alpha'
    elif release['status'] == 'a':
        release['classifier'] = '3 - Alpha'
    elif release['status'] == 'b':
        release['classifier'] = '4 - Beta'
    elif release['status'] == 'rc':
        release['classifier'] = '5 - Production/Stable'
    elif release['status'] is None or release['status'] == '.post':
        release['classifier'] = '6 - Mature'
    else:
        raise Exception('Release must have a development status.')


# --------------------------------------------------------------------- Output

# Export to config.json
if __name__ == '__main__':
    with open('config.json', 'w') as fh:
        json.dump({
            'project': project,
            'author': author,
            'github': github,
            'urls': urls,
            'keywords': keywords,
            'release': release,
        }, fh)
