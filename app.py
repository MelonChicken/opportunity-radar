import streamlit as st
import pandas as pd
import os
import sys
import textwrap

# Add the repository root to sys.path so we can import src
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.pipeline import run_pipeline
from src.storage import load_cards, load_reports
from src.models import OpportunityCard

@st.dialog("Signal Details / 상세 내용")
def show_details_dialog(row, is_ko, T):
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
    st.write(f"[{T['Source Link']}](#)") # Placeholder link
    
st.set_page_config(
    page_title="Research Radar",
    page_icon="📡",
    layout="wide"
)

# --- CSS Styling (Premium Feel) ---
st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
        color: #fafafa;
    }
    .metric-card {
        background-color: #262730;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #41424C;
        text-align: center;
    }
    .signal-card {
        background-color: #1E1E1E; /* Darker card background */
        padding: 24px;
        border-radius: 12px;
        border: 1px solid #333;
        margin-bottom: 16px;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .signal-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.5);
        border-color: #FF4B4B; /* Streamlit Red accent */
    }
    .tag {
        display: inline-block;
        padding: 2px 8px;
        margin-right: 6px;
        margin-bottom: 6px;
        border-radius: 4px;
        background-color: #31333F;
        font-size: 0.8em;
        color: #E6E6E6;
        border: 1px solid #41424C;
    }
    .score-badge {
        font-weight: bold;
        font-size: 1.2em;
        color: #FF4B4B;
    }
