from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.utils.translation import ugettext_lazy as _

from translations.utils import get_translations, translate, renew_translations
from translations.managers import TranslatableManager


class Translation(models.Model):
    content_type = models.ForeignKey(
        verbose_name=_('content type'),
        help_text=_('the model we would like to translate'),
        to=ContentType,
        on_delete=models.CASCADE
    )
    object_id = models.PositiveIntegerField(
        verbose_name=_('object id'),
        help_text=_('the id of the object we would like to translate')
    )
    content_object = GenericForeignKey(
        ct_field='content_type',
        fk_field='object_id'
    )
    field = models.CharField(
        verbose_name=_('field'),
        help_text=_('the field of the object we would like to translate'),
        max_length=512
    )
    language = models.CharField(
        verbose_name=_('language'),
        help_text=_('the language of the field we would like to translate'),
        max_length=32,
        choices=settings.LANGUAGES
    )
    text = models.TextField(
        verbose_name=_('text'),
        help_text=_('the text of the field we would like to translate')
    )

    def __str__(self):
        return '{id}: {text}'.format(id=self.id, text=self.text)

    class Meta:
        unique_together = ('content_type', 'object_id', 'field', 'language',)
        verbose_name = _('translation')
        verbose_name_plural = _('translations')


class TranslatableModel(models.Model):
    objects = TranslatableManager()
    translations = GenericRelation(
        Translation,
        content_type_field='content_type',
        object_id_field='object_id',
        related_query_name="%(app_label)s_%(class)ss"
    )

    # -------------- META classes

    class Meta:
        abstract = True

    class TranslatableMeta:
        fields = None

    # -------------- overridable methods

    @staticmethod
    def is_field_translatable(field):
        return isinstance(field, (models.CharField, models.TextField,)) \
               and not isinstance(field, models.EmailField) \
               and (not hasattr(field, 'choices') or not field.choices)

    @classmethod
    def get_translatable_fields(cls):
        if hasattr(cls, 'TranslatableMeta'):
            if cls.TranslatableMeta.fields is None:
                fields = []
                for field in cls._meta.get_fields():
                    if cls.is_field_translatable(field):
                        fields.append(field)
            else:
                fields = [cls._meta.get_field(field_name) for field_name in cls.TranslatableMeta.fields]
        else:
            raise Exception('{cls} class is not a translatable model.'.format(cls=cls))
        return fields

    # -------------- methods of Translatable object

    def renew_translations(self, iso_alpha_2_language_code=None):
        renew_translations(self, iso_alpha_2_language_code=iso_alpha_2_language_code)

    # -------------- methods of Translatable queryset and object

    def get_translations(self, *relations, iso_alpha_2_language_code=None):
        return get_translations(self, *relations, iso_alpha_2_language_code=iso_alpha_2_language_code)

    def get_translated(self, *relations, iso_alpha_2_language_code=None, translations_queryset=None):
        translate(
            self, *relations,
            iso_alpha_2_language_code=iso_alpha_2_language_code,
            translations_queryset=translations_queryset
        )
        return self
