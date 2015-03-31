#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

from arbitrator import __version__, version_info

on_rtd = os.environ.get('READTHEDOCS', None) == 'True'

project = 'arbitrator'
copyright = '2015, Dan Tracy'
version = __version__
release = '.'.join(str(x) for x in version_info[:2])

needs_sphinx = '1.0'
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
]

templates_path = []
source_suffix = '.rst'
source_encoding = 'utf-8-sig'
master_doc = 'index'
pygments_style = 'sphinx'
html_static_path = []
exclude_patterns = []

if not on_rtd:  # only import and set the theme if we're building docs locally
    import sphinx_rtd_theme
    html_theme = 'sphinx_rtd_theme'
    html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

intersphinx_mapping = {
    'python': ('https://docs.python.org/', None),
    'tornado': ('http://www.tornadoweb.org/en/stable/', None),
}
