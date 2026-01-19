# Research Radar 📡

**AI-Powered Market Intelligence Dashboard for Startups & Developers.**

Research Radar automatically monitors global research reports (e.g., PwC), uses LLMs to filter out "corporate fluff," and extracts concrete **business opportunities** and **technology gaps** relevant to startups.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://catch-opportunity.streamlit.app/)


## ✨ Key Features

- **🎯 Startup-Focused AI Filter**: 
  - Automatically discards generic macro-economic statements (e.g., "GDP is growing").
  - **Keeps & Scores** specific pain points, unmet needs, and operational inefficiencies (e.g., "Banks struggle with unstructured data").
- **🇰🇷 Full Korean Language Support**:
  - **Dual-Language UI**: One-click toggle between English and Korean.
  - **Content Translation**: AI automatically translates extracting signals (Summary, Evidence, Expected Value) and Report Metadata into Korean.
- **📊 Interactive Dashboard**:
  - **Smart Filters**: Filter opportunities by Industry, Technology tag, and Importance Score.
  - **Detail View**: Click any card to see full evidence, confidence score, and source links in a modal popup.
  - **Admin View**: Inspect "Discarded Signals" to verify what the AI is filtering out.
- **⚡ Real-time Ingestion**: 
  - Fetch RSS feeds, parse HTML/PDF, and generate insights on-demand.

## 🛠️ Tech Stack

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?logo=openai&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?logo=pandas&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-E92063?logo=pydantic&logoColor=white)

- **Frontend**: Streamlit (Python)
- **AI Core**: OpenAI GPT-3.5 Turbo (JSON Mode)
- **Data Engineering**: Feedparser, BeautifulSoup4, PyPDF
- **Data Validation**: Pydantic
- **Storage**: JSON (Lightweight MVP)

## 🚀 Getting Started

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/radar.git
cd radar

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Create a `.env` file in the root directory and add your OpenAI Key:

```ini
OPENAI_API_KEY=sk-your-api-key-here
```

### 3. Running the Dashboard

```bash
python -m streamlit run app.py
```
Visit `http://localhost:8501` in your browser.

---

## 🔄 Managing Data

### Reprocess & Translate All Data
If you want to re-run the AI extraction on **all** existing reports (e.g., to apply new filters or generate Korean translations for old data):

```bash
python reprocess_data.py
```

### Reset Data
To completely wipe all ingested data and start fresh:
```bash
python reset_data.py
```

## 📂 Project Structure

- `src/`: Core logic (Ingestion, Parsing, LLM, Models).
- `data/`: JSON storage for Reports and Opportunity Cards.
- `app.py`: Streamlit Dashboard entry point.
- `reprocess_data.py`: Script to batch-update existing data.

---
**Built for the "Agentic Coding" Project.**
