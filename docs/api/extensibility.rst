Extensibility API
=================

.. automodule:: pluralio
   :members: add_irregular, add_plural, add_singular, add_uncountable, add_plural_rule, add_singular_rule, register_language, is_plural, is_singular, supported_languages, join, ordinal, template
   :show-inheritance:
   :no-index:

Examples
--------

Adding an irregular word pair:

.. code-block:: python

   from pluralio import add_irregular, pluralize, singularize

   add_irregular("person", "people")
   pluralize("person")       # "people"
   singularize("people")     # "person"

Adding a plural-only mapping:

.. code-block:: python

   from pluralio import add_plural, pluralize

   add_plural("joven", "jóvenes", lang="es")
   pluralize("joven", lang="es")  # "jóvenes"

Adding a singular-only mapping (accent restoration):

.. code-block:: python

   from pluralio import add_singular, singularize

   add_singular("alemanes", "alemán", lang="es")
   singularize("alemanes", lang="es")  # "alemán"

Marking a word as uncountable:

.. code-block:: python

   from pluralio import add_uncountable, pluralize, singularize

   add_uncountable("data")
   pluralize("data")    # "data"
   singularize("data")  # "data"

Adding a custom regex rule:

.. code-block:: python

   from pluralio import add_plural_rule, pluralize

   add_plural_rule(r"us$", "i")
   pluralize("cactus")  # "cacti"

Registering a new language:

.. code-block:: python

   from pluralio import register_language, pluralize, singularize

   register_language(
       "xx",
       plural_rules=[(r"$", "s")],
       singular_rules=[(r"s$", "")],
       irregular_plurals={"foo": "foos"},
       uncountable={"bar"},
   )
   pluralize("word", lang="xx")  # "words"
   pluralize("foo", lang="xx")   # "foos"
   pluralize("bar", lang="xx")   # "bar"

Checking plural / singular:

.. code-block:: python

   from pluralio import is_plural, is_singular

   is_plural("cats")       # True
   is_singular("cat")      # True
   is_plural("gatos", lang="es")   # True
   is_singular("gato", lang="es")  # True
