"""
Buttons CSS module: All button styles
"""

def load_buttons_css():
    return """
    /* Default Button Styling */
    .stButton button {
        background-color: var(--bg-secondary) !important;
        border: 1px solid var(--border-color) !important;
        color: var(--text-primary) !important;
        border-radius: 6px !important;
        box-shadow: var(--shadow-sm) !important;
    }
    .stButton button:hover {
        border-color: var(--accent-primary) !important;
        color: var(--accent-primary) !important;
        background-color: var(--accent-light) !important;
    }
    
    /* View Full Analysis Button */
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
    
    /* Primary Action Buttons */
    .btn-primary button {
        background-color: var(--accent-primary) !important;
        color: white !important;
        border: none !important;
    }

    /* Custom RR Button */
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
    
    /* Download Button */
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
"""
