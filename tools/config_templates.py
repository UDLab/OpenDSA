# Header prepended to every RST file, contains settings for a specific module
rst_header = '''\

.. _%(mod_name)s:


.. raw:: html

   <script>ODSA.SETTINGS.DISP_MOD_COMP = %(dispModComp)s;ODSA.SETTINGS.MODULE_NAME = "%(mod_name)s";ODSA.SETTINGS.MODULE_LONG_NAME = "%(long_name)s";ODSA.SETTINGS.MODULE_CHAPTER = "%(mod_chapter)s"; ODSA.SETTINGS.BUILD_DATE = "%(mod_date)s"; ODSA.SETTINGS.BUILD_CMAP = %(build_cmap)s;%(mod_options)s</script>

%(unicode_directive)s
'''

rst_footer = '''\
 .. raw:: html
 
    <script type="text/javascript">
     $(function () {
       var moduleName = "%(module_name)s";
       var sections = %(sections)s;
       TimeMe.initialize({
         idleTimeoutInSeconds: 10
       });
       sections.forEach(function (section, i) {
         TimeMe.trackTimeOnElement(section);
       });
       var timeObj = {};
       setInterval(function () {
         timeObj[moduleName.substring(0, 5)] = TimeMe.getTimeOnCurrentPageInSeconds().toFixed(2);
         sections.forEach(function (section, i) {
           timeObj[i + "-" + section.substring(0, 5)] = TimeMe.getTimeOnElementInSeconds(section).toFixed(2);
         });
         for (var sec of sections) {
         }
         console.log(JSON.stringify(timeObj))
       }, 2000);
     });
    </script>
 '''

rst_header_unicode = '''\

.. |--| unicode:: U+2013   .. en dash
.. |---| unicode:: U+2014  .. em dash, trimming surrounding whitespace
   :trim:

'''


# Used to generate the index.rst file
index_header = '''\
.. This file is part of the OpenDSA eTextbook project. See
.. http://opendsa.org for more details.
.. Copyright (c) 2011-2023 by the OpenDSA Project Contributors, and
.. distributed under an MIT open source license.

.. OpenDSA documentation master file, created by
   sphinx-quickstart on Sat Mar 17 18:07:39 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. avmetadata:: OpenDSA Sample eTextbook
   :author: OpenDSA Contributors
   :topic: Data Structures

.. chapnum::
   :start: {0}
   :prefix: {1}

'''

todo_rst_template = '''\
.. index:: ! todo

TODO List
=========
'''
makefile_template = '''\
# Makefile for Sphinx documentation
# THIS FILE GENERATED BY 'tools\\configure.py' AND 'tools\\config_templates.py' SCRIPTS
#
# You can set these variables from the command line.
# PYTHON should match the exec of the rest of OpenDSA
PYTHON = %(python_executable)s
SPHINXBUILD   = sphinx-build
SPHINXOPTS    = %(sphinx_options)s
# -E is option to always build from new environment, regardless of changed files
# -vv and -vvv are options for verbose build output
# -P is for starting pdb exactly when and where exception occurs
HTMLDIR       = %(rel_book_output_path)s
TAGS = %(tag)s
.PHONY: clean html

all: html

clean:
	-rm -rf ./$(HTMLDIR)*
	-rm source/ToDo.rst

cleanbuild: clean html

html:
	$(SPHINXBUILD) $(TAGS) $(SPHINXOPTS) -b html source $(HTMLDIR)
	rm html/_static/jquery.js
	cp "%(odsa_dir)slib/conceptMap.html" $(HTMLDIR)
	rm *.json
	@echo
	@echo "Build finished. The HTML pages are in $(HTMLDIR)."
	rm Makefile

slides:
	@SLIDES=yes \
	$(SPHINXBUILD) $(SPHINXOPTS) -b slides source $(HTMLDIR)
	rm html/_static/jquery.js
	cp "%(odsa_dir)slib/styles.css" html/_static/ # Overwrites
	rm *.json
	@echo
	@echo "Build finished. The HTML pages are in $(HTMLDIR)."
'''