</style>
""", unsafe_allow_html=True)

# --- Sidebar ---
st.sidebar.title("Research Radar 📡")
st.sidebar.markdown("---")

if st.sidebar.button("Run Ingestion Pipeline 🚀"):
    with st.sidebar.status("Running Pipeline...", expanded=True) as status:
        st.write("Initializing...")
        
        # Log container
        log_container = st.empty()
        
        def ui_logger(msg):
            log_container.text(msg)
            print(msg)
            
        try:
            reports_found, reports_processed, cards_created = run_pipeline(log_callback=ui_logger)
            status.update(label="Pipeline Completed!", state="complete", expanded=False)
            st.sidebar.success(f"Found: {reports_found}, Processed: {reports_processed}, New Cards: {cards_created}")
            st.rerun()
        except Exception as e:
            status.update(label="Pipeline Failed", state="error")
            st.sidebar.error(f"Error: {e}")

# --- Language Settings ---
lang = st.sidebar.radio("Language / 언어", ["English", "한국어"])
is_ko = lang == "한국어"

T = {
    "Dashboard Title": "Opportunity Dashboard" if not is_ko else "기회 포착 대시보드",
    "Dashboard Subtitle": "Monitor high-value signals extracted from PwC Global Research." if not is_ko else "PwC 글로벌 리서치에서 추출한 핵심 사업 기회 신호를 모니터링합니다.",
    "Total Signals": "Total Signals" if not is_ko else "전체 신호",
    "Critical Signals": "Critical Signals (>80)" if not is_ko else "핵심 신호 (>80)",
    "Reports Tracked": "Reports Tracked" if not is_ko else "분석 리포트",
    "Filters": "Filters" if not is_ko else "필터",
    "Industry": "Industry" if not is_ko else "산업군",
    "Technology": "Technology" if not is_ko else "기술",
    "Min Score": "Min Importance Score" if not is_ko else "최소 중요도 점수",
    "Run Pipeline": "Run Ingestion Pipeline 🚀" if not is_ko else "수집 파이프라인 실행 🚀",
    "Show Admin": "Show Admin View (Discarded Signals)" if not is_ko else "관리자 뷰 보기 (버려진 신호)",
    "No Signals": "No opportunity cards found. Run the ingestion pipeline to get started." if not is_ko else "기회 카드가 없습니다. 수집 파이프라인을 실행해주세요.",
    "Footer": "Built with Streamlit & OpenAI" if not is_ko else "Streamlit & OpenAI 기반 제작",
    "Page": "Page" if not is_ko else "페이지",
    "Showing": "Showing" if not is_ko else "표시 중",
    "of": "of" if not is_ko else "/",
    "signals": "signals" if not is_ko else "건",
    "View Details": "View Details & Source" if not is_ko else "상세 정보 및 출처 확인",
    "Source Link": "Source Report Link would go here" if not is_ko else "원본 리포트 링크가 여기에 표시됩니다",
}
            
st.sidebar.subheader(T["Filters"])
# Filters logic
all_cards = load_cards()
df_cards = pd.DataFrame([c.model_dump() for c in all_cards])

if not df_cards.empty:
    # Industry Filter
    all_industries = set()
    for tags in df_cards['industry_tags']:
        all_industries.update(tags)
    selected_industries = st.sidebar.multiselect(T["Industry"], sorted(list(all_industries)))
    
    # Tech Filter
    all_techs = set()
    for tags in df_cards['technology_tags']:
        all_techs.update(tags)
    selected_techs = st.sidebar.multiselect(T["Technology"], sorted(list(all_techs)))
    
    # Score Filter
    min_score = st.sidebar.slider(T["Min Score"], 0, 100, 50)
else:
    selected_industries = []
    selected_techs = []
    min_score = 0


# --- Main Dashboard ---
st.title(T["Dashboard Title"])

# Admin Toggle
if st.sidebar.checkbox(T["Show Admin"]):
    st.subheader("Discarded Signals (Admin)")
    from src.storage import load_discarded_signals
    discarded = load_discarded_signals()
    
    if discarded:
        df_discarded = pd.DataFrame([d.model_dump() for d in discarded])
        st.dataframe(df_discarded, use_container_width=True)
    else:
        st.info("No discarded signals found.")
else:
    st.markdown(T["Dashboard Subtitle"])

    # Metrics Row
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="metric-card"><h3>{T["Total Signals"]}</h3><h2>{len(df_cards)}</h2></div>', unsafe_allow_html=True)
    with col2:
        high_value_count = len(df_cards[df_cards['importance_score'] > 80]) if not df_cards.empty else 0
        st.markdown(f'<div class="metric-card"><h3>{T["Critical Signals"]}</h3><h2>{high_value_count}</h2></div>', unsafe_allow_html=True)
    with col3:
        reports_count = len(load_reports())
        st.markdown(f'<div class="metric-card"><h3>{T["Reports Tracked"]}</h3><h2>{reports_count}</h2></div>', unsafe_allow_html=True)

    st.markdown("---")

    # Filtering Data
    if not df_cards.empty:
        filtered_df = df_cards.copy()
        
        if selected_industries:
            # Check if any selected industry is in the row's industry_tags
            filtered_df = filtered_df[filtered_df['industry_tags'].apply(lambda x: any(i in x for i in selected_industries))]
            
        if selected_techs:
            filtered_df = filtered_df[filtered_df['technology_tags'].apply(lambda x: any(t in x for t in selected_techs))]
            
        filtered_df = filtered_df[filtered_df['importance_score'] >= min_score]
        
        # Sort by Importance
        filtered_df = filtered_df.sort_values(by="importance_score", ascending=False)
        
        # --- Pagination ---
        items_per_page = 5
        total_items = len(filtered_df)
        total_pages = max(1, (total_items + items_per_page - 1) // items_per_page)
        
        if total_pages > 1:
            page = st.number_input(T["Page"], min_value=1, max_value=total_pages, value=1)
        else:
            page = 1
            
        start_idx = (page - 1) * items_per_page
        end_idx = start_idx + items_per_page
        
        page_df = filtered_df.iloc[start_idx:end_idx]
        
        st.caption(f"{T['Showing']} {start_idx+1}-{min(end_idx, total_items)} {T['of']} {total_items} {T['signals']}")
        
        # Display Cards
        for index, row in page_df.iterrows():
            # Language Fallback Logic
            attack = row.get('attack_vector_ko') if is_ko and row.get('attack_vector_ko') else row.get('attack_vector')
            holder = row.get('pain_holder_ko') if is_ko and row.get('pain_holder_ko') else row.get('pain_holder')
            evidence = row.get('evidence_sentence_ko') if is_ko and row.get('evidence_sentence_ko') else row.get('evidence_sentence')
            
            # HTML Construction
            ind_tags = ' '.join([f'<span class="tag">{tag}</span>' for tag in row.get('industry_tags', [])])
            tech_tags = ' '.join([f'<span class="tag" style="background-color:#4a2b2b;">{tag}</span>' for tag in row.get('technology_tags', [])])
            
            # Use strict dedent to prevent markdown code block rendering
            card_html = textwrap.dedent(f"""
                <div class="signal-card">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <h3 style="margin:0;">{attack}</h3>
                        <span class="score-badge">{row['importance_score']}</span>
                    </div>
                    <div style="margin-top:8px; color:#ddd;">
                        <strong>{'For' if not is_ko else '대상'}:</strong> {holder}
                    </div>
                    <p style="color:#bbb; font-style:italic; margin-top:8px;">"{evidence}"</p>
                    <div style="margin-top:10px;">
                        {ind_tags}
                        {tech_tags}
                    </div>
                </div>
            """)


            with st.container():
                st.markdown(card_html, unsafe_allow_html=True)
                
                # Click Action - Use primary button for visibility
                if st.button(T["View Details"], key=f"btn_{row['card_id']}", use_container_width=True, type="primary"):
                    print(f"DEBUG: Button clicked corresponding to {row['card_id']}")
                    show_details_dialog(row.to_dict(), is_ko, T)
                    
    else:
        st.info(T["No Signals"])

# --- Footer ---
st.markdown(f"<br><br><div style='text-align:center; color:#666;'>{T['Footer']}</div>", unsafe_allow_html=True)
