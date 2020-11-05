from rest_framework import generics

from .models import Continent
from .serializers import ContinentSerializer


class ContinentListView(generics.ListAPIView):
    queryset = Continent.objects.all()
    serializer_class = ContinentSerializer

    def get_queryset(self):
        """
        Return queryset.

        Args:
            self: (todo): write your description
        """
        queryset = super(ContinentListView, self).get_queryset()
        return queryset.translate_related(
            'countries',
            'countries__cities',
        ).translate()


class ContinentView(generics.RetrieveAPIView):
    queryset = Continent.objects.all()
    serializer_class = ContinentSerializer

    def get_queryset(self):
        """
        Return the queryset of the queryset.

        Args:
            self: (todo): write your description
        """
        queryset = super(ContinentView, self).get_queryset()
        return queryset.translate_related(
            'countries',
            'countries__cities',
        ).translate()
