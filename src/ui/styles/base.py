"""
Base CSS module: Global variables, typography, and resets
"""

def load_base_css():
    return """
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Noto+Sans+KR:wght@400;500;600;700&display=swap');

    :root {
        /* Color Palette (Tailwind-like Slate & Blue) */
        
        /* Backgrounds */
        --bg-color: #F8F9FA;
        --bg-secondary: #FFFFFF;
        --bg-sidebar: #0F172A;
        
        /* Text */
        --text-primary: #111827;
        --text-secondary: #6B7280;
        --text-on-dark: #F3F4F6;
        
        /* Accents */
        --accent-primary: #2563EB;
        --accent-hover: #1D4ED8;
        --accent-light: #EFF6FF;
        
        /* Borders */
        --border-color: #E2E8F0;
        
        /* Semantic */
        --color-critical: #EF4444;
        --color-warning: #F59E0B;
        --color-success: #10B981;
        --color-neutral: #9CA3AF;
        
        /* Shadows */
        --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        
        /* Spacing */
        --radius-md: 12px;
        --radius-sm: 8px;
    }

    /* Global Typography & Reset */
    .stApp {
        background-color: var(--bg-color);
        font-family: 'Inter', 'Noto Sans KR', sans-serif;
        color: var(--text-primary);
    }
    
    h1, h2, h3, h4, h5 { 
        color: var(--text-primary) !important; 
        font-family: 'Inter', 'Noto Sans KR', sans-serif;
        font-weight: 700;
        letter-spacing: -0.02em;
    }
    
    p, span, div {
        color: var(--text-primary);
    }
"""
