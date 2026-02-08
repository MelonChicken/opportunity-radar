def get_translations(is_ko: bool):
    """Returns the translation dictionary based on the selected language."""
    T = {
        "Dashboard Title": "Research Radar" if not is_ko else "리서치 레이더",
        "Dashboard Subtitle": "High-value startup opportunities extracted from global research." if not is_ko else "글로벌 리서치에서 추출한 핵심 스타트업 사업 기회",
        "Total Signals": "Total Signals" if not is_ko else "전체 신호",
        "Critical Signals": "Critical Signals" if not is_ko else "핵심 신호 (80+)",
        "Reports Tracked": "Active Sources" if not is_ko else "분석 리포트",
        "Search Placeholder": "Search by industry, pain point, technology... (e.g. fraud detection)" if not is_ko else "산업, 페인 포인트, 기술로 검색... (예: 사기 탐지)",
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
        "Footer": "Built with Streamlit & Antigravity" if not is_ko else "Streamlit & Antigravity 기반 제작",
        "Report Source": "Source Report" if not is_ko else "원본 리포트",
        
        # Admin / Pipeline
        "Admin Title": "System Administration" if not is_ko else "시스템 관리",
        "Pipeline Control": "Data Pipeline Control" if not is_ko else "데이터 파이프라인 제어",
        "Run Pipeline": "Run Pipeline" if not is_ko else "파이프라인 실행",
        "Status Log": "Execution Logs" if not is_ko else "실행 로그",
        "Reset Data": "Reset Data" if not is_ko else "데이터 초기화",
        
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
""",
        # --- New Layout Translations ---
        "Trending Title": "Trending Critical Sectors" if not is_ko else "급상승 핵심 분야",
        "Sector_AI": "Artificial Intelligence" if not is_ko else "인공지능 (AI)",
        "Sector_Cybersecurity": "Cybersecurity" if not is_ko else "사이버 보안",
        "Sector_Energy": "Sustainable Energy" if not is_ko else "지속 가능 에너지",
        "Sector_Legal": "Legal Services" if not is_ko else "법률 서비스",
        "Sector_Finance": "Financial Services" if not is_ko else "금융 서비스",
        
        "Framework Title": "Founder-in-Residence Framework" if not is_ko else "창업가 사내독립기업(FIR) 프레임워크",
        "Framework Desc": "Our proprietary scoring system ensures you focus on real problems, not just hype. Signals are filtered through a multi-stage validation process." if not is_ko else "독자적인 스코어링 시스템을 통해 과장된 유행이 아닌 실제 문제를 포착합니다. 모든 시그널은 다단계 검증 과정을 거쳐 필터링됩니다.",
        "Learn More": "Learn more about scoring" if not is_ko else "스코어링 방법 더 알아보기",
        
        "Methodology Title": "Founder-in-Residence Framework" if not is_ko else "창업가 사내독립기업(FIR) 프레임워크",
        "Methodology Subtitle": "Our methodology for distilling millions of data points into actionable opportunities." if not is_ko else "수백만 개의 데이터 포인트에서 실행 가능한 기회를 추출하는 방법론입니다.",
        "Funnel Title": "The Selection Funnel" if not is_ko else "선별 깔때기 (Funnel)",
        "Funnel_Step1_Title": "Signal Aggregation" if not is_ko else "시그널 수집",
        "Funnel_Step1_Desc": "Processing real-time reports from PwC Global Network." if not is_ko else "PwC 글로벌 네트워크의 실시간 리포트 처리.",
        "Funnel_Step2_Title": "Founder-Viability Filter" if not is_ko else "창업 타당성 필터",
        "Funnel_Step2_Desc": "Can a small team solve this? Is it technically feasible today?" if not is_ko else "소규모 팀으로 해결 가능한가? 기술적으로 구현 가능한가?",
        "Funnel_Step3_Title": "Criticality Scoring" if not is_ko else "중요도 채점",
        "Funnel_Step3_Desc": "Ranking by market size, pain intensity, and competitive landscape." if not is_ko else "시장 규모, 고통의 강도, 경쟁 구도를 기반으로 순위 산정.",
        "Benchmark Title": "Scoring Benchmarks" if not is_ko else "점수 기준",
        "Bench_High_Label": "CRITICAL SIGNAL" if not is_ko else "핵심 신호",
        "Bench_High_Desc": "High urgency. Immediate problem-market fit potential. Validated pain points." if not is_ko else "높은 시급성. 즉각적인 문제-시장 적합성(PMF) 잠재력. 검증된 페인 포인트.",
        "Bench_Mid_Label": "POTENTIAL OPPORTUNITY" if not is_ko else "잠재적 기회",
        "Bench_Mid_Desc": "Emerging trend. Requires further market education or technical innovation." if not is_ko else "떠오르는 트렌드. 추가적인 시장 교육이나 기술 혁신이 필요함.",
        "Quote Text": "\"Don't build based on intuition. Build based on verified market friction.\"" if not is_ko else "\"직감으로 짓지 말고, 검증된 시장의 마찰(Friction) 위에 지어라.\"",
        "Quote Author": "— Research Radar Philosophy" if not is_ko else "— 리서치 레이더 철학",
        "Quick Filters": "Try" if not is_ko else "추천 검색어",
        
        # P0: 2. Methodology Details
        "Funnel_Step1_Value": "Inputs: 50,000+ Reports/Day" if not is_ko else "입력: 하루 50,000+ 리포트",
        "Funnel_Step2_Value": "Filter: < 1% Pass Rate" if not is_ko else "필터: 통과율 1% 미만",
        "Funnel_Step2_Criteria": "Criteria: Market Readiness, Founder Fit, Execution Barrier" if not is_ko else "**기준:** 시장 준비도, 창업가 적합성, 실행 장벽",
        "Funnel_Step3_Value": "Output: ~10 Critical Signals" if not is_ko else "출력: ~10개의 핵심 신호",
        "Validation_Process": "Validation Process details..." if not is_ko else "검증 프로세스 상세...",
        "Data_Source_Reliability": "Source Reliability: PwC (100%)" if not is_ko else "출처 신뢰도: PwC (100%)",
        
        # --- Phase 1 UX Improvements ---
        "View Full Analysis": "View Full Analysis" if not is_ko else "상세 분석 보기",
        "Updated ago": "Updated {time_diff} ago" if not is_ko else "마지막 업데이트: {time_diff} 전",
        
        # --- Details Modal ---
        "Prompt Title": "ChatGPT Prompt" if not is_ko else "ChatGPT 프롬프트",
        
        # --- Onboarding (P0: 1.2) ---
        "Onboarding_Title": "Discover Market Opportunities" if not is_ko else "시장 기회를 발견하세요",
        "Onboarding_Subtitle": "3 steps to maximize your research efficiency" if not is_ko else "리서치 효율을 극대화하는 3가지 단계",
        "Onb_Step1_Title": "Global Scan" if not is_ko else "글로벌 스캔",
        "Onb_Step1_Desc": "Analyzing reports from PwC Global Network in real-time." if not is_ko else "PwC 글로벌 네트워크의 리포트를 실시간으로 분석합니다.",
        "Onb_Step2_Title": "Critical Signals" if not is_ko else "핵심 신호",
        "Onb_Step2_Desc": "Focus on signals with Importance Score 80+." if not is_ko else "중요도 점수 80점 이상의 신호에 집중하세요.",
        "Onb_Step3_Title": "Take Action" if not is_ko else "실행",
        "Onb_Step3_Desc": "Filter, Export, and Generate Briefs for your strategy." if not is_ko else "필터링, 내보내기, 브리핑 생성으로 전략을 수립하세요.",
        "Start Exploring": "Start Exploring" if not is_ko else "탐색 시작하기",
        "Open ChatGPT": "Open ChatGPT" if not is_ko else "ChatGPT 열기",
        "Download Prompt": "Download Prompt (.txt)" if not is_ko else "프롬프트 다운로드 (.txt)",
        "Score_Title": "Scores" if not is_ko else "점수 및 신뢰도",
        "Score": "Score" if not is_ko else "중요도",
        "Confidence_Label": "Confidence" if not is_ko else "신뢰도",
        "Report ID": "Report ID" if not is_ko else "리포트 ID",
        "Tags": "Tags" if not is_ko else "태그",
        "Target_Label": "Target (Who)" if not is_ko else "타겟 고객 (Who)",
        "Pain_Label": "Pain (Why)" if not is_ko else "페인 포인트 (Why)",
        "Evidence_Label": "Evidence" if not is_ko else "근거 문장",
        
        # --- P1: Major UX Improvements ---
        "Score_Tooltip": "Business Opportunity Value (0-100)" if not is_ko else "사업 기회 가치 (0-100)",
        "Confidence_Tooltip": "Data Source Reliability" if not is_ko else "데이터 소스 신뢰도",
        "Last Updated": "Last Updated" if not is_ko else "마지막 업데이트",
         "Updated_Exact": "Last updated: {time_str} KST" if not is_ko else "마지막 업데이트: {time_str} KST",
         "Update_Frequency": "Update frequency: Every 24h" if not is_ko else "업데이트 주기: 24시간마다",
         "Show More": "Show More" if not is_ko else "더 보기",
         "Show Less": "Show Less" if not is_ko else "접기",
         
         # P1: Search & Filter
         "Search_Placeholder_New": "Search keywords (e.g. 'fraud', 'AI')..." if not is_ko else "키워드 검색 (예: '사기', 'AI')...",
         "Filter_Result_Count": "Viewing {count} opportunities" if not is_ko else "{count} 개의 기회를 보고 있습니다",
         "No_Results_Found": "No opportunities found matching your criteria." if not is_ko else "검색 조건에 맞는 기회가 없습니다.",
         "Sort_Highest_Score": "Highest Score" if not is_ko else "높은 점수순",
         "Target_Label": "Target" if not is_ko else "타겟",
         
         # P1: Scoring Explanation
         "Score_Explanation_Title": "How we score opportunities" if not is_ko else "기회 점수 산정 방식",
         "Score_Formula_Desc": "The Importance Score is a weighted average of three key factors:" if not is_ko else "중요도 점수는 세 가지 핵심 요소의 가중 평균입니다:",
         "Score_Breakdown_Label": "Score Breakdown" if not is_ko else "점수 구성",
         "Factor_Pain": "Pain Intensity (40%)" if not is_ko else "고통의 강도 (40%)",
         "Factor_Market": "Market Size (30%)" if not is_ko else "시장 규모 (30%)",
         "Factor_Feasibility": "Technical Feasibility (30%)" if not is_ko else "기술적 실현 가능성 (30%)",
         "Score_Help_Link": "How is this scored?" if not is_ko else "점수 산정 방식 보기",
         
         # P2: Advanced Filters
         "Filter_Label_Score_Range": "Importance Score Range" if not is_ko else "중요도 점수 범위",
         "Filter_Apply_Button": "Apply Filters" if not is_ko else "필터 적용",
    }
    return T
