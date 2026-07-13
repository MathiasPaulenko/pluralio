Usage Guide
===========

Basic usage
-----------

.. code-block:: python

   from pluralio import pluralize, singularize

   # English (default)
   pluralize("cat")           # "cats"
   pluralize("box")           # "boxes"
   pluralize("child")         # "children"
   singularize("cities")      # "city"
   singularize("mice")        # "mouse"

   # Other languages
   pluralize("gato", lang="es")      # "gatos"
   pluralize("livro", lang="pt")     # "livros"
   pluralize("chat", lang="fr")      # "chats"
   pluralize("libro", lang="it")     # "libri"
   pluralize("libro", lang="eo")     # "libroj"

Count-aware pluralization
-------------------------

Pass a ``count`` argument to get the singular form when ``count == 1``:

.. code-block:: python

   pluralize("item", count=1)    # "item"
   pluralize("item", count=0)    # "items"
   pluralize("item", count=5)    # "items"
   pluralize("item", count=-1)   # "items"
   pluralize("item")             # "items" (count=None → plural)

Case preservation
-----------------

The output mirrors the casing of the input:

.. code-block:: python

   pluralize("Library")     # "Libraries"
   pluralize("LIBRARY")     # "LIBRARIES"
   pluralize("library")     # "libraries"
   pluralize("McDonald")    # "McDonalds"
   pluralize("iPhone")      # "iPhones"

Hyphenated words
----------------

Only the head noun is pluralized (first segment by default, last segment
for known prefixes):

.. code-block:: python

   pluralize("mother-in-law")     # "mothers-in-law"
   pluralize("forget-me-not")     # "forget-me-nots"
   pluralize("café-théâtre", lang="fr")  # "cafés-théâtres"

Whitespace preservation
-----------------------

Leading and trailing whitespace is preserved:

.. code-block:: python

   pluralize("  cat  ")     # "  cats  "
   singularize(" cats ")    # " cat "

Unicode normalization
---------------------

All non-ASCII input is normalized to NFC before processing, so NFD-encoded
strings work correctly:

.. code-block:: python

   import unicodedata
   nfd = unicodedata.normalize("NFD", "lápiz")
   pluralize(nfd, lang="es")  # "lápices"

Checking plural / singular
--------------------------

.. code-block:: python

   from pluralio import is_plural, is_singular

   is_plural("cats")       # True
   is_singular("cat")      # True
   is_plural("sheep")      # True (uncountable → both)
   is_singular("sheep")    # True
