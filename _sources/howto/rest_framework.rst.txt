*************************************
How to: Integrate with Rest Framework
*************************************

In case of generic views override the ``get_queryset`` method:

.. code-block:: python

   from rest_framework import generics

   from .models import Continent
   from .serializers import ContinentSerializer


   class ContinentListView(generics.ListAPIView):
       queryset = Continent.objects.all()
       serializer_class = ContinentSerializer

       def get_queryset(self):
           queryset = super(ContinentListView, self).get_queryset()
           return queryset.translate_related(
               'countries',
               'countries__cities',
           ).translate()


   class ContinentView(generics.RetrieveAPIView):
       queryset = Continent.objects.all()
       serializer_class = ContinentSerializer

       def get_queryset(self):
           queryset = super(ContinentView, self).get_queryset()
           return queryset.translate_related(
               'countries',
               'countries__cities',
           ).translate()

Also in case of viewsets override the ``get_queryset`` method:

.. code-block:: python

   from rest_framework import viewsets

   from .models import Continent
   from .serializers import ContinentSerializer


   class ContinentViewSet(viewsets.ModelViewSet):
       queryset = Continent.objects.all()
       serializer_class = ContinentSerializer

       def get_queryset(self):
           queryset = super(ContinentViewSet, self).get_queryset()
           return queryset.translate_related(
               'countries',
               'countries__cities',
           ).translate()

In case of a custom view use
the :doc:`extended queryset capabilities <../guide/querysets>`.

.. note::

   Note that the ``translate`` method in the examples above is not receiving a
   language code. This means it will use the :term:`active language` code
   automatically, which is a good practice to keep up in the views.
