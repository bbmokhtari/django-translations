******
Models
******

This module provides an in depth knowledge of the translatable models.

Make models translatable
========================

To make a model translatable inherit the model from the
:class:`~translations.models.Translatable` model.

.. literalinclude:: ../../sample/models.py
   :lines: 1-6, 24-48
   :emphasize-lines: 4, 7

Since :class:`~translations.models.Translatable` is an abstract model there is
no need to migrate afterwards.

Specify translatable fields
===========================

To specify the translatable fields specify the
:attr:`~translations.models.Translatable.TranslatableMeta.fields` attribute
of the :class:`~translations.models.Translatable.TranslatableMeta` class
declared inside a :class:`~translations.models.Translatable` model.

.. literalinclude:: ../../sample/models.py
   :lines: 1-6, 24-51
   :emphasize-lines: 33-34

By default the
:attr:`~translations.models.Translatable.TranslatableMeta.fields` attribute is
set to ``None``. This means the translation will use the text based fields
automatically, fields like :class:`~django.db.models.CharField` and
:class:`~django.db.models.TextField`. (it automatically ignores the fields with
the ``choices`` and :class:`~django.db.models.EmailField`)

If needed, the
:attr:`~translations.models.Translatable.TranslatableMeta.fields` attribute
can be set to nothing. You can do this by setting it to ``[]``.
