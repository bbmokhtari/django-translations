*************
Guide: Models
*************

This module provides an in depth knowledge of the Translations models.

.. _models.Translatable:

Make models translatable
========================

To make a model translatable inherit it from the
:class:`~translations.models.Translatable` abstract model.

.. literalinclude:: ../../sample/models.py
   :lines: 7

.. literalinclude:: ../../sample/models.py
   :pyobject: Continent
   :lines: 1-26
   :emphasize-lines: 1

.. note::

   Since ``Translatable`` is an abstract model there
   is no need to migrate afterwards.

.. warning::

   Care not to inherit the ``Translation`` model
   accidentally instead of the ``Translatable``
   model.

.. _models.Translatable.TranslatableMeta.fields:

Specify models' translatable fields
===================================

To specify the model's translatable fields specify the
:attr:`~translations.models.Translatable.TranslatableMeta.fields` attribute
of the :class:`~translations.models.Translatable.TranslatableMeta` class
declared inside the ``Translatable`` model.

.. literalinclude:: ../../sample/models.py
   :pyobject: Continent
   :emphasize-lines: 1, 28-29

By default the ``fields`` attribute is set to ``None``.
This means the translation will use the text based fields
automatically. (like ``CharField`` and
``TextField`` - this does not include
``EmailField`` or the fields with ``choices``)

.. literalinclude:: ../../sample/models.py
   :pyobject: City
   :emphasize-lines: 1

If needed, the ``fields`` attribute can be set to nothing.
This can be done by explicitly setting it to ``[]``.

.. literalinclude:: ../../sample/models.py
   :pyobject: Timezone
   :emphasize-lines: 1, 15-16

Changing the models and fields configurations
=============================================

To synchronize the translations with the apps models configurations run
the :mod:`~translations.management.commands.synctranslations` command.

.. code-block:: shell

   $ python manage.py synctranslations

This is useful in the cases when you decide to change the configurations of
the models and fields later on, but you have already defined some translations
for them and the translations are obsolete now.

.. note::

   Since this command deletes the obsolete translations which are not useful
   any more based on the current models and fields configurations,
   it has to make sure that you are aware of the risks.

   So you either have to run it in a TTY environment and respond *yes* when it
   asks you if you are sure,
   or you have to declare that you are sure explicitly while calling
   the command using the ``--no-input`` option.
