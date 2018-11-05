**************
Guide: Context
**************

This module provides an in depth knowledge of the Translations context.

.. important::

   The examples are assumed to CRUD this dataset.

   +---------------+-------------+-------------+
   | Type\\Lang    | English     | German      |
   +===============+=============+=============+
   | Continent     | Europe      | Europa      |
   |               +-------------+-------------+
   |               | Asia        | Asien       |
   +---------------+-------------+-------------+
   | Country       | Germany     | Deutschland |
   |               +-------------+-------------+
   |               | South Korea | Südkorea    |
   +---------------+-------------+-------------+
   | City          | Cologne     | Köln        |
   |               +-------------+-------------+
   |               | Seoul       | Seul        |
   +---------------+-------------+-------------+

   Please memorize this dataset in order to understand the examples better.

What is context
===============

When something is going to be stated it can be done so in the context of a
certain language.

Initialize a context
====================

To initialize a context use the :class:`~translations.context.Context`
class.
The instances to be affected by the context must be defined in the
initialization, meaning which entity and what relations of it
should the context act upon. This is called the context's purview.

All the actions like `reading the translations`_,
`updating the translations`_, etc only affects the
objects in the defined purview.

.. testsetup:: Context.__init__.1

   from sample.utils import create_samples

   create_samples(
       continent_names=['europe', 'asia'],
       country_names=['germany', 'south korea'],
       city_names=['cologne', 'seoul'],
       continent_fields=['name', 'denonym'],
       country_fields=['name', 'denonym'],
       city_fields=['name', 'denonym'],
       langs=['de']
   )

.. testsetup:: Context.__init__.2

   from sample.utils import create_samples

   create_samples(
       continent_names=['europe', 'asia'],
       country_names=['germany', 'south korea'],
       city_names=['cologne', 'seoul'],
       continent_fields=['name', 'denonym'],
       country_fields=['name', 'denonym'],
       city_fields=['name', 'denonym'],
       langs=['de']
   )

.. testsetup:: Context.__init__.3

   from sample.utils import create_samples

   create_samples(
       continent_names=['europe', 'asia'],
       country_names=['germany', 'south korea'],
       city_names=['cologne', 'seoul'],
       continent_fields=['name', 'denonym'],
       country_fields=['name', 'denonym'],
       city_fields=['name', 'denonym'],
       langs=['de']
   )

To initialize a context for an instance and some relations of it:

.. testcode:: Context.__init__.1

   from translations.context import Context
   from sample.models import Continent

   europe = Continent.objects.get(code='EU')
   relations = ('countries', 'countries__cities',)

   # initialize context
   with Context(europe, *relations) as context:
       print('Context initialized!')

.. testoutput:: Context.__init__.1

   Context initialized!

To initialize a context for a queryset and some relations of it:

.. testcode:: Context.__init__.2

   from translations.context import Context
   from sample.models import Continent

   continents = Continent.objects.all()
   relations = ('countries', 'countries__cities',)

   # initialize context
   with Context(continents, *relations) as context:
       print('Context initialized!')

.. testoutput:: Context.__init__.2

   Context initialized!

To initialize a context for a list of instances and some relations of it:

.. testcode:: Context.__init__.3

   from translations.context import Context
   from sample.models import Continent

   continents = list(Continent.objects.all())
   relations = ('countries', 'countries__cities',)

   # initialize context
   with Context(continents, *relations) as context:
       print('Context initialized!')

.. testoutput:: Context.__init__.3

   Context initialized!

The entity must be a model instance, a queryset or a list of model
instances.
The model of the entity must be
:ref:`translatable <models.Translatable>`.

The relations must be an unpacked list of strings.
They may be separated by ``__``\ s to represent a deeply nested relation.
The model of the relations must be
:ref:`translatable <models.Translatable>`.

.. note::

   It is **recommended** for the relations of the entity to be
   prefetched before initializing a context,
   in order to reach optimal performance.

   To do this use
   :meth:`~django.db.models.query.QuerySet.select_related`,
   :meth:`~django.db.models.query.QuerySet.prefetch_related` or
   :func:`~django.db.models.prefetch_related_objects`.

Creating the translations
=========================

To create the translations of the context's purview in a language
use the :meth:`~translations.context.Context.create` method.
This creates the translations using the :ref:`translatable fields \
<models.Translatable.TranslatableMeta.fields>` of the context's purview.
It accepts a language code which determines the language to
create the translation in.

.. testsetup:: Context.create.1

   from sample.utils import create_samples

   create_samples(
       continent_names=['europe', 'asia'],
       country_names=['germany', 'south korea'],
       city_names=['cologne', 'seoul'],
       langs=['de']
   )

