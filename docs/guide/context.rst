*******
Context
*******

This module provides an in depth knowledge of the Translations context.

What is context
===============

When something is going to be stated it can be done so in the context of a
certain language.

Initiate a context
==================

To initiate a context use the :class:`~translations.context.Context`
class. The context's scope must be defined in the initiation, meaning which
``entity`` and what ``*relations`` of that entity should it affect.

All the actions like `reading the translations`_,
`updating the translations`_, etc only affects the
objects in the defined scope.

.. testsetup:: guide_init

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

To initiate a context for a model instance:

.. testcode:: guide_init

   from sample.models import Continent
   from translations.context import Context

   # fetch an instance
   europe = Continent.objects.get(code='EU')

   # initiate context
   with Context(europe, 'countries', 'countries__cities') as context:
       print('Context created!')

.. testoutput:: guide_init

   Context created!

To initiate a context for a queryset:

.. testcode:: guide_init

   from sample.models import Continent
   from translations.context import Context

   # fetch a queryset
   continents = Continent.objects.all()

   # initiate context
   with Context(continents, 'countries', 'countries__cities') as context:
       print('Context created!')

.. testoutput:: guide_init

   Context created!

To initiate a context for a list of model instances:

.. testcode:: guide_init

   from sample.models import Continent
   from translations.context import Context

   # fetch a list of instances
   continents = list(Continent.objects.all())

   # initiate context
   with Context(continents, 'countries', 'countries__cities') as context:
       print('Context created!')

.. testoutput:: guide_init

   Context created!

The ``entity`` must be a model instance, a queryset or a list of model
instances.
The model of the ``entity`` must be
:ref:`translatable <translatable-models>`.

The ``*relations`` must be an unpacked list of strings.
They may be separated by ``__``\ s to represent a deeply nested relation.
The model of the ``*relations`` must be
:ref:`translatable <translatable-models>`.

.. note::

   It is **recommended** for the relations of the entity to be
   prefetched before initiating a context,
   in order to reach optimal performance.

   To do this use
   :meth:`~django.db.models.query.QuerySet.select_related`,
   :meth:`~django.db.models.query.QuerySet.prefetch_related` or
   :func:`~django.db.models.prefetch_related_objects`.

Creating the translations
=========================

To create the translations of the context's scope in a language use the
:meth:`~translations.context.Context.create` method.
This creates the translations using the :ref:`translatable fields \
<specify-fields>` of the context's scope.
It takes in a ``lang`` parameter which determines the language to
create the translation in.

.. testsetup:: guide_create_0

   from tests.sample import create_samples

   create_samples(
       continent_names=['europe', 'asia'],
       country_names=['germany', 'south korea'],
       city_names=['cologne', 'seoul'],
       langs=['de']
   )

.. testsetup:: guide_create_1

   from tests.sample import create_samples

   create_samples(
       continent_names=['europe', 'asia'],
       country_names=['germany', 'south korea'],
       city_names=['cologne', 'seoul'],
       langs=['de']
   )

.. testsetup:: guide_create_2

   from tests.sample import create_samples

   create_samples(
       continent_names=['europe', 'asia'],
       country_names=['germany', 'south korea'],
       city_names=['cologne', 'seoul'],
       langs=['de']
   )

To create the translations of the defined scope for a model instance:

.. testcode:: guide_create_0

   from sample.models import Continent
   from translations.context import Context

   # fetch an instance
   europe = Continent.objects.get(code='EU')

   # initiate context
   with Context(europe, 'countries', 'countries__cities') as context:
       # change the instance like before
       europe.name = 'Europa'
       europe.countries.all()[0].name = 'Deutschland'
       europe.countries.all()[0].cities.all()[0].name = 'Köln'

       # create the translations in German
       context.create(lang='de')

   print('Translations created!')

.. testoutput:: guide_create_0

   Translations created!

To create the translations of the defined scope for a queryset:

