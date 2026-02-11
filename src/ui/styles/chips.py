"""
Chips CSS module: Styles for Streamlit pills (st.pills) components.
Rewritten from scratch for maximum specificity and dark-mode compatibility.
"""


def load_chips_css():
    return """
    /* ===========================================
       ST.PILLS CHIP STYLING — FROM SCRATCH
       Maximum specificity to override Streamlit theme
       =========================================== */

    /* --- UNSELECTED STATE --- */
    div[data-testid="stPills"] button {
        background-color: #EFF6FF !important;
        color: #2563EB !important;
        border: 1px solid #BFDBFE !important;
        border-radius: 9999px !important;
        padding: 0.35rem 1.0rem !important;
        font-family: "Inter", sans-serif !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        cursor: pointer !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 1px 2px 0 rgba(0,0,0,0.05) !important;
    }

    /* Force text color on ALL inner elements (unselected) */
    div[data-testid="stPills"] button p,
    div[data-testid="stPills"] button span,
    div[data-testid="stPills"] button div,
    div[data-testid="stPills"] button label,
    div[data-testid="stPills"] button * {
        color: #2563EB !important;
    }

    /* --- HOVER STATE --- */
    div[data-testid="stPills"] button:hover {
        background-color: #DBEAFE !important;
        color: #1D4ED8 !important;
        border-color: #93C5FD !important;
    }
    div[data-testid="stPills"] button:hover p,
    div[data-testid="stPills"] button:hover span,
    div[data-testid="stPills"] button:hover div,
    div[data-testid="stPills"] button:hover * {
        color: #1D4ED8 !important;
    }

    /* --- SELECTED STATE (aria-pressed) --- */
    div[data-testid="stPills"] button[aria-pressed="true"] {
        background-color: #2563EB !important;
        color: #FFFFFF !important;
        border: 1px solid #2563EB !important;
        box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.3) !important;
    }
    div[data-testid="stPills"] button[aria-pressed="true"] p,
    div[data-testid="stPills"] button[aria-pressed="true"] span,
    div[data-testid="stPills"] button[aria-pressed="true"] div,
    div[data-testid="stPills"] button[aria-pressed="true"] label,
    div[data-testid="stPills"] button[aria-pressed="true"] * {
        color: #FFFFFF !important;
    }

    /* --- SELECTED STATE (aria-checked fallback for some Streamlit versions) --- */
    div[data-testid="stPills"] button[aria-checked="true"] {
        background-color: #2563EB !important;
        color: #FFFFFF !important;
        border: 1px solid #2563EB !important;
    }
    div[data-testid="stPills"] button[aria-checked="true"] p,
    div[data-testid="stPills"] button[aria-checked="true"] span,
    div[data-testid="stPills"] button[aria-checked="true"] div,
    div[data-testid="stPills"] button[aria-checked="true"] * {
        color: #FFFFFF !important;
    }

    /* --- SELECTED STATE (data-active / data-selected fallback) --- */
    div[data-testid="stPills"] button[data-active="true"],
    div[data-testid="stPills"] button[data-selected="true"],
    div[data-testid="stPills"] button.st-emotion-cache-active {
        background-color: #2563EB !important;
        color: #FFFFFF !important;
        border: 1px solid #2563EB !important;
    }
    div[data-testid="stPills"] button[data-active="true"] *,
    div[data-testid="stPills"] button[data-selected="true"] *,
    div[data-testid="stPills"] button.st-emotion-cache-active * {
        color: #FFFFFF !important;
    }

    /* --- EMOJI / ICON SPACING --- */
    div[data-testid="stPills"] button span[role="img"] {
        margin-right: 6px !important;
    }

    /* --- LABEL ABOVE CHIPS --- */
    .chip-container-label {
        color: #64748B;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    """
