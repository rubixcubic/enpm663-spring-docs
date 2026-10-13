import os, sys
from datetime import date

project = "ENPM663 Spring 2027"
author = "Z. Kootbally"
copyright = f"{date.today().year}, {author}"
release = "v0.4.7"

extensions = [
    "myst_parser",
    "sphinx.ext.autosummary",
    "sphinxcontrib.mermaid",
    "sphinx_autodoc_typehints",
    "sphinx_copybutton",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
    "sphinx_design",
    "sphinx_proof",
    "sphinx.ext.todo",
    "sphinx.ext.mathjax",
    "sphinx.ext.viewcode",
]

plantuml = "https://www.plantuml.com/plantuml/png/"
plantuml_output_format = "png"

# Prerender options for better performance
katex_prerender = True

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}
proof_numbered = {
    "theorem": True,
    "lemma": True,
    "algorithm": True,
    "example": False,
}

todo_include_todos = True

templates_path = ["_templates"]
# ---------------------------------------------------------------------------
# What is published.
#
# No lecture is published yet (2026-10-11). L1 to L13 are hidden
# completely and open one at a time as their decks are finished. To open
# lecture N:
#   1. remove N from HIDDEN_LECTURES below,
#   2. restore its line in the toctree of lectures/index.rst,
#   3. turn its plain-text tags ("L7") back into links,
#      :doc:`L7 </lectures/lecture7/l7_index>`, in the glossary and on the
#      pages that mention it.
# The source files stay on disk.
# ---------------------------------------------------------------------------
HIDDEN_LECTURES = range(1, 14)

exclude_patterns = [f"lectures/lecture{n}/**" for n in HIDDEN_LECTURES]

# GP1 to GP4 are held back until they are posted. Remove an entry here
# (and restore its toctree line in assignments/index.rst) to publish it.
HIDDEN_GPS = range(1, 5)
exclude_patterns += [f"assignments/gp{n}.rst" for n in HIDDEN_GPS]

# The final demo page is held back with the GPs until its specification is
# posted (Week 12). To publish it, delete this line and restore its toctree
# line and its link in assignments/index.rst.
HIDE_FINAL_DEMO = True
if HIDE_FINAL_DEMO:
    exclude_patterns += ["assignments/final_demo.rst"]

# The Course Skills Package page is held back until the package's v1.0.0 is
# published with GP1 (2027-02-03). To publish it, delete this line and add
# "Course Skills Package <skills>" to a toctree in ariac/ariac.rst.
HIDE_SKILLS_PAGE = True
if HIDE_SKILLS_PAGE:
    exclude_patterns += ["ariac/skills.rst"]

# ---------------------------------------------------------------------------
# PyData Sphinx Theme
# ---------------------------------------------------------------------------
html_theme = "pydata_sphinx_theme"

html_theme_options = {
    # Logo (place files in _static/images/)
    "logo": {
        # No text: the logo already says ENPM663, and both linked to the home page.
        "alt_text": "ENPM663 Spring 2027, home",
        "image_light": "_static/images/enpm663_logo_light.svg",
        "image_dark": "_static/images/enpm663_logo_dark.svg",
    },
    # Header / navbar icon links
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/rubixcubic/enpm663-spring-docs",
            "icon": "fa-brands fa-github",
            "type": "fontawesome",
        },
    ],
    "back_to_top_button": True,
    # Light/dark mode toggle
    "navbar_end": ["theme-switcher", "navbar-icon-links"],
    # Navigation
    "header_links_before_dropdown": 7,
    "navigation_depth": 3,
    "show_nav_level": 1,
    "show_toc_level": 1,
    "show_prev_next": True,
    # Footer
    "footer_start": ["copyright"],
    "footer_end": ["theme-version"],
    # Syntax highlighting for light and dark modes
    "pygments_light_style": "igor",
    "pygments_dark_style": "nord",
}

# Edit on GitHub button
html_context = {
    "github_user": "rubixcubic",
    "github_repo": "enpm663-spring-docs",
    "github_version": "main",
    "doc_path": "docs/source",
    "default_mode": "dark",
}

numfig = True
numfig_format = {
    "pseudocode": "Algorithm %s",
}

html_static_path = ["_static"]
master_doc = "index"

html_css_files = [
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css", "my.css"
]

# sidebar-persist.js loads without `defer` so the stored sidebar state is
# applied before the first paint (same as ENPM702 and ENPM818Z).
html_js_files = [
    ("sidebar-persist.js", {"defer": None}),
    # Shape of the Read the Docs version menu; see the file's header.
    ("flyout-style.js", {"defer": "defer"}),
]