import streamlit as st
import pandas as pd
from src.ui.components import render_kpi_section, render_signal_card, show_details_dialog
from src.logic.filters import filter_dataframe, sort_dataframe, paginate_dataframe

def render_sidebar():
    """
    Renders the sidebar and returns the language setting (is_ko boolean).
    """
    with st.sidebar:
        st.title("Research Radar 📡")
        st.caption("AI-Powered Intelligence")
        st.markdown("---")
        
        # Language Settings
        lang = st.radio("Language / 언어", ["English", "한국어"])
        is_ko = lang == "한국어"
        
        st.markdown("---")
        st.caption("v2.0.0 | PwC Global Research")
        
    return is_ko

def render_main_content(df_cards, reports, T, is_ko, all_industries, all_techs, report_map):
    """
    Renders the main content of the application.
    """
    st.markdown("###") # Top Spacer

    # 1. KPI / Header Section
    render_kpi_section(df_cards, reports, T)

    # Tabs
    tab1, tab2 = st.tabs([T["Tab_Dashboard"], T["Tab_Guide"]])

    with tab2:
        st.markdown(T["Guide_Intro"])
        st.markdown("---")
        st.markdown(T["Guide_Methodology"])
        
    with tab1:
        # 2. Control Bar (Search & Filter)
        st.markdown(f'<div class="filter-bar">', unsafe_allow_html=True)
        c1, c2, c3 = st.columns([2, 1, 1])
        
        with c1:
            search_query = st.text_input("Search", placeholder=T["Search Placeholder"], label_visibility="collapsed")
            
        with c2:
            sort_option = st.selectbox("Sort", [T["Sort_Newest"], T["Sort_Score"]], label_visibility="collapsed")
            
        with c3:
            # Toggle for Advanced Filters
            show_advanced = st.toggle(T["Advanced Filters"], value=False)
            
        st.markdown('</div>', unsafe_allow_html=True)
        
        selected_industries = []
        selected_techs = []
        min_score = 0

        # 3. Advanced Filters (Collapsible)
        if show_advanced:
            with st.container():
                st.markdown(f"#### {T['Advanced Filters']}")
                af1, af2, af3 = st.columns(3)
                with af1:
                    selected_industries = st.multiselect(T["Industry"], sorted(list(all_industries)))
                with af2:
                    selected_techs = st.multiselect(T["Technology"], sorted(list(all_techs)))
                with af3:
                    min_score = st.slider(T["Min Score"], 0, 100, 50, step=10)
                
                if st.button(T["Reset"], type="secondary"):
                    st.rerun()
                st.markdown("---")
                
        # --- Filtering Logic ---
        if not df_cards.empty:
            # Apply Filters
            filtered_df = filter_dataframe(df_cards, search_query, selected_industries, selected_techs, min_score)
            
            # Apply Sorting
            filtered_df = sort_dataframe(filtered_df, sort_option, T)

            # --- Active Filters Display (Chips) ---
            if search_query:
                st.markdown(f'<span class="filter-chip">🔍 "{search_query}"</span>', unsafe_allow_html=True)
            
            # --- Pagination ---
            if 'page' not in st.session_state:
                st.session_state.page = 1
                
            items_per_page = 6
            
            # Get Paginated Data
            page_df, total_pages, p_start, p_end = paginate_dataframe(filtered_df, st.session_state.page, items_per_page)
            
            # Ensure page is valid after filtering (if we filtered down to fewer pages)
            if st.session_state.page > total_pages:
                 st.session_state.page = total_pages
                 # Re-slice if page changed
                 page_df, total_pages, p_start, p_end = paginate_dataframe(filtered_df, st.session_state.page, items_per_page)
            
            total_items = len(filtered_df)

            # Top Pagination Controls
            c_pg1, c_pg2 = st.columns([1, 1])
            with c_pg1:
                 st.caption(f"{T['Showing']} {p_start+1}-{min(p_end, total_items)} {T['of']} {total_items} {T['signals']}")
            with c_pg2:
                if total_pages > 1:
                    c_b1, c_b2, c_b3, c_b4 = st.columns([1, 1, 3, 1])
                    with c_b2:
                        if st.button("<", key="prev_top", help="Previous Page"):
                             if st.session_state.page > 1:
                                 st.session_state.page -= 1
                                 st.rerun()
                    with c_b3:
                         st.markdown(f"<div style='text-align:center; padding-top:10px;'>{st.session_state.page} / {total_pages}</div>", unsafe_allow_html=True)
                    with c_b4:
                        if st.button(">", key="next_top", help="Next Page"):
                             if st.session_state.page < total_pages:
                                 st.session_state.page += 1
                                 st.rerun()
            
            # --- Card Rendering ---
            cols = st.columns(2)
            
            for i, (index, row) in enumerate(page_df.iterrows()):
                with cols[i % 2]:
                    # Call Component to Render Card
                    render_signal_card(row, index, is_ko, T, report_map)

        else:
            st.info(T["No Signals"])

    # --- Footer ---
    st.markdown("---")
    st.markdown(f"<div style='text-align:center; color:#666; padding: 20px;'>{T['Footer']}</div>", unsafe_allow_html=True)
