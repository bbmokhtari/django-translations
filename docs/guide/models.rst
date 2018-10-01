******
Models
******

This module provides an in depth knowledge of the Translations models.

.. _translatable-models:

Make models translatable
========================

To make a model, a
:class:`translatable model <translations.models.Translatable>`
inherit the model from the :class:`~translations.models.Translatable` model.

.. literalinclude:: ../../sample/models.py
   :lines: 4

.. literalinclude:: ../../sample/models.py
   :pyobject: Continent
   :lines: 1-25
   :emphasize-lines: 1

Since :class:`~translations.models.Translatable` is an abstract model there is
no need to migrate afterwards.

.. warning::

   Care not to inherit the :class:`~translations.models.Translation` model
   accidentally instead of the :class:`~translations.models.Translatable`
   model.

.. _specify-fields:

Specify model's translatable fields
===================================

To specify the model's :attr:`translatable fields \
<translations.models.Translatable.TranslatableMeta.fields>` specify the
:attr:`~translations.models.Translatable.TranslatableMeta.fields` attribute
of the :class:`~translations.models.Translatable.TranslatableMeta` class
declared inside a :class:`~translations.models.Translatable` model.

.. literalinclude:: ../../sample/models.py
   :pyobject: Continent
   :emphasize-lines: 1, 27-28

By default the
:attr:`~translations.models.Translatable.TranslatableMeta.fields` attribute is
set to ``None``. This means the translation will use the text based fields
automatically. (like :class:`~django.db.models.CharField` and
:class:`~django.db.models.TextField` - this does not include
:class:`~django.db.models.EmailField` or the fields with ``choices``)

.. literalinclude:: ../../sample/models.py
   :pyobject: City
   :emphasize-lines: 1

If needed, the
:attr:`~translations.models.Translatable.TranslatableMeta.fields` attribute
can be set to nothing. You can do this by explicitly setting it to ``[]``.

.. literalinclude:: ../../sample/models.py
   :pyobject: Timezone
   :emphasize-lines: 1, 15-16
