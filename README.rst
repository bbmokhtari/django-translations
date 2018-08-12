Translations (In Development)
=============================

.. image:: https://travis-ci.com/perplexionist/django-translations.svg?branch=master
    :target: https://travis-ci.com/perplexionist/django-translations

Translations provides an **easy** and **efficient** way of translating model
contents.

Requirements
------------

* Python (>=3.5) - Python 2.7 is **NOT** supported.
* Django (1.11, 2.0) - Django 2.1 is **NOT** supported (yet).

Installation
------------

1. Install Translations using PIP (use ``--pre``, still in development)::

   $ pip install --pre django-translations

2. Add ``'translations'`` to ``INSTALLED_APPS`` in the settings of your Django
   project::

       INSTALLED_APPS = [
           ...
           'translations',
           ...
       ]

3. Run ``migrate``::

   $ python manage.py migrate

Usage
-----

Model
~~~~~

Inherit ``Translatable`` in any model you want translated.

**No migrations** needed afterwards! That's it!

::

    from translations.models import Translatable

    class Question(Translatable):
        ...

    class Choice(Translatable):
        ...

Query
~~~~~

You can use the extended ORM querysets::

    >>> q = Question.objects.create_translated(
    ...     question_text="What's up?",
    ...     category='usuals',
    ...     lang='en'
    ... )
    <Question: What's up?>
    >>> q.question_text = 'Quoi de neuf?'
    >>> q.category = 'habituels'
    >>> q.update_translations(
    ...     lang='fr'
    ... )
    >>> q.get_translated(lang='en')
    <Question: What's up?>
    >>> q.get_translated(lang='fr')
    <Question: Quoi de neuf?>

Admin
~~~~~

You can also use the admin extensions::

    from django.contrib import admin
    from translations.admin import TranslatableAdmin, TranslationInline

    from .models import Question

    class QuestionAdmin(TranslatableAdmin):
        inlines = [TranslationInline,]

    admin.site.register(Question, QuestionAdmin)

Documentation
-------------

For more interesting capabilities browse through the `documentation`_.

.. _documentation: http://perplexionist.github.io/django-translations
