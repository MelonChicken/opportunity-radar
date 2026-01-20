import streamlit as st

def load_css():
    """Returns the CSS string for the application style."""
    return """
<style>
    :root {
        /* Color Palette */
        --bg-color: #121212;
        --bg-secondary: #1E1E1E;
        --bg-tertiary: #2C2C2C;
        --bg-sidebar: #0E1117; /* Streamlit Default Dark Sidebar Color match or custom */
        --text-primary: #E0E0E0; 
        --text-secondary: #A0A0A0;
        --accent-primary: #4CACBC; 
        --accent-secondary: #FFB74D; 
        --border-color: #333333;
        
        /* Semantic Colors */
        --color-critical: #FF5252;
        --color-opportunity: #2196F3;
        --color-neutral: #9E9E9E;
        
        /* Spacing */
        --spacing-md: 16px;
        --spacing-lg: 24px;
    }

    /* 1. Global Reset & Typography */
    .stApp {
        background-color: var(--bg-color);
        font-family: 'Inter', sans-serif;
        color: var(--text-primary);
    }
    
    h1, h2, h3 { color: #FFFFFF !important; }
    p, span, div { color: var(--text-primary); }
    
    /* 2. Sidebar Fixes (Contrast) */
    section[data-testid="stSidebar"] {
        background-color: var(--bg-sidebar); 
        border-right: 1px solid var(--border-color);
    }
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3, 
    section[data-testid="stSidebar"] span, 
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label {
        color: #E0E0E0 !important; /* Force Light Text */
    }
    /* Fix Radio Buttons in Sidebar */
    .stRadio label {
        color: #E0E0E0 !important;
    }

    /* 3. Helper Classes */
    .kpi-container {
        display: flex;
        gap: var(--spacing-md);
        margin-bottom: var(--spacing-lg);
        background-color: var(--bg-secondary);
        padding: var(--spacing-md);
        border-radius: 8px;
        border: 1px solid var(--border-color);
    }
    .kpi-card {
        flex: 1;
        padding: var(--spacing-md);
        background: rgba(255, 255, 255, 0.03);
        border-radius: 6px;
        border-left: 3px solid var(--accent-primary);
    }
    .kpi-card h3 { color: var(--accent-primary) !important; font-size: 0.9rem !important; text-transform: uppercase; margin: 0 0 4px 0; }
    .kpi-card .value { font-size: 1.8rem; font-weight: 700; color: #FFFFFF; }

    .filter-bar {
        background-color: var(--bg-secondary);
        padding: var(--spacing-md);
        border-radius: 8px;
        margin-bottom: var(--spacing-lg);
        border: 1px solid var(--border-color);
    }
    .filter-chip {
        display: inline-flex;
        align-items: center;
        background-color: rgba(76, 172, 188, 0.15);
        color: var(--accent-primary);
        padding: 4px 12px;
        border-radius: 16px;
        font-size: 0.85rem;
        margin-right: 8px;
        border: 1px solid rgba(76, 172, 188, 0.3);
    }

    /* 4. Card Component (Integrated) */
    .signal-card {
        background-color: var(--bg-secondary);
        border: 1px solid var(--border-color);
        /* Top Radius Only */
        border-top-left-radius: 10px;
        border-top-right-radius: 10px;
        border-bottom: none; /* Connect to button */
        
        padding: 0;
        margin-bottom: 0px; /* No margin bottom, button attaches here */
        display: flex;
        flex-direction: column;
        height: 380px; /* Fixed height for body */
        overflow: hidden;
    }
    
    .card-header {
        padding: var(--spacing-md);
        border-bottom: 1px solid rgba(255,255,255,0.05);
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        background: linear-gradient(180deg, rgba(255,255,255,0.02) 0%, rgba(255,255,255,0) 100%);
    }
    .card-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #FFFFFF;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
        line-height: 1.4;
    }
    .importance-badge {
        padding: 2px 8px;
        border-radius: 4px;
        font-weight: 700;
        font-size: 0.85rem;
        color: #121212;
        min-width: 32px;
        text-align: center;
    }
    .card-body { padding: var(--spacing-md); flex: 1; }
    .quote-box {
        background-color: rgba(255,255,255,0.03);
        padding: 12px;
        border-left: 2px solid var(--text-secondary);
        margin-top: 12px;
        font-style: italic;
        color: var(--text-primary);
        font-size: 0.9rem;
        display: -webkit-box;
        -webkit-line-clamp: 3;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }
    .card-footer {
        padding: 12px 16px;
        background-color: rgba(0,0,0,0.2);
        min-height: 48px;
    }
    .tag {
        display: inline-block;
        padding: 2px 8px;
        border-radius: 12px;
        background-color: rgba(255,255,255,0.1);
        color: var(--text-secondary);
        font-size: 0.75rem;
        margin-right: 4px;
    }

    /* 5. Pagination Buttons & Inputs */
    /* Ensure visible text on buttons - Default Streamlit buttons are often transparent or white in dark mode. */
    .stButton button {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        color: #FFFFFF !important;
    }
    .stButton button:hover {
        background-color: rgba(255, 255, 255, 0.2) !important;
        border-color: #FFFFFF !important;
    }
    
    /* Specific fix for "Next/Prev" buttons if they use icons */
    /* Target ALL content inside the button to be white */
    div[data-testid="stColumn"] button * {
        fill: #FFFFFF !important;
        stroke: #FFFFFF !important;
        color: #FFFFFF !important;
    }
    
    /* 6. Card Action Button (Integrated Look) */
    /* This targets the 'View Details' button container to merge with card */
    div[data-testid="column"] .stButton button {
        width: 100%;
        border-top-left-radius: 0 !important;
        border-top-right-radius: 0 !important;
        border-top: none !important;
        background-color: rgba(255, 255, 255, 0.05) !important; /* Slightly lighter than card */
        text-transform: uppercase;
        letter-spacing: 1px;
        font-size: 0.8rem !important;
    }
    div[data-testid="column"] .stButton button:hover {
        background-color: var(--accent-primary) !important;
        color: #121212 !important; /* Dark text on Hover */
        border-color: var(--accent-primary) !important;
    }
    
    /* 7. Streamlit Overrides */
    .stTextInput input, .stSelectbox, .stMultiSelect { color: white !important; }
    div[data-testid="stExpander"] {
        background-color: var(--bg-secondary) !important;
        border: 1px solid var(--border-color) !important;
    }
    
    /* 8. Dialog / Modal Styling */
    div[data-testid="stDialog"] > div {
        background-color: #1E1E1E !important;
        color: #E0E0E0 !important;
        border: 1px solid #333 !important;
    }
    div[data-testid="stDialog"] h1, div[data-testid="stDialog"] h2, div[data-testid="stDialog"] h3, div[data-testid="stDialog"] p {
        color: #E0E0E0 !important;
    }
    button[aria-label="Close"] {
        color: #FFFFFF !important;
    }
</style>
"""

def apply_styles():
    st.markdown(load_css(), unsafe_allow_html=True)
