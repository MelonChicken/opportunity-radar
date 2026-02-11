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
    
    /* Sidebar Logo */
    .sidebar-logo {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 20px;
    }
    .sidebar-logo-icon {
        width: 32px;
        height: 32px;
        background-color: #2563EB;
        border-radius: 6px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
    }
    .sidebar-brand {
        font-weight: 700;
        color: white;
        font-size: 1.1rem;
    }
    .sidebar-tagline {
        font-size: 0.7rem;
        color: #6B7280;
    }
    
    /* Custom Sidebar Nav Items */
    .nav-active {
        background-color: var(--accent-primary);
        color: white !important;
        padding: 10px 16px;
        border-radius: 8px;
        font-weight: 600;
        margin-bottom: 4px;
        display: flex !important;  /* Force Flexbox */
        align-items: center;
        width: 100%;
        white-space: nowrap;       /* Prevent text wrapping */
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .nav-icon {
        display: flex;
        align-items: center;
        width: 20px;
        justify-content: center;
        flex-shrink: 0;            /* Prevent icon shrinking */
    }
    .nav-text {
        padding-top: 0;            /* Reset padding */
        margin-left: 12px;         /* Uniform spacing */
        white-space: nowrap;       /* Prevent text wrapping */
        overflow: hidden;
        text-overflow: ellipsis;
        line-height: 1.4;
    }
    
    /* Network Integration Badge */
    .network-integration {
        background: #1E293B;
        padding: 12px;
        border-radius: 8px;
        margin-top: 20px;
    }
    .network-header {
        font-size: 0.7rem;
        color: #6B7280;
        margin-bottom: 8px;
        font-weight: bold;
    }
    .network-badges {
        display: flex;
        gap: 8px;
    }
    .network-badge {
        background: #334155;
        padding: 2px 6px;
        border-radius: 4px;
        font-size: 0.65rem;
    }
    
    /* Sidebar Ghost Buttons (Inactive State) */
    section[data-testid="stSidebar"] .stButton button {
        background-color: transparent !important;
        border: none !important;
        color: #94A3B8 !important;
        text-align: left !important;
        padding: 10px 16px !important; /* Match active padding */
        box-shadow: none !important;
        font-weight: 500 !important;
        display: flex !important;
        justify-content: flex-start !important;
        align-items: center !important;
        width: 100% !important;
        white-space: nowrap !important; /* Prevent text wrapping */
        overflow: hidden !important;
        text-overflow: ellipsis !important;
        line-height: 1.4 !important;
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
