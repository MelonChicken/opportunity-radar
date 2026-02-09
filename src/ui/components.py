import streamlit as st
import html
import pandas as pd
from src.logic.prompts import build_prompt_from_card

@st.dialog("Signal Details / 상세 내용", width="large")
def show_details_dialog(row, is_ko, T, report_map):
    # Strict Language Separation (No Fallback to preserve language purity)
    if is_ko:
        attack = row.get('attack_vector_ko', '')
        holder = row.get('pain_holder_ko', '')
        context = row.get('pain_context_ko', '')
        mechanism = row.get('pain_mechanism_ko', '')
        evidence = row.get('evidence_sentence_ko', '')
    else:
        attack = row.get('attack_vector', '')
        holder = row.get('pain_holder', '')
        context = row.get('pain_context', '')
        mechanism = row.get('pain_mechanism', '')
        evidence = row.get('evidence_sentence', '')
    
    # Handle potentially missing data with a language-appropriate placeholder
    if not holder: holder = "-"
    if not context: context = "-"
    if not mechanism: mechanism = "-"
    if not evidence: evidence = "-"
    
    report = report_map.get(row['report_id'])
    report_url = report.url if report else "#"
    
    # Generate Prompt (Always English data for the Prompt Logic usually, but displayed to user)
    # The Prompt Template is internal logic, so English is usually fine, but the user views it.
    prompt_text = build_prompt_from_card(row, report_url)

    left, right = st.columns([1.1, 1.9], gap="medium")

    with left:
        # Calculate score-based styling
        score = row['importance_score']
        conf_val = int(row.get('confidence_score', 0)*100)
        
        if score >= 80:
            score_label = T.get('Score_High', 'High Potential')
            score_color = '#DC2626'
        elif score >= 60:
            score_label = T.get('Score_Medium', 'Medium')
            score_color = '#2563EB'
        else:
            score_label = T.get('Score_Low', 'Low')
            score_color = '#64748B'
        
        # ============ CARD 1: TARGET ============
        with st.container(border=True):
            # Section title with icon
            st.markdown(f"""
            <div style='font-size:14px; font-weight:600; color:#64748B; margin-bottom:12px;'>
                🎯 {T['Target_Label']}
            </div>
            """, unsafe_allow_html=True)
            
            # Target main text (large, bold)
            st.markdown(f"""
            <div style='font-size:20px; font-weight:700; color:#1E293B; margin-bottom:10px; line-height:1.3;'>
                {html.escape(holder)}
            </div>
            """, unsafe_allow_html=True)
            
            # Context as chip
            if context and context != "-":
                st.markdown(f"""
                <span style='display:inline-block; background:#EFF6FF; color:#2563EB; padding:6px 12px; 
                             border-radius:999px; font-size:12px; font-weight:500;'>
                    {html.escape(context)}
                </span>
                """, unsafe_allow_html=True)
        
        # Vertical spacing
        st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)
        
        # ============ CARD 2: PAIN POINT ============
        with st.container(border=True):
            st.markdown(f"""
            <div style='border-left:4px solid #F97316; padding-left:12px;'>
                <div style='font-size:14px; font-weight:600; color:#64748B; margin-bottom:8px;'>
                    ⚠️ {T['Pain_Label']}
                </div>
                <div style='font-size:14px; line-height:1.6; color:#1E293B;'>
                    {html.escape(mechanism)}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Vertical spacing
        st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)
        
        # ============ CARD 3: TAGS ============
        with st.container(border=True):
            # Section title
            st.markdown(f"""
            <div style='font-size:14px; font-weight:600; color:#64748B; margin-bottom:12px;'>
                🏷 {T['Tags']}
            </div>
            """, unsafe_allow_html=True)
            
            # Industry chips (Purple)
            st.markdown(f"<div style='font-size:12px; color:#64748B; margin-bottom:6px;'>{T['Industry']}</div>", unsafe_allow_html=True)
            industry_tags = row.get('industry_tags', [])
            if industry_tags:
                chips_html = ""
                for tag in industry_tags:
                    chips_html += f"""
                    <span style='display:inline-block; background:#EDE9FE; color:#7C3AED; padding:6px 10px; 
                                 border-radius:999px; font-size:12px; font-weight:500; margin-right:6px; margin-bottom:6px;'>
                        {html.escape(str(tag))}
                    </span>
                    """
                st.markdown(f"<div style='display:flex; flex-wrap:wrap; gap:6px; margin-bottom:12px;'>{chips_html}</div>", unsafe_allow_html=True)
            else:
                st.caption("-")
            
            # Technology chips (Green/Teal)
            st.markdown(f"<div style='font-size:12px; color:#64748B; margin-bottom:6px;'>{T['Technology']}</div>", unsafe_allow_html=True)
            tech_tags = row.get('technology_tags', [])
            if tech_tags:
                chips_html = ""
                for tag in tech_tags:
                    chips_html += f"""
                    <span style='display:inline-block; background:#D1FAE5; color:#059669; padding:6px 10px; 
                                 border-radius:999px; font-size:12px; font-weight:500; margin-right:6px; margin-bottom:6px;'>
                        {html.escape(str(tag))}
                    </span>
                    """
                st.markdown(f"<div style='display:flex; flex-wrap:wrap; gap:6px;'>{chips_html}</div>", unsafe_allow_html=True)
            else:
                st.caption("-")
        
        # Vertical spacing
        st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)
        
        # ============ CARD 4: SCORE & METRICS ============
        with st.container(border=True):
            # Section title
            st.markdown(f"""
            <div style='font-size:14px; font-weight:600; color:#64748B; margin-bottom:16px;'>
                📊 {T['Score_Title']}
            </div>
            """, unsafe_allow_html=True)
            
            # Large score number with label
            st.markdown(f"""
            <div style='text-align:center; margin-bottom:16px;'>
                <div style='font-size:48px; font-weight:700; color:{score_color}; line-height:1;'>
                    {score}
                </div>
                <div style='font-size:13px; color:#64748B; margin-top:6px; font-weight:500;'>
                    {score_label}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Confidence meter (enhanced)
            st.markdown(f"""
            <div style='margin-top:16px; padding-top:16px; border-top:1px solid #E2E8F0;'>
                <div style='display:flex; justify-content:space-between; margin-bottom:6px;'>
                    <span style='font-size:12px; color:#64748B;'>
                        {T['Confidence_Label']} 
                        <span style='cursor:help; color:#3B82F6;' title='{T.get("Confidence_Tooltip", "Data Reliability")}'>ⓘ</span>
                    </span>
                    <span style='font-size:12px; font-weight:600; color:#334155;'>{conf_val}%</span>
                </div>
                <div style='background:#E2E8F0; height:6px; border-radius:999px; overflow:hidden;'>
                    <div style='background:linear-gradient(90deg, #3B82F6, #2563EB); height:100%; width:{conf_val}%; transition:width 0.3s ease;'></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Score explanation expander (compact)
            with st.expander(f"ℹ️ {T.get('Score_Help_Link', 'How is this scored?')}"):
                st.caption(T['Score_Formula_Desc'])
                
                # Compact Formula Visualization
                c1, c2, c3, c4, c5 = st.columns([2, 0.5, 2, 0.5, 2])
                with c1:
                    st.markdown(f"<div style='text-align:center; font-size:0.8rem;'>🔥<br><b>{T['Factor_Pain'].split('(')[0]}</b></div>", unsafe_allow_html=True)
                with c2:
                    st.markdown("<div style='text-align:center; font-size:0.8rem; padding-top:10px;'>+</div>", unsafe_allow_html=True)
                with c3:
                     st.markdown(f"<div style='text-align:center; font-size:0.8rem;'>📈<br><b>{T['Factor_Market'].split('(')[0]}</b></div>", unsafe_allow_html=True)
                with c4:
                    st.markdown("<div style='text-align:center; font-size:0.8rem; padding-top:10px;'>+</div>", unsafe_allow_html=True)
                with c5:
                     st.markdown(f"<div style='text-align:center; font-size:0.8rem;'>🛠️<br><b>{T['Factor_Feasibility'].split('(')[0]}</b></div>", unsafe_allow_html=True)
                
                st.markdown("---")
                st.caption(f"**80-100**: {T['Bench_High_Desc']}")
        
        # Vertical spacing
        st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)
        
        # ============ VALUE METRICS (Phase 2) ============
        has_value_data = any([
            row.get('market_size'),
            row.get('value_type'),
            row.get('expected_impact'),
            row.get('timeline')
        ])
        
        if has_value_data:
            with st.container(border=True):
                st.markdown(f"""
                <div style='font-size:14px; font-weight:600; color:#64748B; margin-bottom:12px;'>
                    💰 {T['Potential_Value_Title']}
                </div>
                """, unsafe_allow_html=True)
                
                if row.get('market_size'):
                    st.markdown(f"<div style='font-size:13px; color:#475569; margin-bottom:6px;'>📊 {html.escape(str(row['market_size']))}</div>", unsafe_allow_html=True)
                if row.get('value_type'):
                    st.markdown(f"<div style='font-size:13px; color:#475569; margin-bottom:6px;'>💵 {html.escape(str(row['value_type']))}</div>", unsafe_allow_html=True)
                if row.get('expected_impact'):
                    st.markdown(f"<div style='font-size:13px; color:#475569; margin-bottom:6px;'>📈 {html.escape(str(row['expected_impact']))}</div>", unsafe_allow_html=True)
                if row.get('timeline'):
                    st.markdown(f"<div style='font-size:13px; color:#475569; margin-bottom:6px;'>⏱️ {html.escape(str(row['timeline']))}</div>", unsafe_allow_html=True)
            
            # Vertical spacing
            st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)
        
        # ============ SOURCE REPORT ============
        with st.container(border=True):
            st.markdown(f"""
            <div style='font-size:14px; font-weight:600; color:#64748B; margin-bottom:12px;'>
                📄 {T.get('Report_Title', 'Source Report')}
            </div>
            """, unsafe_allow_html=True)
            
            # Publisher Badge + Date
            st.markdown(f"""
            <div style="display:flex; align-items:center; gap:12px; margin-bottom:10px;">
                <div style="background:#EFF6FF; color:#2563EB; padding:4px 12px; border-radius:12px; font-size:0.75rem; font-weight:700;">
                    {report.source if report else "Unknown"}
                </div>
                <span style="color:#64748B; font-size:0.85rem;">
                    {report.published_at.strftime('%Y-%m-%d') if report else row['report_id']}
                </span>
            </div>
            """, unsafe_allow_html=True)
            
            # Report Title
            if report:
                report_title = report.title_ko if is_ko and report.title_ko else report.title
                st.caption(report_title)
                
                # Enhanced CTA Button
                st.link_button(
                    f"📄 {T['View_Source_Report']} →",
                    report.url,
                    use_container_width=True,
                    type="secondary"
                )
            else:
                st.caption(f"{T['Report ID']}: {row['report_id']}")
        
        # Recency timestamp (at the very bottom)
        if 'created_at' in row and row['created_at']:
            st.caption(f"📅 {row['created_at']}")


    with right:
        st.markdown(f"### {T['Evidence_Label']}")
        st.info(evidence)
        
        st.markdown(f"### {T['Prompt Title']}")
        with st.container(height=140):
            st.code(prompt_text, language="text")

        # Action Buttons
        c1, c2 = st.columns(2)
        with c1:
             # Use HTML for exact styling of the Link Button
             st.markdown(f"""
             <a href="https://chatgpt.com" target="_blank" class="rr-btn" style="text-decoration:none; display:block; text-align:center;">
                {T['Open ChatGPT']}
             </a>
             """, unsafe_allow_html=True)
        with c2:
            st.download_button(
                label=T['Download Prompt'],
                data=prompt_text,
                file_name="prompt.txt",
                use_container_width=True
            )

import datetime

@st.dialog("Welcome to Research Radar", width="large")
def show_onboarding_dialog(T):
    st.markdown(f"""
    <div style="text-align:center; padding-bottom:20px;">
        <h2>🚀 {T.get('Onboarding_Title', 'Discover Market Opportunities')}</h2>
        <p style="color:#94A3B8;">{T.get('Onboarding_Subtitle', '3 steps to maximize your research efficiency')}</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"### 📡 {T.get('Onb_Step1_Title', 'Global Scan')}")
        st.caption(T.get('Onb_Step1_Desc', 'Analyzing reports from PwC, News, and Academia in real-time.'))
    with c2:
        st.markdown(f"### ⚡ {T.get('Onb_Step2_Title', 'Critical Signals')}")
        st.caption(T.get('Onb_Step2_Desc', 'Focus on signals with Importance Score 80+.'))
    with c3:
        st.markdown(f"### 🎯 {T.get('Onb_Step3_Title', 'Take Action')}")
        st.caption(T.get('Onb_Step3_Desc', 'Filter, Export, and Generate Briefs for your strategy.'))
    
    st.markdown("---")
    if st.button(T.get('Start Exploring', 'Start Exploring'), type="primary", use_container_width=True):
        st.session_state.has_seen_onboarding = True
        st.rerun()

def render_kpi_section(df_cards, reports, T, is_ko=False):
    """Renders the KPI Header section."""
    high_value_count = len(df_cards[df_cards['importance_score'] >= 80]) if not df_cards.empty else 0
    reports_count = len(reports)
    
    # Calculate time since last update
    time_diff_str = "N/A"
    if not df_cards.empty and 'created_at' in df_cards.columns:
        last_update = df_cards['created_at'].max()
        if pd.notnull(last_update):
            now = datetime.datetime.now()
            diff = now - last_update
            
            if diff.days > 0:
                time_diff = f"{diff.days}d"
            elif diff.seconds > 3600:
                time_diff = f"{diff.seconds // 3600}h"
            else:
                time_diff = f"{diff.seconds // 60}m"
            
            time_diff_str = T['Updated ago'].format(time_diff=time_diff)
            
            # P0: 1.1 Exact Timestamp
            # Assuming server time is KST or we just format it as such for now (since user requested KST)
            # If created_at is naive, assume UTC or local. Let's format it.
            try:
                 # simplistic formatting
                 time_str = last_update.strftime("%Y-%m-%d %H:%M") 
                 exact_time_str = T['Updated_Exact'].format(time_str=time_str)
            except:
                 exact_time_str = ""
    
    update_freq_str = T.get('Update_Frequency', 'Every 24h')

    st.markdown(f"""
<div class="kpi-container">
    <div class="kpi-card" title="Total number of signals analyzed from all reports">
        <h3>{T['Total Signals']}</h3>
        <div class="value">{len(df_cards)}</div>
        <div class="sub-text">{update_freq_str}</div>
        <div class="last-updated" style="font-size:0.75rem; color:#94A3B8; margin-top:4px;" title="{exact_time_str}">{time_diff_str}</div>
    </div>
    <div class="kpi-card" style="border-left-color: var(--color-critical);" title="Signals with Importance Score >= 80">
        <h3>{T['Critical Signals']}</h3>
        <div class="value" style="color: var(--color-critical);">{high_value_count}</div>
        <div class="sub-text">High business value potential</div>
    </div>
    <div class="kpi-card" style="border-left-color: var(--text-primary);" title="Number of source reports processed">
        <h3>{T['Reports Tracked']}</h3>
        <div class="value">{reports_count}</div>
        <div class="sub-text">Trusted global data sources</div>
    </div>
</div>
""", unsafe_allow_html=True)

    # P2 Task 8: Network Status Trigger (Invisible Button over Card or Link below)
    # Using a clean link/button below the KPIs for "Data Lineage"
    c1, c2, c3 = st.columns(3)
    with c3:
        if st.button(f"ℹ️ {T.get('View Source Details', 'View Source Details')}", key="btn_net_status", use_container_width=True, type="secondary"):
            show_network_status_dialog(False, T) # is_ko passed as False for now or need to thread it through


def render_signal_card(row, index, is_ko, T, report_map):
    """Renders a single signal card (Compact List View - Phase 1+2 Optimized)."""
    # Language Fallback
    attack_raw = row.get('attack_vector_ko') if is_ko and row.get('attack_vector_ko') else row.get('attack_vector')
    holder_raw = row.get('pain_holder_ko') if is_ko and row.get('pain_holder_ko') else row.get('pain_holder')
    evidence_raw = row.get('evidence_sentence_ko') if is_ko and row.get('evidence_sentence_ko') else row.get('evidence_sentence')
    
    # Escape HTML
    attack = html.escape(str(attack_raw))
    holder = html.escape(str(holder_raw))
    
    # Tags & Score
    tags_list = row.get('industry_tags', [])
    base_tag = html.escape(str(tags_list[0])) if tags_list else "GENERAL"
    score = row['importance_score']
    
    # Top 2 tags for compact display
    top_tags = tags_list[:2] if len(tags_list) >= 2 else tags_list
    tags_display = ', '.join([html.escape(str(t)) for t in top_tags])
    
    # Phase 2: Evidence Preview (100 chars)
    evidence_text = str(evidence_raw) if evidence_raw else ""
    evidence_preview = evidence_text[:100] + "..." if len(evidence_text) > 100 else evidence_text
    evidence_preview_escaped = html.escape(evidence_preview)
    
    # Phase 2: Publisher Badge
    report = report_map.get(row.get('report_id'))
    publisher = report.source if report else "Unknown"
    
    # Visual Logic (Cognitive Analysis 1)
    # Score Color Logic: Red (High Urgency), Blue (Opportunity), Gray (Low)
    if score >= 80:
        score_color = "#DC2626"
        score_bg = "#FEF2F2"
    elif score >= 50:
        score_color = "#2563EB"
        score_bg = "#EFF6FF"
    else:
        score_color = "#64748B"
        score_bg = "#F1F5F9"

    with st.container(border=True):
        
        # Header: Category Tag + Publisher + Score
        st.markdown(f"""
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
            <div style="display:flex; gap:8px; align-items:center;">
                <span class="category-tag" style="background:#F8FAFC; color:#475569; border:1px solid #E2E8F0;">{base_tag}</span>
                <span style="background:#F1F5F9; color:#64748B; padding:4px 8px; border-radius:8px; font-size:0.7rem; font-weight:600;">
                    {publisher}
                </span>
            </div>
            <div class="score-badge" title="Importance Score: {score}/100" 
                 style="background:{score_bg}; color:{score_color}; border:1px solid {score_color}33; padding:4px 10px; border-radius:12px; font-size:0.8rem; font-weight:700;">
                 Score {score}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Title (Hero Content)
        st.markdown(f"<div class='card-title' style='margin-bottom:8px; font-size:1.1rem; line-height:1.4;'>{attack}</div>", unsafe_allow_html=True)
        
        # Compact Metadata Grid (Single Row) - Phase 1 Optimization
        st.markdown(f"""
        <div style="display:flex; gap:16px; margin-bottom:8px; font-size:0.85rem; color:#64748B;">
            <div>
                <span style="font-weight:600;">{T.get('Target_Label', 'Target')}:</span> 
                <span style="color:#334155;">{holder}</span>
            </div>
            <div>
                <span style="font-weight:600;">{T.get('Tags', 'Tags')}:</span> 
                <span style="color:#334155;">{tags_display}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Phase 2: Evidence Preview
        if evidence_preview:
            st.markdown(f"""
            <div style="font-size:0.85rem; color:#64748B; margin-top:8px; margin-bottom:12px; padding:8px; background:#F8FAFC; border-left:3px solid #2563EB; border-radius:4px;">
                <span style="font-weight:600; color:#475569;">💡 {T.get('Evidence_Preview', 'Evidence')}:</span><br>
                <span style="font-style:italic; color:#1E293B; line-height:1.5;">{evidence_preview_escaped}</span>
            </div>
            """, unsafe_allow_html=True)
        
        # Actions
        if st.button(T["View Full Analysis"], key=f"btn_full_{row['card_id']}_{index}", use_container_width=True):
             show_details_dialog(row.to_dict(), is_ko, T, report_map)


def render_skeleton_card():
    """Renders a skeleton loading card for infinite scroll."""
    st.markdown("""
    <div class="skeleton-card"></div>
    """, unsafe_allow_html=True)


def render_active_filters(search_query: str, selected_industries: list, selected_techs: list, score_range: tuple, T: dict, on_remove_callback=None):
    """Displays active filters as removable chips below the filter bar."""
    chips = []
    
    # Search Query Chip
    if search_query:
        chips.append(('search', f'🔍 "{search_query}"'))
    
    # Industry Chips
    for ind in selected_industries:
        chips.append(('industry', f'{T.get("Industry", "Industry")}: {ind}'))
    
    # Technology Chips
    for tech in selected_techs:
        chips.append(('tech', f'{T.get("Technology", "Technology")}: {tech}'))
    
    # Score Range Chip (only if not default 50-100)
    if score_range != (50, 100):
        chips.append(('score', f'{T.get("Score", "Score")}: {score_range[0]}-{score_range[1]}'))
    
    # Render chips
    if chips:
        st.markdown('<div class="active-filters">', unsafe_allow_html=True)
        for chip_type, label in chips:
            st.markdown(f'<span class="filter-chip">{label}</span>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        return True
    return False


@st.dialog("Active Data Sources", width="large")
def show_network_status_dialog(is_ko, T):
    st.markdown(f"### {T.get('Reports Tracked', 'Active Sources')}")
    st.caption(f"{T.get('Update_Frequency', 'Update frequency: Every 24h')}")
    
    st.markdown("###")
    
    # 1. PwC Global Insights (Active)
    with st.container(border=True):
        c1, c2 = st.columns([0.8, 0.2])
        with c1:
            st.markdown("**PwC Global Insights**")
            st.caption(T.get('Funnel_Step1_Desc', 'Processing real-time reports from PwC Global Network.'))
            st.progress(1.0) # 100%
        with c2:
            st.success("Connected")
            st.caption("Sync: Just now")

    # 2. News API (Coming Soon)
    with st.container(border=True):
        c1, c2 = st.columns([0.8, 0.2])
        with c1:
            st.markdown("**Global News API**")
            st.caption("Real-time news aggregation.")
        with c2:
            st.markdown("🔒 *Locked*")
            
    # 3. Academic Research (Coming Soon)
    with st.container(border=True):
        c1, c2 = st.columns([0.8, 0.2])
        with c1:
            st.markdown("**Academic Research**")
            st.caption("Papers & Journals.")
        with c2:
            st.markdown("🔒 *Locked*")

@st.dialog("Welcome to Research Radar", width="large")
def show_onboarding_dialog(is_ko, T):
    st.markdown(f"""
    <div style="text-align:center; margin-bottom:24px;">
        <h2 style="color:#1E293B; margin-bottom:8px;">{T['Onboarding_Title']}</h2>
        <p style="color:#64748B; font-size:1.1rem;">{T['Onboarding_Subtitle']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3, gap="medium")
    
    with c1:
        st.markdown(f"""
        <div style="text-align:center; padding:16px; background:#F8FAFC; border-radius:12px; height:100%;">
            <div style="font-size:2.5rem; margin-bottom:12px;">🌍</div>
            <div style="font-weight:700; color:#334155; margin-bottom:8px;">{T['Onb_Step1_Title']}</div>
            <div style="font-size:0.9rem; color:#64748B; line-height:1.5;">{T['Onb_Step1_Desc']}</div>
        </div>
        """, unsafe_allow_html=True)
        
    with c2:
        st.markdown(f"""
        <div style="text-align:center; padding:16px; background:#EFF6FF; border-radius:12px; height:100%; border:1px solid #BFDBFE;">
            <div style="font-size:2.5rem; margin-bottom:12px;">⚡</div>
            <div style="font-weight:700; color:#1E40AF; margin-bottom:8px;">{T['Onb_Step2_Title']}</div>
            <div style="font-size:0.9rem; color:#64748B; line-height:1.5;">{T['Onb_Step2_Desc']}</div>
        </div>
        """, unsafe_allow_html=True)
        
    with c3:
        st.markdown(f"""
        <div style="text-align:center; padding:16px; background:#F8FAFC; border-radius:12px; height:100%;">
            <div style="font-size:2.5rem; margin-bottom:12px;">🚀</div>
            <div style="font-weight:700; color:#334155; margin-bottom:8px;">{T['Onb_Step3_Title']}</div>
            <div style="font-size:0.9rem; color:#64748B; line-height:1.5;">{T['Onb_Step3_Desc']}</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("###")
    
    if st.button(T["Start Exploring"], type="primary", use_container_width=True):
        st.session_state['has_seen_onboarding'] = True
        st.rerun()
