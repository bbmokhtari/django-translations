############
Contribution
############

This module provides comprehensive information on how to contribute to the
project.

***************************
Report bugs/Report features
***************************

You can report bugs and request features in the `issues`_.

.. _`issues`: https://github.com/perplexionist/django-translations/issues

************
Get the code
************

Clone the repository of this project:

.. code-block:: bash

   $ git clone https://github.com/perplexionist/django-translations.git

After cloning the repository (and optionally creating a virtual environment)
install the required libraries for working on the Translations app.

.. code-block:: bash

   $ pip install -r requirements_dev.txt

*******************
The example project
*******************

The example project is a Django project which has the Translations app
installed plus a Sample app to work with the Translations app.

The Sample app is a Django app which provides the info about some continents
and their respective countries and cities using some API endpoints.

To create the example project change directories to the
root directory of the project and run the following command:

.. code-block:: bash

   $ python create.py

This creates a :file:`project` directory in the root directory of the project.

To populate some data for the Sample app run the following command in the
root directory of the project.

.. code-block:: bash

   $ python project/manage.py shell

Then in the python shell run the following command.

.. code-block:: python

   >>> from sample.utils import create_all
   >>> create_all()

To run the example project:

.. code-block:: bash

   $ python project/manage.py runserver

You can check out the example project API endpoints using the following urls:

http://localhost:8000/sample/continent/list/

This API endpoint is used to show a list of continents and their respective
countries and cities.

http://localhost:8000/sample/continent/1/

This API endpoint is used to show a chosen continent and its
countries and cities.

*****
Tests
*****

To run the tests:

.. code-block:: bash

   $ python project/manage.py test

*************
Documentation
*************

To build the documentation:

.. code-block:: bash

   $ make --directory docs html

To run tests on the examples of the documentation:

.. code-block:: bash

   $ make --directory docs doctest

*****
Style
*****

Translations app uses ``flake8`` for styling purposes.

To lint the code:

.. code-block:: bash

   $ flake8

********
Patching
********

You can submit `pull requests`_.

.. _`pull requests`: https://github.com/perplexionist/django-translations/pulls

*******************
Releasing a Version
*******************

Creating a git tag causes Travis CI to create a version with that tag name
automatically.

The tag **must** follow the :pep:`440` conventions.
