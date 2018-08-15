########
Glossary
########

The terms you might see in the documentation:

.. glossary::

   translations dictionary
     a translation dictionary is an easy to search object made out of some
     translations.

     The end result is something like this::

        {
            content_type_id_1: {
                object_id_1: {
                    field_1: text_1,
                    field_2: ...
                },
                object_id_2: ...
            },
            content_type_id_2: ...
        }

    The ``content_type_id`` represents the
    :class:`~django.contrib.contenttypes.models.ContentType` ID, ``object_id``
    represents the ID of the object in that content type, ``field``
    represents the name of the field for that object.
