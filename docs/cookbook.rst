Cookbook
========

Real-world recipes for common pluralization tasks.

Pluralizing a list of words
---------------------------

.. code-block:: python

   from pluralio import pluralize

   words = ["cat", "dog", "child", "city"]
   plurals = [pluralize(w) for w in words]
   # ['cats', 'dogs', 'children', 'cities']

Count-aware UI labels
---------------------

.. code-block:: python

   from pluralio import pluralize

   def label(word: str, count: int) -> str:
       return f"{count} {pluralize(word, count=count)}"

   label("item", 1)   # "1 item"
   label("item", 5)   # "5 items"
   label("mouse", 0)  # "0 mice"

Multi-language support
----------------------

.. code-block:: python

   from pluralio import pluralize, supported_languages

   word = "libro"
   for lang in supported_languages():
       if lang in ("en", "eo", "es", "it"):
           print(f"{lang}: {pluralize(word, lang=lang)}")
   # en: libros
   # eo: libroj
   # es: libros
   # it: libri

Adding domain-specific vocabulary
---------------------------------

.. code-block:: python

   from pluralio import add_irregular, pluralize, singularize

   # Add technical terms
   add_irregular("schema", "schemata")
   add_irregular("datum", "data")
   add_irregular("phenomenon", "phenomena")

   pluralize("schema")      # "schemata"
   singularize("data")      # "datum"

Marking words as uncountable
-----------------------------

.. code-block:: python

   from pluralio import add_uncountable, pluralize, singularize

   # Domain-specific uncountables
   for word in ("feedback", "metadata", "metadata"):
       add_uncountable(word)

   pluralize("feedback")    # "feedback"
   singularize("feedback")  # "feedback"

Custom regex rules for a domain
-------------------------------

.. code-block:: python

   from pluralio import add_plural_rule, add_singular_rule, pluralize, singularize

   # Latin scientific names: -us → -i
   add_plural_rule(r"us$", "i")
   add_singular_rule(r"i$", "us")

   pluralize("cactus")     # "cacti"
   pluralize("fungus")     # "fungi"
   singularize("cacti")    # "cactus"

Registering a mini-language
---------------------------

.. code-block:: python

   from pluralio import register_language, pluralize, singularize

   register_language(
       "xx",
       plural_rules=[(r"a$", "ae"), (r"$", "s")],
       singular_rules=[(r"ae$", "a"), (r"s$", "")],
       irregular_plurals={"rex": "reges"},
       uncountable={"aqua"},
   )

   pluralize("formula", lang="xx")  # "formulae"
   pluralize("rex", lang="xx")      # "reges"
   pluralize("aqua", lang="xx")     # "aqua"
   singularize("reges", lang="xx")  # "rex"

Test isolation with snapshot/restore
------------------------------------

.. code-block:: python

   from pluralio import add_irregular, pluralize
   from pluralio.registry import snapshot, restore

   state = snapshot()
   try:
       add_irregular("foo", "foos")
       assert pluralize("foo") == "foos"
   finally:
       restore(state)
   # After restore, "foo" is back to normal rules
   assert pluralize("foo") == "foos"  # default English rule

Checking word forms
-------------------

.. code-block:: python

   from pluralio import is_plural, is_singular

   # Uncountable words are both plural and singular
   assert is_plural("sheep")
   assert is_singular("sheep")

   # Regular words
   assert is_plural("cats")
   assert is_singular("cat")
   assert not is_plural("cat")
   assert not is_singular("cats")

   # Multi-language
   assert is_plural("gatos", lang="es")
   assert is_singular("gato", lang="es")