.. testcode:: guide_create_1

   from sample.models import Continent
   from translations.context import Context

   # fetch a queryset
   continents = Continent.objects.all()

   # initiate context
   with Context(continents, 'countries', 'countries__cities') as context:
       # change the queryset like before
       continents[0].name = 'Europa'
       continents[0].countries.all()[0].name = 'Deutschland'
       continents[0].countries.all()[0].cities.all()[0].name = 'Köln'

       # create the translations in German
       context.create(lang='de')

   print('Translations created!')

.. testoutput:: guide_create_1

   Translations created!

To create the translations of the defined scope for a list of instances:

.. testcode:: guide_create_2

   from sample.models import Continent
   from translations.context import Context

   # fetch a list of instances
   continents = list(Continent.objects.all())

   # initiate context
   with Context(continents, 'countries', 'countries__cities') as context:
       # change the list of instances like before
       continents[0].name = 'Europa'
       continents[0].countries.all()[0].name = 'Deutschland'
       continents[0].countries.all()[0].cities.all()[0].name = 'Köln'

       # create the translations in German
       context.create(lang='de')

   print('Translations created!')

.. testoutput:: guide_create_2

   Translations created!

The ``lang`` must be a language code already declared in the
:data:`~django.conf.settings.LANGUAGES` setting. It is optional and if it is
not passed in, it is automatically set to the :term:`active language` code.

.. note::

   Creating only affects the translatable fields that have changed.

   If the value of a field is not changed, the translation for it is not
   created. (No need to set all the translatable fields beforehand)

Reading the translations
========================

To read the translations of the context's scope in a language use the
:meth:`~translations.context.Context.read` method.
This applies the translations on the :ref:`translatable fields \
<specify-fields>` of the context's scope.
It takes in a ``lang`` parameter which determines the language to
read the translation in.

.. testsetup:: guide_read

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

To read the translations of the defined scope for a model instance:

.. testcode:: guide_read

   from sample.models import Continent
   from translations.context import Context

   # fetch an instance
   europe = Continent.objects.get(code='EU')

   # initiate context
   with Context(europe, 'countries', 'countries__cities') as context:
       # read the translations in German
       context.read(lang='de')

       # use the instance like before
       print(europe.name)
       print(europe.countries.all()[0].name)
       print(europe.countries.all()[0].cities.all()[0].name)

.. testoutput:: guide_read

   Europa
   Deutschland
   Köln

To read the translations of the defined scope for a queryset:

.. testcode:: guide_read

   from sample.models import Continent
   from translations.context import Context

   # fetch a queryset
   continents = Continent.objects.all()

   # initiate context
   with Context(continents, 'countries', 'countries__cities') as context:
       # read the translations in German
       context.read(lang='de')

       # use the queryset like before
       print(continents[0].name)
       print(continents[0].countries.all()[0].name)
       print(continents[0].countries.all()[0].cities.all()[0].name)

.. testoutput:: guide_read

   Europa
   Deutschland
   Köln

To read the translations of the defined scope for a list of instances:

.. testcode:: guide_read

   from sample.models import Continent
   from translations.context import Context

   # fetch a list of instances
   continents = list(Continent.objects.all())

   # initiate context
   with Context(continents, 'countries', 'countries__cities') as context:
       # read the translations in German
       context.read(lang='de')

       # use the list of instances like before
       print(continents[0].name)
       print(continents[0].countries.all()[0].name)
       print(continents[0].countries.all()[0].cities.all()[0].name)

.. testoutput:: guide_read

   Europa
   Deutschland
   Köln

The ``lang`` must be a language code already declared in the
:data:`~django.conf.settings.LANGUAGES` setting. It is optional and if it is
not passed in, it is automatically set to the :term:`active language` code.

.. note::

   Reading only affects the translatable fields that have a translation.

   If there is no translation for a field, the value of the field is not
   changed. (It remains what it was before)

