import setuptools
import json


with open('README.rst', 'r') as fh:
    long_description = fh.read()

with open('config.json', 'r') as fh:
    info = json.load(fh)


setuptools.setup(
    name=info['dist'],
    version=info['release'],
    description=info['description'],
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url=info['source'],
    author=info['author'],
    author_email=info['email'],
    classifiers=[
        'Development Status :: ' + info['verbose_status'],
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Internationalization',
    ],
    keywords=' '.join(info['keywords']),
    project_urls={
        'Documentation': info['documentation'],
        'Funding': info['funding'],
        'Source': info['source'],
        'Tracker': info['tracker'],
    },
    packages=setuptools.find_packages(
        exclude=[
            'sample',
            'sample.migrations',
            'tests',
        ]
    ),
    python_requires='>=3.5, <4',
)
