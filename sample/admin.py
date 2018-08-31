from django.contrib import admin
from translations.admin import TranslatableAdmin, TranslationInline

from .models import Continent, Country, City


class GeoAdmin(TranslatableAdmin):
    inlines = [TranslationInline]


class ContinentAdmin(TranslatableAdmin):
    inlines = [TranslationInline]


class CountryAdmin(TranslatableAdmin):
    inlines = [TranslationInline]


class CityAdmin(TranslatableAdmin):
    inlines = [TranslationInline]


admin.site.register(Continent, ContinentAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(City, CityAdmin)
