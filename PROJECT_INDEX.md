"""
PROJECT_INDEX.md - Complete Project Reference
"""

# CrewAI Web Scraper - Project Index & File Reference

## 📂 Complete File Structure

```
crew-AI-agents/
│
├── 📋 DOCUMENTATION FILES
│   ├── README.md                    # Main project documentation
│   ├── SETUP.md                     # Detailed setup and installation guide
│   ├── QUICK_START.md              # Quick reference and cheat sheet
│   ├── ARCHITECTURE.md             # Technical architecture details
│   └── PROJECT_INDEX.md            # This file
│
├── 🔧 CONFIGURATION FILES
│   ├── config.py                   # Configuration management
│   ├── .env.example                # Environment variables template
│   ├── .gitignore                  # Git ignore rules
│   └── requirements.txt            # Python dependencies
│
├── 🎯 MAIN APPLICATION
│   ├── main.py                     # Application entry point
│   │   └── WebScraperApp class
│   │       - Interactive UI
│   │       - CLI argument handling
│   │       - Result display
│   │       - JSON export
│   │
│   ├── example_usage.py            # Working example script
│   │   └── Demonstrates all features
│   │
│   └── agents/
│       ├── __init__.py
│       └── scrapper_agent.py       # CrewAI agent configuration
│           └── WebScrapingCrew class
│               - Agent definition
│               - Task creation
│               - Pipeline orchestration
│
├── 🛠️ UTILITY MODULES (utils/)
│   ├── __init__.py
│   ├── web_scraper.py              # Web scraping logic
│   │   └── WebScraper class
│   │       - URL validation
│   │       - HTML fetching
│   │       - Content parsing
│   │       - Pattern extraction
│   │       - Multi-page scraping
│   │
│   ├── data_extractor.py           # Data extraction & structuring
│   │   └── DataExtractor class
│   │       - Service extraction
│   │       - Contact extraction
│   │       - Person identification
│   │       - JSON structuring
│   │
│   └── llm_handler.py              # LLM integration
│       └── LLMHandler class
│           - Content summarization
│           - Service extraction
│           - Data cleaning
│           - Error handling
│
└── 📊 GENERATED OUTPUTS
    ├── scraper.log                 # Application logs (auto-generated)
    ├── extraction_results.json     # Sample output file
    └── example_output.json         # Example script output
```

## 📄 File Descriptions & Quick Links

### Documentation

| File | Purpose | Key Sections |
|------|---------|--------------|
| [README.md](README.md) | **Main guide** - Features, usage, API reference | Features, Quick Start, Output Format, Troubleshooting |
| [SETUP.md](SETUP.md) | **Installation guide** - Prerequisites to production | Installation, Configuration, Verification, Advanced Setup |
| [QUICK_START.md](QUICK_START.md) | **Quick reference** - Common tasks and snippets | 5-Min Setup, Common Tasks, Code Examples, Quick Fixes |
| [ARCHITECTURE.md](ARCHITECTURE.md) | **Technical details** - System design and data flow | Architecture, Components, Data Flow, Security |
| [PROJECT_INDEX.md](PROJECT_INDEX.md) | **This file** - File reference and quick index | |

### Configuration Files

| File | Purpose |
|------|---------|
| [config.py](config.py) | Central configuration hub; loads environment variables, sets defaults |
| [.env.example](.env.example) | Template for environment variables; copy to `.env` and customize |
| [requirements.txt](requirements.txt) | Python package dependencies; install with `pip install -r requirements.txt` |
| [.gitignore](.gitignore) | Git ignore rules; prevents sensitive files from being tracked |

### Main Application

| File | Main Classes/Functions | Purpose |
|------|------------------------|---------|
| [main.py](main.py) | `WebScraperApp` | Application entry point with CLI and interactive modes |
| [example_usage.py](example_usage.py) | `main()` | Working examples demonstrating all features |
| [agents/scrapper_agent.py](agents/scrapper_agent.py) | `WebScrapingCrew` | CrewAI orchestration and agent definition |

### Utility Modules

| File | Main Classes | Public Methods |
|------|-------------|-----------------|
| [utils/web_scraper.py](utils/web_scraper.py) | `WebScraper` | `is_valid_url()`, `fetch_page()`, `parse_html()`, `extract_text()`, `extract_emails()`, `extract_phone_numbers()`, `extract_links()`, `scrape_website()` |
| [utils/data_extractor.py](utils/data_extractor.py) | `DataExtractor` | `extract_overview()`, `extract_services()`, `extract_addresses()`, `extract_people()`, `structure_data()`, `to_json()`, `to_dict()` |
| [utils/llm_handler.py](utils/llm_handler.py) | `LLMHandler` | `summarize_content()`, `extract_services()`, `clean_data()`, `validate_response()` |

## 🚀 Getting Started Paths

### Path 1: Quick Test (5 minutes)

```
1. Read: QUICK_START.md
2. Run: python main.py https://python.org
3. View: Output in terminal
4. Done!
```

### Path 2: Full Setup (30 minutes)

```
1. Read: README.md (overview)
2. Follow: SETUP.md (installation)
3. Run: example_usage.py
4. Test: python main.py (interactive mode)
5. Configure: Edit .env for your needs
```

### Path 3: Development (2 hours)

