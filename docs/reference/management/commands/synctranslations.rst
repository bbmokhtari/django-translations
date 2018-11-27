***************************
Reference: synctranslations
***************************

.. module:: translations.management.commands.synctranslations

This module contains the synctranslations command for the Translations app.

.. class:: Command

   The command which synchronizes the translations with
   the apps models configurations.

   .. attribute:: help

      The command's help text.

   .. method:: execute(*args, **options)

      Execute the :class:`Command`
      with :class:`~django.core.management.base.BaseCommand` arguments.

      This is an overriden version of
      the :class:`~django.core.management.base.BaseCommand`\ 's
      :meth:`~django.core.management.base.BaseCommand.execute` method.
      It defines the standard input on the :class:`Command`.

      :param args: The arguments of
          the :class:`~django.core.management.base.BaseCommand`\
          's :meth:`~django.core.management.base.BaseCommand.execute` method.
      :type args: list
      :param options: The keyword arguments of
          the :class:`~django.core.management.base.BaseCommand`\
          's :meth:`~django.core.management.base.BaseCommand.execute` method.
      :type options: dict
      :return: The return value of
          the :class:`~django.core.management.base.BaseCommand`\
          's :meth:`~django.core.management.base.BaseCommand.execute` method.
      :rtype: str or None

   .. method:: add_arguments(parser)

      Add the arguments that the :class:`Command` accepts
      on an :class:`~argparse.ArgumentParser`.

      Defines the different types of arguments
      that the :class:`Command` accepts
      on the :class:`~argparse.ArgumentParser`.

      :param parser: The parser to add the arguments
         that the :class:`Command` accepts on.
      :type parser: ~argparse.ArgumentParser

   .. method:: get_content_types(*app_labels)

      Return the :class:`~django.contrib.contenttypes.models.ContentType`\ s
      in some apps or all of them.

      If the app labels are passed in it returns
      the :class:`~django.contrib.contenttypes.models.ContentType`\ s
      in those apps,
      if nothing is passed in it returns
      the :class:`~django.contrib.contenttypes.models.ContentType`\ s
      in all apps.

      :param app_labels: The apps in which to get
         the :class:`~django.contrib.contenttypes.models.ContentType`\ s.
      :type app_labels: list(str)
      :return: The :class:`~django.contrib.contenttypes.models.ContentType`\ s
         in the apps.
      :rtype: ~django.db.models.query.QuerySet(\
         ~django.contrib.contenttypes.models.ContentType)

   .. method:: get_obsolete_translations(content_types)

      Return the obsolete translations of some
      :class:`~django.contrib.contenttypes.models.ContentType`\ s.

      Returns the obsolete translations of
      the :class:`~django.contrib.contenttypes.models.ContentType`\ s
      based on the current configurations of their models.

      :param content_types:
         The :class:`~django.contrib.contenttypes.models.ContentType`\ s
         to get the obsolete translations of.
      :type content_types: ~django.db.models.query.QuerySet(\
         ~django.contrib.contenttypes.models.ContentType)
      :return: The obsolete translations of
         the :class:`~django.contrib.contenttypes.models.ContentType`\ s.
      :rtype: ~django.db.models.query.QuerySet(~translations.models.Translation)

   .. method:: log_obsolete_translations(obsolete_translations)

      Log the details of some obsolete translations.

      Logs the model and field details of the obsolete translations.

      :param obsolete_translations: The obsolete translations to log
         the details of.
      :type obsolete_translations: ~django.db.models.query.QuerySet(~translations.models.Translation)

   .. method:: ask_yes_no(message, default=None)

      Ask the user for yes or no with a message and a default value.

      Prompts the user with the message asking them for a yes or no answer,
      optionally a default value can be set for the answer.

      :param message: The question to ask the user for yes or no with.
      :type message: str
      :param default: The default value for the answer.
      :type default: str or bool or None
      :return: The user's yes or no answer.
      :rtype: bool

   .. method:: should_run_synchronization()

      Return whether to run the synchronization or not.

      Determines whether the synchronization should run or not.
      It does so by making sure that the user is aware of the risks.
      If the user is using a TTY it asks them whether they are sure or not and
      if the user is *NOT* using a TTY they have to explicitly declare
      that they are sure in the command.

      :return: whether to run the synchronization or not.
      :rtype: bool

   .. method:: handle(*app_labels, **options)

      Run the :class:`Command` with the configured arguments.

      This is an overriden version of
      the :class:`~django.core.management.base.BaseCommand`\ 's
      :meth:`~django.core.management.base.BaseCommand.handle` method.
      It synchronizes the translations with the apps models configurations.

      :param app_labels: The apps to synchronize the translations with
         the models configurations of.
      :type app_labels: list(str)
      :param options: The configured options of the :class:`Command`.
      :type options: dict(str, str)
