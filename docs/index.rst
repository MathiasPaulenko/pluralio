pluralio
========

Pluralization and singularization for Python — zero dependencies, type-safe,
extensible.

Supports English, Spanish, Portuguese, French, Italian, and Esperanto.

.. image:: https://img.shields.io/pypi/v/pluralio.svg
   :target: https://pypi.org/project/pluralio/
   :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/pluralio.svg
   :target: https://pypi.org/project/pluralio/
   :alt: Python versions

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
   :alt: License

Installation
------------

.. code-block:: bash

   pip install pluralio

Quick start
-----------

.. code-block:: python

   from pluralio import pluralize, singularize

   pluralize("cat")              # "cats"
   pluralize("gato", lang="es")  # "gatos"
   pluralize("libro", lang="eo") # "libroj"
   singularize("cities")         # "city"
   singularize("lápices", lang="es")  # "lápiz"

   # Count-aware
   pluralize("item", count=1)    # "item"
   pluralize("item", count=5)    # "items"

   # Case preservation
   pluralize("Library")          # "Libraries"
   pluralize("LIBRARY")          # "LIBRARIES"

   # Hyphenated words
   pluralize("mother-in-law")    # "mothers-in-law"

Documentation
-------------

.. toctree::
   :maxdepth: 2
   :caption: Guides

   usage
   languages

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   api/core
   api/registry
   api/extensibility
   api/rules

Indices
-------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
