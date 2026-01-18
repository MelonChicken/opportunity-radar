import feedparser
from datetime import datetime
from typing import List, Tuple
from .models import Report, IngestionStatus
from .storage import load_reports, save_reports

# PwC Global Outlook RSS (Placeholder - using a generic one if specific one fails, but stick to the plan)
RSS_URL = "https://feeds.feedburner.com/GlobalPressRoom" 

def parse_date(date_str: str) -> datetime:
    try:
        # Common RSS date formats, feedparser usually handles this but returning struct_time
        # We'll rely on feedparser's parsed version if available
        return datetime.now() # Fallback, should use struct_time conversion
    except:
        return datetime.now()

import requests
import io

def fetch_rss_feed(url: str = RSS_URL) -> List[Report]:
    """
    Fetches new reports from RSS feed using requests (for User-Agent) + feedparser.
    Checks against existing URL in storage to prevent duplicates.
    """
    try:
        headers = {
             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        feed = feedparser.parse(io.BytesIO(response.content))
    except Exception as e:
        print(f"Error fetching RSS: {e}")
        return []

    print(f"DEBUG: Feed Status: {getattr(feed, 'status', 'Unknown')}, Entries: {len(feed.entries)}")
    
    existing_reports = load_reports()
    existing_urls = {r.url for r in existing_reports}
    
    new_reports = []
    
    for entry in feed.entries:
        link = entry.get("link", "")
        if link in existing_urls:
            continue
            
        # Convert published_parsed to datetime
        published_at = datetime.now()
        if hasattr(entry, "published_parsed") and entry.published_parsed:
             published_at = datetime(*entry.published_parsed[:6])
        
        report = Report(
            report_id=f"rep_{int(published_at.timestamp())}_{hash(link)}", # Simple ID generation
            title=entry.get("title", "No Title"),
            source="PwC",
            url=link,
            published_at=published_at,
            summary=entry.get("summary", ""),
            ingestion_status=IngestionStatus.PENDING
        )
        new_reports.append(report)
        existing_urls.add(link) # Avoid duplicates within the same fetch
        
    return new_reports

def ingest_new_reports() -> Tuple[int, int]:
    """
    Orchestrator to fetch and save new pending reports.
    Returns (num_newly_found, num_total_pending)
    """
    new_reports = fetch_rss_feed()
    all_reports = load_reports()
    
    if new_reports:
        all_reports.extend(new_reports)
        save_reports(all_reports)
        
    pending_count = sum(1 for r in all_reports if r.ingestion_status == IngestionStatus.PENDING)
    return len(new_reports), pending_count

