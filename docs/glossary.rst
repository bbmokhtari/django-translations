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

   purview
     The purview is simply an area of effect, it defines the instances to be
     affected and some information about them, so it consists of two parts.

     The first part is a mapping of instances divided into groups based on
     their content types.

     example::

        {
            content_type_id_1: {
                object_id_1: instance_1,
                object_id_2: ...
            },
            content_type_id_2: ...
        }

     The first level keys are content types, the second level keys are object
     ids and the values of the object id keys are the instances.

     The second part is the query that can be used to fetch the translations
     of all the instances in the purview.
