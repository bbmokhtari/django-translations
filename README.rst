Translations
============

Translations is a Django application which provides support for model
translation.

Goal of the Project
-------------------

There are two types of translation:

Static Content Translation
    The content created by the *programmer* in the python modules or templates.

    examples:

    * Please enter the username.
    * The email must be in the format some@email.
    * Navigation menu

    Django provides builtin support for this out of the box. For more info see
    `Django i18n Translation Topic`_

    .. _Django i18n Translation Topic: https://docs.djangoproject.com/en/2.0/
       topics/i18n/translation/

Dynamic Content Translation
    The content created by the *admin* or the *user* using forms or APIs.

    exaxmples:

    * Well, we (programmers) don't know what the content is, since it is
      entered dynamically.

    Django does **NOT** provide builtin support for this.

Translations application provides support for *Dynamic Content Translation*.

Requirements
------------

* Python (2.7, >=3.4)
* Django (1.11, 2.0)

Installation
------------

1. Install Translations using PIP::

   $ pip install django-translations

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

Assume you've created this ``models.py``::

    from django.db import models


    class Question(models.Model):
        question_text = models.CharField(max_length=200)
        category = models.CharField(max_length=200)

        def __str__(self):
            return self.question_text

    class Choice(models.Model):
        question = models.ForeignKey(Question, on_delete=models.CASCADE)
        choice_text = models.CharField(max_length=200)
        votes = models.IntegerField(default=0)

        def __str__(self):
            return self.choice_text

All you have to do is inherit ``Translatable`` in any model you want
translated. **No migrations** needed afterwards! That's it!

::

    from translations.models import Translatable

    class Question(Translatable):
        ...

    class Choice(Translatable):
        ...

Now that you've made your models translatable. you can use the ORM::

    >>> q = Question.objects.create_translated(
    ...     question_text="What's up?",
    ...     category='usuals',
    ...     lang='en'
    ... )
    <Question: What's up?>
    >>> q.question_text = 'Quoi de neuf?'
    >>> q.category = 'habituels'
    >>> q.renew_translations(
    ...     lang='fr'
    ... )
    >>> q.get_translated(lang='en')
    <Question: What's up?>
    >>> q.get_translated(lang='fr')
    <Question: Quoi de neuf?>

Or use the admin extensions::

    from django.contrib import admin
    from translations.admin import TranslatableAdmin, TranslationInline

    from .models import Question

    class QuestionAdmin(TranslatableAdmin):
        inlines = [TranslationInline,]

    admin.site.register(Question, QuestionAdmin)

Documentation
-------------

For more information `Read the Docs`_.

.. _Read the Docs: https://readthedocs.org


