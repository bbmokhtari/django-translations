from rest_framework import serializers

from .models import City, Country, Continent


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = ('id', 'name', 'denonym',)


class CountrySerializer(serializers.ModelSerializer):
    cities = CitySerializer(many=True)

    class Meta:
        model = Country
        fields = ('name', 'denonym', 'code', 'cities',)


class ContinentSerializer(serializers.ModelSerializer):
    countries = CountrySerializer(many=True)

    class Meta:
        model = Continent
        fields = ('name', 'denonym', 'code', 'countries',)
