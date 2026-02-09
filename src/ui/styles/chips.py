"""
Chips CSS module: Specific styles for Streamlit pills and tag components
"""

def load_chips_css():
    return """
    /* ============================================
       STREAMLIT PILLS / CHIPS STYLING
       Targeting st.pills, st.segmented_control, st.radio
       ============================================ */
    
    /* 1. Safe Overrides for Wrapper Elements 
       NOTE: We do NOT use 'all: unset' to avoid breaking layout.
       Instead, we override specific properties with !important.
    */
    
    div[data-testid="stStack"] button,
    div[data-testid="stPills"] button,
    div[data-testid="stSegmentedControl"] button {
        /* Base Shape & Box Model */
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        box-sizing: border-box !important;
        margin: 0 !important;
        
        /* Typography */
        font-family: "Inter", sans-serif !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        line-height: 1.5 !important;
        text-transform: none !important;
        
        /* Visual Style (Unselected Default) */
        background-color: #EFF6FF !important; /* bg-blue-50 */
        color: #2563EB !important;           /* text-blue-600 */
        border: 1px solid #BFDBFE !important; /* border-blue-200 */
        border-radius: 9999px !important;     /* Pillow shape */
        padding: 0.35rem 1.0rem !important;
        
        /* Interactions */
        cursor: pointer !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05) !important;
    }

    /* 2. Hover State */
    div[data-testid="stStack"] button:hover,
    div[data-testid="stPills"] button:hover,
    div[data-testid="stSegmentedControl"] button:hover {
        background-color: #DBEAFE !important; /* bg-blue-100 */
        color: #1D4ED8 !important;            /* text-blue-700 */
        border-color: #3B82F6 !important;
        transform: translateY(-1px);
    }

    /* 3. Selected State (Active) */
    div[data-testid="stStack"] button[aria-pressed="true"],
    div[data-testid="stPills"] button[aria-pressed="true"],
    div[data-testid="stSegmentedControl"] button[aria-pressed="true"] {
        background-color: #2563EB !important; /* bg-blue-600 */
        color: #FFFFFF !important;            /* text-white */
        border: 1px solid #2563EB !important;
        box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.3) !important;
    }
    
    /* 4. Text Color Safeguard (Inner Spans/Paragraphs) */
    div[data-testid="stStack"] button p,
    div[data-testid="stStack"] button span,
    div[data-testid="stStack"] button div,
    div[data-testid="stPills"] button p,
    div[data-testid="stPills"] button span,
    div[data-testid="stPills"] button div,
    div[data-testid="stSegmentedControl"] button p,
    div[data-testid="stSegmentedControl"] button span {
        color: inherit !important;
        font-weight: inherit !important;
        font-family: inherit !important;
    }
    
    /* 5. Icon/Emoji Spacing (if present) */
    div[data-testid="stStack"] button span[role="img"],
    div[data-testid="stPills"] button span[role="img"] {
        margin-right: 6px !important;
    }
    
    /* 6. Chip Container Helper (for non-streamlit chips if needed) */
    .chip-container-label {
        color: #64748B; 
        font-size: 0.85rem; 
        font-weight: 600; 
        text-transform: uppercase; 
        letter-spacing: 0.05em;
    }
    """
