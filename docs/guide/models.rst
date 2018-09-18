******
Models
******

This module provides an in depth knowledge of the translatable models.

Make models translatable
========================

To make a model translatable inherit the model from the
:class:`~translations.models.Translatable` model.

.. literalinclude:: ../../sample/models.py
   :lines: 1-6, 24-44
   :emphasize-lines: 4, 7

Since :class:`~translations.models.Translatable` is an abstract model there is
no need to migrate afterwards.

Control translatable fields
===========================

