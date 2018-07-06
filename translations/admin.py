from django.contrib.contenttypes.admin import GenericStackedInline

from .models import Translation, TranslatableModel
from .forms import generate_translation_form


class TranslationInline(GenericStackedInline):
    model = Translation
    extra = 1


class TranslatableAdminMixin(object):
    def get_translation_choices(self):
        choices = [
            (None, '---------')
        ]
        if issubclass(self.model, TranslatableModel):
            for field in self.model.get_translatable_fields():
                choices.append((field.name, field.verbose_name))
        return choices

    def handle_translation_inlines(self, inlines):
        choices = self.get_translation_choices()
        remove_inlines = []
        for i, v in enumerate(inlines):
            if isinstance(v, TranslationInline):
                if len(choices) == 1:
                    remove_inlines.append(i)
                else:
                    inlines[i].form = generate_translation_form(choices)
        remove_inlines.reverse()
        for index in remove_inlines:
            inlines.pop(index)


"""
from nested_inline.admin import NestedStackedInline, NestedModelAdmin


class TranslationInline(NestedStackedInline, GenericStackedInline):
    model = Translation
    extra = 1


class TranslatableAdmin(TranslatableAdminMixin, NestedModelAdmin):
    def get_inline_instances(self, request, obj=None):
        inlines = super(TranslatableAdmin, self).get_inline_instances(request, obj)
        inlines = list(inlines)
        self.handle_translation_inlines(inlines)
        return inlines


class TranslatableInline(TranslatableAdminMixin, NestedStackedInline):
    def get_inline_instances(self, request, obj=None):
        inlines = super(TranslatableInline, self).get_inline_instances(request, obj)
        inlines = list(inlines)
        self.handle_translation_inlines(inlines)
        return inlines

"""
