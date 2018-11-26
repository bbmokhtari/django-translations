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

      This is an overriden version of
      the :class:`~django.core.management.base.BaseCommand`\ 's
      :meth:`~django.core.management.base.BaseCommand.execute` method.
      It defines the standard input on the :class:`Command`.

   .. method:: add_arguments(parser)

      Add the arguments which the :class:`Command` accepts
      on an :class:`~argparse.ArgumentParser`.

      Defines the different types of arguments
      that the :class:`Command` accepts
      on the :class:`~argparse.ArgumentParser`.

   .. method:: get_content_types(*app_labels)

      Return the :class:`~django.contrib.contenttypes.models.ContentType`\ s
      in some apps or all of them.

      If the app labels are passed in it returns
      the :class:`~django.contrib.contenttypes.models.ContentType`\ s
      in those apps,
      if nothing is passed in it returns
      the :class:`~django.contrib.contenttypes.models.ContentType`\ s
      in all apps.

   .. method:: get_obsolete_translations(*content_types)

      Return the obsolete translations of some
      :class:`~django.contrib.contenttypes.models.ContentType`\ s.

      Returns the obsolete translations of
      the :class:`~django.contrib.contenttypes.models.ContentType`\ s
      based on the current configurations of their models.

   .. method:: log_obsolete_translations(obsolete_translations)

      Log the obsolete translations.

   .. method:: ask_yes_no(message, default=None)

      Ask the user for yes or no with a message and a default value.

   .. method:: should_run_synchronization()

      Return whether to run the synchronization or not.

   .. method:: handle(*app_labels, **options)

      Run the :class:`Command` with the configured arguments.
