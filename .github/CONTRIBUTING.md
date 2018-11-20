# Contribution

[comment]: # (any changes to this module must also be reflected in /docs/contribution.rst)

This module provides comprehensive information on how to contribute to
Django Translations.

## Report bugs/Request features

You can report bugs or request features in
[issues](https://github.com/bbmokhtari/django-translations/issues).

## Patching

You can submit [pull
requests](https://github.com/bbmokhtari/django-translations/pulls).

## Code

Clone the repository of Django Translations:

``` bash
$ git clone https://github.com/bbmokhtari/django-translations.git
```

After cloning the repository (and preferably creating a virtual
environment) install the required libraries for working on it. To do
this change directories into the root directory of the cloned repository
and run the following command:

``` bash
$ pip install -r requirements_dev.txt
```

## The example project

The example project is a Django project which has the Translations app
installed plus a Sample app that works with the Translations app.

The Sample app is a Django app which provides certain info about some
continents and their respective countries and cities using some API
endpoints.

Change directories into the root directory of the cloned repository and
from here on out run all the commands in that directory:

To create the example project:

``` bash
$ python create.py
```

This creates a `project` directory in the root directory of the cloned
repository.

Run migrations:

``` bash
$ python project/manage.py migrate
```

To populate some data for the Sample app:

``` bash
$ python project/manage.py shell
```

Then in the python shell:

``` python
>>> from sample.utils import create_all
>>> create_all()
```

To run the example project:

``` bash
$ python project/manage.py runserver
```

Check API endpoints:

<http://localhost:8000/sample/continent/list/>

This API endpoint is used to show a list of continents and their
respective countries and cities.

<http://localhost:8000/sample/continent/1/>

This API endpoint is used to show a certain continent and its countries
and cities.

The example project supports `German (de)` and `Turkish (tr)` languages.

Change the *language* settings in your browser and reload the API
endpoint, or if you are using a rest client like Postman change the
`Accept-Language` header in your request. The API endpoint should show
you the response in the requested language.

## Configurations

To change the basic configurations of Django Translations edit the
`config.py` file. When you are done, generate the configurations file.

To generate the configurations file change directories into the root
directory of the cloned repository and run the following command:

``` bash
$ python config.py
```

This generates a file named `config.json` in the root directory of the
cloned repository.

## Tests

To run the tests: (make sure you have created [The example project]())

``` bash
$ python project/manage.py test
```

## Documentation

To build the documentation: (make sure you have created [The example
project](), also make sure to generate the
[Configurations](#configurations))

``` bash
$ make --directory docs html
```

To run tests on the examples of the documentation:

``` bash
$ make --directory docs doctest
```

## Style

Django Translations uses `flake8` for styling purposes.

To lint the code:

``` bash
$ flake8
```

## Releasing a version

Creating a git tag automatically causes Travis CI to:

  - Lint the code
  - Run unit tests
  - Run documentation tests

And if all of the above pass:

  - Generate the proper documentation with the git tag as the version
    number and upload it to GitHub Pages.
  - Generate the python package with the git tag as the version number
    and upload it to PyPI.

The tag **must** follow the `PEP 440` conventions.
