*****
Query
*****

.. module:: translations.query

This module contains the quereis for the Translations app.

.. function:: _get_translations_query_fetcher(model, lang)

   Return the translations query getter specialized for a model and some
   language.

   Returns a function that can be used to convert lookups and queries of a
   model to their equivalent for searching the translations of that lookup or
   query in a language.

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
   language:

   .. testcode:: _get_translations_query_fetcher

      from sample.models import Continent
      from translations.query import _get_translations_query_fetcher

      getter = _get_translations_query_fetcher(Continent, 'de')
      
      query = getter(countries__name__icontains='Deutsch')

      # output
      print(query)

   .. testoutput:: _get_translations_query_fetcher

      (AND:
          ('countries__translations__field', 'name'),
          ('countries__translations__language', 'de'),
          ('countries__translations__text__icontains', 'Deutsch'),
      )
