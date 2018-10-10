import os
import re
import json


# ------------------------------------------------------------- Static Content

# project
project = {
    'name': 'Django Translations',
    'github': 'django-translations',
    'dist': 'django-translations',
    'desc': 'An easy, efficient and modular way of translating django models.',
    'logo': 'translation.svg',
}

# author
author = {
    'name': 'Behzad B. Mokhtari',
    'email': 'perplexionist.dev@gmail.com',
    'github': 'perplexionist',
}

# github
github = {
    'user': author['github'],
    'repo': project['github'],
}

# donation
donation = {
    'btc': '1JL5mNf2cqpgLCpWUuxYgnUfmzobRVqLhV',
}

# urls
urls = {
    'source': 'https://github.com/{user}/{repo}'.format(**github),
    'tracker': 'https://github.com/{user}/{repo}/issues'.format(**github),
    'documentation': 'https://{user}.github.io/{repo}'.format(**github),
    'funding': 'https://blockchain.info/address/{}'.format(donation['btc']),
}

# search optimization
keywords = ['django', 'internationalization']

# ------------------------------------------------------------ Dynamic Content

release = {
    'name': os.environ.get('TRAVIS_TAG', ''),  # e.g. `1.0.0rc2`
    'version': '',                            # e.g. `1.0.0`
    'status': '',                             # e.g. `rc`
    'classifier': '',                         # e.g. `5 - Production/Stable`
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

    if status == '.dev':
        release['classifier'] = '2 - Pre-Alpha'
    elif status == 'a':
        release['classifier'] = '3 - Alpha'
    elif status == 'b':
        release['classifier'] = '4 - Beta'
    elif status == 'rc':
        release['classifier'] = '5 - Production/Stable'
    elif status is None or status == '.post':
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
