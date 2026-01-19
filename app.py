import streamlit as st
import pandas as pd
import os
import sys
import textwrap
import html

# Add the repository root to sys.path so we can import src
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.pipeline import run_pipeline
from src.storage import load_cards, load_reports
from src.models import OpportunityCard

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
    
    st.write(f"[{T['Source Link']}]({report_url})")
    
st.set_page_config(
    page_title="Research Radar",
    page_icon="📡",
    layout="wide"
)

# --- CSS Styling (Premium Feel) ---
# --- CSS Styling (Premium Design System - High Contrast) ---
st.markdown("""
<style>
    /* 1. Global Reset & Typography */
    .stApp {
        background-color: #0F1419; /* Deep Dark Background */
        font-family: 'Inter', -apple-system, system-ui, sans-serif;
    }
    h1 {
        font-size: 32px !important;
        font-weight: 700 !important;
        color: #FFFFFF !important;
        padding-bottom: 16px;
    }
    h2, h3 {
        font-weight: 600 !important;
        color: rgba(255, 255, 255, 0.88) !important;
    }
    
    /* 2. Top Navigation & Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        border-bottom: 1px solid rgba(255,255,255,0.1);
        padding-bottom: 0px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 4px 4px 0 0;
        color: rgba(255,255,255,0.5); /* Inactive Text */
        font-size: 16px;
        font-weight: 600;
        border: none;
    }
    .stTabs [aria-selected="true"] {
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: #FFFFFF !important; /* Active White */
        border-bottom: 3px solid #1E88E5;
    }
    
    /* 3. Metrics / KPI Cards */
    .metric-card {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-left: 4px solid #1E88E5; /* Accent Border */
        border-radius: 8px;
        padding: 24px 32px;
        height: 160px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        text-align: left;
        transition: transform 0.2s;
    }
    .metric-card:hover {
        background-color: rgba(255, 255, 255, 0.08);
        border-color: rgba(255, 255, 255, 0.25);
    }
    .metric-card h3 {
        font-size: 14px;
        font-weight: 600;
        color: #1E88E5 !important;
        margin-bottom: 12px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .metric-card h2 {
        font-size: 48px;
        font-weight: 700;
        color: #FFFFFF !important;
        margin: 0;
        line-height: 1.1;
    }
    
    /* 4. Signal Cards (The Main UI) */
    .signal-card {
        background-color: rgba(255, 255, 255, 0.08); /* Increased contrast */
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 8px;
        padding: 32px;
        margin-bottom: 24px;
        position: relative;
        overflow: hidden;
        transition: all 0.2s ease-out;
    }
    .signal-card:hover {
        background-color: rgba(255, 255, 255, 0.12);
        border-color: rgba(255, 255, 255, 0.25);
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        transform: translateY(-2px);
    }
    .signal-card h3 {
        font-size: 18px !important;
        margin: 0 0 4px 0;
        color: #FFFFFF !important;
    }
    
    /* 5. Components & Filters */
    .filter-container {
        background-color: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 32px;
    }
    
    /* Fix Expander Header Contrast */
    .streamlit-expanderHeader {
        color: #FFFFFF !important;
        font-weight: 600;
        background-color: rgba(255,255,255,0.05) !important;
        border-radius: 4px;
    }
    .streamlit-expanderHeader svg {
        fill: #FFFFFF !important;
    }
    .streamlit-expanderContent {
        background-color: transparent !important;
        color: #FFFFFF !important;
    }
    
    /* Fix Multiselect & Inputs */
    .stMultiSelect label, .stSlider label, .stCheckbox label {
        color: #FFFFFF !important;
    }
    
    /* Fix Reset Button (Secondary) to be visible */
    button[kind="secondary"] {
        background-color: #0F1419 !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        color: #FFFFFF !important;
    }
    button[kind="secondary"]:hover {
        border-color: #1E88E5 !important;
        color: #1E88E5 !important;
    }
    
    /* Tags */
    .tag {
        display: inline-block;
        padding: 4px 10px;
        margin-right: 6px;
        margin-bottom: 6px;
        border-radius: 4px;
        background-color: rgba(255,255,255,0.1);
        font-size: 12px;
        color: rgba(255,255,255,0.9);
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    /* 6. Sidebar Cleanup */
    [data-testid="stSidebar"] {
        background-color: #0b0e11;
        border-right: 1px solid rgba(255,255,255,0.05);
    }
    
    /* 7. Pagination & Buttons */
    div[data-testid="stColumn"] button {
        height: 44px;
        min-width: 44px;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s;
    }
    div[data-testid="stColumn"] button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
</style>
""", unsafe_allow_html=True)

