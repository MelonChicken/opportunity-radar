"""
Buttons CSS module: All button styles
"""

def load_buttons_css():
    return """
    /* Default Button Styling */
    .stButton button {
        background-color: var(--btn-secondary-bg) !important;
        border: 1px solid var(--btn-secondary-border) !important;
        color: var(--btn-secondary-text) !important;
        border-radius: 10px !important;
        padding: 0.5rem 1rem !important;
        font-size: 13px !important;
        font-weight: 600 !important;
        box-shadow: var(--shadow-sm) !important;
        transition: all 0.2s ease !important;
    }
    .stButton button:hover {
        background-color: var(--btn-secondary-hover) !important;
        border-color: var(--btn-secondary-border) !important;
        color: var(--btn-secondary-text) !important;
    }
    
    /* Primary Button (type="primary") */
    .stButton button[kind="primary"],
    .stButton button[data-baseweb="button"][kind="primary"] {
        background-color: var(--btn-primary-bg) !important;
        color: var(--btn-primary-text) !important;
        border: none !important;
    }
    .stButton button[kind="primary"]:hover,
    .stButton button[data-baseweb="button"][kind="primary"]:hover {
        background-color: var(--btn-primary-hover) !important;
        color: var(--btn-primary-text) !important;
    }
    
    /* Primary button text - force white color */
    .stButton button[kind="primary"] p,
    .stButton button[kind="primary"] span,
    .stButton button[data-baseweb="button"][kind="primary"] p,
    .stButton button[data-baseweb="button"][kind="primary"] span {
        color: var(--btn-primary-text) !important;
    }
    
    /* View Full Analysis Button */
    .view-full-analysis-btn button {
        width: 100% !important;
        background-color: var(--btn-secondary-bg) !important;
        border: 1px solid var(--btn-secondary-border) !important;
        color: var(--chip-text) !important;
        font-weight: 600 !important;
    }
    .view-full-analysis-btn button:hover {
        background-color: var(--chip-bg) !important;
        border-color: var(--chip-border) !important;
    }
    
    /* Custom RR Button */
    .rr-btn {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      background: var(--btn-secondary-bg);
      color: var(--btn-secondary-text) !important;
      border: 1px solid var(--btn-secondary-border);
      border-radius: 10px;
      padding: 10px 18px;
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
      text-decoration: none !important;
      transition: all 0.2s;
    }
    .rr-btn:hover {
      background: var(--btn-secondary-hover);
      border-color: var(--btn-secondary-border);
      color: var(--btn-secondary-text) !important;
    }
    
    
    /* Download Button - Secondary (default) */
    div[data-testid="stDownloadButton"] button {
      background-color: var(--btn-secondary-bg) !important;
      color: var(--btn-secondary-text) !important;
      border: 1px solid var(--btn-secondary-border) !important;
      border-radius: 10px !important;
      padding: 0.5rem 1rem !important;
      font-size: 13px !important;
      font-weight: 600 !important;
      transition: all 0.2s ease !important;
    }
    div[data-testid="stDownloadButton"] button:hover {
      background-color: var(--btn-secondary-hover) !important;
      border-color: var(--btn-secondary-border) !important;
      color: var(--btn-secondary-text) !important;
    }
    div[data-testid="stDownloadButton"] button p {
       color: var(--btn-secondary-text) !important;
    }
    
    /* Download Button - Primary */
    div[data-testid="stDownloadButton"] button[kind="primary"],
    div[data-testid="stDownloadButton"] button[data-kind="primary"] {
      background-color: var(--btn-primary-bg) !important;
      color: var(--btn-primary-text) !important;
      border: none !important;
    }
    div[data-testid="stDownloadButton"] button[kind="primary"]:hover,
    div[data-testid="stDownloadButton"] button[data-kind="primary"]:hover {
      background-color: var(--btn-primary-hover) !important;
    }
    div[data-testid="stDownloadButton"] button[kind="primary"] p,
    div[data-testid="stDownloadButton"] button[data-kind="primary"] p {
       color: var(--btn-primary-text) !important;
    }
    
    
    /* Link Button - Primary (using CSS variables) */
    div[data-testid="stLinkButton"] a,
    div[data-testid="stLinkButton"] > a,
    [data-testid="stLinkButton"] a {
      background-color: var(--btn-primary-bg) !important;
      color: var(--btn-primary-text) !important;
      border: none !important;
      border-radius: 10px !important;
      padding: 0.5rem 1rem !important;
      font-size: 13px !important;
      font-weight: 600 !important;
      text-decoration: none !important;
      transition: all 0.2s ease !important;
      display: inline-flex !important;
      align-items: center !important;
      justify-content: center !important;
    }
    
    /* All link states - force white text */
    div[data-testid="stLinkButton"] a:link,
    div[data-testid="stLinkButton"] a:visited,
    div[data-testid="stLinkButton"] a:active,
    [data-testid="stLinkButton"] a:link,
    [data-testid="stLinkButton"] a:visited,
    [data-testid="stLinkButton"] a:active {
      color: var(--btn-primary-text) !important;
    }
    
    div[data-testid="stLinkButton"] a:hover,
    [data-testid="stLinkButton"] a:hover {
      background-color: var(--btn-primary-hover) !important;
      color: var(--btn-primary-text) !important;
    }
    
    /* Force text color for all nested elements */
    div[data-testid="stLinkButton"] a *,
    div[data-testid="stLinkButton"] a p,
    div[data-testid="stLinkButton"] a span,
    div[data-testid="stLinkButton"] a div,
    [data-testid="stLinkButton"] a *,
    [data-testid="stLinkButton"] a p,
    [data-testid="stLinkButton"] a span,
    [data-testid="stLinkButton"] a div {
      color: var(--btn-primary-text) !important;
    }




"""
