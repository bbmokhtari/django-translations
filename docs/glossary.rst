########
Glossary
########

The terms you might see in the documentation:

.. glossary::

   supported language
     A supported language is a language which is included in
     the :data:`~django.conf.settings.LANGUAGES` setting.

   default language
     The default language is a language which is set by
     the :data:`~django.conf.settings.LANGUAGE_CODE` setting.

   translation language
     A translation language is a language which is in
     the collection of :term:`supported language`\ s minus
     the :term:`default language`.

   active language
     The active language is a language which is automatically activated in
     each request. It is usually determined by the ``Accept-Language`` header
     received in each HTTP request (from the browser or another client).
     You can access it in Django using the
     :func:`~django.utils.translation.get_language` function.
