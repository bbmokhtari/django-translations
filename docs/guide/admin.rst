*****
Admin
*****

This module provides an in depth knowledge of the Translations admin.

Make admin translatable
=======================

To make an admin, a
:class:`translatable admin <translations.admin.TranslatableAdmin>`
inherit the admin from the :class:`~translations.admin.TranslatableAdmin`
model. Then add :class:`~translations.admin.TranslationInline` as its inline.

.. literalinclude:: ../../sample/admin.py
   :lines: 2

.. literalinclude:: ../../sample/admin.py
   :pyobject: ContinentAdmin
