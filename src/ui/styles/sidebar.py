"""
Sidebar CSS module: Dark theme sidebar navigation
"""

def load_sidebar_css():
    return """
    /* Sidebar Styling (Dark Theme Override) */
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
        color: #94A3B8 !important;
        text-align: left !important;
        padding-left: 0px !important;
        box-shadow: none !important;
        font-weight: 500 !important;
        display: flex !important;
        justify-content: flex-start !important;
        align-items: center !important;
        width: 100% !important;
    }
    section[data-testid="stSidebar"] .stButton button:hover {
        background-color: rgba(255,255,255,0.05) !important;
        color: #F1F5F9 !important;
        border: none !important;
    }
    section[data-testid="stSidebar"] .stButton {
        margin-bottom: 4px;
    }
"""
