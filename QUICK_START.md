"""
QUICK_START.md - Quick Reference & Common Commands
"""

# CrewAI Web Scraper - Quick Start Guide

## 🚀 5-Minute Setup

```bash
# 1. Clone and navigate
git clone https://github.com/Akshita1220174/crew-AI-agents.git
cd crew-AI-agents

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure
cp .env.example .env
# Edit .env and add your OpenAI API key

# 5. Run
python main.py
```

## 📖 Basic Usage

### Interactive Mode (Recommended for First-Time Users)

```bash
python main.py
```

**Then:**
1. Enter website URL (e.g., https://example.com)
2. Wait for processing
3. View results
4. Choose to export as JSON

### Command-Line Mode (One-Off Scraping)

```bash
python main.py https://example.com
```

Results will print to console.

### Programmatic Usage

```python
from agents.scrapper_agent import WebScrapingCrew

crew = WebScrapingCrew()
results = crew.scrape_and_extract(url="https://example.com", max_pages=5)

if results['success']:
    data = results['data']
    print(data['overview'])
    print(data['contacts']['emails'])
```

## 🎯 Common Tasks

### Scrape a Single Website

```bash
python main.py https://www.example.com
```

### Scrape Multiple Websites

```bash
# Create a script: batch_scrape.py
import json
from agents.scrapper_agent import WebScrapingCrew

urls = [
    "https://site1.com",
    "https://site2.com",
    "https://site3.com"
]

crew = WebScrapingCrew()
results = []

for url in urls:
    result = crew.scrape_and_extract(url=url, max_pages=3)
    results.append({url: result['data']})

# Save all results
with open('batch_results.json', 'w') as f:
    json.dump(results, f, indent=2)
```

### Export Results to JSON

```bash
python main.py https://example.com
# Then choose "yes" when asked to export
```

Or programmatically:

```python
import json
from agents.scrapper_agent import WebScrapingCrew

crew = WebScrapingCrew()
results = crew.scrape_and_extract(url="https://example.com")

with open('results.json', 'w') as f:
    json.dump(results['data'], f, indent=2)
```

### Extract Just Emails

```python
from agents.scrapper_agent import WebScrapingCrew

crew = WebScrapingCrew()
results = crew.scrape_and_extract(url="https://example.com")

emails = results['data']['contacts']['emails']
for email in emails:
    print(email)
```

### Extract Just Contact Information

```python
from agents.scrapper_agent import WebScrapingCrew

crew = WebScrapingCrew()
results = crew.scrape_and_extract(url="https://example.com")

contacts = results['data']['contacts']
print(f"Emails: {contacts['emails']}")
print(f"Phones: {contacts['phones']}")
print(f"Addresses: {contacts['addresses']}")
```

### View Application Logs

```bash
# Real-time log viewing
tail -f scraper.log  # macOS/Linux

# Windows PowerShell
Get-Content -Tail 20 -Wait scraper.log
```

## ⚙️ Configuration Quick Reference

### .env File Essentials

```env
# REQUIRED
OPENAI_API_KEY=your_key_here

# OPTIONAL (Defaults shown)
OPENAI_MODEL=gpt-3.5-turbo
REQUEST_TIMEOUT=10
MAX_RETRIES=3
RETRY_DELAY=2
USE_SELENIUM=False
SELENIUM_HEADLESS=True
OUTPUT_JSON_INDENT=2
```

### Adjusting Scraping Behavior

```env
# Faster scraping (less thorough)
REQUEST_TIMEOUT=5
MAX_RETRIES=1
RETRY_DELAY=0

# Thorough scraping (slower)
REQUEST_TIMEOUT=30
MAX_RETRIES=5
RETRY_DELAY=3
```

## 🐛 Quick Fixes

| Problem | Solution |
|---------|----------|
| "API key not set" | Add `OPENAI_API_KEY` to `.env` |
| Timeout errors | Increase `REQUEST_TIMEOUT` in `.env` |
| Module not found | `pip install -r requirements.txt` |
| No data extracted | Try different URL or increase `MAX_RETRIES` |
| SSL errors | Update certificates or use `verify=False` in code |

## 📊 Output Quick Reference

**JSON Structure:**

```json
{
  "overview": "string",
  "services": ["string", ...],
  "contacts": {
    "emails": ["string", ...],
    "phones": ["string", ...],
    "addresses": ["string", ...]
  },
  "people": [
    {"name": "string", "designation": "string"},
    ...
  ]
}
```

## 🔗 Useful URLs for Testing

```
https://python.org          - Well-structured
https://github.com         - Tech-focused
https://wikipedia.org      - Large content
https://example.com        - Minimal test
https://httpbin.org        - API testing
```

## 📚 Example Code Snippets

### Example 1: Basic Scraping

```python
from agents.scrapper_agent import WebScrapingCrew

crew = WebScrapingCrew()
result = crew.scrape_and_extract("https://example.com")

if result['success']:
    print("✓ Success")
    data = result['data']
else:
    print(f"✗ Error: {result['error']}")
```

### Example 2: Error Handling

```python
try:
    crew = WebScrapingCrew()
    result = crew.scrape_and_extract("https://example.com")
    
    if result['success']:
        data = result['data']
        # Process data
    else:
        print(f"Scraping failed: {result['error']}")
        
except Exception as e:
    print(f"Error: {str(e)}")
```

### Example 3: Using Individual Components

```python
from utils.web_scraper import WebScraper
from utils.data_extractor import DataExtractor
from utils.llm_handler import LLMHandler

# Initialize
scraper = WebScraper()
extractor = DataExtractor()
llm = LLMHandler()

# Scrape
data = scraper.scrape_website("https://example.com", max_pages=3)

# Extract
structured = extractor.structure_data(data)

# AI Processing (optional)
if scraped['pages']:
    summary = llm.summarize_content(data['pages'][0]['content'])
```

### Example 4: Batch Processing

```python
import json
from agents.scrapper_agent import WebScrapingCrew

urls = ["https://site1.com", "https://site2.com"]
crew = WebScrapingCrew()
results = {}

for url in urls:
    try:
        result = crew.scrape_and_extract(url)
        results[url] = result['data'] if result['success'] else str(result['error'])
    except Exception as e:
        results[url] = f"Error: {str(e)}"

with open('results.json', 'w') as f:
    json.dump(results, f, indent=2)

print(f"✓ Processed {len(results)} URLs")
```

## 🎓 Learning Resources

- [README.md](README.md) - Full documentation
- [SETUP.md](SETUP.md) - Detailed setup guide
- [ARCHITECTURE.md](ARCHITECTURE.md) - Technical details
- [example_usage.py](example_usage.py) - Working examples

## 🔐 Security Reminders

- ✅ Keep `.env` out of version control
- ✅ Use environment variables in production
- ✅ Don't share API keys
- ✅ Respect website terms of service
- ✅ Implement rate limiting for large-scale scraping

## 🚨 Common Mistakes to Avoid

1. **Forgetting .env configuration** → Add your API key first!
2. **Using inactive URLs** → Test with working URLs
3. **Exceeding rate limits** → Add delays between requests
4. **Storing sensitive data** → Never log API keys
5. **Ignoring robots.txt** → Check before large-scale scraping

## ⚡ Performance Tips

```python
# Fast (basic information)
crew.scrape_and_extract(url, max_pages=1)

# Balanced
crew.scrape_and_extract(url, max_pages=3)

# Comprehensive (slower)
crew.scrape_and_extract(url, max_pages=10)
```

## 📞 Still Need Help?

1. Check [Troubleshooting in SETUP.md](SETUP.md#troubleshooting)
2. Review logs: `tail -f scraper.log`
3. Test with example: `python example_usage.py`
4. Check configuration: `python -c "from config import *; print('Config OK')"`

---

**💡 Pro Tips:**
- Use interactive mode to test URLs before batch processing
- Export results as JSON for data pipeline integration
- Monitor scraper.log for API issues
- Test with example_usage.py before production use

**Updated**: March 28, 2026
