******
Models
******

This module provides an in depth knowledge of the Translations models.

.. _translatable-models:

Make models translatable
========================

To make a model translatable inherit it from the
:class:`~translations.models.Translatable` abstract model.

.. literalinclude:: ../../sample/models.py
   :lines: 4

.. literalinclude:: ../../sample/models.py
   :pyobject: Continent
   :lines: 1-25
   :emphasize-lines: 1

.. note::

   Since ``Translatable`` is an abstract model there
   is no need to migrate afterwards.

.. warning::

   Care not to inherit the ``Translation`` model
   accidentally instead of the ``Translatable``
   model.

.. _specify-fields:

Specify model's translatable fields
===================================

To specify the model's translatable fields specify the
:attr:`~translations.models.Translatable.TranslatableMeta.fields` attribute
of the :class:`~translations.models.Translatable.TranslatableMeta` class
declared inside the translatable model.

.. literalinclude:: ../../sample/models.py
   :pyobject: Continent
   :emphasize-lines: 1, 27-28

By default the ``fields`` attribute is
set to ``None``. This means the translation will use the text based fields
automatically. (like ``CharField`` and
``TextField`` - this does not include
``EmailField`` or the fields with ``choices``)

.. literalinclude:: ../../sample/models.py
   :pyobject: City
   :emphasize-lines: 1

If needed, the ``fields`` attribute
can be set to nothing. This can be done by explicitly setting it to ``[]``.

.. literalinclude:: ../../sample/models.py
   :pyobject: Timezone
   :emphasize-lines: 1, 15-16
