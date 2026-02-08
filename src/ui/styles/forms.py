"""
Forms CSS module: Input fields, filters, and widget overrides
"""

def load_forms_css():
    return """
    /* Filter Bar */
    .filter-bar {
        margin-bottom: 24px;
        display: flex;
        align-items: center;
        gap: 16px;
    }
    
    /* Custom Input Styling */
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
        display: none !important;
    }
    
    /* Input Placeholder */
    div[data-testid="stTextInput"] input::placeholder {
        color: var(--text-secondary) !important;
        opacity: 1 !important;
        font-weight: 400;
    }
    div[data-testid="stTextInput"] input::-webkit-input-placeholder {
        color: var(--text-secondary) !important;
        opacity: 1 !important;
    }

    /* Multiselect & Selectbox */
    .stMultiSelect div[data-baseweb="select"], 
    .stSelectbox div[data-baseweb="select"] {
        background-color: var(--bg-secondary) !important;
        border-color: var(--border-color) !important;
        color: var(--text-primary) !important;
    }
    .stMultiSelect div[data-baseweb="select"] > div, 
    .stSelectbox div[data-baseweb="select"] > div {
        background-color: var(--bg-secondary) !important;
        color: var(--text-primary) !important;
    }
    
    /* Selected Tags */
    .stMultiSelect div[data-baseweb="tag"] {
        background-color: var(--accent-light) !important;
        color: var(--accent-primary) !important;
        border: 1px solid var(--accent-primary) !important;
    }
    .stMultiSelect div[data-baseweb="tag"] span {
        color: var(--accent-primary) !important;
    }
    
    /* Dropdown Popover */
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
    
    /* Dropdown Options */
    li[role="option"] {
        background-color: white !important;
        color: var(--text-primary) !important;
        display: flex !important;
        align-items: center !important;
    }
    li[role="option"] div, 
    li[role="option"] span {
        color: var(--text-primary) !important;
    }
    li[role="option"]:hover {
        background-color: var(--accent-light) !important;
    }
    li[role="option"]:hover * {
        background-color: transparent !important;
        color: var(--text-primary) !important;
    }
    li[role="option"][aria-selected="true"] {
         background-color: var(--accent-light) !important;
         color: var(--accent-primary) !important;
         font-weight: 600 !important;
    }
    li[role="option"][aria-selected="true"] * {
        color: var(--accent-primary) !important;
        background-color: transparent !important;
    }

    /* Select Box Placeholder */
    .stMultiSelect div[data-baseweb="select"] span, 
    .stSelectbox div[data-baseweb="select"] span,
    .stMultiSelect div[data-baseweb="select"] div, 
    .stSelectbox div[data-baseweb="select"] div {
        color: var(--text-secondary) !important;
        opacity: 1 !important;
        -webkit-text-fill-color: var(--text-secondary) !important;
    }
    
    /* Slider */
    div[data-testid="stSlider"] div[role="slider"] {
        background-color: var(--accent-primary) !important;
    }
    div[data-testid="stSlider"] div[data-baseweb="slider"] > div > div {
        background-color: var(--accent-primary) !important;
    }

    /* Expander */
    div[data-testid="stExpander"] {
        background-color: var(--bg-secondary) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: var(--radius-sm);
    }
"""
