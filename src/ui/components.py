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

    left, right = st.columns([1.1, 1.9], gap="large")

    with left:
        st.markdown(f"### {T['Target_Label']}")
        st.write(f"**{holder}**")
        st.caption(f"Context: {context}")
        
        st.markdown(f"### {T['Pain_Label']}")
        st.write(mechanism)
        
        st.markdown(f"### {T['Tags']}")
        ind_tags = ", ".join(row.get('industry_tags', []))
        tech_tags = ", ".join(row.get('technology_tags', []))
        st.write(f"**{T['Industry']}:** {ind_tags}")
        st.write(f"**{T['Technology']}:** {tech_tags}")
        
        st.markdown(f"### {T['Score_Title']}")
        # Split Score/Confidence (P1: 2.2)
        sc1, sc2 = st.columns(2)
        with sc1:
             st.metric(label=T['Score'], value=row['importance_score'], help=T.get('Score_Tooltip', "Business Opportunity Value"))
        with sc2:
             conf_val = int(row.get('confidence_score', 0)*100)
             st.metric(label=T['Confidence_Label'], value=f"{conf_val}%", help=T.get('Confidence_Tooltip', "Data Reliability"))
             st.progress(conf_val / 100)
        
        # P1 Task 5: Scoring Explanation (Inline Expander)
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
        
        # Recency Info (P1: 2.1)
        if 'created_at' in row and row['created_at']:
            st.caption(f"📅 {T.get('Last Updated', 'Date')}: {row['created_at']}")
        
        st.markdown("---")
        st.markdown(f"**{T['Report ID']}:** {row['report_id']}")
        st.write(f"[{T['Report Source']}]({report_url})")

    with right:
        st.markdown(f"### {T['Evidence_Label']}")
        st.info(evidence)
        
        st.markdown(f"### {T['Prompt Title']}")
        with st.container(height=220):
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
    """Renders a single signal card (Expanded View by default)."""
    # Language Fallback
    attack_raw = row.get('attack_vector_ko') if is_ko and row.get('attack_vector_ko') else row.get('attack_vector')
    holder_raw = row.get('pain_holder_ko') if is_ko and row.get('pain_holder_ko') else row.get('pain_holder')
    evidence_raw = row.get('evidence_sentence_ko') if is_ko and row.get('evidence_sentence_ko') else row.get('evidence_sentence')
    mechanism_raw = row.get('pain_mechanism_ko') if is_ko and row.get('pain_mechanism_ko') else row.get('pain_mechanism')
    
    # Escape HTML
    attack = html.escape(str(attack_raw))
    holder = html.escape(str(holder_raw))
    desc_full = html.escape(str(mechanism_raw))
    
    # Tags & Score
    tags_list = row.get('industry_tags', [])
    base_tag = html.escape(str(tags_list[0])) if tags_list else "GENERAL"
    score = row['importance_score']
    
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
        
        # Header: Category + Score
        st.markdown(f"""
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
            <span class="category-tag" style="background:#F8FAFC; color:#475569; border:1px solid #E2E8F0;">{base_tag}</span>
            <div class="score-badge" title="Importance Score: {score}/100" 
                 style="background:{score_bg}; color:{score_color}; border:1px solid {score_color}33; padding:4px 10px; border-radius:12px; font-size:0.8rem; font-weight:700;">
                 Score {score}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Title (Hero Content)
        st.markdown(f"<div class='card-title' style='margin-bottom:8px; font-size:1.1rem; line-height:1.4;'>{attack}</div>", unsafe_allow_html=True)
        
        # Full Content (Always Visible)
        st.markdown(f"""
        <div style="font-size:0.95rem; color:#1E293B; margin-bottom:12px; line-height:1.6; background:#F8FAFC; padding:12px; border-radius:8px;">
            {desc_full}
        </div>
        
        <div style="display:grid; grid-template-columns: 1fr 1fr; gap:12px; margin-bottom:16px;">
            <div>
                <div style="font-size:0.75rem; color:#64748B; font-weight:600; text-transform:uppercase; margin-bottom:4px;">{T.get('Target_Label', 'Target')}</div>
                <div style="font-size:0.9rem; color:#334155; font-weight:500;">{holder}</div>
            </div>
            <div>
                 <div style="font-size:0.75rem; color:#64748B; font-weight:600; text-transform:uppercase; margin-bottom:4px;">{T.get('Tags', 'Tags')}</div>
                 <div style="font-size:0.85rem; color:#475569;">{', '.join(tags_list)}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Actions
        if st.button(T["View Full Analysis"], key=f"btn_full_{row['card_id']}_{index}", use_container_width=True):
             show_details_dialog(row.to_dict(), is_ko, T, report_map)

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
