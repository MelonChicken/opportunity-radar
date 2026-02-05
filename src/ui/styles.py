import streamlit as st



# Additional CSS for Premium Quote
# We can append this to the main CSS or include it here if we want to separate "Premium Components"
# For now, adding it to the main block is cleaner.
def load_css():
    base_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Noto+Sans+KR:wght@400;500;600;700&display=swap');

    :root {
        /* 1. Color Palette (Tailwind-like Slate & Blue) */
        
        /* Backgrounds */
        --bg-color: #F8F9FA;       /* Slate-50 equivalent */
        --bg-secondary: #FFFFFF;   /* White Card */
        --bg-sidebar: #0F172A;     /* Slate-900 (Dark Sidebar) */
        
        /* Text */
        --text-primary: #111827;   /* Slate-900 */
        --text-secondary: #6B7280; /* Slate-500 */
        --text-on-dark: #F3F4F6;   /* Slate-100 */
        
        /* Accents */
        --accent-primary: #2563EB; /* Blue-600 */
        --accent-hover: #1D4ED8;   /* Blue-700 */
        --accent-light: #EFF6FF;   /* Blue-50 */
        
        /* Borders */
        --border-color: #E2E8F0;   /* Slate-200 */
        
        /* Semantic */
        --color-critical: #EF4444; /* Red-500 */
        --color-warning: #F59E0B;  /* Amber-500 */
        --color-success: #10B981;  /* Emerald-500 */
        --color-neutral: #9CA3AF;  /* Slate-400 */
        
        /* Shadows */
        --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        
        /* Spacing */
        --radius-md: 12px;
        --radius-sm: 8px;
    }

    /* 2. Global Typography & Reset */
    .stApp {
        background-color: var(--bg-color);
        font-family: 'Inter', 'Noto Sans KR', sans-serif;
        color: var(--text-primary);
    }
    
    h1, h2, h3, h4, 5 { 
        color: var(--text-primary) !important; 
        font-family: 'Inter', 'Noto Sans KR', sans-serif;
        font-weight: 700;
        letter-spacing: -0.02em;
    }
    
    p, span, div {
        color: var(--text-primary);
    }
    
    /* 3. Sidebar Styling (Dark Theme Override) */
    section[data-testid="stSidebar"] {
        background-color: var(--bg-sidebar);
        border-right: 1px solid #1E293B;
    }
    section[data-testid="stSidebar"] * {
        color: var(--text-on-dark) !important;
    }
    section[data-testid="stSidebar"] .block-container {
        padding-top: 2rem;
    }
    
    /* Custom Sidebar Nav Items */
    .nav-active {
        background-color: var(--accent-primary);
        color: white !important;
        padding: 10px 16px;
        border-radius: 8px;
        font-weight: 600;
        margin-bottom: 4px;
        display: block;
    }
    
    /* Sidebar Ghost Buttons (Inactive State) */
    section[data-testid="stSidebar"] .stButton button {
        background-color: transparent !important;
        border: none !important;
        color: #94A3B8 !important; /* Slate-400 */
        text-align: left !important;
        padding-left: 0px !important; /* Alignment Fix: Removed padding so it sits flush with column gap */
        box-shadow: none !important;
        font-weight: 500 !important;
        
        /* Force Left Alignment */
        display: flex !important;
        justify-content: flex-start !important;
        align-items: center !important;
        width: 100% !important;
    }
    section[data-testid="stSidebar"] .stButton button:hover {
        background-color: rgba(255,255,255,0.05) !important;
        color: #F1F5F9 !important; /* Light text on hover */
        border: none !important;
    }
    section[data-testid="stSidebar"] .stButton {
        margin-bottom: 4px; /* Tight spacing like list */
    }

    /* 4. KPI Cards (White + Shadow) */
    .kpi-container {
        display: flex;
        gap: 20px;
        margin-bottom: 32px;
    }
    .kpi-card {
        flex: 1;
        background-color: var(--bg-secondary);
        border: 1px solid var(--border-color);
        border-radius: var(--radius-md);
        padding: 24px;
        box-shadow: var(--shadow-sm);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .kpi-card h3 {
        color: var(--text-secondary) !important;
        font-size: 0.75rem !important;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin: 0 0 8px 0;
        font-weight: 600;
    }
    .kpi-card .value {
        font-size: 2.5rem;
        font-weight: 800;
        color: var(--text-primary);
        line-height: 1.1;
    }
    .kpi-card .sub-text {
        font-size: 0.85rem;
        color: var(--text-secondary);
        margin-top: 4px;
    }

    /* 5. Filter Bar (Clean Search) */
    .filter-bar {
        margin-bottom: 24px;
        display: flex;
        align-items: center;
        gap: 16px;
    }
    
    /* Custom Input Styling (Hard to override Streamlit completely, but attempting wrapper) */
    div[data-testid="stTextInput"] input {
        background-color: var(--bg-secondary) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: var(--radius-sm) !important;
        color: var(--text-primary) !important;
        padding: 10px 12px !important;
        box-shadow: var(--shadow-sm);
    }
    div[data-testid="stTextInput"] input:focus {
        border-color: var(--accent-primary) !important;
        box-shadow: 0 0 0 2px var(--accent-light) !important;
    }
    div[data-testid="stTextInput"] label {
        display: none !important; /* Hide label for cleaner search look as requested */
    }
    
    /* Input Placeholder Visibility Fix */
    div[data-testid="stTextInput"] input::placeholder {
        color: var(--text-secondary) !important;
        opacity: 1 !important; /* Force visibility */
        font-weight: 400;
    }
    div[data-testid="stTextInput"] input::-webkit-input-placeholder {
        color: var(--text-secondary) !important;
        opacity: 1 !important;
    }

    /* 6. Signal Card (Premium Light Layout) */
    .signal-card {
        /* background-color: var(--bg-secondary); Removed to let container handle bg */
        /* border: 1px solid var(--border-color); Removed */
        /* border-radius: var(--radius-md); Removed */
        padding: 0px; /* Padding handled by container */
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        /* box-shadow: var(--shadow-sm); Removed */
        margin-bottom: 12px;
    }
    .signal-card:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-md);
    }
    
    /* Card Header: Tag + Score */
    .card-top {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 16px;
    }
    .category-tag {
        background-color: var(--accent-light);
        color: var(--accent-primary);
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        padding: 4px 8px;
        border-radius: 4px;
        letter-spacing: 0.05em;
    }
    .score-badge {
        background-color: var(--accent-light);
        color: var(--accent-primary);
        font-weight: 800;
        font-size: 0.9rem;
        /* Fix Overflow: Ensure width adapts or stays fixed without shrinking */
        min-width: 80px; /* Expanded for "Score 95" text */
        height: 32px;
        padding: 0 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 16px; /* Pill shape */
        flex-shrink: 0; /* Prevent shrinking */
        white-space: nowrap;
    }
    
    /* Card Content */
    .card-title {
        color: var(--text-primary);
        font-size: 1.1rem;
        font-weight: 700;
        line-height: 1.4;
        margin-bottom: 12px;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }
    .card-desc {
        color: var(--text-secondary);
        font-size: 0.9rem;
        line-height: 1.5;
        margin-bottom: 16px;
        display: -webkit-box;
        -webkit-line-clamp: 3;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }
    .card-meta {
        font-size: 0.8rem;
        color: var(--text-secondary);
        margin-bottom: 20px;
    }
    .card-meta strong {
        color: var(--text-primary);
    }
    
    /* Card Footer: Pills + Action */
    .card-footer {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-top: 16px;
        border-top: 1px solid var(--border-color);
    }
    .pill {
        display: inline-block;
        border: 1px solid var(--border-color);
        border-radius: 4px;
        padding: 2px 8px;
        font-size: 0.7rem;
        color: var(--text-secondary);
        background-color: #FAFAFA;
        margin-right: 4px;
    }
    .view-link {
        color: var(--accent-primary);
        font-size: 0.85rem;
        font-weight: 600;
        text-decoration: none;
        cursor: pointer;
    }
    .view-link:hover { text-decoration: underline; }

    .stButton button {
        background-color: var(--bg-secondary) !important;
        border: 1px solid var(--border-color) !important;
        color: var(--text-primary) !important;
        border-radius: 6px !important;
        box-shadow: var(--shadow-sm) !important;
    }
    
    /* Special Overlap for Card Button */
    /* Special Overlap for Card Button using Wrapper Strategy */
    /* Checkpoint 2: Flexbox + Negative Margin (Robust Flow) */
    
    /* Simplified Card Button Style - No more negative margin hack needed if we use container */
    /* But we want to target the specific button inside the special container */
    
    .view-full-analysis-btn button {
        width: 100% !important;
        background-color: white !important;
        border: 1px solid var(--border-color) !important;
        color: var(--accent-primary) !important;
        font-weight: 600 !important;
        box-shadow: none !important;
    }
    .view-full-analysis-btn button:hover {
        background-color: var(--accent-light) !important;
        border-color: var(--accent-primary) !important;
    }
    
    .stButton button:hover {
        border-color: var(--accent-primary) !important;
        color: var(--accent-primary) !important;
        background-color: var(--accent-light) !important;
    }
    
    /* Primary Action Buttons */
    .btn-primary button {
        background-color: var(--accent-primary) !important;
        color: white !important;
        border: none !important;
    }

    /* 8. Widget Overrides (Force Light Mode in Main Area) */
    
    /* Multiselect & Selectbox Container */
    .stMultiSelect div[data-baseweb="select"], .stSelectbox div[data-baseweb="select"] {
        background-color: var(--bg-secondary) !important;
        border-color: var(--border-color) !important;
        color: var(--text-primary) !important;
    }
    .stMultiSelect div[data-baseweb="select"] > div, .stSelectbox div[data-baseweb="select"] > div {
        background-color: var(--bg-secondary) !important;
        color: var(--text-primary) !important;
    }
    
    /* Selected Tags in Multiselect */
    .stMultiSelect div[data-baseweb="tag"] {
        background-color: var(--accent-light) !important;
        color: var(--accent-primary) !important;
        border: 1px solid var(--accent-primary) !important;
    }
    .stMultiSelect div[data-baseweb="tag"] span {
        color: var(--accent-primary) !important;
    }
    
    /* Dropdown Options (The Popover) */
    /* Dropdown Options (The Popover) */
    /* Dropdown Options (The Popover) - Aggressive Override */
    div[data-baseweb="popover"] {
        background-color: white !important;
        border: 1px solid var(--border-color) !important;
    }
    
    div[data-baseweb="popover"] > div {
        background-color: white !important;
    }

    div[data-baseweb="menu"] {
        background-color: white !important;
        border: none !important;
    }
    
    /* List Items (Options) */
    li[role="option"] {
        background-color: white !important;
        color: var(--text-primary) !important;
        display: flex !important;
        align-items: center !important;
    }
    
    /* Text inside List Items */
    li[role="option"] div, li[role="option"] span {
        color: var(--text-primary) !important;
    }
    
    /* Hover State */
    li[role="option"]:hover {
        background-color: var(--accent-light) !important;
    }
    li[role="option"]:hover * {
        background-color: transparent !important; /* Let parent bg show */
        color: var(--text-primary) !important;
    }
    
    /* Selected State */
    li[role="option"][aria-selected="true"] {
         background-color: var(--accent-light) !important;
         color: var(--accent-primary) !important;
         font-weight: 600 !important;
    }
    li[role="option"][aria-selected="true"] * {
        color: var(--accent-primary) !important;
        background-color: transparent !important;
    }

    /* Text inside the select box (including placeholder "Choose options") */
    .stMultiSelect div[data-baseweb="select"] span, 
    .stSelectbox div[data-baseweb="select"] span,
    .stMultiSelect div[data-baseweb="select"] div, 
    .stSelectbox div[data-baseweb="select"] div {
        color: var(--text-secondary) !important;
        opacity: 1 !important; /* Fix for invisible placeholder */
        -webkit-text-fill-color: var(--text-secondary) !important;
    }
    
    /* Slider Color Force */
    div[data-testid="stSlider"] div[role="slider"] {
        background-color: var(--accent-primary) !important;
    }
    div[data-testid="stSlider"] div[data-baseweb="slider"] > div > div {
        background-color: var(--accent-primary) !important;
    }

    div[data-testid="stExpander"] {
        background-color: var(--bg-secondary) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: var(--radius-sm);
    }
    
    /* 8. Dialog / Modal Styling */
    /* 8. Dialog / Modal Styling (Force Light Theme) */
    /* 8. Dialog / Modal Styling (Force Light Theme) */
    div[data-testid="stDialog"] div[role="dialog"] {
        background-color: #FFFFFF !important;
        color: #111827 !important; /* Slate-900 */
        border: 1px solid #E2E8F0 !important;
    }
    
    /* Force text colors inside the dialog - BUT BE CAREFUL not to override Code Block & Buttons */
    div[data-testid="stDialog"] h1, 
    div[data-testid="stDialog"] h2, 
    div[data-testid="stDialog"] h3, 
    div[data-testid="stDialog"] h4, 
    div[data-testid="stDialog"] h5, 
    div[data-testid="stDialog"] h6, 
    div[data-testid="stDialog"] p,
    div[data-testid="stDialog"] span,
    div[data-testid="stDialog"] li {
        color: #111827 !important;
    }
    
    /* REMOVED generic div selector to prevent breaking complex components */

    /* Exclude Close Button */
    div[data-testid="stDialog"] button[aria-label="Close"] {
        color: #64748B !important; 
    }

    /* Prompt Box High Contrast Override (Dark Theme for Prompt) */
    /* Target everything inside stCodeBlock GLOBALLY to force white text */
    [data-testid="stCodeBlock"],
    [data-testid="stCodeBlock"] *,
    .stCodeBlock code,
    .stCodeBlock pre {
        background-color: #1E293B !important; /* Slate-900 */
        color: #E5E7EB !important; /* Slate-50 White */
        font-family: 'Consolas', 'Monaco', monospace !important;
        text-shadow: none !important;
        -webkit-text-fill-color: #E5E7EB !important;
    }
    
    /* Ensure the container itself has the border and radius */
    [data-testid="stCodeBlock"] {
        border-radius: 8px !important;
        border: 1px solid #334155 !important;
    }
    
    /* Fix Buttons inside Dialog (Link Buttons & Download Buttons) */
    /* These often need white text if they are 'primary' or dark buttons */
    /* We reset color to 'initial' or specific white if class indicates button */
    
    div[data-testid="stDialog"] a[role="button"],
    div[data-testid="stDialog"] button:not([aria-label="Close"]) {
         /* Check if we can just reset color. Streamlit buttons usually handle their own text color 
            unless overriden by my broad selector. Removing the broad 'div' selector above 
            should fix the main issue, but let's be safe. */
         color: initial !important;
    }
    
    /* If the buttons are primary/secondary and look dark, they need light text */
    div[data-testid="stDialog"] button p {
         color: inherit !important;
    }

    /* PREMIUM QUOTE BOX (OPTION 1) */
    .rr-quote-wrap {
      margin: 32px 0 10px 0;
      padding: 34px 40px;
      border-radius: 22px;
      background: linear-gradient(135deg, #2B66F6 0%, #1E3A8A 100%);
      position: relative;
      overflow: hidden;
      box-shadow: 0 14px 36px rgba(2, 6, 23, 0.18);
    }
    .rr-quote-wrap:hover {
      transform: translateY(-2px);
      transition: 160ms ease;
    }
    .rr-quote-wrap:before {
      content: "";
      position: absolute;
      inset: 0;
      background: radial-gradient(circle at 20% 20%, rgba(255,255,255,0.18), transparent 40%),
                  radial-gradient(circle at 85% 25%, rgba(255,255,255,0.10), transparent 35%);
      pointer-events: none;
    }
    .rr-quote {
      font-size: 22px;
      line-height: 1.45;
      font-weight: 650;
      color: rgba(255,255,255,0.92) !important; /* Force White */
      margin: 0;
      letter-spacing: -0.2px;
      font-family: 'Inter', sans-serif !important;
      position: relative;
      z-index: 2;
    }
    .rr-quote-mark {
      position: absolute;
      top: 18px;
      left: 18px;
      font-size: 52px;
      color: rgba(255,255,255,0.28);
      font-weight: 900;
      z-index: 1;
    }
    .rr-quote-sub {
      margin-top: 14px;
      color: rgba(255,255,255,0.72) !important;
      font-size: 13px;
      letter-spacing: 0.2px;
      position: relative;
      z-index: 2;
    }
    .rr-quote-sub span {
      display: inline-block;
      padding: 6px 10px;
      border: 1px solid rgba(255,255,255,0.22);
      border-radius: 999px;
      background: rgba(15, 23, 42, 0.18);
      color: rgba(255,255,255,0.9) !important;
    }
    
    .rr-center {
      max-width: 980px;
      margin: 0 auto;
    }

    /* ChatGPT Prompt Box (Styled st.code) */
    [data-testid="stCodeBlock"] {
      background: linear-gradient(135deg, #0B1220, #020617) !important;
      border-radius: 14px;
      padding: 10px;
      border: 1px solid rgba(148,163,184,0.15);
      margin-bottom: 20px;
    }
    [data-testid="stCodeBlock"] pre {
        background: transparent !important;
    }
    /* Force Bright Text on ALL elements inside Code Block */
    /* Force Bright Text on ALL elements inside Code Block (Aggressive Override) */
    [data-testid="stCodeBlock"] code,
    [data-testid="stCodeBlock"] span,
    [data-testid="stCodeBlock"] pre,
    [data-testid="stCodeBlock"] div {
        color: #FFFFFF !important;
        font-family: 'Inter', sans-serif !important; 
        text-shadow: none !important;
        -webkit-text-fill-color: #FFFFFF !important;
        background-color: transparent !important;
    }

    .rr-btn {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      background: #F8FAFC;
      color: #020617 !important;
      border: 1px solid rgba(148,163,184,0.35);
      border-radius: 10px;
      padding: 10px 18px;
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
      text-decoration: none !important;
      transition: all 0.2s;
    }
    .rr-btn:hover {
      background: #E5E7EB;
      border-color: rgba(148,163,184,0.5);
      color: #020617 !important;
    }
    
    /* Override Global Download Button to match rr-btn style */
    div[data-testid="stDownloadButton"] button {
      background-color: #F8FAFC !important;
      color: #020617 !important;
      border: 1px solid rgba(148,163,184,0.35) !important;
      border-radius: 10px !important;
      padding: 0.5rem 1rem !important;
      font-size: 13px !important;
      font-weight: 600 !important;
    }
    div[data-testid="stDownloadButton"] button:hover {
      background-color: #E5E7EB !important;
      border-color: rgba(148,163,184,0.5) !important;
      color: #020617 !important;
    }
    div[data-testid="stDownloadButton"] button p {
       color: #020617 !important;
    }
</style>
"""
    return base_css

def apply_styles():
    st.markdown(load_css(), unsafe_allow_html=True)
