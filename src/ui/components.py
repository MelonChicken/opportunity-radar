import streamlit as st
import html
import pandas as pd

@st.dialog("Signal Details / 상세 내용")
def show_details_dialog(row, is_ko, T, report_map):
    # Language Fallback
    attack = row.get('attack_vector_ko') if is_ko and row.get('attack_vector_ko') else row.get('attack_vector')
    holder = row.get('pain_holder_ko') if is_ko and row.get('pain_holder_ko') else row.get('pain_holder')
    context = row.get('pain_context_ko') if is_ko and row.get('pain_context_ko') else row.get('pain_context')
    mechanism = row.get('pain_mechanism_ko') if is_ko and row.get('pain_mechanism_ko') else row.get('pain_mechanism')
    evidence = row.get('evidence_sentence_ko') if is_ko and row.get('evidence_sentence_ko') else row.get('evidence_sentence')
    
    st.subheader(attack)
    st.caption(f"Score: {row['importance_score']} | Confidence: {int(row.get('confidence_score', 0)*100)}%")
    
    st.markdown("---")
    
    st.markdown(f"**{'Target Customer (Who)' if not is_ko else '타겟 고객 (Who)'}**")
    st.write(f"**{holder}** in *{context}*")

    st.markdown(f"**{'Pain Point (Why)' if not is_ko else '페인 포인트 (Why)'}**")
    st.write(mechanism)
    
    st.markdown(f"**{'Evidence' if not is_ko else '근거 문장'}**")
    st.info(f"{evidence}")
    
    st.markdown("---")
    st.markdown(f"**Report ID:** {row['report_id']}")
    st.markdown(f"**{'Source Report' if not is_ko else '원본 리포트'}**")
    
    report = report_map.get(row['report_id'])
    report_url = report.url if report else "#"
    
    st.write(f"[{T['Report Source']}]({report_url})")

def render_kpi_section(df_cards, reports, T):
    """Renders the KPI Header section."""
    high_value_count = len(df_cards[df_cards['importance_score'] >= 80]) if not df_cards.empty else 0
    reports_count = len(reports)

    st.markdown(f"""
    <div class="kpi-container">
        <div class="kpi-card">
            <h3>{T['Total Signals']}</h3>
            <div class="value">{len(df_cards)}</div>
        </div>
        <div class="kpi-card">
            <h3>{T['Critical Signals']}</h3>
            <div class="value" style="color: var(--color-critical);">{high_value_count}</div>
        </div>
        <div class="kpi-card">
            <h3>{T['Reports Tracked']}</h3>
            <div class="value" style="color: var(--accent-secondary);">{reports_count}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_signal_card(row, index, is_ko, T, report_map):
    """Renders a single signal card."""
    # Language Fallback
    attack_raw = row.get('attack_vector_ko') if is_ko and row.get('attack_vector_ko') else row.get('attack_vector')
    holder_raw = row.get('pain_holder_ko') if is_ko and row.get('pain_holder_ko') else row.get('pain_holder')
    evidence_raw = row.get('evidence_sentence_ko') if is_ko and row.get('evidence_sentence_ko') else row.get('evidence_sentence')
    
    # Escape HTML
    attack = html.escape(str(attack_raw))
    holder = html.escape(str(holder_raw))
    evidence = html.escape(str(evidence_raw))[:200] + "..." # Truncate for safety
    
    # Tags
    tags_list = row.get('industry_tags', [])[:3]
    ind_tags = ' '.join([f'<span class="tag">{html.escape(str(tag))}</span>' for tag in tags_list])
    
    # Color Coding
    score = row['importance_score']
    if score >= 80:
        badge_color = "var(--color-critical)"
    elif score >= 50:
        badge_color = "var(--color-opportunity)"
    else:
        badge_color = "var(--color-neutral)"
        
    # Card HTML Construction
    card_html = f"""
    <div class="signal-card">
        <div class="card-header">
            <h3 class="card-title">{attack}</h3>
            <div class="importance-badge" style="background-color:{badge_color}; color:#000;">{score}</div>
        </div>
        <div class="card-body">
            <div class="info-row">
                <span class="info-label">TARGET:</span>
                <strong>{holder}</strong>
            </div>
            <div class="quote-box">
                "{evidence}"
            </div>
        </div>
        <div class="card-footer">
            <div>{ind_tags}</div>
            <div style="font-size:0.75rem; opacity:0.7;">Start-up Opportunity</div>
        </div>
    </div>
    """
    
    st.markdown(card_html, unsafe_allow_html=True)
    
    # View Details Button
    # Use key to avoid duplicate ID errors
    if st.button(T["View Details"], key=f"btn_{row['card_id']}_{index}", use_container_width=True):
        show_details_dialog(row.to_dict(), is_ko, T, report_map)
