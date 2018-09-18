******
Models
******

This module provides an in depth knowledge of the translatable models.

Make models translatable
========================

To make a model translatable inherit the model from the
:class:`~translations.models.Translatable` model.

.. literalinclude:: ../../sample/models.py
   :lines: 1-6, 24-48
   :emphasize-lines: 4, 7

Since :class:`~translations.models.Translatable` is an abstract model there is
no need to migrate afterwards.

Specify translatable fields
===========================

To specify the translatable fields specify the
:attr:`~translations.models.Translatable.TranslatableMeta.fields` attribute
of the :class:`~translations.models.Translatable.TranslatableMeta` class
declared inside a :class:`~translations.models.Translatable` model.

.. literalinclude:: ../../sample/models.py
   :lines: 1-6, 24-51
   :emphasize-lines: 33-34

By default the
:attr:`~translations.models.Translatable.TranslatableMeta.fields` attribute is
set to ``None``. This means the translation will use the text based fields
automatically, fields like :class:`~django.db.models.CharField` and
:class:`~django.db.models.TextField`. (it automatically ignores the fields with
the ``choices`` and :class:`~django.db.models.EmailField`)

If needed, the
:attr:`~translations.models.Translatable.TranslatableMeta.fields` attribute
can be set to nothing. You can do this by setting it to ``[]``.

Apply instance translations
===========================

To apply the translations of an instance use the
:meth:`~translations.models.Translatable.apply_translations` method.

.. testsetup:: guide_apply_translations_instance
   
   from tests.sample import create_samples

   create_samples(
       continent_names=['europe', 'asia'],
       country_names=['germany', 'south korea'],
       city_names=['cologne', 'munich', 'seoul', 'ulsan'],
       continent_fields=['name', 'denonym'],
       country_fields=['name', 'denonym'],
       city_fields=['name', 'denonym'],
       langs=['de']
   )

.. testcode:: guide_apply_translations_instance

   from sample.models import Continent

   # fetch an instance like before
   europe = Continent.objects.get(code='EU')

   # apply translations in place
   europe.apply_translations(lang='de')

   # use the instance like before
   print('Europe is called `{}` in German.'.format(europe.name))
   print('European is called `{}` in German.'.format(europe.denonym))

.. testoutput:: guide_apply_translations_instance

   Europe is called `Europa` in German.
   European is called `Europäisch` in German.

If successful, :meth:`~translations.models.Translatable.apply_translations`
applies the translations on the translatable
:attr:`~translations.models.Translatable.TranslatableMeta.fields` in place
and returns ``None``. If it fails it throws the necessary error.

.. note::

   This is a convention in python that if a method does something in place it
   should return ``None``.

:meth:`~translations.models.Translatable.apply_translations` can also apply
the translations of the instance's relations.

.. testsetup:: guide_apply_translations_relations
   
   from tests.sample import create_samples

   create_samples(
       continent_names=['europe', 'asia'],
       country_names=['germany', 'south korea'],
       city_names=['cologne', 'munich', 'seoul', 'ulsan'],
       continent_fields=['name', 'denonym'],
       country_fields=['name', 'denonym'],
       city_fields=['name', 'denonym'],
       langs=['de']
   )

.. testcode:: guide_apply_translations_relations

   from sample.models import Continent

   # fetch an instance like before
   europe = Continent.objects.prefetch_related(
       'countries',
       'countries__cities',
   ).get(code='EU')

   # apply translations in place
   europe.apply_translations(
       'countries',
       'countries__cities',
       lang='de'
   )

   # use the instance like before
   print('Europe is called `{}` in German.'.format(europe.name))
   print('European is called `{}` in German.'.format(europe.denonym))

   # use the relations like before
   germany = europe.countries.all()[0]
   cologne = germany.cities.all()[0]
   print('Germany is called `{}` in German.'.format(germany.name))
   print('German is called `{}` in German.'.format(germany.denonym))

.. testoutput:: guide_apply_translations_relations

   Europe is called `Europa` in German.
   European is called `Europäisch` in German.
   Germany is called `Deutschland` in German.
   German is called `Deutsche` in German.
   Cologne is called `Köln` in German.
   Cologner is called `Kölner` in German.
