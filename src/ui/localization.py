def get_translations(is_ko: bool):
    """Returns the translation dictionary based on the selected language."""
    T = {
        "Dashboard Title": "Research Radar" if not is_ko else "리서치 레이더",
        "Dashboard Subtitle": "High-value startup opportunities extracted from global research." if not is_ko else "글로벌 리서치에서 추출한 핵심 스타트업 사업 기회",
        "Total Signals": "Total Signals" if not is_ko else "전체 신호",
        "Critical Signals": "Critical Signals" if not is_ko else "핵심 신호 (80+)",
        "Reports Tracked": "Active Sources" if not is_ko else "분석 리포트",
        "Search Placeholder": "Search signals, pain points..." if not is_ko else "신호, 페인 포인트 검색...",
        "Industry": "Industry" if not is_ko else "산업군",
        "Technology": "Technology" if not is_ko else "기술",
        "Min Score": "Importance Score" if not is_ko else "중요도 점수",
        "Sort By": "Sort By" if not is_ko else "정렬 기준",
        "Sort_Newest": "Newest First" if not is_ko else "최신순",
        "Sort_Score": "Highest Score" if not is_ko else "중요도순",
        "Reset": "Reset Filters" if not is_ko else "필터 초기화",
        "Advanced Filters": "Advanced Filters" if not is_ko else "상세 필터",
        "Show Admin": "Admin View" if not is_ko else "관리자 뷰",
        "No Signals": "No signals match your criteria." if not is_ko else "조건에 맞는 신호가 없습니다.",
        "Footer": "Built with Streamlit & OpenAI" if not is_ko else "Streamlit & OpenAI 기반 제작",
        "Report Source": "Source Report" if not is_ko else "원본 리포트",
        
        # Pagination / Status
        "Showing": "Showing" if not is_ko else "표시 중",
        "of": "of" if not is_ko else "/",
        "signals": "signals" if not is_ko else "건",
        "View Details": "View Details" if not is_ko else "상세 보기",
        
        # User Guide Strings
        "Tab_Dashboard": "Dashboard" if not is_ko else "대시보드",
        "Tab_Guide": "Methodology" if not is_ko else "방법론",
        
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
    return T