# Used to generate the conf.py file
conf = '''\
# -*- coding: utf-8 -*-
#
# OpenDSA documentation build configuration file, created by
# sphinx-quickstart on Sat Mar 17 18:07:39 2012.
#
# This file is execfile()d with the current directory set to its containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

import sys, os
import json

#checking if we are building a book or class notes (slides)
on_slides = os.environ.get('SLIDES', None) == "yes"
# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#sys.path.insert(0, os.path.abspath('.'))

# -- General configuration -----------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
# needs_sphinx = '2.4'

# Add any Sphinx extension module names here, as strings. They can be extensions
# coming with Sphinx (named 'sphinx.ext.*') or your custom ones.

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.doctest', 'sphinx.ext.todo', 'sphinx.ext.mathjax', 'sphinx.ext.ifconfig']

ourCustoms = ['avembed', 'avmetadata', 'extrtoolembed', 'codeinclude', 'chapnum', 'odsalink', 'odsascript', 'inlineav', 'html5', 'odsafig', 'odsatable', 'chapref', 'odsatoctree', 'showhidecontent', 'iframe']

customsDir = '%(odsa_dir)sRST/ODSAextensions/odsa/'
for c in ourCustoms:
	sys.path.append(os.path.abspath(customsDir + c))
	extensions.append(c)

# One custom extension that breaks the naming convention:
sys.path.append(os.path.abspath(customsDir + 'sphinx-numfig'))
extensions.append('numfig')

slides_lib = '%(slides_lib)s'

#only import hieroglyph when building course notes
if slides_lib == 'hieroglyph':
  extensions.append('hieroglyph')

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The encoding of source files.
#source_encoding = 'utf-8-sig'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'OpenDSA'
copyright = u'2011-2023 by OpenDSA Project Contributors and distributed under an MIT license'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = '0'
# The full version, including alpha/beta/rc tags.
release = '0.4.1'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
language = %(text_lang)s
locale_dirs = ['locale/']   # path is example but recommended.
gettext_compact = False     # optional

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
#today = ''
# Else, today_fmt is used as the format for a strftime call.
#today_fmt = '%%B %%d, %%Y'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = []

# The reST default role (used for this markup: `text`) to use for all documents.
#default_role = None

# If true, '()' will be appended to :func: etc. cross-reference text.
#add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
#add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
#show_authors = False

#language to highlight source code in
highlight_language = 'guess' #'%(code_lang)s'

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx' #'sphinx'

# A list of ignored prefixes for module index sorting.
#modindex_common_prefix = []

# -- Options for HTML Slide output ---------------------------------------------------
sys.path.append('%(theme_dir)s')
slide_theme_path = ['%(theme_dir)s']

# Themes that are defined by hieroglyph; using them breaks some custom ODSA content
# slide_theme = 'single-level' # basic theme
# slide_theme = 'slides' # default theme
# slide_theme = 'slides2' # animated theme

# Custom themes, made for ODSA content:
slide_theme = 'slidess' # working, default theme for all slides
# The 'haiku' theme is not for slides

#slide_theme_options = {'custom_css':'custom.css'}

slide_link_html_to_slides = not on_slides
slide_link_html_sections_to_slides = not on_slides
#slide_relative_path = "./slides/"

slide_link_to_html = True
slide_html_relative_path = "../"


# -- Options for HTML output ---------------------------------------------------
#The fully-qualified name of a HTML Translator, that is used to translate document
#trees to HTML.
html_translator_class = 'html5.HTMLTranslator'


# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
sys.path.append('%(theme_dir)s')
html_theme_path = ['%(theme_dir)s']
if on_slides:
   html_theme = 'slides'
else:
   html_theme = '%(theme)s'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
html_theme_options = json.loads(%(html_theme_options)s)

# Add any paths that contain custom themes here, relative to this directory.
#html_theme_path = []

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
html_title = '%(title)s'

# A shorter title for the navigation bar.  Default is the same as html_title.
#html_short_title = None

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
html_logo =  "_static/OpenDSALogoT64.png"

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
#html_favicon = None

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Manipulates the lists of scripts that jQuery automatically loads
# The Sphinx-generated search page is dependent on certain files being loaded in the head element whereas
# we normally want to load these scripts in the body to make the page load faster
# 'script_files' will be loaded in the head element on search.html and in the body on all other pages
# (setting this value here overrides Sphinx's default script files, so we have to add 'underscore.js' and 'doctools.js')
# 'search_scripts' are only loaded on the search page
# 'odsa_scripts' will be loaded as part of the body on all pages
# 'css_files' adds our custom CSS files to be loaded in the head element so that page doesn't have to re-render
# all the content that loaded before the CSS files
# 'odsa_root_path' specifies the relative path from the HTML output directory to the ODSA root directory and is used
# to properly link to Privacy.html
# The code that appends these scripts can be found in RST/_themes/haiku/layout.html and basic/layout.html

html_context = {"script_files": [
                  #'https://code.jquery.com/jquery-2.1.4.min.js',
                  '%(eb2root)slib/jquery.min.js',
                  '%(eb2root)slib/jquery.migrate.min.js',
                  'https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.1/MathJax.js?config=TeX-AMS-MML_HTMLorMML',
                  'https://cdnjs.cloudflare.com/ajax/libs/localforage/1.9.0/localforage.min.js'
                  %(html_js_files)s
                ],
                "search_scripts": [
                  '_static/underscore.js',
                  '_static/doctools.js'
                ],
                "odsa_scripts": [
                  #'https://code.jquery.com/ui/1.11.4/jquery-ui.min.js',
                  '%(eb2root)slib/jquery.scrolldepth.js',
                  '%(eb2root)slib/timeme.js',
                  '%(eb2root)slib/jquery.ui.min.js',
                  '%(eb2root)slib/jquery.transit.js',
                  '%(eb2root)slib/raphael.js',
                  '%(eb2root)slib/JSAV-min.js',
                  '_static/config.js',
                  '%(eb2root)slib/timeme-min.js',
                  '%(eb2root)slib/odsaUtils-min.js',
                  '%(eb2root)slib/odsaMOD-min.js',
                  'https://cdnjs.cloudflare.com/ajax/libs/d3/4.13.0/d3.min.js',
                  'https://d3js.org/d3-selection-multi.v1.min.js',
                  '%(eb2root)slib/dataStructures.js',
                  '%(eb2root)slib/conceptMap.js'
                ],
                "css_files": [
                  '%(eb2root)slib/normalize.css',
                  '%(eb2root)slib/JSAV.css',
                  '%(eb2root)slib/odsaMOD-min.css',
                  '%(eb2root)slib/jquery.ui.min.css',
                  #'https://code.jquery.com/ui/1.11.4/themes/smoothness/jquery-ui.css',
                  '%(eb2root)slib/odsaStyle-min.css'
                   %(html_css_files)s                  
                ],
                "odsa_root_path": "%(eb2root)s",
                %(text_translated)s}

if on_slides:
   html_context["css_files"].append('%(eb2root)slib/ODSAcoursenotes.css');
   html_context["odsa_scripts"].append('%(eb2root)slib/ODSAcoursenotes.js');

if '%(theme)s' != 'haiku':
  html_context['script_files'] += html_context['odsa_scripts']

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
html_last_updated_fmt = '%%b %%d, %%Y'

# Custom sidebar templates, maps document names to template names.
#html_sidebars = []

# Additional templates that should be rendered to pages, maps page names to
# template names.
#html_additional_pages = {}

# If false, no module index is generated.
#html_domain_indices = True

# If false, no index is generated.
#html_use_index = True

# If true, the index is split into individual pages for each letter.
#html_split_index = False

# If true, links to the reST sources are added to the pages.
#html_show_sourcelink = True

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
#html_show_sphinx = True

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
#html_show_copyright = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
#html_use_opensearch = ''

# This is the file name suffix for HTML files (e.g. ".xhtml").
#html_file_suffix = None

# Output file base name for HTML help builder.
htmlhelp_basename = 'OpenDSAdoc'


# -- My stuff ------------------------------------------------

todo_include_todos = True

#---- OpenDSA variables ---------------------------------------

# @efouh: despise the fact that we are using an url hash, gradebook still needs book name
book_name = '%(book_name)s'

# Boolean to control whether book will compile in local mode, which means no communication with the server
local_mode = %(local_mode)s


#Absolute path to OpenDSA directory
odsa_path = '%(odsa_dir)s'

#Absolute path of eTextbook (build) directory
ebook_path = '%(book_dir)s%(rel_book_output_path)s'

#path (from the RST home) to the sourcecode directory that I want to use
sourcecode_path = '%(code_dir)s'

# Dictionary containing code_lang to extension mapping
code_lang = '%(code_lang)s'

# Boolean that controls whether or not code is displayed in tabs if more than one language is available
tabbed_codeinc = %(tabbed_code)s

# Path to AV/ directory (local or remote)
av_dir = '%(av_root_dir)s'

# Path to Exercises/ directory (local or remote)
exercises_dir = '%(exercises_root_dir)s'

# Path to translation json file
translation_file = '%(odsa_dir)stools/language_msg.json'
'''


# Used to create a JS file with settings common to all modules
config_js_template = '''\
"use strict";
(function () {
  var settings = {};
  //@efouh: added this variable back because it is needed by gradebook.html
  settings.BOOK_NAME = "%(book_name)s";
  settings.BOOK_LANG = "%(lang)s";
  settings.REQ_FULL_SS = %(req_full_ss)s;
  settings.BUILD_TO_ODSA = "OpenDSA/";
  settings.LOCAL_MODE = %(local_mode)s;
  settings.NARRATION_ENABLED = %(narration_enabled)s;

  window.ODSA = window.ODSA || {};
  window.ODSA.SETTINGS = settings;
}());
'''

# Add the index.html file that redirects to the build/html directory
index_html_template = '''\
<html lang="en">
<head>
  <script>
    window.location.replace(window.location.href.replace(/\\/(index.html)?$/, '/%s'));
  </script>
</head>
</html>
'''
