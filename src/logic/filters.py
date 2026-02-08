import pandas as pd

def filter_dataframe(df: pd.DataFrame, search_query: str, selected_industries: list, selected_techs: list, score_range: tuple) -> pd.DataFrame:
    """
    Filters the cards dataframe based on search query, industries, technologies, and score range.
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
            'attack_vector_ko', 'pain_mechanism_ko', 'pain_holder_ko'
        ]
        
        # Create a boolean mask initialized to False
        mask = pd.Series([False] * len(filtered_df), index=filtered_df.index)
        
        for col in search_cols:
            if col in filtered_df.columns:
                mask |= filtered_df[col].str.lower().str.contains(query, na=False)
        
        filtered_df = filtered_df[mask]

    # 2. Category Filters
    if selected_industries:
        # Assuming 'industry_tags' is a list of strings
        filtered_df = filtered_df[filtered_df['industry_tags'].apply(
            lambda x: any(i in x for i in selected_industries) if isinstance(x, list) else False
        )]
        
    if selected_techs:
        # Assuming 'technology_tags' is a list of strings
        filtered_df = filtered_df[filtered_df['technology_tags'].apply(
            lambda x: any(t in x for t in selected_techs) if isinstance(x, list) else False
        )]
        
    # 3. Score Range Filter
    if score_range:
        min_s, max_s = score_range
        filtered_df = filtered_df[
            (filtered_df['importance_score'] >= min_s) & 
            (filtered_df['importance_score'] <= max_s)
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

def paginate_dataframe(df: pd.DataFrame, current_page: int, items_per_page: int):
    """
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
