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

.. note::

   An admin may contain an inline which itself needs to be translatable. Since
   translations appear as inlines to the admins, then the inlines themselves
   should have translation inlines in order to be translatable, and since
   Django does not support nested inlines there may be a need to use an
   external library. In that case check out :doc:`../howto/customadmin`.

Specify admin's translatable fields
===================================

To specify the admin's :attr:`translatable fields \
<translations.models.Translatable.TranslatableMeta.fields>`
:ref:`specify its model's translatable fields <specify-fields>`.