.. warning::

   Filtering any queryset after reading the translations will cause
   the translations of that queryset to be reset.

   .. testcode:: guide_read

      from sample.models import Continent
      from translations.context import Context

      europe = Continent.objects.prefetch_related(
          'countries',
          'countries__cities',
      ).get(code='EU')

      with Context(europe, 'countries', 'countries__cities') as context:
          context.read(lang='de')

          print(europe.name)
          print(europe.countries.exclude(name='')[0].name + '  -- Wrong')
          print(europe.countries.exclude(name='')[0].cities.all()[0].name + '  -- Wrong')

   .. testoutput:: guide_read

      Europa
      Germany  -- Wrong
      Cologne  -- Wrong

   The solution is to do the filtering before reading the
   translations. To do this on the relations use
   :class:`~django.db.models.Prefetch`.

   .. testcode:: guide_read

      from django.db.models import Prefetch
      from sample.models import Continent, Country
      from translations.context import Context

      europe = Continent.objects.prefetch_related(
          Prefetch(
              'countries',
              queryset=Country.objects.exclude(name=''),
          ),
          'countries__cities',
      ).get(code='EU')

      with Context(europe, 'countries', 'countries__cities') as context:
          context.read(lang='de')

          print(europe.name)
          print(europe.countries.all()[0].name + '  -- Correct')
          print(europe.countries.all()[0].cities.all()[0].name + '  -- Correct')

   .. testoutput:: guide_read

      Europa
      Deutschland  -- Correct
      Köln  -- Correct

Updating the translations
=========================

To update the translations of the context's scope in a language use the
:meth:`~translations.context.Context.update` method.
This updates the translations using the :ref:`translatable fields \
<specify-fields>` of the context's scope.
It takes in a ``lang`` parameter which determines the language to
update the translation in.

.. testsetup:: guide_update

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

To update the translations of the defined scope for a model instance:

.. testcode:: guide_update

   from sample.models import Continent
   from translations.context import Context

   # fetch an instance
   europe = Continent.objects.get(code='EU')

   # initiate context
   with Context(europe, 'countries', 'countries__cities') as context:
       # change the instance like before
       europe.name = 'Europa (changed)'
       europe.countries.all()[0].name = 'Deutschland (changed)'
       europe.countries.all()[0].cities.all()[0].name = 'Köln (changed)'

       # update the translations in German
       context.update(lang='de')

   print('Translations updated!')

.. testoutput:: guide_update

   Translations updated!

To update the translations of the defined scope for a queryset:

.. testcode:: guide_update

   from sample.models import Continent
   from translations.context import Context

   # fetch a queryset
   continents = Continent.objects.all()

   # initiate context
   with Context(continents, 'countries', 'countries__cities') as context:
       # change the queryset like before
       continents[0].name = 'Europa (changed)'
       continents[0].countries.all()[0].name = 'Deutschland (changed)'
       continents[0].countries.all()[0].cities.all()[0].name = 'Köln (changed)'

       # update the translations in German
       context.update(lang='de')

   print('Translations updated!')

.. testoutput:: guide_update

   Translations updated!

To update the translations of the defined scope for a list of instances:

.. testcode:: guide_update

   from sample.models import Continent
   from translations.context import Context

   # fetch a list of instances
   continents = list(Continent.objects.all())

   # initiate context
   with Context(continents, 'countries', 'countries__cities') as context:
       # change the list of instances like before
       continents[0].name = 'Europa (changed)'
       continents[0].countries.all()[0].name = 'Deutschland (changed)'
       continents[0].countries.all()[0].cities.all()[0].name = 'Köln (changed)'

       # update the translations in German
       context.update(lang='de')

   print('Translations updated!')

.. testoutput:: guide_update

   Translations updated!

The ``lang`` must be a language code already declared in the
:data:`~django.conf.settings.LANGUAGES` setting. It is optional and if it is
not passed in, it is automatically set to the :term:`active language` code.

.. note::

   Updating only affects the translatable fields that have changed.

   If the value of a field is not changed, the translation for it is not
   updated. (No need to initialize all the translatable fields beforehand)

Deleting the translations
=========================

To delete the translations of the context's scope in a language use the
:meth:`~translations.context.Context.delete` method.
This deletes the translations of the :ref:`translatable fields \
<specify-fields>` of the context's scope.
It takes in a ``lang`` parameter which determines the language to
delete the translation in.