# --- Sidebar ---
st.sidebar.title("Research Radar 📡")
st.sidebar.caption("AI-Powered Intelligence")
st.sidebar.markdown("---")

# Global Actions (Pipeline)
# Global Actions (Pipeline)
if st.sidebar.button("Run Ingestion Pipeline 🚀", type="primary"):
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

st.sidebar.markdown("---")

# Language Settings
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
    "Show Admin": "Show Admin View (Discarded Signals)" if not is_ko else "관리자 뷰 보기 (버려진 신호)",
    "No Signals": "No opportunity cards found. Run the ingestion pipeline to get started." if not is_ko else "기회 카드가 없습니다. 수집 파이프라인을 실행해주세요.",
    "Footer": "Built with Streamlit & OpenAI" if not is_ko else "Streamlit & OpenAI 기반 제작",
    "Page": "Page" if not is_ko else "페이지",
    "Showing": "Showing" if not is_ko else "표시 중",
    "of": "of" if not is_ko else "/",
    "signals": "signals" if not is_ko else "건",
    "View Details": "View Details & Source" if not is_ko else "상세 정보 및 출처 확인",
    "Source Link": "Source Report" if not is_ko else "원본 리포트",
    
    # User Guide Strings
    "Tab_Dashboard": "📊 Dashboard" if not is_ko else "📊 대시보드",
    "Tab_Guide": "📚 User Guide & Methodology" if not is_ko else "📚 사용 가이드 및 방법론",
    
    "Guide_Intro": """### How to Use Research Radar
1. **Filter**: Use the sidebar to select industries or technologies of interest.
2. **Explore**: Browse the opportunity cards. Each card represents a distinct **'Attack Vector'** (Startup Idea).
3. **Deep Dive**: Click **'View Details'** to see the full context, who holds the pain point, and the source report link.
""" if not is_ko else """### 리서치 레이더 사용법
1. **필터**: 사이드바를 사용하여 관심 있는 산업군이나 기술을 선택하세요.
2. **탐색**: 기회 카드를 살펴보세요. 각 카드는 구체적인 **'공략 포인트'** (스타트업 아이디어)를 나타냅니다.
3. **상세 보기**: **'상세 정보 확인'**을 클릭하여 전체 맥락, 페인 포인트의 주체, 원본 리포트 링크를 확인하세요.
""",

    "Guide_Methodology": """### Scoring Methodology (The 'Founder-in-Residence' Framework)
Our AI analyzes reports using a strict Venture Capital framework to identify **valid startup opportunities**, not just trends.

| Component | Meaning |
| :--- | :--- |
| **Pain Holder** | **Who** is suffering? (e.g., "Compliance Officers" is better than "Banks") |
| **Pain Mechanism** | **Why** is it hard? (Manual entry, siloed data, regulatory pressure) |
| **Attack Vector** | **How** can a startup solve this? (e.g., "Automated Reconciliation Agent") |

#### Importance Score (0-100)
- **< 50 (Discarded)**: Vague statements, macro trends, or problems solvable only by policy/regulation.
- **50 - 79 (Opportunity)**: Valid pain points, but may be niche or less urgent.
- **80+ (Critical Signal)**: **High Urgency**. Specific pain, clear target, and plausible solution.
""" if not is_ko else """### 점수 산정 방법론 ('Founder-in-Residence' 프레임워크)
AI는 단순한 트렌드가 아닌 **실질적인 스타트업 사업 기회**를 포착하기 위해 엄격한 벤처 캐피탈 프레임워크를 사용합니다.

| 항목 | 의미 |
| :--- | :--- |
| **페인 홀더 (Pain Holder)** | **누가** 고통받고 있는가? (예: "은행"보다 "준법 감시 담당자"가 더 구체적임) |
| **메커니즘 (Mechanism)** | **왜** 어려운가? (수기 입력, 데이터 고립, 규제 압박 등) |
| **공략 포인트 (Attack Vector)** | 스타트업이 **어떻게** 해결할 수 있는가? (예: "자동 대사 에이전트") |

#### 중요도 점수 (0-100)
- **< 50 (제외됨)**: 모호한 진술, 거시 경제 트렌드, 또는 정책/규제로만 해결 가능한 문제.
- **50 - 79 (사업 기회)**: 유효한 페인 포인트이나, 니치 마켓이거나 시급성이 낮을 수 있음.
- **80+ (핵심 신호)**: **높은 시급성**. 구체적인 고통, 명확한 대상, 그리고 실현 가능한 해결책이 존재함.
"""
}
            
# Logic to load data but wait to render filters
all_cards = load_cards()
df_cards = pd.DataFrame([c.model_dump() for c in all_cards])

