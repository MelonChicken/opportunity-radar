
import feedparser
import sys
import requests
import io

RSS_URL = "https://feeds.feedburner.com/GlobalPressRoom"

def test_feed():
    print(f"Testing URL: {RSS_URL}")
    
    # Test 1: Direct feedparser
    print("\n--- Test 1: Direct feedparser.parse ---")
    feed = feedparser.parse(RSS_URL)
    print(f"Status: {getattr(feed, 'status', 'Unknown')}")
    print(f"Bozo: {feed.bozo}")
    if feed.bozo:
        print(f"Bozo Exception: {feed.bozo_exception}")
    print(f"Entries found: {len(feed.entries)}")
    
    if len(feed.entries) > 0:
        print(f"  -> First Entry Keys: {feed.entries[0].keys()}")
        print(f"  -> First Entry Link: {feed.entries[0].get('link')}")
    
    if len(feed.entries) == 0:
        print("  -> FAILED to find entries directly.")

    # Test 2: Requests + feedparser
    print("\n--- Test 2: Requests User-Agent + feedparser ---")
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(RSS_URL, headers=headers, timeout=10)
        print(f"Response Code: {response.status_code}")
        
        feed2 = feedparser.parse(io.BytesIO(response.content))
        print(f"Entries found: {len(feed2.entries)}")
        
        if len(feed2.entries) > 0:
            print("  -> SUCCESS with Requests + User-Agent")
            print(f"  -> Title of first entry: {feed2.entries[0].title}")
    except Exception as e:
        print(f"Requests failed: {e}")

if __name__ == "__main__":
    test_feed()
