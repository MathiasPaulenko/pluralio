"""Sphinx configuration for pluralio documentation."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

project = "pluralio"
author = "Mathias Paulenko"
release = "2.1.2"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx.ext.doctest",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "furo"
html_static_path = ["_static"]

html_theme_options = {
    "sidebar_hide_name": False,
    "navigation_with_keys": True,
    "source_repository": "https://github.com/MathiasPaulenko/pluralio",
    "source_branch": "main",
    "source_directory": "docs/",
}

html_title = "pluralio"
html_logo = None
html_favicon = None

autodoc_default_options = {
    "members": True,
    "show-inheritance": True,
    "undoc-members": False,
    "exclude-special": True,
}

autodoc_typehints = "signature"
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = False

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}

doctest_global_setup = """
import pluralio
"""
