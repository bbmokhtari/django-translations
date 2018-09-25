*********
Utilities
*********

This module provides an in depth knowledge of the Translations utilities.

Make list of instances translatable
===================================

To make a list of homogeneous instances, a
:class:`translatable list of instances <translations.models.Translatable>`
:ref:`make the instance model translatable <translatable-models>`.

Specify list of instances' translatable fields
==============================================

To specify the list of instances' :attr:`translatable fields \
<translations.models.Translatable.TranslatableMeta.fields>`
:ref:`specify the instance model's translatable fields <specify-fields>`.

Apply list of instances translations
===========================

To apply the translations of a
:class:`translatable list of instances <translations.models.Translatable>`
use the
:meth:`~translations.utils.apply_translations`
method.

.. testsetup:: guide_apply_translations_list

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

.. testcode:: guide_apply_translations_list

   from sample.models import Continent
   from translations.utils import apply_translations

   # fetch a list of instances like before
   continents = list(Continent.objects.all())

   # apply the translations in place
   apply_translations(continents, lang='de')

   # use the list of instances like before
   europe = continents[0]
   asia = continents[1]

   # output
   print('`Europe` is called `{}` in German.'.format(europe.name))
   print('`European` is called `{}` in German.'.format(europe.denonym))
   print('`Asia` is called `{}` in German.'.format(asia.name))
   print('`Asian` is called `{}` in German.'.format(asia.denonym))

.. testoutput:: guide_apply_translations_list

   `Europe` is called `Europa` in German.
   `European` is called `Europäisch` in German.
   `Asia` is called `Asien` in German.
   `Asian` is called `Asiatisch` in German.

The ``lang`` parameter is optional. It determines the language to apply the
translations in. It must be a language code already declared in the
:data:`~django.conf.settings.LANGUAGES` setting. If it is not passed in, it
will be automatically set to the :term:`active language` code.

If successful,
:meth:`~translations.utils.apply_translations`
applies the translations of the list of instances on its
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
