import streamlit as st
import pandas as pd
import os
import sys

# Add the repository root to sys.path so we can import src
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.storage import load_cards, load_reports
from src.ui.styles import apply_styles
from src.ui.localization import get_translations
from src.ui.layout import render_sidebar, render_main_content
from src.ui.components import show_onboarding_dialog
from src.pipeline import run_pipeline

# --- Page Configuration ---
st.set_page_config(
    page_title="Opportunity Radar",
    page_icon="📡",
    layout="wide"
)

def main():
    # --- Apply CSS ---
    apply_styles()
    
    # --- Language Initialization ---
    if 'language' not in st.session_state:
        st.session_state.language = "English"
        
    # --- Onboarding State (Initialize only once) ---
    if 'has_seen_onboarding' not in st.session_state:
        st.session_state.has_seen_onboarding = False

    # --- Sidebar ---
    # Defensive Coding: Handle potential module caching where render_sidebar might still return a tuple
    sidebar_result = render_sidebar()
    if isinstance(sidebar_result, tuple):
        page = sidebar_result[1] # Legacy/Cached behavior (is_ko, page)
    else:
        page = sidebar_result

    # --- Localization ---
    is_ko = st.session_state.language == "한국어"
    T = get_translations(is_ko)

    # Show onboarding dialog only on first visit
    if not st.session_state.has_seen_onboarding:
        show_onboarding_dialog(is_ko, T)

    # --- Router ---
    # Admin page removed per user request.
    
    # --- Data Loading (Lazy load unless needed) ---
    all_cards = load_cards()
    df_cards = pd.DataFrame([c.model_dump() for c in all_cards])

    reports = load_reports()
    report_map = {r.report_id: r for r in reports}

    # Extract Filters Data
    all_industries = set()
    all_techs = set()

    if not df_cards.empty:
        for tags in df_cards['industry_tags']:
             if isinstance(tags, list):
                all_industries.update(tags)
        for tags in df_cards['technology_tags']:
             if isinstance(tags, list):
                all_techs.update(tags)

    # --- Main Content Area ---
    render_main_content(page, df_cards, reports, T, is_ko, all_industries, all_techs, report_map)

if __name__ == "__main__":
    main()