.. testsetup:: Context.create.2

   from sample.utils import create_samples

   create_samples(
       continent_names=['europe', 'asia'],
       country_names=['germany', 'south korea'],
       city_names=['cologne', 'seoul'],
       langs=['de']
   )

.. testsetup:: Context.create.3

   from sample.utils import create_samples

   create_samples(
       continent_names=['europe', 'asia'],
       country_names=['germany', 'south korea'],
       city_names=['cologne', 'seoul'],
       langs=['de']
   )

To create the translations of an instance and some relations of it:

.. testcode:: Context.create.1

   from translations.context import Context
   from sample.models import Continent

   europe = Continent.objects.get(code='EU')
   relations = ('countries', 'countries__cities',)

   with Context(europe, *relations) as context:

       # change the instance like before
       europe.name = 'Europa'
       europe.countries.all()[0].name = 'Deutschland'
       europe.countries.all()[0].cities.all()[0].name = 'Köln'

       # create the translations in German
       context.create('de')

       print('Translations created!')

.. testoutput:: Context.create.1

   Translations created!

To create the translations of a queryset and some relations of it:

.. testcode:: Context.create.2

   from translations.context import Context
   from sample.models import Continent

   continents = Continent.objects.all()
   relations = ('countries', 'countries__cities',)

   with Context(continents, *relations) as context:

       # change the queryset like before
       continents[0].name = 'Europa'
       continents[0].countries.all()[0].name = 'Deutschland'
       continents[0].countries.all()[0].cities.all()[0].name = 'Köln'

       # create the translations in German
       context.create('de')

       print('Translations created!')

.. testoutput:: Context.create.2

   Translations created!

To create the translations of a list of instances and some relations of it:

.. testcode:: Context.create.3

   from translations.context import Context
   from sample.models import Continent

   continents = list(Continent.objects.all())
   relations = ('countries', 'countries__cities',)

   with Context(continents, *relations) as context:

       # change the list of instances like before
       continents[0].name = 'Europa'
       continents[0].countries.all()[0].name = 'Deutschland'
       continents[0].countries.all()[0].cities.all()[0].name = 'Köln'

       # create the translations in German
       context.create('de')

       print('Translations created!')

.. testoutput:: Context.create.3

   Translations created!

The language code must already be declared in the
``LANGUAGES`` setting. It is optional and if it is
not passed in, it is automatically set to the :term:`active language` code.

Creating duplicate translations for a field raises
``IntegrityError``, to update the translations check out
`updating the translations`_.

.. note::

   Creating only affects the translatable fields that have changed.

   If the value of a field is not changed, the translation for it is not
   created. (No need to set all the translatable fields beforehand)

Reading the translations
========================

To read the translations of the context's purview in a language
use the :meth:`~translations.context.Context.read` method.
This reads the translations onto the :ref:`translatable fields \
<models.Translatable.TranslatableMeta.fields>` of the context's purview.
It accepts a language code which determines the language to
read the translation in.

.. testsetup:: Context.read.1

   from sample.utils import create_samples

   create_samples(
       continent_names=['europe', 'asia'],
       country_names=['germany', 'south korea'],
       city_names=['cologne', 'seoul'],
       continent_fields=['name', 'denonym'],
       country_fields=['name', 'denonym'],
       city_fields=['name', 'denonym'],
       langs=['de']
   )

.. testsetup:: Context.read.2

   from sample.utils import create_samples

   create_samples(
       continent_names=['europe', 'asia'],
       country_names=['germany', 'south korea'],
       city_names=['cologne', 'seoul'],
       continent_fields=['name', 'denonym'],
       country_fields=['name', 'denonym'],
       city_fields=['name', 'denonym'],
       langs=['de']
   )

.. testsetup:: Context.read.3

   from sample.utils import create_samples

   create_samples(
       continent_names=['europe', 'asia'],
       country_names=['germany', 'south korea'],
       city_names=['cologne', 'seoul'],
       continent_fields=['name', 'denonym'],
       country_fields=['name', 'denonym'],
       city_fields=['name', 'denonym'],
       langs=['de']
   )

To read the translations of an instance and some relations of it:

.. testcode:: Context.read.1

   from translations.context import Context
   from sample.models import Continent

   europe = Continent.objects.get(code='EU')
   relations = ('countries', 'countries__cities',)

   with Context(europe, *relations) as context:

       # read the translations in German
       context.read('de')

       # use the instance like before
       print(europe)
       print(europe.countries.all())
       print(europe.countries.all()[0].cities.all())

