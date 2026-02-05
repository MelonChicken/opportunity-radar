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

def render_kpi_section(df_cards, reports, T):
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

    st.markdown(f"""
<div class="kpi-container">
    <div class="kpi-card" title="Total number of signals analyzed from all reports">
        <h3>{T['Total Signals']}</h3>
        <div class="value">{len(df_cards)}</div>
        <div class="sub-text">Latest signals analyzed</div>
        <div class="last-updated" style="font-size:0.75rem; color:#94A3B8; margin-top:4px;">{time_diff_str}</div>
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

def render_signal_card(row, index, is_ko, T, report_map):
    """Renders a single signal card."""
    # Language Fallback
    attack_raw = row.get('attack_vector_ko') if is_ko and row.get('attack_vector_ko') else row.get('attack_vector')
    holder_raw = row.get('pain_holder_ko') if is_ko and row.get('pain_holder_ko') else row.get('pain_holder')
    evidence_raw = row.get('evidence_sentence_ko') if is_ko and row.get('evidence_sentence_ko') else row.get('evidence_sentence')
    mechanism_raw = row.get('pain_mechanism_ko') if is_ko and row.get('pain_mechanism_ko') else row.get('pain_mechanism')
    
    # Escape HTML
    attack = html.escape(str(attack_raw))
    holder = html.escape(str(holder_raw))
    # Evidence is essentially the "Description" now. 
    # The design shows a summary, not just a quote. We'll use mechanism + evidence snippets?
    # Actually design shows "Current manual assessment processes...". This looks like 'pain_mechanism' or 'pain_context'.
    # Let's use 'pain_mechanism' as the detailed description.
    desc = html.escape(str(mechanism_raw))[:140] + "..."
    
    # Tags & Score
    tags_list = row.get('industry_tags', [])
    base_tag = html.escape(str(tags_list[0])) if tags_list else "GENERAL"
    
    extra_count = len(tags_list) - 1
    if extra_count > 0:
        # Improved: Display "+2 more" instead of just "+2"
        more_text = f"+{extra_count} more"
        primary_tag = f"{base_tag} <span style='opacity:0.7; font-weight:500; margin-left:4px; font-size:0.7rem;'>{more_text}</span>"
    else:
        primary_tag = base_tag

    score = row['importance_score']
    
    # Footer Pills (Mocking "Critical", "Enterprise" based on score/tags)
    urgency = "Critical" if score >= 80 else "Potential"
    # Secondary pill just one of the tags or 'Enterprise'
    secondary_pill = html.escape(str(tags_list[1])) if len(tags_list) > 1 else "Niche"

    # Card HTML
    card_html = f"""
<div class="signal-card">
    <div>
        <div class="card-top">
            <span class="category-tag">{primary_tag}</span>
            <!-- Improved: Explicit Score Label -->
            <div class="score-badge" title="Importance Score: {score}/100">Score {score}</div>
        </div>
        <div class="card-title">{attack}</div>
        <div class="card-desc">{desc}</div>
        <div class="card-meta">
            Target: <strong>{holder}</strong>
        </div>
    </div>
    <div class="card-footer">
        <div>
            <span class="pill">{urgency}</span>
            <span class="pill">{secondary_pill}</span>
        </div>
        <!-- View Details is handled by the button below to ensure functionality -->
    </div>
</div>
"""
    
    # Wrapper for Visual Grouping (One Card Look)
    with st.container(border=True): # Border handles the card outline now
        st.markdown(card_html, unsafe_allow_html=True)
        
        # Helper div to target the button with CSS
        st.markdown('<div class="view-full-analysis-btn">', unsafe_allow_html=True)
        if st.button(T["View Full Analysis"], key=f"btn_{row['card_id']}_{index}", use_container_width=True):
             show_details_dialog(row.to_dict(), is_ko, T, report_map)
        st.markdown('</div>', unsafe_allow_html=True)