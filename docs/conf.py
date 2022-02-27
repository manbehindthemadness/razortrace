#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
razortrace documentation build configuration file
"""

import os
import sys
import sphinx_rtd_theme


sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, os.path.abspath('../'))

project = 'Razortrace'
copyright = '2022, Kevin Eales'
author = 'Kevin Eales'

version = '0.1'
release = '0.1'

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
]

intersphinx_mapping = {"python": ("https://docs.python.org/3", None)}

templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
language = None

exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
pygments_style = 'sphinx'
todo_include_todos = False

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
htmlhelp_basename = 'razortrace documentation'
html_js_files = [
    "js/script.js"
]
html_css_files = [
    "css/styles.css",
    "css/dark.css",
    "css/light.css"
]

html_logo = "_static/razor.png"
html_favicon = "_static/favicon.ico"

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

latex_documents = [
    (master_doc, 'Razortrace.tex', 'razortrace Documentation',
     'Kevin (eales)', 'manual'),
]

texinfo_documents = [
    (master_doc, 'Razortrace', 'razortrace Documentation',
     author, 'Razortrace', 'Straightforward memory leak detection.',
     'Miscellaneous'),
]


def run_apidoc(_):
    """

    :param _:
    :return:
    """
    from sphinx.ext.apidoc import main
    import os
    import sys
    import shutil
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    cur_dir = os.path.abspath(os.path.dirname(__file__))
    module = '../razortrace/'
    output_path = os.path.join(cur_dir, 'source')
    main(['-o', output_path, module, '--force', '--separate'])

    static_dir = os.path.join(cur_dir, '_static')
    static_dir_files = os.listdir(static_dir)
    dest_dir = os.path.join(output_path, '_static/')
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    for filename in static_dir_files:
        full_filename = os.path.join(static_dir, filename)
        dest_filename = os.path.join(dest_dir, filename)
        shutil.copy(full_filename, dest_filename)


def setup(app):
    """

    :param app:
    :return:
    """
    # app.add_js_file("js/script.js")
    # app.add_css_file("css/styles.css")
    # app.add_css_file("css/dark.css")
    # app.add_css_file("css/light.css")
    app.connect('builder-inited', run_apidoc)

issues_github_path = '/razortrace'

autoclass_content = 'both'
autodoc_mock_imports = ["razortrace.tools"]
