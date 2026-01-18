import requests
import io
from bs4 import BeautifulSoup
from pypdf import PdfReader

def parse_html_content(url: str) -> str:
    """
    Fetches HTML and extracts main content text using BeautifulSoup.
    """
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script, style, and navigation/footer elements
        for element in soup(["script", "style", "nav", "footer", "header", "aside", "form", "noscript", "iframe"]):
            element.extract()
            
        # Get text
        text = soup.get_text(separator=' ')
        return clean_text(text)
    except Exception as e:
        print(f"Error parsing HTML {url}: {e}")
        return ""

def parse_pdf_content(url: str) -> str:
    """
    Downloads PDF and extracts text using PyPDF.
    """
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        with io.BytesIO(response.content) as f:
            reader = PdfReader(f)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + " "
            return clean_text(text)
    except Exception as e:
        print(f"Error parsing PDF {url}: {e}")
        return ""

def clean_text(text: str) -> str:
    """
    Normalizes text (removes excess whitespace, noise).
    """
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = ' '.join(chunk for chunk in chunks if chunk)
    return text

