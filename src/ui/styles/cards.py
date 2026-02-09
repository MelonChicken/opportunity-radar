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
    
    /* Phase 1: Responsive Grid Layout for Signal Cards */
    .signal-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 16px;
        margin-bottom: 24px;
    }
    
    /* Tablet: 2 columns */
    @media (max-width: 1200px) {
        .signal-grid {
            grid-template-columns: repeat(2, 1fr);
        }
    }
    
    /* Mobile: 1 column */
    @media (max-width: 768px) {
        .signal-grid {
            grid-template-columns: 1fr;
        }
    }
    
    /* Phase 1: Skeleton Loading Animation */
    .skeleton-card {
        background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
        background-size: 200% 100%;
        animation: skeleton-loading 1.5s ease-in-out infinite;
        border-radius: var(--radius-md);
        height: 180px;
        border: 1px solid var(--border-color);
    }
    
    @keyframes skeleton-loading {
        0% { background-position: 200% 0; }
        100% { background-position: -200% 0; }
    }
    
    /* Phase 1: Compact Card Height */
    .signal-card-compact {
        min-height: 180px;
        max-height: 200px;
    }
    
    /* Phase 1: Filter Chips */
    .active-filters {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin: 12px 0;
    }
    
    .filter-chip {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: #EFF6FF;
        color: #2563EB;
        border: 1px solid #BFDBFE;
        border-radius: 16px;
        padding: 6px 12px;
        font-size: 0.85rem;
        font-weight: 500;
    }
    
    .filter-chip button {
        background: none;
        border: none;
        color: #2563EB;
        font-size: 1.1rem;
        cursor: pointer;
        padding: 0;
        margin-left: 4px;
        line-height: 1;
        opacity: 0.7;
        transition: opacity 0.2s;
    }
    
    .filter-chip button:hover {
        opacity: 1;
    }
"""
