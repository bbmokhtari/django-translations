########
Glossary
########

The terms you might see in the documentation:

.. glossary::

   translations dictionary
     A translation dictionary is an easy to search object made out of some
     translations.

     example::

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

   relations hierarchy
     A relations hierarchy is a hierarchy containing each level of relation
     and information about whether they are included or not.

     example::

        {
            root_relation_1: {
                'included': root_relation_1_inclusion_state,
                'relations': {
                    nested_relation_1: {
                        'included': nested_relation_1_inclusion_state,
                        'relations': ...
                    },
                    nested_relation_2: {
                        'included': nested_relation_2_inclusion_state,
                        'relations': ...
                    },
                }
            },
            root_relation_2: ...
        }