# Load Reports and create Map
reports = load_reports()
report_map = {r.report_id: r for r in reports}

all_industries = set()
all_techs = set()

if not df_cards.empty:
    for tags in df_cards['industry_tags']:
        all_industries.update(tags)
    for tags in df_cards['technology_tags']:
        all_techs.update(tags)

selected_industries = []
selected_techs = []
min_score = 0


# --- Main Dashboard ---
st.title(T["Dashboard Title"])

# Tabs
tab1, tab2 = st.tabs([T["Tab_Dashboard"], T["Tab_Guide"]])

with tab2:
    st.markdown(T["Guide_Intro"])
    st.markdown("---")
    st.markdown(T["Guide_Methodology"])
    
with tab1:
    # --- Top Controls & Filters ---
    st.markdown("###") # Spacer
    
    with st.expander("🔍 Filters & Search / 필터 및 검색", expanded=True):
        # Filter Container Style
        st.markdown('<div class="filter-container">', unsafe_allow_html=True)
        f_col1, f_col2 = st.columns(2)
        with f_col1:
            selected_industries = st.multiselect(T["Industry"], sorted(list(all_industries)))
        with f_col2:
            selected_techs = st.multiselect(T["Technology"], sorted(list(all_techs)))
            
        f_col3, f_col4 = st.columns([3, 1])
        with f_col3:
            min_score = st.slider(T["Min Score"], 0, 100, 50)
        with f_col4:
            st.markdown("<br>", unsafe_allow_html=True) 
            if st.button("🔄 Reset / 초기화", use_container_width=True):
                # Reset logic usually requires session state or rerun with clearing params
                # For now just rerun, user has to manually clear if session state not bound
                st.rerun()

        # Admin Toggle (Small)
        show_admin = st.checkbox(T["Show Admin"])
        st.markdown('</div>', unsafe_allow_html=True)

    if show_admin:
        st.subheader("Discarded Signals (Admin)")
        from src.storage import load_discarded_signals
        discarded = load_discarded_signals()
        
        if discarded:
            df_discarded = pd.DataFrame([d.model_dump() for d in discarded])
            st.dataframe(df_discarded, use_container_width=True)
        else:
            st.info("No discarded signals found.")
    else:
        # Metrics Row (Premium Layout with Trends)
        m_col1, m_col2, m_col3 = st.columns(3)
        
        # Metric 1: Total Signals
        with m_col1:
            st.markdown(f"""
            <div class="metric-card">
                <h3>{T["Total Signals"]}</h3>
                <h2>{len(df_cards)}</h2>
                <div style="font-size:12px; color:rgba(255,255,255,0.5); margin-top:8px;">
                    Updated just now
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        # Metric 2: Critical Signals
        with m_col2:
            high_value_count = len(df_cards[df_cards['importance_score'] > 80]) if not df_cards.empty else 0
            st.markdown(f"""
            <div class="metric-card" style="border-left-color: #43A047;">
                <h3 style="color:#43A047 !important;">{T["Critical Signals"]}</h3>
                <h2>{high_value_count}</h2>
                <div style="font-size:12px; color:rgba(255,255,255,0.5); margin-top:8px;">
                     High Urgency
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        # Metric 3: Reports
        with m_col3:
            reports_count = len(reports)
            st.markdown(f"""
            <div class="metric-card" style="border-left-color: #8E24AA;">
                <h3 style="color:#8E24AA !important;">{T["Reports Tracked"]}</h3>
                <h2>{reports_count}</h2>
                <div style="font-size:12px; color:rgba(255,255,255,0.5); margin-top:8px;">
                    Active Sources
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # Filtering Logic
        if not df_cards.empty:
            filtered_df = df_cards.copy()
            
            if selected_industries:
                filtered_df = filtered_df[filtered_df['industry_tags'].apply(lambda x: any(i in x for i in selected_industries))]
                
            if selected_techs:
                filtered_df = filtered_df[filtered_df['technology_tags'].apply(lambda x: any(t in x for t in selected_techs))]
                
            filtered_df = filtered_df[filtered_df['importance_score'] >= min_score]
            
            # Sort by Importance
            filtered_df = filtered_df.sort_values(by="importance_score", ascending=False)
            
            # --- Pagination (Improved) ---
            if 'page' not in st.session_state:
                st.session_state.page = 1
                
            items_per_page = 5
            total_items = len(filtered_df)
            total_pages = max(1, (total_items + items_per_page - 1) // items_per_page)
            
            if st.session_state.page > total_pages:
                st.session_state.page = total_pages
            
            # Pagination UI
            if total_pages > 1:
                col_c = st.columns(9)
                start_p = max(1, st.session_state.page - 2)
                end_p = min(total_pages, start_p + 4)
                if end_p - start_p < 4: start_p = max(1, end_p - 4)
                
                # First/Prev
                with col_c[0]:
                    if st.button("<<", key="first"): st.session_state.page = 1; st.rerun()
                with col_c[1]:
                    if st.button("<", key="prev") and st.session_state.page > 1: st.session_state.page -= 1; st.rerun()
                
                # Numbers
                idx = 2
                for p in range(start_p, end_p + 1):
                    if idx < 7:
                        with col_c[idx]:
                            if p == st.session_state.page:
                                st.button(str(p), key=f"p_{p}", disabled=True, type="primary")
                            else:
                                if st.button(str(p), key=f"p_{p}"): st.session_state.page = p; st.rerun()
                    idx+=1
                    
                # Next/Last
                with col_c[7]:
                     if st.button(">", key="next") and st.session_state.page < total_pages: st.session_state.page += 1; st.rerun()
                with col_c[8]:
                     if st.button(">>", key="last"): st.session_state.page = total_pages; st.rerun()
            
            # Slice Data
            p_start = (st.session_state.page - 1) * items_per_page
            p_end = p_start + items_per_page
            page_df = filtered_df.iloc[p_start:p_end]
            
            st.caption(f"{T['Showing']} {p_start+1}-{min(p_end, total_items)} {T['of']} {total_items} {T['signals']}")
            
            # Render Cards
            for index, row in page_df.iterrows():
                # Language Fallback
                attack_raw = row.get('attack_vector_ko') if is_ko and row.get('attack_vector_ko') else row.get('attack_vector')
                holder_raw = row.get('pain_holder_ko') if is_ko and row.get('pain_holder_ko') else row.get('pain_holder')
                evidence_raw = row.get('evidence_sentence_ko') if is_ko and row.get('evidence_sentence_ko') else row.get('evidence_sentence')
                
                # Escape HTML to prevent breakage
                attack = html.escape(str(attack_raw))
                holder = html.escape(str(holder_raw))
                evidence = html.escape(str(evidence_raw))
                
                # Tags
                ind_tags = ' '.join([f'<span class="tag">{html.escape(str(tag))}</span>' for tag in row.get('industry_tags', [])])
                tech_tags = ' '.join([f'<span class="tag" style="background-color:rgba(255, 100, 100, 0.1); color:#ffcccc;">{html.escape(str(tag))}</span>' for tag in row.get('technology_tags', [])])
                
                # Badge Style
                score_class = "score-high" if row['importance_score'] >= 80 else ""
                
                # Detailed Card Layout
                card_html = textwrap.dedent(f"""
                    <div class="signal-card">
                        <!-- Header Row -->
                        <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:16px;">
                            <div style="flex: 1; padding-right: 16px; border-left: 3px solid #1E88E5; padding-left: 12px;">
                                <h3 style="margin:0; font-size:18px; line-height:1.4;">{attack}</h3>
                                <div style="margin-top:6px; font-size:13px; color:rgba(255,255,255,0.6);">
                                    <span style="color:rgba(255,255,255,0.4);">Target:</span> <strong style="color:rgba(255,255,255,0.9);">{holder}</strong>
                                </div>
                            </div>
                            <div style="text-align:right;">
                                <span class="score-badge {score_class}" style="display:inline-block; margin-bottom:4px;">
                                    {row['importance_score']}
                                </span>
                            </div>
                        </div>
                        
                        <!-- Quote Block -->
                        <div style="background:rgba(255,255,255,0.03); padding:16px; border-radius:6px; margin-bottom:16px; border-left: 2px solid rgba(255,255,255,0.1);">
                            <p style="color:rgba(255,255,255,0.7); font-style:italic; font-size:14px; margin:0; line-height:1.6;">
                                "{evidence}"
                            </p>
                        </div>
                        
                        <!-- Footer Row -->
                        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">
                            <div style="display:flex; flex-wrap:wrap; gap:4px;">
                                {ind_tags} {tech_tags}
                            </div>
                        </div>
                    </div>
                """)
                
                with st.container():
                    st.markdown(card_html, unsafe_allow_html=True)
                    if st.button(T["View Details"], key=f"btn_{row['card_id']}", use_container_width=True):
                        show_details_dialog(row.to_dict(), is_ko, T, report_map)

        else:
            st.info(T["No Signals"])

# --- Footer ---
st.markdown(f"<br><br><div style='text-align:center; color:#666;'>{T['Footer']}</div>", unsafe_allow_html=True)
