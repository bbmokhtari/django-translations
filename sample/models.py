from django.db import models
from django.utils.translation import ugettext_lazy as _

from translations.models import Translatable


class Timezone(Translatable):
    name = models.CharField(
        verbose_name=_('name'),
        help_text=_('the name of the timezone'),
        max_length=32,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('timezone')
        verbose_name_plural = _('timezones')

    class TranslatableMeta:
        fields = []


class Continent(Translatable):
    name = models.CharField(
        verbose_name=_('name'),
        help_text=_('the name of the continent'),
        max_length=64,
    )
    denonym = models.CharField(
        verbose_name=_('denonym'),
        help_text=_('the denonym of the continent'),
        max_length=64,
        blank=True,
    )
    code = models.CharField(
        verbose_name=_('code'),
        help_text=_('the code of the continent'),
        max_length=2,
        unique=True,
        primary_key=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('continent')
        verbose_name_plural = _('continents')

    class TranslatableMeta:
        fields = ['name', 'denonym']


class Country(Translatable):
    name = models.CharField(
        verbose_name=_('name'),
        help_text=_('the name of the country'),
        max_length=64,
    )
    denonym = models.CharField(
        verbose_name=_('denonym'),
        help_text=_('the denonym of the country'),
        max_length=64,
        blank=True,
    )
    code = models.CharField(
        verbose_name=_('code'),
        help_text=_('the code of the country'),
        max_length=2,
        unique=True,
        primary_key=True,
    )
    continent = models.ForeignKey(
        verbose_name=_('continent'),
        help_text=_('the continent of the country'),
        to=Continent,
        on_delete=models.CASCADE,
        related_name='countries',
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('country')
        verbose_name_plural = _('countries')

    class TranslatableMeta:
        fields = ['name', 'denonym']


class City(Translatable):
    name = models.CharField(
        verbose_name=_('name'),
        help_text=_('the name of the city'),
        max_length=64,
    )
    denonym = models.CharField(
        verbose_name=_('denonym'),
        help_text=_('the denonym of the city'),
        max_length=64,
        blank=True,
    )
    country = models.ForeignKey(
        verbose_name=_('country'),
        help_text=_('the country of the city'),
        to=Country,
        on_delete=models.CASCADE,
        related_name='cities',
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('city')
        verbose_name_plural = _('cities')
