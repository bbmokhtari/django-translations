*********
QuerySets
*********

This module provides an in depth knowledge of the translatable querysets.

Make querysets translatable
===========================

To make a queryset, a
:class:`translatable querysets <translations.querysets.TranslatableQuerySet>`
:ref:`make its model translatable <translatable-models>`.

Specify queryset's translatable fields
======================================

Just :ref:`specify the model's translatable fields <specify-fields>`, and the
:class:`translatable querysets <translations.querysets.TranslatableQuerySet>`
will use those :attr:`translatable fields \
<translations.models.Translatable.TranslatableMeta.fields>` in the translation
automatically.

Apply queryset translations
===========================

To apply the translations of a
:class:`translatable queryset <translations.querysets.TranslatableQuerySet>`
use the :meth:`~translations.querysets.TranslatableQuerySet.apply_translations`
method.

.. testsetup:: guide_apply_translations_queryset

   from tests.sample import create_samples

   create_samples(
       continent_names=['europe', 'asia'],
       country_names=['germany', 'south korea'],
       city_names=['cologne', 'seoul'],
       continent_fields=['name', 'denonym'],
       country_fields=['name', 'denonym'],
       city_fields=['name', 'denonym'],
       langs=['de']
   )

.. testcode:: guide_apply_translations_queryset

   from sample.models import Continent

   # fetch a queryset like before
   continents = Continent.objects.all()

   # apply the translations in place
   continents.apply_translations(lang='de')

   # use the queryset like before
   europe = continents[0]
   asia = continents[1]
   print('`Europe` is called `{}` in German.'.format(europe.name))
   print('`European` is called `{}` in German.'.format(europe.denonym))
   print('`Asia` is called `{}` in German.'.format(asia.name))
   print('`Asian` is called `{}` in German.'.format(asia.denonym))

.. testoutput:: guide_apply_translations_queryset

   `Europe` is called `Europa` in German.
   `European` is called `Europäisch` in German.
   `Asia` is called `Asien` in German.
   `Asian` is called `Asiatisch` in German.

The ``lang`` parameter is optional. It determines the language to apply the
translations in. It must be a language code already declared in the
:data:`~django.conf.settings.LANGUAGES` setting. If it is not passed in, it
will be automatically set to the :term:`active language` code.

If successful,
:meth:`~translations.querysets.TranslatableQuerySet.apply_translations`
applies the translations of the queryset on its
:attr:`translatable fields \
<translations.models.Translatable.TranslatableMeta.fields>` and returns
``None``. If failed, it throws the appropriate error.

.. note::

   This is a convention in python that if a method changes the object
   in place it should return ``None``.

.. note::

   If there is no translation for a field in the
   :attr:`translatable fields \
   <translations.models.Translatable.TranslatableMeta.fields>`,
   the translation of the field falls back to the value of the field
   in the instance.
