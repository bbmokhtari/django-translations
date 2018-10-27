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

   To fetch the translations query getter specialized for a model and some
   language(s) (a custom language):

   .. testcode:: _fetch_translations_query_getter

      from sample.models import Continent
      from translations.query import _fetch_translations_query_getter

      getter = _fetch_translations_query_getter(Continent, 'de')
      query = getter(countries__name__icontains='Deutsch')

      # output
      print(query)

   .. testoutput:: _fetch_translations_query_getter

      (AND:
          (AND:
              ('countries__translations__field', 'name'),
              ('countries__translations__language', 'de'),
              ('countries__translations__text__icontains', 'Deutsch'),
          ),
      )

   To fetch the translations query getter specialized for a model and some
   language(s) (multiple custom languages):

   .. testcode:: _fetch_translations_query_getter

      from sample.models import Continent
      from translations.query import _fetch_translations_query_getter

      getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])
      query = getter(countries__name__icontains='Deutsch')

      print(query)

   .. testoutput:: _fetch_translations_query_getter

      (AND:
          (AND:
              ('countries__translations__field', 'name'),
              ('countries__translations__language__in', ['de', 'tr']),
              ('countries__translations__text__icontains', 'Deutsch'),
          ),
      )

.. class:: TQ

   Encapsulate translation filters as objects that can then be combined
   logically (using `&` and `|`).

   To query using :class:`TQ`:

   .. testsetup:: tq

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

   .. testcode:: tq

      from sample.models import Continent
      from translations.query import TQ

      continents = Continent.objects.filter(
          TQ(countries__cities__name__startswith='Köln', _lang='de') |
          TQ(countries__cities__name__startswith='Koln', _lang='tr') |
          TQ(countries__cities__name__startswith='Cologne', _lang='en')
      ).distinct()

      print(continents)

   .. testoutput:: tq

      <TranslatableQuerySet [
          <Continent: Europe>,
      ]>

   .. method:: __init__(self, *args, **kwargs)

      Initialize a :class:`TQ` with :class:`~django.db.models.Q` arguments and
      some language(s).

      Receives the normal :class:`~django.db.models.Q` arguments and also some
      language(s) to use for querying.

      :param args: The arguments of
          the :class:`~django.db.models.Q`\
          's :meth:`~django.db.models.Q.__init__` method.
      :type args: list
      :param kwargs: The keyword arguments of
          the :class:`~django.db.models.Q`\
          's :meth:`~django.db.models.Q.__init__` method.
      :type kwargs: dict
      :param _lang: The language(s) to use for querying.
      :type _lang: str or list or None
      :raise ValueError: If the language code is not included in
          the :data:`~django.conf.settings.LANGUAGES` setting.

      To Initialize a :class:`TQ`:

      .. testcode:: init

         from translations.query import TQ

         tq = TQ(countries__cities__name__startswith='Köln', _lang='de')

         print(tq)
         print(tq.lang)

      .. testoutput:: init

         (AND:
             ('countries__cities__name__startswith', 'Köln'),
         )
         de
