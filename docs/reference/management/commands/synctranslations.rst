***************************
Reference: synctranslations
***************************

.. module:: translations.management.commands.synctranslations

This module contains the synctranslations command for the Translations app.

.. class:: Command

   The command which synchronizes the translation objects with
   the configurations.

   .. method:: add_arguments(self, parser)

      pass

   .. method:: execute(self, *args, **options)

      pass

   .. method:: get_content_types(self, *app_labels)

      Return the content types of some apps or all of them.

   .. method:: get_obsolete_translations(self, *content_types)

      Return the obsolete translations of some content types.

   .. method:: log_obsolete_translations(self, obsolete_translations)

      Log the obsolete translations.

   .. method:: ask_yes_no(self, message, default=None)

      Ask user for yes or no with a message and a default value.

   .. method:: should_run_synchronization(self)

      Return whether to run synchronization or not.

   .. method:: handle(self, *app_labels, **options)

      pass
