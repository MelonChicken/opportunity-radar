"""
Package initializer for modular CSS styles
"""

import streamlit as st

from .base import load_base_css
from .sidebar import load_sidebar_css
from .cards import load_cards_css
from .forms import load_forms_css
from .buttons import load_buttons_css
from .dialogs import load_dialogs_css
from .components import load_components_css
from .chips import load_chips_css
from .utilities import load_utilities_css


def load_css():
    """
    Load all CSS modules and combine them into a single stylesheet.
    
    Returns:
        str: Complete CSS as a string wrapped in <style> tags
    """
    css_modules = [
        load_base_css(),
        load_utilities_css(),
        load_sidebar_css(),
        load_cards_css(),
        load_forms_css(),
        load_buttons_css(),
        load_dialogs_css(),
        load_components_css(),
        load_chips_css(),
    ]
    
    combined_css = "\n".join(css_modules)
    return f"<style>\n{combined_css}\n</style>"


def apply_styles():
    """
    Apply all CSS styles to the Streamlit app.
    """
    st.markdown(load_css(), unsafe_allow_html=True)


__all__ = [
    'load_base_css',
    'load_sidebar_css',
    'load_cards_css',
    'load_forms_css',
    'load_buttons_css',
    'load_dialogs_css',
    'load_components_css',
    'load_css',
    'apply_styles',
]
