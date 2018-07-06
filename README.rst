Translations
============

Translations is a Django application which provides support for database content
translation.

What does it mean? 
------------------
There are two types of translation:

Static Content Translation
    The content created by the *programmer* in python modules or templates.

    examples:
        * Please enter the username.
        * The email must be in the format some@email.
        * Navigation menu

    Django provides builtin support for this out of the box. For more info see
    `Django i18n Translation Topic`_

    .. _Django i18n Translation Topic: https://docs.djangoproject.com/en/2.0/topics/i18n/
       translation/

Dynamic Content Translation
    The content created by the *admin* or the *user* using forms or APIs.

    exaxmples:
        * Well, we (programmers) don't know what the content is, since it is
          entered dynamically.

    Django does **NOT** provide builtin support for this.

Translations application provides support for `Dynamic Content Translation`.

Requirements
------------

* Python (2.7, >=3.4)
* Django (1.11, 2.0)

Installation
------------

1. Install Translations

   Using PIP::

       $ pip install django-translations

   Using Git::

       $ git clone https://github.com/perplexionist/django-translations.git
       $ python setup.py install

2. add ``'translations'`` to ``INSTALLED_APPS`` in the settings of your Django
   project::

       INSTALLED_APPS = [
           ...
           'translations',
           ...
       ]


Usage
-----

