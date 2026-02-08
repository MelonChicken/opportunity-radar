"""
Dialogs CSS module: Modal and dialog styling
"""

def load_dialogs_css():
    return """
    /* Dialog Container */
    div[data-testid="stDialog"] div[role="dialog"] {
        background-color: #FFFFFF !important;
        color: #111827 !important;
        border: 1px solid #E2E8F0 !important;
    }
    
    /* Dialog Text Colors */
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
    
    /* Code Block Override (Must come after dialog text rules) */
    div[data-testid="stDialog"] [data-testid="stCodeBlock"],
    div[data-testid="stDialog"] [data-testid="stCodeBlock"] code,
    div[data-testid="stDialog"] [data-testid="stCodeBlock"] pre,
    div[data-testid="stDialog"] [data-testid="stCodeBlock"] p,
    div[data-testid="stDialog"] [data-testid="stCodeBlock"] span,
    div[data-testid="stDialog"] [data-testid="stCodeBlock"] div {
        background-color: #0F172A !important;
        color: #F8FAFC !important;
        -webkit-text-fill-color: #F8FAFC !important;
    }

    /* Dialog Buttons */
    div[data-testid="stDialog"] button[aria-label="Close"] {
        color: #64748B !important; 
    }
    div[data-testid="stDialog"] a[role="button"],
    div[data-testid="stDialog"] button:not([aria-label="Close"]) {
         color: initial !important;
    }
    div[data-testid="stDialog"] button p {
         color: inherit !important;
    }
"""
