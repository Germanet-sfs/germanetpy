# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath('..'))


# -- Project information -----------------------------------------------------

project = 'germanetpy'
copyright = '2020, Neele Falk'
author = 'Neele Falk'

# The full version, including alpha/beta/rc tags
release = '0.2.0'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
    ## Include autosymmary
    'sphinx.ext.autosummary',
]

## Include Python objects as they appear in source files
## Default: alphabetically ('alphabetical')
autodoc_member_order = 'bysource'
## Default flags used by autodoc directives
autodoc_default_options = ['members', 'show-inheritance']
## Generate autodoc stubs with summaries from code
autosummary_generate = True

source_suffix = '.rst'
# master_doc = 'index'
root_doc = 'index'   # keeps 'index' as the entry point; 'master_doc' is deprecated
# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'alabaster'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

pygments_style = 'sphinx'

# -- Extension configuration -------------------------------------------------

html_theme_options = {
    'github_button': True,  ## Use v2 button
    'github_user': 'bencampbell30',
    'github_repo': 'germanetpy',
    'github_banner': True,
}

html_sidebars = {
    '**': [
        'about.html',
        'navigation.html',
        'searchbox.html',
    ]
}

html_show_sourcelink = True

intersphinx_mapping = {'https://docs.python.org/3': None}
