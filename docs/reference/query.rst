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
   :param lang: The language(s) which the translations query getter is
       specialized for.
   :type lang: str or list(str)
   :return: The translations query getter specialized for the model and the
       language(s).
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

   Encapsulate translation queries as objects that can then be combined
   logically (using `&` and `|`).

   Provides functionalities like :meth:`_combine` to combine :class:`TQ`
   objects logically with another :class:`~django.db.models.Q` objects
   using some probe language(s).

   To use :class:`TQ`:

   .. testsetup:: TQ

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

   .. testcode:: TQ

      from sample.models import Continent
      from translations.query import TQ

      continents = Continent.objects.filter(
          TQ(
              countries__cities__name__startswith='Cologne',
          )('en')         # use English for this query
          |               # logical combinator
          TQ(
              countries__cities__name__startswith='Köln',
          )('de')         # use German for this query
      ).distinct()

      print(continents)

   .. testoutput:: TQ

      <TranslatableQuerySet [
          <Continent: Europe>,
      ]>

   .. method:: __init__(*args, **kwargs)

      Initialize a :class:`TQ` with :class:`~django.db.models.Q` arguments.

      This is an overriden version of
      the :class:`~django.db.models.Q`\ 's
      :meth:`~django.db.models.Q.__init__` method.
      It defines custom translation configurations on
      the :class:`TQ`.

      :param args: The arguments of
          the :class:`~django.db.models.Q`\
          's :meth:`~django.db.models.Q.__init__` method.
      :type args: list
      :param kwargs: The keyword arguments of
          the :class:`~django.db.models.Q`\
          's :meth:`~django.db.models.Q.__init__` method.
      :type kwargs: dict

      To Initialize a :class:`TQ`:

      .. testcode:: init

         from translations.query import TQ

         tq = TQ(countries__cities__name__startswith='Köln')

         print(tq)

      .. testoutput:: init

         (AND:
             ('countries__cities__name__startswith', 'Köln'),
         )

   .. method:: __deepcopy__(memodict)

      Return a copy of the :class:`TQ` object.

      This is an overriden version of
      the :class:`~django.db.models.Q`\ 's
      :meth:`~django.db.models.Q.__deepcopy__` method.
      It copies the custom translation configurations from
      the current :class:`TQ` to
      the copied :class:`TQ`.

      :param memodict: The argument of
          the :class:`~django.db.models.Q`\
          's :meth:`~django.db.models.Q.__deepcopy__` method.
      :return: The copy of the :class:`TQ` object.
      :rtype: TQ

      To get a copy of a :class:`TQ` object:

      .. testcode:: deepcopy

         from translations.query import TQ
         import copy

         tq = TQ(countries__cities__name__startswith='Köln')('de')
         cp = copy.deepcopy(tq)

         print(cp)
         print(cp.lang)

      .. testoutput:: deepcopy

         (AND:
             ('countries__cities__name__startswith', 'Köln'),
         )
         de

   .. method:: __call__(lang)

      Specialize the :class:`TQ` for some language(s).

      Causes the :class:`TQ` to be queried in the specified language(s).

      :param lang: The language(s) to specialize the query for.
      :type lang: str or list or None
      :raise ValueError: If the language code(s) is(are) not included in
          the :data:`~django.conf.settings.LANGUAGES` setting.

      To specialize the :class:`TQ` for some language(s):

      .. testcode:: call

         from translations.query import TQ

         tq = TQ(countries__cities__name__startswith='Köln')('de')

         print(tq)
         print(tq.lang)

      .. testoutput:: call

         (AND:
             ('countries__cities__name__startswith', 'Köln'),
         )
         de

   .. method:: _combine(other, conn)

      Return the result of logical combination with
      another :class:`~django.db.models.Q` object.

      This is an overriden version of
      the :class:`~django.db.models.Q`\ 's
      :meth:`~django.db.models.Q._combine` method.
      It combines the :class:`TQ` object with
      another :class:`~django.db.models.Q` object logically.

      :param other: the other :class:`~django.db.models.Q` object.
      :type other: ~django.db.models.Q
      :param conn: The type of logical combination.
      :type conn: str
      :return: the result of logical combination with
          the other :class:`~django.db.models.Q` object.
      :rtype: ~django.db.models.Q

      To get the result of logical combination with
      another :class:`~django.db.models.Q` object:

      .. testcode:: combine

         from translations.query import TQ

         tq1 = TQ(countries__cities__name__startswith='Köln')('de')
         tq2 = TQ(countries__cities__name__startswith='Koln')('tr')

         print(tq1 | tq2)

      .. testoutput:: combine

         (OR:
             (AND:
                 ('countries__cities__name__startswith', 'Koln'),
             ),
             (AND:
                 ('countries__cities__name__startswith', 'Köln'),
             ),
         )
