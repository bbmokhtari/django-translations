from django.contrib import admin
from translations.admin import TranslatableAdmin, TranslationInline

from .models import Timezone, Continent, Country, City


class TimezoneAdmin(TranslatableAdmin):
    inlines = [TranslationInline]


class ContinentAdmin(TranslatableAdmin):
    inlines = [TranslationInline]


class CountryAdmin(TranslatableAdmin):
    inlines = [TranslationInline]


class CityAdmin(TranslatableAdmin):
    inlines = [TranslationInline]


admin.site.register(Timezone, TimezoneAdmin)
admin.site.register(Continent, ContinentAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(City, CityAdmin)
