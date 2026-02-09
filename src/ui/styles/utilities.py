"""
Utilities CSS module: Common utility classes for spacing, flexbox, text
"""

def load_utilities_css():
    return """
    /* Text Utilities */
    .text-center { text-align: center; }
    .text-secondary { color: var(--text-secondary); }
    .text-bold { font-weight: 600; }
    .text-sm { font-size: 0.875rem; }
    .text-xs { font-size: 0.75rem; }
    
    /* Spacing Utilities */
    .mb-8 { margin-bottom: 8px; }
    .mb-12 { margin-bottom: 12px; }
    .mb-16 { margin-bottom: 16px; }
    .mb-20 { margin-bottom: 20px; }
    .mb-24 { margin-bottom: 24px; }
    .mb-32 { margin-bottom: 32px; }
    .mt-20 { margin-top: 20px; }
    .p-24 { padding: 24px; }
    
    /* Flexbox Utilities */
    .flex { display: flex; }
    .flex-center {
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .flex-between {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .flex-col {
        display: flex;
        flex-direction: column;
    }
    .gap-8 { gap: 8px; }
    .gap-10 { gap: 10px; }
    .gap-12 { gap: 12px; }
    
    /* Empty State */
    .empty-state {
        text-align: center;
        padding: 40px;
        background: #F8FAFC;
        border-radius: 12px;
        border: 1px dashed #CBD5E1;
    }
    .empty-state-icon {
        font-size: 2rem;
        margin-bottom: 10px;
    }
    .empty-state-title {
        color: #64748B;
    }
    .empty-state-text {
        color: #94A3B8;
    }
"""
