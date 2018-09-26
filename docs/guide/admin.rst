*****
Admin
*****

This module provides an in depth knowledge of the Translations admin.

Make admin translatable
=======================

To make an admin, a
:class:`translatable admin <translations.admin.TranslatableAdmin>`:

1. :ref:`Make its model translatable <translatable-models>`.
2. Inherit the admin from the :class:`~translations.admin.TranslatableAdmin`
   admin.

   .. literalinclude:: ../../sample/admin.py
      :lines: 2

   .. literalinclude:: ../../sample/admin.py
      :pyobject: ContinentAdmin
      :emphasize-lines: 1

3. Add :class:`~translations.admin.TranslationInline` as its inline.

   .. literalinclude:: ../../sample/admin.py
      :pyobject: ContinentAdmin
      :emphasize-lines: 2