.. testoutput:: Context.read.1

   Europa
   <TranslatableQuerySet [
       <Country: Deutschland>,
   ]>
   <TranslatableQuerySet [
       <City: Köln>,
   ]>

To read the translations of a queryset and some relations of it:

.. testcode:: Context.read.2

   from translations.context import Context
   from sample.models import Continent

   continents = Continent.objects.all()
   relations = ('countries', 'countries__cities',)

   with Context(continents, *relations) as context:

       # read the translations in German
       context.read('de')

       # use the queryset like before
       print(continents)
       print(continents[0].countries.all())
       print(continents[0].countries.all()[0].cities.all())

.. testoutput:: Context.read.2

   <TranslatableQuerySet [
       <Continent: Europa>,
       <Continent: Asien>,
   ]>
   <TranslatableQuerySet [
       <Country: Deutschland>,
   ]>
   <TranslatableQuerySet [
       <City: Köln>,
   ]>

To read the translations of a list of instances and some relations of it:

.. testcode:: Context.read.3

   from translations.context import Context
   from sample.models import Continent

   continents = list(Continent.objects.all())
   relations = ('countries', 'countries__cities',)

   with Context(continents, *relations) as context:

       # read the translations in German
       context.read('de')

       # use the list of instances like before
       print(continents)
       print(continents[0].countries.all())
       print(continents[0].countries.all()[0].cities.all())

.. testoutput:: Context.read.3

   [
       <Continent: Europa>,
       <Continent: Asien>,
   ]
   <TranslatableQuerySet [
       <Country: Deutschland>,
   ]>
   <TranslatableQuerySet [
       <City: Köln>,
   ]>

The language code must already be declared in the
``LANGUAGES`` setting. It is optional and if it is
not passed in, it is automatically set to the :term:`active language` code.

.. note::

   Reading only affects the translatable fields that have a translation.

   If there is no translation for a field, the value of the field is not
   changed. (It remains what it was before)

.. warning::

   .. testsetup:: Context.read.warning.1

      from sample.utils import create_samples

      create_samples(
          continent_names=['europe', 'asia'],
          country_names=['germany', 'south korea'],
          city_names=['cologne', 'seoul'],
          continent_fields=['name', 'denonym'],
          country_fields=['name', 'denonym'],
          city_fields=['name', 'denonym'],
          langs=['de']
      )

   .. testsetup:: Context.read.warning.2

      from sample.utils import create_samples

      create_samples(
          continent_names=['europe', 'asia'],
          country_names=['germany', 'south korea'],
          city_names=['cologne', 'seoul'],
          continent_fields=['name', 'denonym'],
          country_fields=['name', 'denonym'],
          city_fields=['name', 'denonym'],
          langs=['de']
      )

   Any methods on the relations queryset which imply
   a database query will reset previously translated results:

   .. testcode:: Context.read.warning.1

      from translations.context import Context
      from sample.models import Continent

      continents = Continent.objects.prefetch_related(
          'countries',
      )

      with Context(continents, 'countries') as context:
          context.read('de')
          # querying after translation
          print(continents[0].countries.exclude(name=''))

   .. testoutput:: Context.read.warning.1

      <TranslatableQuerySet [
          <Country: Germany>,
      ]>

   In some cases the querying can be done before the translation:

   .. testcode:: Context.read.warning.2

      from django.db.models import Prefetch
      from translations.context import Context
      from sample.models import Continent, Country

      # querying before translation
      continents = Continent.objects.prefetch_related(
          Prefetch(
              'countries',
              queryset=Country.objects.exclude(name=''),
          ),
      )

      with Context(continents, 'countries') as context:
          context.read('de')
          print(continents[0].countries.all())

   .. testoutput:: Context.read.warning.2

      <TranslatableQuerySet [
          <Country: Deutschland>,
      ]>

Updating the translations
=========================

To update the translations of the context's purview in a language
use the :meth:`~translations.context.Context.update` method.
This updates the translations using the :ref:`translatable fields \
<models.Translatable.TranslatableMeta.fields>` of the context's purview.
It accepts a language code which determines the language to
update the translation in.

.. testsetup:: Context.update.1

   from sample.utils import create_samples

   create_samples(
       continent_names=['europe', 'asia'],
       country_names=['germany', 'south korea'],
       city_names=['cologne', 'seoul'],
       continent_fields=['name', 'denonym'],
       country_fields=['name', 'denonym'],
       city_fields=['name', 'denonym'],
       langs=['de']
   )

.. testsetup:: Context.update.2

   from sample.utils import create_samples

   create_samples(
       continent_names=['europe', 'asia'],
       country_names=['germany', 'south korea'],
       city_names=['cologne', 'seoul'],
       continent_fields=['name', 'denonym'],
       country_fields=['name', 'denonym'],
       city_fields=['name', 'denonym'],
       langs=['de']
   )

