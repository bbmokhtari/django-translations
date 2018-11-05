**********
Ref: Query
**********

.. module:: translations.query

This module contains the query utilities for the Translations app.

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

   .. testcode:: _fetch_translations_query_getter.1

      from translations.query import _fetch_translations_query_getter
      from sample.models import Continent

      getter = _fetch_translations_query_getter(Continent, 'de')
      query = getter(countries__name__icontains='Deutsch')

      # output
      print(query)

   .. testoutput:: _fetch_translations_query_getter.1

      (AND:
          (AND:
              ('countries__translations__field', 'name'),
              ('countries__translations__language', 'de'),
              ('countries__translations__text__icontains', 'Deutsch'),
          ),
      )

   To fetch the translations query getter specialized for a model and some
   language(s) (multiple custom languages):

   .. testcode:: _fetch_translations_query_getter.2

      from translations.query import _fetch_translations_query_getter
      from sample.models import Continent

      getter = _fetch_translations_query_getter(Continent, ['de', 'tr'])
      query = getter(countries__name__icontains='Deutsch')

      print(query)

   .. testoutput:: _fetch_translations_query_getter.2

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

   Provides functionalities like :meth:`__call__` to Specialize
   the :class:`TQ` for some language(s) and :meth:`_combine` to
   combine :class:`TQ` objects logically with
   other :class:`~django.db.models.Q` objects.

   .. testsetup:: TQ.1

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

   To use :class:`TQ`:

   .. testcode:: TQ.1

      from translations.query import TQ
      from sample.models import Continent

      continents = Continent.objects.filter(
          TQ(
              countries__cities__name__startswith='Cologne',
          )         # use probe language (default English) for this query
          |         # logical combinator
          TQ(
              countries__cities__name__startswith='Köln',
          )('de')   # use German for this query
      ).distinct()

      print(continents)

   .. testoutput:: TQ.1

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

      .. testcode:: TQ.__init__.1

         from translations.query import TQ

         tq = TQ(countries__cities__name__startswith='Köln')

         print(tq)

      .. testoutput:: TQ.__init__.1

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

      .. testcode:: TQ.__deepcopy__.1

         import copy
         from translations.query import TQ

         tq = TQ(countries__cities__name__startswith='Köln')('de')
         cp = copy.deepcopy(tq)

         print(cp)
         print(cp.lang)

      .. testoutput:: TQ.__deepcopy__.1

         (AND:
             ('countries__cities__name__startswith', 'Köln'),
         )
         de

   .. method:: __call__(lang=None)

      Specialize the :class:`TQ` for some language(s).

      Causes the :class:`TQ` to be queried in the specified language(s).

      :param lang: The language(s) to specialize the query for.
          ``None`` means use the :term:`active language` code.
      :type lang: str or list or None
      :raise ValueError: If the language code(s) is(are) not included in
          the :data:`~django.conf.settings.LANGUAGES` setting.

      To specialize the :class:`TQ` for some language(s):

      .. testcode:: TQ.__call__.1

         from translations.query import TQ

         tq = TQ(countries__cities__name__startswith='Köln')('de')

         print(tq)
         print(tq.lang)

      .. testoutput:: TQ.__call__.1

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

      .. testcode:: TQ._combine.1

         from translations.query import TQ

         tq1 = TQ(countries__cities__name__startswith='Köln')('de')
         tq2 = TQ(countries__cities__name__startswith='Koln')('tr')

         print(tq1 | tq2)

      .. testoutput:: TQ._combine.1

         (OR:
             (AND:
                 ('countries__cities__name__startswith', 'Koln'),
             ),
             (AND:
                 ('countries__cities__name__startswith', 'Köln'),
             ),
         )
