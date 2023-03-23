# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

import os
import pathlib
import sys
from pkg_resources import get_distribution
sys.path.insert(0, os.path.abspath('../src'))

root = pathlib.Path(__file__).parent.parent.absolute()
os.environ["PYTHONPATH"] = str(root)
sys.path.insert(0, str(root))
print("python exec:", sys.executable)
print("sys.path:", sys.path)

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'OpenClimate pyClient'
copyright = '2023, Open Earth Foundation'
author = 'Open Earth Foundation'
release = "0.1.0"
version = "0.1"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "nbsphinx",
    "recommonmark",
    "sphinx.ext.mathjax",
    "sphinx.ext.autosummary",
    "sphinx.ext.extlinks",
    "sphinx.ext.intersphinx",
    "numpydoc",
    "nbsphinx",
    "IPython.sphinxext.ipython_directive",
    "IPython.sphinxext.ipython_console_highlighting",
    "sphinxcontrib.srclinks",
]

nbsphinx_execute = 'always'
nbsphinx_allow_errors = True
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', "**.ipynb_checkpoints"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme_options = {
    "logo_only": True,
    "display_version": False,
    "style_nav_header_background": "#1d3550",
}

# make file (relative to this directory) to place at the top of the sidebar.
html_logo = "img/OC-Logo_white.png"
html_theme = "sphinx_rtd_theme"
html_static_path = ['_static']
html_css_files = [
    "css/custom.css",
]
