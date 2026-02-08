"""
Cards CSS module: KPI cards and signal cards
"""

def load_cards_css():
    return """
    /* KPI Cards (White + Shadow) */
    .kpi-container {
        display: flex;
        gap: 20px;
        margin-bottom: 32px;
    }
    .kpi-card {
        flex: 1;
        background-color: var(--bg-secondary);
        border: 1px solid var(--border-color);
        border-radius: var(--radius-md);
        padding: 24px;
        box-shadow: var(--shadow-sm);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .kpi-card h3 {
        color: var(--text-secondary) !important;
        font-size: 0.75rem !important;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin: 0 0 8px 0;
        font-weight: 600;
    }
    .kpi-card .value {
        font-size: 2.5rem;
        font-weight: 800;
        color: var(--text-primary);
        line-height: 1.1;
    }
    .kpi-card .sub-text {
        font-size: 0.85rem;
        color: var(--text-secondary);
        margin-top: 4px;
    }

    /* Signal Card (Premium Light Layout) */
    .signal-card {
        padding: 0px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        margin-bottom: 12px;
    }
    .signal-card:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-md);
    }
    
    /* Card Header: Tag + Score */
    .card-top {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 16px;
    }
    .category-tag {
        background-color: var(--accent-light);
        color: var(--accent-primary);
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        padding: 4px 8px;
        border-radius: 4px;
        letter-spacing: 0.05em;
    }
    .score-badge {
        background-color: var(--accent-light);
        color: var(--accent-primary);
        font-weight: 800;
        font-size: 0.9rem;
        min-width: 80px;
        height: 32px;
        padding: 0 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 16px;
        flex-shrink: 0;
        white-space: nowrap;
    }
    
    /* Card Content */
    .card-title {
        color: var(--text-primary);
        font-size: 1.1rem;
        font-weight: 700;
        line-height: 1.4;
        margin-bottom: 12px;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }
    .card-desc {
        color: var(--text-secondary);
        font-size: 0.9rem;
        line-height: 1.5;
        margin-bottom: 16px;
        display: -webkit-box;
        -webkit-line-clamp: 3;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }
    .card-meta {
        font-size: 0.8rem;
        color: var(--text-secondary);
        margin-bottom: 20px;
    }
    .card-meta strong {
        color: var(--text-primary);
    }
    
    /* Card Footer: Pills + Action */
    .card-footer {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-top: 16px;
        border-top: 1px solid var(--border-color);
    }
    .pill {
        display: inline-block;
        border: 1px solid var(--border-color);
        border-radius: 4px;
        padding: 2px 8px;
        font-size: 0.7rem;
        color: var(--text-secondary);
        background-color: #FAFAFA;
        margin-right: 4px;
    }
    .view-link {
        color: var(--accent-primary);
        font-size: 0.85rem;
        font-weight: 600;
        text-decoration: none;
        cursor: pointer;
    }
    .view-link:hover { 
        text-decoration: underline; 
    }
"""
