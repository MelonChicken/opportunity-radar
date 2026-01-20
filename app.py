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

# --- Page Configuration ---
st.set_page_config(
    page_title="Research Radar",
    page_icon="📡",
    layout="wide"
)

def main():
    # --- Apply CSS ---
    apply_styles()

    # --- Sidebar ---
    is_ko = render_sidebar()

    # --- Localization ---
    T = get_translations(is_ko)

    # --- Data Loading ---
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
    render_main_content(df_cards, reports, T, is_ko, all_industries, all_techs, report_map)

if __name__ == "__main__":
    main()
