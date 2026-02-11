import streamlit as st
import html
import pandas as pd
import datetime
from src.logic.prompts import build_prompt_from_card

@st.dialog("Signal Details / 상세 내용", width="large")
def show_details_dialog(row, is_ko, T, report_map):
    """Completely redesigned signal details dialog with optimal structure."""
    
    # Extract language-specific data
    if is_ko:
        attack = row.get('attack_vector_ko', row.get('attack_vector', '-'))
        holder = row.get('pain_holder_ko', row.get('pain_holder', '-'))
        context = row.get('pain_context_ko', row.get('pain_context', '-'))
        mechanism = row.get('pain_mechanism_ko', row.get('pain_mechanism', '-'))
        evidence = row.get('evidence_sentence_ko', row.get('evidence_sentence', '-'))
    else:
        attack = row.get('attack_vector', '-')
        holder = row.get('pain_holder', '-')
        context = row.get('pain_context', '-')
        mechanism = row.get('pain_mechanism', '-')
        evidence = row.get('evidence_sentence', '-')
    
    # Report and score data
    report = report_map.get(row['report_id'])
    report_url = report.url if report else "#"
    prompt_text = build_prompt_from_card(row, report_url)
    
    score = row['importance_score']
    conf_val = int(row.get('confidence_score', 0) * 100)
    
    # Score-based styling
    if score >= 80:
        score_color = '#DC2626'
        score_bg = '#FEF2F2'
        score_label = T.get('Score_High', 'High Potential')
    elif score >= 60:
        score_color = '#2563EB'
        score_bg = '#EFF6FF'
        score_label = T.get('Score_Medium', 'Medium')
    else:
        score_color = '#64748B'
        score_bg = '#F1F5F9'
        score_label = T.get('Score_Low', 'Low')
    
    # === HEADER: Color-coded with score ===
    st.markdown(f"""
    <div style='background:{score_bg}; padding:20px 24px; border-radius:12px; margin-bottom:24px; 
                border-left:5px solid {score_color}; display:flex; justify-content:space-between; align-items:center;'>
        <div style='flex:1;'>
            <div style='font-size:26px; font-weight:700; color:#1E293B; margin-bottom:8px; line-height:1.2;'>
                {html.escape(attack)}
            </div>
            <div style='font-size:15px; color:#64748B; font-weight:500;'>
                🎯 {html.escape(holder)}{' • ' + html.escape(context) if context != '-' else ''}
            </div>
        </div>
        <div style='text-align:center; min-width:90px; padding-left:20px;'>
            <div style='font-size:42px; font-weight:800; color:{score_color}; line-height:1;'>
                {score}
            </div>
            <div style='font-size:11px; color:#64748B; margin-top:4px; font-weight:600; text-transform:uppercase;'>
                {score_label}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # === MAIN LAYOUT: 60/40 Split ===
    left_col, right_col = st.columns([6, 4], gap="large")
    
    with left_col:
        # Pain Point Card
        st.markdown(f"""
        <div style='background:#FFFFFF; padding:18px; border-radius:10px; border:1px solid #E2E8F0; margin-bottom:16px;'>
            <div style='font-size:13px; font-weight:700; color:#64748B; margin-bottom:10px; text-transform:uppercase; letter-spacing:0.5px;'>
                ⚠️ {T['Pain_Label']}
            </div>
            <div style='max-height:120px; overflow-y:auto; color:#1E293B; font-size:14px; line-height:1.7; padding-right:8px;'>
                {html.escape(mechanism)}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Evidence Card (Quote style)
        st.markdown(f"""
        <div style='background:#F8FAFC; padding:18px; border-radius:10px; border-left:4px solid #2563EB; margin-bottom:16px;'>
            <div style='font-size:13px; font-weight:700; color:#64748B; margin-bottom:10px; text-transform:uppercase; letter-spacing:0.5px;'>
                💡 {T['Evidence_Label']}
            </div>
            <div style='max-height:100px; overflow-y:auto; color:#334155; font-size:13px; line-height:1.7; 
                        font-style:italic; padding-right:8px;'>
                "{html.escape(evidence)}"
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # ChatGPT Prompt Card - Custom Container
        prompt_escaped = html.escape(prompt_text)
        st.markdown(f"""
        <div class="prompt-section">
            <div class="prompt-header">💬 {T['Prompt Title']}</div>
            <div style="background-color: #0F172A; border-radius: 10px; padding: 20px;">
                <div class="prompt-container" style="height: 140px;">
                    <pre class="prompt-text" style="color: #FFFFFF !important; user-select: all; cursor: text; padding: 16px; margin: 0;">{prompt_escaped}</pre>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Action Buttons
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            st.link_button(
                f"💬 {T['Open ChatGPT']}",
                "https://chatgpt.com",
                use_container_width=True,
                type="primary"
            )
        with btn_col2:
            st.download_button(
                label=f"📋 {T.get('Download Prompt', 'Download Prompt')}",
                data=prompt_text,
                file_name="prompt.txt",
                use_container_width=True,
                type="primary"
            )
    
    with right_col:
        # Metrics Card (Compact)
        st.markdown(f"""
        <div style='background:#FFFFFF; padding:18px; border-radius:10px; border:1px solid #E2E8F0; margin-bottom:16px;'>
            <div style='font-size:13px; font-weight:700; color:#64748B; margin-bottom:12px; text-transform:uppercase; letter-spacing:0.5px;'>
                📊 {T['Score_Title']}
            </div>
            <div style='text-align:center; margin-bottom:16px; padding-bottom:16px; border-bottom:1px solid #E2E8F0;'>
                <div style='font-size:36px; font-weight:800; color:{score_color}; line-height:1;'>
                    {score}
                </div>
                <div style='font-size:11px; color:#94A3B8; margin-top:4px; font-weight:600;'>
                    / 100 {score_label}
                </div>
            </div>
            <div style='margin-bottom:8px;'>
                <div style='display:flex; justify-content:space-between; margin-bottom:6px;'>
                    <span style='font-size:11px; color:#64748B; font-weight:600;'>{T['Confidence_Label']}</span>
                    <span style='font-size:11px; color:#1E293B; font-weight:700;'>{conf_val}%</span>
                </div>
                <div style='background:#E2E8F0; height:6px; border-radius:999px; overflow:hidden;'>
                    <div style='background:linear-gradient(90deg, #3B82F6, #2563EB); height:100%; width:{conf_val}%;'></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Tags Card (Compact chips)
        industry_tags = row.get('industry_tags', [])[:3]  # Limit to 3
        tech_tags = row.get('technology_tags', [])[:3]
        
        if industry_tags or tech_tags:
            tags_html = ""
            for tag in industry_tags:
                tags_html += f'<span class="chip-tag-small">{html.escape(str(tag))}</span>'
            for tag in tech_tags:
                tags_html += f'<span class="chip-tag-small">{html.escape(str(tag))}</span>'
            
            st.markdown(f"""
            <div style='background:#FFFFFF; padding:18px; border-radius:10px; border:1px solid #E2E8F0; margin-bottom:16px;'>
                <div style='font-size:13px; font-weight:700; color:#64748B; margin-bottom:10px; text-transform:uppercase; letter-spacing:0.5px;'>
                    🏷 {T['Tags']}
                </div>
                <div style='display:flex; flex-wrap:wrap; gap:4px;'>
                    {tags_html}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Source Report Card
        if report:
            report_title = report.title_ko if (is_ko and report.title_ko) else report.title
            st.markdown(f"""
            <div style='background:#FFFFFF; padding:18px; border-radius:10px; border:1px solid #E2E8F0;'>
                <div style='font-size:13px; font-weight:700; color:#64748B; margin-bottom:10px; text-transform:uppercase; letter-spacing:0.5px;'>
                    📄 {T.get('Report_Title', 'Source')}
                </div>
                <div style='background:#F8FAFC; padding:10px; border-radius:6px; margin-bottom:10px;'>
                    <div style='display:flex; align-items:center; gap:8px; margin-bottom:6px;'>
                        <span style='background:#2563EB; color:#FFFFFF; padding:2px 8px; border-radius:10px; font-size:10px; font-weight:700;'>
                            {html.escape(report.source)}
                        </span>
                        <span style='color:#94A3B8; font-size:11px;'>
                            {report.published_at.strftime('%Y-%m-%d')}
                        </span>
                    </div>
                    <div style='color:#475569; font-size:12px; line-height:1.4;'>
                        {html.escape(report_title[:80])}{'...' if len(report_title) > 80 else ''}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.link_button(
                f"📄 {T['View_Source_Report']}",
                report.url,
                use_container_width=True,
                type="primary"
            )

def render_kpi_section(df_cards, reports, T, is_ko=False):
    """Renders the KPI Header section."""
    high_value_count = len(df_cards[df_cards['importance_score'] >= 80]) if not df_cards.empty else 0
    reports_count = len(reports)
    
    # Calculate time since last update
    time_diff_str = "N/A"
    exact_time_str = ""
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

@st.dialog("Welcome to Opportunity Radar", width="large")
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