```
1. Study: ARCHITECTURE.md
2. Review: Source code in utils/
3. Modify: Create custom extractors
4. Test: Run example_usage.py
5. Deploy: See SETUP.md advanced section
```

### Path 4: Batch Processing

```
1. Review: Batch processing in QUICK_START.md
2. Implement: Custom script
3. Test: With few URLs first
4. Deploy: Implement rate limiting
5. Monitor: Check scraper.log
```

## 🔑 Key Classes & Usage

### WebScraper

```python
from utils.web_scraper import WebScraper

scraper = WebScraper()
data = scraper.scrape_website("https://example.com", max_pages=5)
```

### DataExtractor

```python
from utils.data_extractor import DataExtractor

extractor = DataExtractor()
structured = extractor.structure_data(scraped_data)
json_output = extractor.to_json()
```

### LLMHandler

```python
from utils.llm_handler import LLMHandler

llm = LLMHandler()
summary = llm.summarize_content(text)
services = llm.extract_services(text)
```

### WebScrapingCrew

```python
from agents.scrapper_agent import WebScrapingCrew

crew = WebScrapingCrew()
results = crew.scrape_and_extract(url="https://example.com")
```

### WebScraperApp

```python
from main import WebScraperApp

app = WebScraperApp()
app.run_interactive()  # Interactive mode
# OR
app.run_cli("https://example.com")  # CLI mode
```

## 🔄 Data Flow

```
User Input (URL)
    ↓
URL Validation (web_scraper.py)
    ↓
Fetch Content (requests + retry logic)
    ↓
Parse HTML (BeautifulSoup)
    ↓
Extract Information:
  - Text content
  - Emails/Phones/Addresses
  - Links
    ↓
Multi-page crawling (if applicable)
    ↓
LLM Processing (llm_handler.py):
  - Summarization
  - Service extraction
  - Data cleaning
    ↓
Data Structuring (data_extractor.py)
    ↓
JSON Output
    ↓
Display/Export/Save
```

## 🎯 Common Use Cases

### Use Case 1: Extract Business Emails

See: [QUICK_START.md - Extract Just Emails](QUICK_START.md#extract-just-emails)

### Use Case 2: Batch Scrape Multiple Sites

See: [QUICK_START.md - Scrape Multiple Websites](QUICK_START.md#scrape-multiple-websites)

### Use Case 3: Integrate with Python Application

See: [README.md - Programmatic API](README.md#programmatic-api)

### Use Case 4: Deploy to Production

See: [SETUP.md - Production Deployment](SETUP.md#production-deployment)

## 🛠️ Customization Guide

### Add Custom Extractor

1. Subclass `DataExtractor` in `utils/data_extractor.py`
2. Implement custom extraction methods
3. Use in `scrape_and_extract()` pipeline

### Change LLM Provider

1. Modify `LLMHandler` in `utils/llm_handler.py`
2. Implement provider-specific client
3. Update config with new API keys

### Add Database Storage

1. Create `utils/database.py`
2. Implement storage methods
3. Integrate in `scrape_and_extract()`

### Create REST API

1. Create `api.py` with FastAPI/Flask
2. Expose `WebScrapingCrew` as endpoints
3. Deploy with Gunicorn/Uvicorn

## 📋 Configuration Reference

### Environment Variables

```env
# API Configuration
OPENAI_API_KEY              # Your OpenAI API key (REQUIRED)
OPENAI_MODEL               # LLM model (default: gpt-3.5-turbo)

# Network Configuration
REQUEST_TIMEOUT            # HTTP timeout in seconds (default: 10)
MAX_RETRIES               # Retry attempts (default: 3)
RETRY_DELAY               # Delay between retries (default: 2)

# Advanced Features
USE_SELENIUM              # Enable browser automation (default: False)
SELENIUM_HEADLESS         # Headless mode (default: True)

# Output Configuration
OUTPUT_JSON_INDENT        # JSON formatting (default: 2)
```

See [.env.example](.env.example) for complete list.

## 🧪 Testing & Examples

### Quick Test

```bash
python main.py https://python.org
```

### Full Example

```bash
python example_usage.py
```

### Interactive Mode

```bash
python main.py
```

## 🐛 Debugging

1. **Check Logs**: `tail -f scraper.log`
2. **Enable Debug Mode**: Change logging level in `main.py`
3. **Test URL**: Use `https://example.com`
4. **Test Config**: `python -c "from config import *"`
5. **Test Import**: `python -c "from agents.scrapper_agent import WebScrapingCrew"`

## 📚 Additional Resources

- [CrewAI Documentation](https://docs.crewai.com/)
- [BeautifulSoup Docs](https://www.crummy.com/software/BeautifulSoup/)
- [OpenAI API Reference](https://platform.openai.com/docs/)
- [Python Requests Guide](https://requests.readthedocs.io/)

## ✅ Checklist for First Use

- [ ] Python 3.8+ installed
- [ ] Repository cloned
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file created with API key
- [ ] Configuration tested (`python -c "from config import *"`)
- [ ] Example run successful (`python example_usage.py`)
- [ ] First URL scraped successfully (`python main.py [url]`)

---

**File Last Updated:** March 28, 2026  
**Project Version:** 1.0.0  
**Python Version:** 3.8+  
**CrewAI Version:** 0.28.0+
