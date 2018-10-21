*****
Query
*****

.. module:: translations.query

This module contains the query utilities for the Translations app.

.. function:: _fetch_translations_query_getter(model, lang)

   Return the translations query getter specialized for a model and some
   language(s).

   Returns the function that can be used to convert lookups and queries of the
   model to their equivalent for searching the translations of that lookup or
   query in the specified language(s).

   :param model: The model which the translations query getter is specialized
       for.
   :type model: type(~django.db.models.Model)
   :param lang: The lang which the translations query getter is specialized
       for.
   :type lang: str or list(str)
   :return: The translations query getter specialized for the model and the
       language.
   :rtype: function

   To fetch the translations query getter specialized for a model and a
   language:

   .. testcode:: _fetch_translations_query_getter

      from sample.models import Continent
      from translations.query import _fetch_translations_query_getter

      getter = _fetch_translations_query_getter(Continent, 'de')
      query = getter(countries__name__icontains='Deutsch')

      # output
      print(query)

   .. testoutput:: _fetch_translations_query_getter

      (AND:
          ('countries__translations__field', 'name'),
          ('countries__translations__language', 'de'),
          ('countries__translations__text__icontains', 'Deutsch'),
      )

   To fetch the translations query getter specialized for a model and some
   languages:

   .. testcode:: _fetch_translations_query_getter

      from sample.models import Continent
      from translations.query import _fetch_translations_query_getter

      getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])
      query = getter(countries__name__icontains='Deutsch')

      print(query)

   .. testoutput:: _fetch_translations_query_getter

      (AND:
          ('countries__translations__field', 'name'),
          ('countries__translations__language__in', ['de', 'tr']),
          ('countries__translations__text__icontains', 'Deutsch'),
      )

.. class:: TQ(~django.db.models.Q)

   Encapsulate translation filters as objects that can then be combined
   logically (using `&` and `|`).

   .. method:: __init__(self, *args, **kwargs)

      Initialize a `TQ` with the default `Q` parameters and some
      language(s) to apply on the filter.

      :param args: The arguments of
          the :class:`default Q <django.db.models.Q>`\
          's :meth:`~django.db.models.Q.__init__` method.
      :type args: list
      :param kwargs: The keyword arguments of
          the :class:`default Q <django.db.models.Q>`\
          's :meth:`~django.db.models.Q.__init__` method.
      :type kwargs: dict
      :param _lang: The language(s) to apply on the filter.
      :type _lang: str or list(str)
      :raise ValueError: If the language code is not included in
          the :data:`~django.conf.settings.LANGUAGES` setting.

      .. testsetup:: init

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

      To Initialize a `TQ`:

      .. testcode:: init

         from sample.models import Continent
         from translations.query import TQ

         continents = Continent.objects.filter(
             TQ(countries__cities__name__startswith='Köl', _lang='de') |
             TQ(countries__cities__name__startswith='Kol', _lang='tr')
         ).distinct()

         print(continents)

      .. testoutput:: init

         <TranslatableQuerySet [
             <Continent: Europe>,
         ]>