.. testsetup:: guide_delete_0

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

.. testsetup:: guide_delete_1

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

.. testsetup:: guide_delete_2

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

To delete the translations of the defined scope for a model instance:

.. testcode:: guide_delete_0

   from sample.models import Continent
   from translations.context import Context

   # fetch an instance
   europe = Continent.objects.get(code='EU')

   # initiate context
   with Context(europe, 'countries', 'countries__cities') as context:
       # delete the translations in German
       context.delete(lang='de')

   print('Translations deleted!')

.. testoutput:: guide_delete_0

   Translations deleted!

To delete the translations of the defined scope for a queryset:

.. testcode:: guide_delete_1

   from sample.models import Continent
   from translations.context import Context

   # fetch a queryset
   continents = Continent.objects.all()

   # initiate context
   with Context(continents, 'countries', 'countries__cities') as context:
       # delete the translations in German
       context.delete(lang='de')

   print('Translations deleted!')

.. testoutput:: guide_delete_1

   Translations deleted!

To delete the translations of the defined scope for a list of instances:

.. testcode:: guide_delete_2

   from sample.models import Continent
   from translations.context import Context

   # fetch a list of instances
   continents = list(Continent.objects.all())

   # initiate context
   with Context(continents, 'countries', 'countries__cities') as context:
       # delete the translations in German
       context.delete(lang='de')

   print('Translations deleted!')

.. testoutput:: guide_delete_2

   Translations deleted!

The ``lang`` must be a language code already declared in the
:data:`~django.conf.settings.LANGUAGES` setting. It is optional and if it is
not passed in, it is automatically set to the :term:`active language` code.

Resetting the translations
==========================

To reset the translations of the context's scope in a language use the
:meth:`~translations.context.Context.reset` method.
This resets the translations on the :ref:`translatable fields \
<specify-fields>` of the context's scope.

.. testsetup:: guide_reset

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

To reset the translations of the defined scope for a model instance:

.. testcode:: guide_reset

   from sample.models import Continent
   from translations.context import Context

   # fetch an instance
   europe = Continent.objects.get(code='EU')

   # initiate context
   with Context(europe, 'countries', 'countries__cities') as context:
       # changes happened to the fields, create, read, update, delete, etc...

       # reset the translations
       context.reset()

       # use the instance like before
       print(europe)
       print(europe.countries.all()[0])
       print(europe.countries.all()[0].cities.all()[0])

.. testoutput:: guide_reset

   Europe
   Germany
   Cologne

To reset the translations of the defined scope for a queryset:

.. testcode:: guide_reset

   from sample.models import Continent
   from translations.context import Context

   # fetch a queryset
   continents = Continent.objects.all()

   # initiate context
   with Context(continents, 'countries', 'countries__cities') as context:
       # changes happened to the fields, create, read, update, delete, etc...

       # reset the translations
       context.reset()

       # use the queryset like before
       print(continents[0])
       print(continents[0].countries.all()[0])
       print(continents[0].countries.all()[0].cities.all()[0])

.. testoutput:: guide_reset

   Europe
   Germany
   Cologne

To reset the translations of the defined scope for a list of instances:

.. testcode:: guide_reset

   from sample.models import Continent
   from translations.context import Context

   # fetch a list of instances
   continents = list(Continent.objects.all())

   # initiate context
   with Context(continents, 'countries', 'countries__cities') as context:
       # changes happened to the fields, create, read, update, delete, etc...

       # reset the translations
       context.reset()

       # use the list of instances like before
       print(continents[0])
       print(continents[0].countries.all()[0])
       print(continents[0].countries.all()[0].cities.all()[0])

.. testoutput:: guide_reset

   Europe
   Germany
   Cologne

The ``lang`` must be a language code already declared in the
:data:`~django.conf.settings.LANGUAGES` setting. It is optional and if it is
not passed in, it is automatically set to the :term:`active language` code.
