Rules Modules
=============

.. automodule:: pluralio.rules
   :members:
   :show-inheritance:

Individual language rule modules are auto-registered at import time.
Each module builds a :class:`~pluralio.registry.LanguageRules` dataclass
and calls :func:`~pluralio.registry.register`.

.. toctree::
   :maxdepth: 1

   en
   es
   pt
   fr
   it
   eo
