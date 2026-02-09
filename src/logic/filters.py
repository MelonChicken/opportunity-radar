import pandas as pd
import streamlit as st

@st.cache_data(ttl=60)  # Cache for 60 seconds for real-time filter performance
def filter_dataframe(df: pd.DataFrame, search_query: str, selected_industries: list, selected_techs: list, score_range: tuple, date_range: tuple = None) -> pd.DataFrame:
    """
    Filters the cards dataframe based on search query, industries, technologies, score, and date range.
    """
    if df.empty:
        return df

    filtered_df = df.copy()

    # 1. Search Filter
    if search_query:
        query = search_query.lower()
        # Check against multiple fields including Korean ones if available
        # Using a list of potential columns to check safely
        search_cols = [
            'attack_vector', 'pain_mechanism', 'pain_holder',
            'attack_vector_ko', 'pain_mechanism_ko', 'pain_holder_ko',
            'industry_tags', 'technology_tags' # Added tags to search scope
        ]
        
        # Create a boolean mask initialized to False
        mask = pd.Series([False] * len(filtered_df), index=filtered_df.index)
        
        for col in search_cols:
            if col in filtered_df.columns:
                # Handle list columns (tags) by joining them into strings first
                if col in ['industry_tags', 'technology_tags']:
                     mask |= filtered_df[col].apply(lambda x: query in " ".join(x).lower() if isinstance(x, list) else query in str(x).lower())
                else:
                     mask |= filtered_df[col].str.lower().str.contains(query, na=False)
        
        filtered_df = filtered_df[mask]

    # 2. Category Filters (OR logic within category, AND logic between categories)
    if selected_industries:
        # Check if ANY of the selected industries are present in the row's list
        filtered_df = filtered_df[filtered_df['industry_tags'].apply(
            lambda x: any(i in x for i in selected_industries) if isinstance(x, list) else False
        )]
        
    if selected_techs:
        # Check if ANY of the selected techs are present in the row's list
        filtered_df = filtered_df[filtered_df['technology_tags'].apply(
            lambda x: any(t in x for t in selected_techs) if isinstance(x, list) else False
        )]
        
    # 3. Score Range Filter
    if score_range:
        min_s, max_s = score_range
        if 'importance_score' in filtered_df.columns:
            filtered_df = filtered_df[
                (filtered_df['importance_score'] >= min_s) & 
                (filtered_df['importance_score'] <= max_s)
            ]
            
    # 4. Date Range Filter (Task 3.1)
    if date_range and len(date_range) == 2 and 'created_at' in filtered_df.columns:
        start_date, end_date = date_range
        # Ensure created_at is datetime
        if not pd.api.types.is_datetime64_any_dtype(filtered_df['created_at']):
             try:
                filtered_df['created_at'] = pd.to_datetime(filtered_df['created_at'])
             except:
                pass # Skip if conversion fails
        
        # Convert start/end to timestamp for comparison (normalize to midnight if needed, but simple comparison works for dates)
        start_ts = pd.Timestamp(start_date)
        end_ts = pd.Timestamp(end_date) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1) # Include full end day
        
        filtered_df = filtered_df[
            (filtered_df['created_at'] >= start_ts) & 
            (filtered_df['created_at'] <= end_ts)
        ]
        
    return filtered_df

def sort_dataframe(df: pd.DataFrame, sort_option: str, T: dict) -> pd.DataFrame:
    """
    Sorts the dataframe based on the selected option.
    T is the translation dictionary to match sort option strings.
    """
    if df.empty:
        return df
        
    sorted_df = df.copy()
    
    if sort_option == T.get("Sort_Newest", "Sort_Newest"):
         if 'created_at' in sorted_df.columns:
             sorted_df = sorted_df.sort_values(by=["created_at", "importance_score"], ascending=[False, False])
         else:
             sorted_df = sorted_df.sort_values(by="importance_score", ascending=False)
             
    elif sort_option == T.get("Sort_Score", "Sort_Score"):
         sorted_df = sorted_df.sort_values(by="importance_score", ascending=False)
         
    return sorted_df

def get_virtual_window(df: pd.DataFrame, scroll_index: int, window_size: int = 20):
    """
    Returns a subset of dataframe for virtual scrolling (infinite scroll performance optimization).
    
    Args:
        df: The full filtered dataframe
        scroll_index: Current scroll position index
        window_size: Number of items to render simultaneously (default: 20)
    
    Returns:
        Tuple of (windowed_df, start_idx, end_idx, total_items)
    """
    total_items = len(df)
    
    if total_items == 0:
        return df, 0, 0, 0
    
    # Center the window around scroll_index
    half_window = window_size // 2
    start_idx = max(0, scroll_index - half_window)
    end_idx = min(total_items, start_idx + window_size)
    
    # Adjust start if we're at the end
    if end_idx - start_idx < window_size and total_items >= window_size:
        start_idx = max(0, end_idx - window_size)
    
    window_df = df.iloc[start_idx:end_idx]
    
    return window_df, start_idx, end_idx, total_items


def paginate_dataframe(df: pd.DataFrame, current_page: int, items_per_page: int):
    """
    DEPRECATED: Use get_virtual_window() for infinite scroll instead.
    Returns the subset of dataframe for the current page and pagination metadata.
    """
    total_items = len(df)
    total_pages = max(1, (total_items + items_per_page - 1) // items_per_page)
    
    # Ensure current_page is valid
    current_page = max(1, min(current_page, total_pages))
    
    p_start = (current_page - 1) * items_per_page
    p_end = p_start + items_per_page
    
    page_df = df.iloc[p_start:p_end]
    
    return page_df, total_pages, p_start, p_end
