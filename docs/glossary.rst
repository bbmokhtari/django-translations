########
Glossary
########

The terms you might see in the documentation:

.. glossary::

   active language
     The active language is a language which is automatically activated in
     each request. It is usually determined by the ``Accept-Language`` header
     received in each HTTP request (from the browser or another client). You
     can access it in Django using the
     :func:`~django.utils.translation.get_language` function.

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

     The ``root_relation`` represents the first-level relation of the model,
     ``included`` represents whether the relation is included or not,
     ``relations`` represents the nested relations inside the relation and
     the ``nested_relation`` represents the second-level relation of the
     model and so on.

   entity groups
     The entity groups are a group of objects divided into groups based on
     their content types and object ids.

     example::

        {
            content_type_id_1: {
                object_id_1: object_1,
                object_id_2: ...
            },
            content_type_id_2: ...
        }

     The first level keys are content types, the second level keys are object
     ids and the values of the object ids keys are the actual objects.
