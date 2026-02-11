"""
Dialogs CSS module: Modal and dialog styling
"""

def load_dialogs_css():
    return """
    /* ============================================
       BACKDROP OVERLAY FIX - Full Viewport Coverage
       ============================================ */
    
    /* Force dialog container to cover full viewport */
    section[data-testid="stDialog"] {
        position: fixed !important;
        inset: 0 !important;
        width: 100vw !important;
        height: 100vh !important;
        z-index: 999 !important;
    }
    
    /* Streamlit's backdrop overlay layer (usually first child) */
    section[data-testid="stDialog"] > div:first-child,
    div[data-testid="stDialog"] > div:first-child,
    section[data-testid="stDialog"] > div[style*="background"],
    div[data-testid="stDialog"] > div[style*="background"] {
        position: fixed !important;
        inset: 0 !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        bottom: 0 !important;
        width: 100vw !important;
        height: 100vh !important;
        background-color: rgba(0, 0, 0, 0.6) !important;
        z-index: 998 !important;
    }
    
    /* Modal content box - ensure proper stacking */
    section[data-testid="stDialog"] div[role="dialog"],
    div[data-testid="stDialog"] div[role="dialog"] {
        position: relative !important;
        z-index: 1000 !important;
        max-width: 1200px !important;
        margin: auto !important;
        background-color: #FFFFFF !important;
        color: #111827 !important;
        border: 1px solid #E2E8F0 !important;
    }
    
    /* Dialog Text Colors - exclude buttons */
    div[data-testid="stDialog"] h1, 
    div[data-testid="stDialog"] h2, 
    div[data-testid="stDialog"] h3, 
    div[data-testid="stDialog"] li {
        color: #111827 !important;
    }
    
    /* Dialog text - exclude ALL button types AND entire prompt-section */
    div[data-testid="stDialog"] p:not(button p):not(.stButton p):not(.stLinkButton p):not(.stDownloadButton p):not(.prompt-section p):not(.prompt-section *),
    div[data-testid="stDialog"] span:not(button span):not(.stButton span):not(.stLinkButton span):not(.stDownloadButton span):not(.prompt-section span):not(.prompt-section *) {
        color: var(--text-primary) !important;
    }
    
    /* Prompt Section */
    .prompt-section {
        margin-bottom: 36px;
    }
    
    .prompt-header {
        font-size: 13px;
        font-weight: 700;
        color: var(--text-secondary) !important;
        margin-bottom: 10px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .prompt-container {
        position: relative;
        background-color: var(--bg-sidebar);
        border-radius: 10px;
        height: 180px;
        overflow-y: auto;
        overflow-x: hidden;
    }
    
    .prompt-text {
        margin: 0;
        padding: 52px 28px 24px 28px;
        background-color: var(--bg-sidebar) !important;
        color: #FFFFFF !important;
        font-family: ui-monospace, "Cascadia Code", "Consolas", monospace !important;
        font-size: 12px !important;
        line-height: 1.6 !important;
        white-space: pre-wrap !important;
        word-wrap: break-word !important;
    }
    
    /* Force white text in prompt with highest specificity - but exclude header */
    div[data-testid="stDialog"] .prompt-container,
    div[data-testid="stDialog"] .prompt-container *,
    div[data-testid="stDialog"] .prompt-text,
    div[data-testid="stDialog"] .prompt-text *,
    div[data-testid="stDialog"] pre.prompt-text {
        color: #FFFFFF !important;
    }
    
    .prompt-copy-btn {
        position: absolute;
        top: 8px;
        right: 8px;
        background-color: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: #FFFFFF !important;
        padding: 6px 10px;
        border-radius: 6px;
        font-size: 11px;
        cursor: pointer;
        transition: all 0.2s;
        z-index: 10;
    }
    
    .prompt-copy-btn:hover {
        background-color: rgba(255, 255, 255, 0.25);
    }
    
    /* Dialog Header with Score */
    .dialog-header {
        padding: 20px 24px;
        border-radius: 12px;
        margin-bottom: 24px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .dialog-header-left {
        flex: 1;
    }
    .dialog-header-title {
        font-size: 1.2rem;
        font-weight: 700;
        margin-bottom: 8px;
        color: var(--text-primary);
    }
    .dialog-header-subtitle {
        font-size: 0.95rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .dialog-score-badge {
        font-size: 2rem;
        font-weight: 800;
        padding: 12px 20px;
        border-radius: 12px;
    }
    .dialog-score-label {
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-top: 4px;
    }
    
    /* Dialog Layout - 60/40 Split */
    .dialog-columns {
        display: flex;
        gap: 24px;
    }
    .dialog-column-left {
        flex: 0 0 60%;
    }
    .dialog-column-right {
        flex: 0 0 40%;
    }
    
    /* Dialog Cards */
    .dialog-card {
        background: #FFFFFF;
        padding: 18px;
        border-radius: 10px;
        border: 1px solid #E2E8F0;
        margin-bottom: 16px;
    }
    .dialog-card-header {
        font-size: 13px;
        font-weight: 700;
        color: #64748B;
        margin-bottom: 10px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .dialog-card-content {
        color: #1E293B;
        font-size: 14px;
        line-height: 1.7;
    }
    .dialog-card-scrollable {
        max-height: 120px;
        overflow-y: auto;
        padding-right: 8px;
    }
    
    /* Prompt Card */
    .dialog-prompt-card {
        background: #0F172A;
        padding: 18px;
        border-radius: 10px;
        margin-bottom: 16px;
    }
    .dialog-prompt-header {
        font-size: 13px;
        font-weight: 700;
        color: #94A3B8;
        margin-bottom: 10px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .dialog-prompt-content {
        max-height: 150px;
        overflow-y: auto;
        padding-right: 8px;
    }
    .dialog-prompt-text {
        margin: 0;
        font-family: ui-monospace, "Cascadia Code", monospace;
        font-size: 12px;
        color: #F1F5F9;
        line-height: 1.6;
        white-space: pre-wrap;
        word-wrap: break-word;
        user-select: all;
        cursor: text;
    }
    
    /* Progress Bar */
    .progress-bar-wrapper {
        margin-bottom: 12px;
    }
    .progress-bar-label {
        display: flex;
        justify-content: space-between;
        font-size: 13px;
        font-weight: 600;
        color: #334155;
        margin-bottom: 6px;
    }
    .progress-bar-container {
        background: #E2E8F0;
        height: 6px;
        border-radius: 999px;
        overflow: hidden;
    }
    .progress-bar-fill {
        height: 100%;
        background: linear-gradient(90deg, #3B82F6, #2563EB);
    }
"""
