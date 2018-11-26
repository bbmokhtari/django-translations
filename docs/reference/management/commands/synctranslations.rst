***************************
Reference: synctranslations
***************************

.. module:: translations.management.commands.synctranslations

This module contains the synctranslations command for the Translations app.

.. class:: Command

   The command which synchronizes the translation objects with
   the configurations.

   .. method:: execute(*args, **options)

      Execute the :class:`Command`
      with :class:`~django.core.management.base.BaseCommand` arguments.

   .. method:: add_arguments(parser)

      Add the arguments which the parser accepts.

   .. method:: get_content_types(*app_labels)

      Return the content types of some apps or all of them.

   .. method:: get_obsolete_translations(*content_types)

      Return the obsolete translations of some content types.

   .. method:: log_obsolete_translations(obsolete_translations)

      Log the obsolete translations.

   .. method:: ask_yes_no(message, default=None)

      Ask the user for yes or no with a message and a default value.

   .. method:: should_run_synchronization()

      Return whether to run the synchronization or not.

   .. method:: handle(*app_labels, **options)

      Run the :class:`Command` with the configured arguments.
