import streamlit as st
import pandas as pd
from src.ui.components import render_kpi_section, render_signal_card, show_details_dialog
from src.logic.filters import filter_dataframe, sort_dataframe, paginate_dataframe

def render_sidebar():
    """
    Renders the sidebar and returns the language setting (is_ko boolean).
    """
    with st.sidebar:
        # Custom Logo Area
        st.markdown("""
        <div style="display:flex; align-items:center; gap:10px; margin-bottom: 20px;">
            <div style="width:32px; height:32px; background-color: #2563EB; border-radius:6px; display:flex; align-items:center; justify-content:center; color:white; font-weight:bold;">R</div>
            <div>
                <div style="font-weight:700; color:white; font-size:1.1rem;">Research Radar</div>
                <div style="font-size:0.7rem; color:#6B7280;">Opportunity Discovery Platform</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation (Custom Button List)
        if 'nav_page' not in st.session_state:
            st.session_state.nav_page = "Dashboard"
            
        nav_items = ["Dashboard", "Opportunities", "Methodology"]
        
        # Lucide SVGs (Inline)
        # We use a helper dict to map names to SVG content.
        # Icons: BarChart2 (Dashboard), Target (Opportunities), FlaskConical (Methodology)
        
        lucide_icons = {
            "Dashboard": """<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line></svg>""",
            "Opportunities": """<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><circle cx="12" cy="12" r="6"></circle><circle cx="12" cy="12" r="2"></circle></svg>""",
            "Methodology": """<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 2v7.31"></path><path d="M14 2v7.31"></path><path d="M8.5 2h7"></path><path d="M14 9.3a6.5 6.5 0 1 1-4 0"></path></svg>"""
        }
        
        for item in nav_items:
            svg = lucide_icons.get(item, "")
            
            if st.session_state.nav_page == item:
                # Active State (Blue Pill) - HTML allows SVG
                # Adjusted alignment to match the column layout of inactive state roughly
                label_html = f"""
                <div class="nav-active" style="display:flex; align-items:center; gap:12px; padding-left:12px;">
                    <span style="display:flex; align-items:center; width:20px; justify-content:center;">{svg}</span>
                    <span style="padding-top:2px;">{item}</span>
                </div>
                """
                st.markdown(label_html, unsafe_allow_html=True)
            else:
                # Inactive State (Ghost Button)
                # Using Columns [Icon, Button]
                # Adjust column ratio to bring text closer if needed, or rely on style cleanup
                
                c_icon, c_btn = st.columns([0.15, 0.85])
                with c_icon:
                    # Centered icon in the small column
                    st.markdown(f"<div style='margin-top:6px; display:flex; justify-content:center; opacity:0.7;'>{svg}</div>", unsafe_allow_html=True)
                with c_btn:
                     if st.button(item, key=f"nav_{item}", use_container_width=True):
                        st.session_state.nav_page = item
                        st.rerun()
        
        page = st.session_state.nav_page
        
        st.markdown("---")
        
        # Language Settings
        lang = st.radio("Language / 언어", ["English", "한국어"], 
                        index=0 if st.session_state.get('language', 'English') == 'English' else 1,
                        key="sidebar_lang")
        
        if lang != st.session_state.get('language'):
            st.session_state.language = lang
            st.rerun()
        
        st.markdown("---")
        st.caption("v2.1.0 | PwC Global Research")
        
        # Network Integration (Mock)
        st.markdown("""
        <div style="background:#1E293B; padding:12px; border-radius:8px; margin-top:20px;">
            <div style="font-size:0.7rem; color:#6B7280; margin-bottom:8px; font-weight:bold;">NETWORK INTEGRATION</div>
            <div style="display:flex; gap:8px;">
                <span style="background:#334155; padding:2px 6px; border-radius:4px; font-size:0.65rem;">PwC Insights</span>
                <span style="background:#334155; padding:2px 6px; border-radius:4px; font-size:0.65rem;">OpenAI</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    return page

def render_main_content(page, df_cards, reports, T, is_ko, all_industries, all_techs, report_map):
    """
    Renders the main content of the application based on the selected page.
    """
    st.markdown("###") # Top Spacer

    # --- VIEW: DASHBOARD ---
    if page == "Dashboard":
        # Header Area with Language Selector
        # Header Area
        st.markdown(f"""
        <div>
            <h1 style="font-size: 2rem; margin-bottom: 8px;">{T['Dashboard Title']}</h1>
            <p style="color: var(--text-secondary); margin-bottom: 32px;">{T['Dashboard Subtitle']}</p>
        </div>
        """, unsafe_allow_html=True)

        # 1. KPI / Header Section
        render_kpi_section(df_cards, reports, T, is_ko)

        # 2. Middle Section: Trending & Framework
        m1, m2 = st.columns([1.2, 1.8], gap="large")
        
        # Calculate Trending Sectors
        top_sectors = []
        if not df_cards.empty and 'industry_tags' in df_cards.columns:
            all_tags = df_cards['industry_tags'].explode().dropna()
            if not all_tags.empty:
                counts = all_tags.value_counts().head(3)
                max_val = counts.iloc[0] if not counts.empty else 1
                for tag, count in counts.items():
                    pct = int((count / max_val) * 85)
                    final_label = tag
                    if is_ko:
                        if tag == "Artificial Intelligence": final_label = T.get('Sector_AI', tag)
                        elif tag == "Cybersecurity": final_label = T.get('Sector_Cybersecurity', tag)
                        elif tag == "Sustainable Energy": final_label = T.get('Sector_Energy', tag)
                        elif tag == "Legal Services": final_label = T.get('Sector_Legal', tag)
                        elif tag == "Financial Services": final_label = T.get('Sector_Finance', tag)
                    top_sectors.append((final_label, pct, count))
        
        while len(top_sectors) < 3:
            top_sectors.append(("-", 0, 0))

        with m1:
            st.markdown(f"### 📈 {T['Trending Title']}")
            # Trending Container
            st.markdown(f"""
            <div style="background:white; border:1px solid var(--border-color); border-radius:12px; padding:24px; height:100%; box-shadow: var(--shadow-sm);">
                <div style="margin-bottom:16px;">
                    <div style="display:flex; justify-content:space-between; margin-bottom:4px; font-size:0.9rem; font-weight:500;">
                        <span>01 &nbsp; {top_sectors[0][0]} <span style="color:var(--text-secondary); margin-left:4px; font-size:0.8rem;">({top_sectors[0][2]})</span></span>
                    </div>
                    <div style="height:6px; width:100%; background:#F1F5F9; border-radius:3px;">
                        <div style="height:100%; width:{top_sectors[0][1]}%; background:var(--accent-primary); border-radius:3px;"></div>
                    </div>
                </div>
                <div style="margin-bottom:16px;">
                    <div style="display:flex; justify-content:space-between; margin-bottom:4px; font-size:0.9rem; font-weight:500;">
                        <span>02 &nbsp; {top_sectors[1][0]} <span style="color:var(--text-secondary); margin-left:4px; font-size:0.8rem;">({top_sectors[1][2]})</span></span>
                    </div>
                    <div style="height:6px; width:100%; background:#F1F5F9; border-radius:3px;">
                        <div style="height:100%; width:{top_sectors[1][1]}%; background:var(--accent-primary); border-radius:3px;"></div>
                    </div>
                </div>
                <div>
                    <div style="display:flex; justify-content:space-between; margin-bottom:4px; font-size:0.9rem; font-weight:500;">
                        <span>03 &nbsp; {top_sectors[2][0]} <span style="color:var(--text-secondary); margin-left:4px; font-size:0.8rem;">({top_sectors[2][2]})</span></span>
                    </div>
                    <div style="height:6px; width:100%; background:#F1F5F9; border-radius:3px;">
                        <div style="height:100%; width:{top_sectors[2][1]}%; background:var(--accent-primary); border-radius:3px;"></div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        with m2:
            # Framework Section
            st.markdown(f"### 🛠 {T['Framework Title']}")
            st.markdown(f"""
            <div style="background:white; border:1px solid var(--border-color); border-radius:12px; padding:24px; height:100%; display:flex; flex-direction:column; justify-content:center; box-shadow: var(--shadow-sm);">
                <p style="color:var(--text-secondary); margin-bottom:24px; line-height:1.6; font-size:0.95rem;">{T['Framework Desc']}</p>
                <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:12px; text-align:center;">
                     <div style="flex:1;">
                        <div style="background:#EFF6FF; width:40px; height:40px; border-radius:50%; display:flex; align-items:center; justify-content:center; margin:0 auto 8px auto; color:var(--accent-primary);">
                            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><ellipse cx="12" cy="5" rx="9" ry="3"></ellipse><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"></path><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"></path></svg>
                        </div>
                        <div style="font-size:0.8rem; font-weight:600;">Data</div>
                     </div>
                     <div style="padding-top:10px; color:#CBD5E1;">→</div>
                     <div style="flex:1;">
                        <div style="background:#EFF6FF; width:40px; height:40px; border-radius:50%; display:flex; align-items:center; justify-content:center; margin:0 auto 8px auto; color:var(--accent-primary);">
                             <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="4" width="16" height="16" rx="2" ry="2"></rect><rect x="9" y="9" width="6" height="6"></rect><line x1="9" y1="1" x2="9" y2="4"></line><line x1="15" y1="1" x2="15" y2="4"></line><line x1="9" y1="20" x2="9" y2="23"></line><line x1="15" y1="20" x2="15" y2="23"></line><line x1="20" y1="9" x2="23" y2="9"></line><line x1="20" y1="14" x2="23" y2="14"></line><line x1="1" y1="9" x2="4" y2="9"></line><line x1="1" y1="14" x2="4" y2="14"></line></svg>
                        </div>
                        <div style="font-size:0.8rem; font-weight:600;">AI Analysis</div>
                     </div>
                     <div style="padding-top:10px; color:#CBD5E1;">→</div>
                     <div style="flex:1;">
                        <div style="background:#EFF6FF; width:40px; height:40px; border-radius:50%; display:flex; align-items:center; justify-content:center; margin:0 auto 8px auto; color:var(--accent-primary);">
                            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
                        </div>
                        <div style="font-size:0.8rem; font-weight:600;">Validation</div>
                     </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("###")
        st.divider()
        
        # New Header + Search
        s1, s2, s3 = st.columns([0.6, 0.3, 0.1])
        with s1:
            st.markdown(f"### ⚡ {T['Critical Signals']} (Latest)")
        with s2:
            dash_search = st.text_input("Search", placeholder=T["Search Placeholder"], key="dash_search", label_visibility="collapsed")
        with s3:
            st.markdown("<div style='height: 4px;'></div>", unsafe_allow_html=True)
            if st.button("View All", key="view_all_signals", type="secondary", use_container_width=True):
                st.session_state.nav_page = "Opportunities"
                st.rerun()
        
        # Show specific high-score signals manually
        if not df_cards.empty:
            filtered_view = df_cards
            if dash_search:
                term = dash_search.lower()
                filtered_view = df_cards[
                    df_cards.apply(lambda r: 
                        term in str(r.get('attack_vector', '')).lower() or 
                        term in str(r.get('pain_holder', '')).lower() or
                        term in str(r.get('industry_tags', '')).lower(), axis=1)
                ]

            if 'importance_score' in filtered_view.columns:
                top_signals = filtered_view.sort_values(by='importance_score', ascending=False, na_position='last')
            else:
                top_signals = filtered_view.sort_values(by='created_at', ascending=False)
                
            top_signals = top_signals.head(4)

            cols = st.columns(2)
            for i, (index, row) in enumerate(top_signals.iterrows()):
                with cols[i % 2]:
                    render_signal_card(row, index, is_ko, T, report_map)
        else:
            st.info(T["No Signals"])

    # --- VIEW: OPPORTUNITIES ---
    elif page == "Opportunities":
        # Opportunity Feed Header
        st.markdown(f"## {T.get('Feed Title', 'Opportunity Feed')}")
        
        # Control Bar (Search & Filter)
        st.markdown(f'<div class="filter-bar">', unsafe_allow_html=True)
        c1, c2, c3 = st.columns([3, 1, 1], gap="small")
        
        with c1:
            # Cognitive Analysis: Better Placeholder
            search_query = st.text_input("Search", placeholder=T.get("Search_Placeholder_New", T["Search Placeholder"]), label_visibility="collapsed", key="feed_search")
            
            # Cognitive Analysis: Chips for "Try:" section
            q_tags = ["Fraud Detection", "Climate Risk", "Legal AI", "Supply Chain"] if not is_ko else ["사기 탐지", "기후 리스크", "법률 AI", "공급망"]
            
            # Helper to create chip-like buttons using custom CSS or just columns
            # Using columns for now as Streamlit native buttons are limited in style without extra hacks
            st.markdown(f"<div style='margin-top:8px; margin-bottom:8px; display:flex; align-items:center; gap:8px;'>", unsafe_allow_html=True)
            st.markdown(f"<span style='font-size:0.85rem; color:#64748B; margin-right:4px;'>{T.get('Quick Filters', 'Try')}:</span>", unsafe_allow_html=True)
            
            # Callback safely updates state
            def set_search_query(q):
                st.session_state.feed_search = q

            # We render buttons horizontally. 
            # Note: Streamlit buttons inside markdown is tricky. We'll use columns below the text label.
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Chip Row
            chip_cols = st.columns([1, 1, 1, 1, 3]) # Adjust ratios to fit
            for i, tag in enumerate(q_tags):
                 if i < 4:
                     # Use type="secondary" for a softer look (if theme supports it, else default)
                     chip_cols[i].button(tag, key=f"qtag_{i}", on_click=set_search_query, args=(tag,), use_container_width=True)
            
        with c2:
            # Sort Logic: Added Highest Score
            sort_options = ["Latest", "Highest Score"] if not is_ko else ["최신순", "높은 점수순"]
            sort_selection = st.selectbox("Sort", sort_options, label_visibility="collapsed", key="feed_sort")
            
        with c3:
            # Cognitive Analysis: Show active count if possible?
            # For now, just Toggle
            show_advanced = st.toggle(T["Advanced Filters"], value=False)
            
        st.markdown('</div>', unsafe_allow_html=True)
        
        selected_industries = []
        selected_techs = []
        min_score = 0

        # Advanced Filters (Collapsible)
        score_range = (0, 100) # Default
        if show_advanced:
            with st.container():
                st.markdown(f"#### {T['Advanced Filters']}")
                
                # P2: Advanced Filters Structure (3 Columns)
                af1, af2, af3 = st.columns([2, 2, 1], gap="medium")
                
                with af1:
                    st.caption(f"**{T['Industry']} & {T['Technology']}**")
                    selected_industries = st.multiselect(T["Industry"], sorted(list(all_industries)), label_visibility="collapsed", placeholder=f"Select {T['Industry']}...")
                    selected_techs = st.multiselect(T["Technology"], sorted(list(all_techs)), label_visibility="collapsed", placeholder=f"Select {T['Technology']}...")
                
                with af2:
                    st.caption(f"**{T.get('Filter_Label_Score_Range', 'Score Range')}**")
                    score_range = st.slider(T.get('Filter_Label_Score_Range', 'Score Range'), 0, 100, (50, 100), label_visibility="collapsed")
                    
                    # Future: Date Range or Confidence Range here
                
                with af3:
                    st.caption(f"**{T.get('Actions', 'Actions')}**")
                    if st.button(T["Reset"], type="secondary", use_container_width=True):
                        st.session_state.feed_search = ""
                        st.rerun()
                
                st.markdown("---")
                
        # Filtering Logic
        if not df_cards.empty:
            # Apply Filters (Updated for Range)
            filtered_df = filter_dataframe(df_cards, search_query, selected_industries, selected_techs, score_range)
            
            # Sort Logic
            if sort_selection in ["Importance", "Highest Score", "높은 점수순", "중요도순"] and 'importance_score' in filtered_df.columns:
                filtered_df = filtered_df.sort_values(by='importance_score', ascending=False)
            else:
                filtered_df = filtered_df.sort_values(by='created_at', ascending=False)

            # Active Filters Display & Result Count
            st.markdown(f"<div style='margin-bottom:16px; font-size:1.1rem; color:#334155;'>{T['Filter_Result_Count'].format(count=len(filtered_df))}</div>", unsafe_allow_html=True)

            if search_query:
                st.markdown(f'<span class="filter-chip" style="background:#EFF6FF; color:#2563EB; border:1px solid #BFDBFE;">🔍 "{search_query}"</span>', unsafe_allow_html=True)
            
            if filtered_df.empty:
                 # Empty State
                 st.markdown(f"""
                 <div style="text-align:center; padding:40px; background:#F8FAFC; border-radius:12px; border:1px dashed #CBD5E1;">
                     <div style="font-size:2rem; margin-bottom:10px;">🔍</div>
                     <h3 style="color:#64748B;">{T.get('No_Results_Found', 'No results found.')}</h3>
                     <p style="color:#94A3B8;">Try adjusting your filters or search terms.</p>
                 </div>
                 """, unsafe_allow_html=True)
            else:
                # Pagination
                if 'card_page' not in st.session_state:
                    st.session_state.card_page = 1
                    
                items_per_page = 6
                page_df, total_pages, p_start, p_end = paginate_dataframe(filtered_df, st.session_state.card_page, items_per_page)
                
                if st.session_state.card_page > total_pages:
                        st.session_state.card_page = max(1, total_pages)
                        page_df, total_pages, p_start, p_end = paginate_dataframe(filtered_df, st.session_state.card_page, items_per_page)
                
                # Card Rendering
                cols = st.columns(2)
                for i, (index, row) in enumerate(page_df.iterrows()):
                    with cols[i % 2]:
                        # Call Component to Render Card
                        render_signal_card(row, index, is_ko, T, report_map)

                # Pagination Controls
                if total_pages > 1:
                    c_pg1, c_pg2 = st.columns([1, 1])
                    with c_pg2:
                        c_b1, c_b2, c_b3, c_b4 = st.columns([1, 1, 3, 1])
                        with c_b2:
                            if st.button("<", key="prev_top", help="Previous Page"):
                                    if st.session_state.card_page > 1:
                                        st.session_state.card_page -= 1
                                        st.rerun()
                        with c_b3:
                                st.markdown(f"<div style='text-align:center; padding-top:10px;'>{st.session_state.card_page} / {total_pages}</div>", unsafe_allow_html=True)
                        with c_b4:
                            if st.button(">", key="next_top", help="Next Page"):
                                    if st.session_state.card_page < total_pages:
                                        st.session_state.card_page += 1
                                        st.rerun()
        else:
            st.info(T["No Signals"])

    # --- VIEW: METHODOLOGY ---
    elif page == "Methodology":
        # Header (Hidden in Logic but using simple Markdown)
        st.markdown("###")
        
        st.markdown(f"""
        <div style="text-align:center; margin-bottom:40px;">
            <h2 style="font-size:2.2rem; margin-bottom:12px;">{T['Methodology Title']}</h2>
            <p style="color:var(--text-secondary); font-size:1.1rem;">{T['Methodology Subtitle']}</p>
        </div>
        """, unsafe_allow_html=True)

        # Dual Card Layout
        c_left, c_right = st.columns(2, gap="large")
        
        with c_left:
            st.markdown(f"""
<div style="background:white; padding:32px; border-radius:16px; border:1px solid var(--border-color); height:100%;">
<h3 style="color:var(--accent-primary) !important; margin-bottom:24px;">{T['Funnel Title']}</h3>
<!-- Step 1 -->
<div style="display:flex; gap:16px; margin-bottom:24px;">
<div style="min-width:32px; height:32px; background:#EFF6FF; color:var(--accent-primary); border-radius:50%; display:flex; align-items:center; justify-content:center; font-weight:bold;">1</div>
<div>
<div style="font-weight:700; color:var(--text-primary); margin-bottom:4px;">{T['Funnel_Step1_Title']}</div>
<div style="font-size:0.9rem; color:var(--text-secondary); line-height:1.5;">{T['Funnel_Step1_Desc']}</div>
<div style="margin-top:8px; display:inline-block; background:#F1F5F9; padding:4px 8px; border-radius:4px; font-size:0.75rem; color:#475569; font-weight:600;">{T['Funnel_Step1_Value']}</div>
<div style="font-size:0.75rem; color:#64748B; margin-top:4px;">{T['Data_Source_Reliability']}</div>
</div>
</div>
<!-- Step 2 -->
<div style="display:flex; gap:16px; margin-bottom:24px;">
<div style="min-width:32px; height:32px; background:#EFF6FF; color:var(--accent-primary); border-radius:50%; display:flex; align-items:center; justify-content:center; font-weight:bold;">2</div>
<div>
<div style="font-weight:700; color:var(--text-primary); margin-bottom:4px;">{T['Funnel_Step2_Title']}</div>
<div style="font-size:0.9rem; color:var(--text-secondary); line-height:1.5;">{T['Funnel_Step2_Desc']}</div>
<div style="margin-top:8px; font-size:0.8rem; color:#DC2626; font-weight:600;">{T['Funnel_Step2_Value']}</div>
<div style="font-size:0.8rem; color:#475569; margin-top:4px;">{T['Funnel_Step2_Criteria']}</div>
</div>
</div>
<!-- Step 3 -->
<div style="display:flex; gap:16px;">
<div style="min-width:32px; height:32px; background:#EFF6FF; color:var(--accent-primary); border-radius:50%; display:flex; align-items:center; justify-content:center; font-weight:bold;">3</div>
<div>
<div style="font-weight:700; color:var(--text-primary); margin-bottom:4px;">{T['Funnel_Step3_Title']}</div>
<div style="font-size:0.9rem; color:var(--text-secondary); line-height:1.5;">{T['Funnel_Step3_Desc']}</div>
<div style="margin-top:8px; display:inline-block; background:#DCFCE7; padding:4px 8px; border-radius:4px; font-size:0.75rem; color:#166534; font-weight:600;">{T['Funnel_Step3_Value']}</div>
</div>
</div>
</div>
""", unsafe_allow_html=True)
            
        with c_right:
            st.markdown(f"""
<div style="background:#0F172A; padding:32px; border-radius:16px; height:100%; color:white;">
<div style="margin-bottom:24px;">
<span style="color:var(--accent-light) !important; font-size:1.5rem; font-weight:700; font-family:'Inter', sans-serif;">{T['Benchmark Title']}</span>
</div>
<div style="border-left:2px solid #334155; padding-left:24px; margin-left:8px; padding-bottom:32px; position:relative;">
<div style="position:absolute; left:-7px; top:0; width:12px; height:12px; background:#3B82F6; border-radius:50%;"></div>
<div style="font-size:1.5rem; font-weight:bold; color:white; margin-bottom:4px;">80 - 100</div>
<div style="font-size:0.75rem; font-weight:bold; color:#3B82F6; letter-spacing:0.1em; margin-bottom:8px;">{T['Bench_High_Label']}</div>
<div style="font-size:0.9rem; color:#94A3B8; line-height:1.5;">{T['Bench_High_Desc']}</div>
</div>
<div style="border-left:2px solid #334155; padding-left:24px; margin-left:8px; position:relative;">
<div style="position:absolute; left:-7px; top:0; width:12px; height:12px; background:#64748B; border-radius:50%;"></div>
<div style="font-size:1.5rem; font-weight:bold; color:white; margin-bottom:4px;">50 - 79</div>
<div style="font-size:0.75rem; font-weight:bold; color:#94A3B8; letter-spacing:0.1em; margin-bottom:8px;">{T['Bench_Mid_Label']}</div>
<div style="font-size:0.9rem; color:#94A3B8; line-height:1.5;">{T['Bench_Mid_Desc']}</div>
</div>
</div>
""", unsafe_allow_html=True)

        st.markdown("###")
        
        # Quote Card
        st.markdown(f"""
<div class="rr-center">
  <div class="rr-quote-wrap">
    <div class="rr-quote-mark">“</div>
    <p class="rr-quote">{T['Quote Text'].strip('"')}</p>
    <div class="rr-quote-sub"><span>{T['Quote Author']}</span></div>
  </div>
</div>
""", unsafe_allow_html=True)

    # --- Footer ---
    st.markdown("---")
    st.markdown(f"<div style='text-align:center; color:#666; padding: 20px;'>{T['Footer']}</div>", unsafe_allow_html=True)

def render_admin_view(T, run_pipeline_callback=None):
    """
    Renders the Admin Dashboard for pipeline control.
    """
    st.markdown(f"## {T['Admin Title']}")
    
    st.info("Trigger the backend data ingestion pipeline manually from here.")
    
    c1, c2 = st.columns([1, 2])
    
    with c1:
        st.markdown(f"### {T['Pipeline Control']}")
        
        # We use a callback wrapper to handle the spinner and logging in the UI
        if st.button(T["Run Pipeline"], type="primary", use_container_width=True):
            if run_pipeline_callback:
                run_pipeline_callback()
            else:
                st.warning("Pipeline callback not connected.")
                
        st.markdown("---")
        if st.button(T["Reset Data"], type="secondary", use_container_width=True):
            st.warning("Reset functionality not yet connected.")
            
    with c2:
        st.markdown(f"### {T['Status Log']}")
        status_placeholder = st.empty()
        status_placeholder.code("Waiting for command...", language="text")
        
    return status_placeholder
