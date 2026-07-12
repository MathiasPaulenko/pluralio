"""Language rule modules for pluralio.

Each submodule (``en``, ``es``, ``fr``, ``it``, ``pt``) defines the
complete pluralization/singularization rules for one language and
registers them at import time.

Importing this package — either directly or via ``import pluralio`` —
triggers registration of all built-in languages.
"""

from pluralio.rules import (  # noqa: F401 — triggers registration
    en,
    eo,
    es,
    fr,
    it,
    pt,
)

__all__ = ["en", "eo", "es", "fr", "it", "pt"]