.. testsetup:: Context.update.3

   from sample.utils import create_samples

   create_samples(
       continent_names=['europe', 'asia'],
       country_names=['germany', 'south korea'],
       city_names=['cologne', 'seoul'],
       continent_fields=['name', 'denonym'],
       country_fields=['name', 'denonym'],
       city_fields=['name', 'denonym'],
       langs=['de']
   )

To update the translations of an instance and some relations of it:

.. testcode:: Context.update.1

   from translations.context import Context
   from sample.models import Continent

   europe = Continent.objects.get(code='EU')
   relations = ('countries', 'countries__cities',)

   with Context(europe, *relations) as context:

       # change the instance like before
       europe.name = 'Europa (changed)'
       europe.countries.all()[0].name = 'Deutschland (changed)'
       europe.countries.all()[0].cities.all()[0].name = 'Köln (changed)'

       # update the translations in German
       context.update('de')

       print('Translations updated!')

.. testoutput:: Context.update.1

   Translations updated!

To update the translations of a queryset and some relations of it:

.. testcode:: Context.update.2

   from translations.context import Context
   from sample.models import Continent

   continents = Continent.objects.all()
   relations = ('countries', 'countries__cities',)

   with Context(continents, *relations) as context:

       # change the queryset like before
       continents[0].name = 'Europa (changed)'
       continents[0].countries.all()[0].name = 'Deutschland (changed)'
       continents[0].countries.all()[0].cities.all()[0].name = 'Köln (changed)'

       # update the translations in German
       context.update('de')

       print('Translations updated!')

.. testoutput:: Context.update.2

   Translations updated!

To update the translations of a list of instances and some relations of it:

.. testcode:: Context.update.3

   from translations.context import Context
   from sample.models import Continent

   continents = list(Continent.objects.all())
   relations = ('countries', 'countries__cities',)

   with Context(continents, *relations) as context:

       # change the list of instances like before
       continents[0].name = 'Europa (changed)'
       continents[0].countries.all()[0].name = 'Deutschland (changed)'
       continents[0].countries.all()[0].cities.all()[0].name = 'Köln (changed)'

       # update the translations in German
       context.update('de')

       print('Translations updated!')

.. testoutput:: Context.update.3

   Translations updated!

The language code must already be declared in the
``LANGUAGES`` setting. It is optional and if it is
not passed in, it is automatically set to the :term:`active language` code.

.. note::

   Updating only affects the translatable fields that have changed.

   If the value of a field is not changed, the translation for it is not
   updated. (No need to initialize all the translatable fields beforehand)

Deleting the translations
=========================

To delete the translations of the context's purview in a language
use the :meth:`~translations.context.Context.delete` method.
This deletes the translations for the :ref:`translatable fields \
<models.Translatable.TranslatableMeta.fields>` of the context's purview.
It accepts a language code which determines the language to
delete the translation in.

.. testsetup:: Context.delete.1

   from sample.utils import create_samples

   create_samples(
       continent_names=['europe', 'asia'],
       country_names=['germany', 'south korea'],
       city_names=['cologne', 'seoul'],
       continent_fields=['name', 'denonym'],
       country_fields=['name', 'denonym'],
       city_fields=['name', 'denonym'],
       langs=['de']
   )

.. testsetup:: Context.delete.2

   from sample.utils import create_samples

   create_samples(
       continent_names=['europe', 'asia'],
       country_names=['germany', 'south korea'],
       city_names=['cologne', 'seoul'],
       continent_fields=['name', 'denonym'],
       country_fields=['name', 'denonym'],
       city_fields=['name', 'denonym'],
       langs=['de']
   )

.. testsetup:: Context.delete.3

   from sample.utils import create_samples

   create_samples(
       continent_names=['europe', 'asia'],
       country_names=['germany', 'south korea'],
       city_names=['cologne', 'seoul'],
       continent_fields=['name', 'denonym'],
       country_fields=['name', 'denonym'],
       city_fields=['name', 'denonym'],
       langs=['de']
   )

To delete the translations of an instance and some relations of it:

.. testcode:: Context.delete.1

   from translations.context import Context
   from sample.models import Continent

   europe = Continent.objects.get(code='EU')
   relations = ('countries', 'countries__cities',)

   with Context(europe, *relations) as context:

       # delete the translations in German
       context.delete('de')

       print('Translations deleted!')

.. testoutput:: Context.delete.1

   Translations deleted!

To delete the translations of a queryset and some relations of it:

