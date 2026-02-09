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
        
        /* Primary Blue Palette */
        --primary-50: #EFF6FF;
        --primary-100: #DBEAFE;
        --primary-500: #3B82F6;
        --primary-600: #2563EB;
        --primary-700: #1D4ED8;
        
        /* Accents (Direct values, no nesting) */
        --accent-primary: #2563EB;
        --accent-hover: #1D4ED8;
        --accent-light: #EFF6FF;
        
        /* Semantic Button Colors (Direct values for reliability) */
        --btn-primary-bg: #2563EB;
        --btn-primary-hover: #1D4ED8;
        --btn-primary-text: #FFFFFF;
        --btn-secondary-bg: #F8FAFC;
        --btn-secondary-hover: #E5E7EB;
        --btn-secondary-text: #020617;
        --btn-secondary-border: rgba(148, 163, 184, 0.35);
        
        
        /* Chip/Badge Colors (Direct values for consistency) */
        --chip-bg: #EFF6FF;
        --chip-text: #2563EB;
        --chip-border: #BFDBFE;
        --chip-hover-bg: #2563EB;
        --chip-hover-text: #FFFFFF;
        
        /* Borders */
        --border-color: #E2E8F0;
        
        /* Semantic Status */
        --color-critical: #EF4444;
        --color-warning: #F59E0B;
        --color-success: #10B981;
        --color-neutral: #9CA3AF;
        
        /* Shadows */
        --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        --shadow-chip: 0 2px 8px rgba(37, 99, 235, 0.15);
        --shadow-chip-hover: 0 4px 12px rgba(37, 99, 235, 0.25);
        
        /* Spacing */
        --radius-md: 12px;
        --radius-sm: 8px;
        --radius-full: 9999px;
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
"""