.. testcode:: Context.delete.2

   from translations.context import Context
   from sample.models import Continent

   continents = Continent.objects.all()
   relations = ('countries', 'countries__cities',)

   with Context(continents, *relations) as context:

       # delete the translations in German
       context.delete('de')

       print('Translations deleted!')

.. testoutput:: Context.delete.2

   Translations deleted!

To delete the translations of a list of instances and some relations of it:

.. testcode:: Context.delete.3

   from translations.context import Context
   from sample.models import Continent

   continents = list(Continent.objects.all())
   relations = ('countries', 'countries__cities',)

   with Context(continents, *relations) as context:

       # delete the translations in German
       context.delete('de')

       print('Translations deleted!')

.. testoutput:: Context.delete.3

   Translations deleted!

The language code must already be declared in the
``LANGUAGES`` setting. It is optional and if it is
not passed in, it is automatically set to the :term:`active language` code.

Resetting the translations
==========================

To reset the translations of the context's purview to the :term:`default language`
use the :meth:`~translations.context.Context.reset` method.
This resets the translations on the :ref:`translatable fields \
<models.Translatable.TranslatableMeta.fields>` of the context's purview.

.. testsetup:: Context.reset.1

   from sample.utils import create_samples

   create_samples(
       continent_names=['europe', 'asia'],
       country_names=['germany', 'south korea'],
       city_names=['cologne', 'seoul'],
       continent_fields=['name', 'denonym'],
       country_fields=['name', 'denonym'],
       city_fields=['name', 'denonym'],
       langs=['de']
   )

.. testsetup:: Context.reset.2

   from sample.utils import create_samples

   create_samples(
       continent_names=['europe', 'asia'],
       country_names=['germany', 'south korea'],
       city_names=['cologne', 'seoul'],
       continent_fields=['name', 'denonym'],
       country_fields=['name', 'denonym'],
       city_fields=['name', 'denonym'],
       langs=['de']
   )

.. testsetup:: Context.reset.3

   from sample.utils import create_samples

   create_samples(
       continent_names=['europe', 'asia'],
       country_names=['germany', 'south korea'],
       city_names=['cologne', 'seoul'],
       continent_fields=['name', 'denonym'],
       country_fields=['name', 'denonym'],
       city_fields=['name', 'denonym'],
       langs=['de']
   )

To reset the translations of an instance and some relations of it:

.. testcode:: Context.reset.1

   from translations.context import Context
   from sample.models import Continent

   europe = Continent.objects.get(code='EU')
   relations = ('countries', 'countries__cities',)

   with Context(europe, *relations) as context:

       # changes happened to the fields, create, read, update, delete, etc...
       context.read('de')

       # reset the translations
       context.reset()

       # use the instance like before
       print(europe)
       print(europe.countries.all())
       print(europe.countries.all()[0].cities.all())

.. testoutput:: Context.reset.1

   Europe
   <TranslatableQuerySet [
       <Country: Germany>,
   ]>
   <TranslatableQuerySet [
       <City: Cologne>,
   ]>

To reset the translations of a queryset and some relations of it:

.. testcode:: Context.reset.2

   from translations.context import Context
   from sample.models import Continent

   continents = Continent.objects.all()
   relations = ('countries', 'countries__cities',)

   with Context(continents, *relations) as context:

       # changes happened to the fields, create, read, update, delete, etc...
       context.read('de')

       # reset the translations
       context.reset()

       # use the queryset like before
       print(continents)
       print(continents[0].countries.all())
       print(continents[0].countries.all()[0].cities.all())

.. testoutput:: Context.reset.2

   <TranslatableQuerySet [
       <Continent: Europe>,
       <Continent: Asia>,
   ]>
   <TranslatableQuerySet [
       <Country: Germany>,
   ]>
   <TranslatableQuerySet [
       <City: Cologne>,
   ]>

To reset the translations of a list of instances and some relations of it:

.. testcode:: Context.reset.3

   from translations.context import Context
   from sample.models import Continent

   continents = list(Continent.objects.all())
   relations = ('countries', 'countries__cities',)

   with Context(continents, *relations) as context:

       # changes happened to the fields, create, read, update, delete, etc...
       context.read('de')

       # reset the translations
       context.reset()

       # use the list of instances like before
       print(continents)
       print(continents[0].countries.all())
       print(continents[0].countries.all()[0].cities.all())

.. testoutput:: Context.reset.3

   [
       <Continent: Europe>,
       <Continent: Asia>,
   ]
   <TranslatableQuerySet [
       <Country: Germany>,
   ]>
   <TranslatableQuerySet [
       <City: Cologne>,
   ]>
