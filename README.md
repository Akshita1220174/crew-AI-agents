# CrewAI Web Scraper - Intelligent Web Scraping & Information Extraction

A sophisticated Python project using **CrewAI** that builds an AI-powered agent capable of intelligent web scraping and structured data extraction from websites.

## 🎯 Features

- ✅ **Intelligent Web Scraping** - Fetches full website content with multi-page support
- ✅ **Structured Data Extraction** - Automatically extracts:
  - Website overview and purpose
  - Services/products offered
  - Contact information (emails, phones, addresses)
  - Team member details (names, designations)
- ✅ **LLM Integration** - Uses OpenAI/LiteLLM for:
  - Content summarization
  - Intelligent data cleaning
  - Context-aware extraction
- ✅ **CrewAI Integration** - Orchestrates AI agents for complex workflows
- ✅ **Robust Error Handling** - Handles invalid URLs, blocked requests, and network issues
- ✅ **JSON Export** - Output in structured, production-ready JSON format
- ✅ **Modular & Clean Code** - Well-organized, documented, and maintainable codebase

## 📋 Project Structure

```
crew-AI-agents/
├── main.py                 # Main entry point and user interface
├── config.py              # Configuration and environment variables
├── requirements.txt       # Python dependencies
├── .env.example          # Environment configuration template
├── utils/
│   ├── __init__.py
│   ├── web_scraper.py    # Web scraping logic
│   ├── data_extractor.py # Data extraction and structuring
│   └── llm_handler.py    # LLM integration
├── agents/
│   ├── __init__.py
│   └── scrapper_agent.py # CrewAI agent and task definitions
├── README.md             # This file
└── scraper.log          # Application logs (auto-generated)
```

## 🚀 Quick Start

### 1. Installation

Clone the repository and install dependencies:

```bash
# Clone the repository
git clone https://github.com/Akshita1220174/crew-AI-agents.git
cd crew-AI-agents

# Create a virtual environment (recommended)
python -m venv venv
source venv/Scripts/activate  # On Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Create a `.env` file based on `.env.example`:

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:

```env
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-3.5-turbo
REQUEST_TIMEOUT=10
MAX_RETRIES=3
RETRY_DELAY=2
```

### 3. Usage

#### Interactive Mode

Run the application and follow the prompts:

```bash
python main.py
```

You'll be prompted to:
1. Enter a website URL
2. Wait for scraping and analysis
3. View extracted results
4. Optionally export as JSON

#### Command-Line Mode

Pass a URL directly:

```bash
python main.py https://example.com
```

Results will be printed to console and saved to `extraction_results.json`.

## 📊 Output Format

The application returns structured data in the following JSON format:

```json
{
  "overview": "Website summary describing the main purpose and offerings",
  "services": [
    "Service or product 1",
    "Service or product 2",
    "Service or product 3"
  ],
  "contacts": {
    "emails": [
      "contact@example.com",
      "info@example.com"
    ],
    "phones": [
      "+1 (555) 123-4567",
      "+1 (555) 987-6543"
    ],
    "addresses": [
      "123 Main Street, City, State 12345",
      "456 Oak Avenue, City, State 67890"
    ]
  },
  "people": [
    {
      "name": "John Doe",
      "designation": "CEO"
    },
    {
      "name": "Jane Smith",
      "designation": "CTO"
    }
  ]
}
```

## 🛠️ Components Overview

### `web_scraper.py`
Handles all web scraping operations:
- URL validation
- Multi-page scraping with retry logic
- HTML parsing and text extraction
- Email and phone number extraction
- Internal link discovery

**Key Methods:**
- `fetch_page(url)` - Fetch HTML with retry logic
- `parse_html(html)` - Parse HTML to BeautifulSoup
- `extract_text(soup)` - Extract clean text
- `extract_emails(content)` - Find email addresses
- `extract_phone_numbers(content)` - Find phone numbers
- `scrape_website(url, max_pages)` - Main scraping function

### `data_extractor.py`
Processes and structures scraped data:
- Overview extraction
- Service identification
- Contact information aggregation
- Person/team member detection
- JSON serialization

**Key Methods:**
- `extract_overview(text, title)` - Generate overview
- `extract_services(text)` - Identify services
- `extract_addresses(text)` - Find addresses
- `extract_people(text)` - Identify team members
- `structure_data(scraped_data)` - Organize into JSON
- `to_json(data, pretty)` - Convert to JSON string

### `llm_handler.py`
Integrates with OpenAI for intelligent processing:
- Content summarization
- Service identification using AI
- Data cleaning and validation

**Key Methods:**
- `summarize_content(content, max_length)` - AI summarization
- `extract_services(content)` - AI-based service extraction
- `clean_data(data_dict)` - Data validation and cleaning

### `scrapper_agent.py`
CrewAI orchestration:
- Defines Web Researcher agent
- Creates data extraction tasks
- Manages the complete pipeline

### `config.py`
Central configuration management:
- API keys
- Timeouts and retry settings
- Output formatting
- Environment variable loading

## 🔧 Advanced Usage

### Programmatic API

Use the scraper in your own Python code:

```python
from agents.scrapper_agent import WebScrapingCrew
import json

# Initialize crew
crew = WebScrapingCrew()

# Scrape and extract
results = crew.scrape_and_extract(
    url="https://example.com",
    max_pages=5
)

# Check results
if results['success']:
    data = results['data']
    print(f"Found {len(data['contacts']['emails'])} emails")
    print(f"Found {len(data['people'])} team members")
else:
    print(f"Error: {results['error']}")
```

### Using Individual Components

```python
from utils.web_scraper import WebScraper
from utils.data_extractor import DataExtractor
from utils.llm_handler import LLMHandler

# Initialize components
scraper = WebScraper()
extractor = DataExtractor()
llm = LLMHandler()

# Scrape website
scraped_data = scraper.scrape_website("https://example.com")

# Extract and structure
structured_data = extractor.structure_data(scraped_data)

# Get AI summary
summary = llm.summarize_content(scraped_data['pages'][0]['content'])
```

## ⚙️ Configuration Options

### Environment Variables

Edit `.env` to customize:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-3.5-turbo

# Scraping Behavior
REQUEST_TIMEOUT=10              # Timeout for HTTP requests (seconds)
MAX_RETRIES=3                   # Number of retry attempts
RETRY_DELAY=2                   # Delay between retries (seconds)

# Selenium (for JavaScript-heavy sites)
USE_SELENIUM=False              # Enable Selenium for dynamic content
SELENIUM_HEADLESS=True          # Run browser in headless mode

# Output
OUTPUT_JSON_INDENT=2            # JSON indentation level
```

## 🚨 Error Handling

The application gracefully handles:

- ❌ Invalid URLs
- ❌ Network timeouts
- ❌ HTTP errors (404, 500, etc.)
- ❌ Blocked/403 responses
- ❌ SSL certificate errors
- ❌ Connection refused
- ❌ Malformed HTML

All errors are logged to `scraper.log` for debugging.

## 📝 Logging

Application logs are saved to `scraper.log`:

```bash
tail -f scraper.log  # Monitor logs in real-time
```

Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL

## 🤖 How It Works

1. **URL Validation** - Checks if the URL is properly formatted
2. **Web Scraping** - Fetches HTML content with retry logic
3. **HTML Parsing** - Converts HTML to structured DOM
4. **Text Extraction** - Removes scripts/styles and cleans text
5. **Pattern Matching** - Extracts emails, phones, addresses
6. **AI Summarization** - Uses LLM to create overview
7. **Data Organization** - Structures data into JSON format
8. **AI Cleaning** - Optional: Uses LLM to clean and validate data
9. **Output** - Returns structured JSON or exports to file

## 📦 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| crewai | 0.28.0 | AI agent orchestration |
| crewai-tools | 0.1.7 | CrewAI utilities |
| requests | 2.31.0 | HTTP requests |
| beautifulsoup4 | 4.12.2 | HTML parsing |
| selenium | 4.15.2 | Dynamic content (optional) |
| openai | 1.3.0 | OpenAI API |
| python-dotenv | 1.0.0 | Environment variables |
| pydantic | 2.4.2 | Data validation |

## 🔐 Security Considerations

- **API Keys**: Never commit `.env` files with real API keys
- **User-Agent**: Uses realistic browser headers to avoid detection
- **Rate Limiting**: Implements delays between requests
- **SSL Verification**: Enables certificate verification by default
- **Error Logging**: Logs don't contain sensitive data

## 🐛 Troubleshooting

### Missing API Key
```
WARNING: OPENAI_API_KEY not set
```
**Solution**: Add your OpenAI API key to `.env` file

### Connection Timeout
```
Timeout fetching https://example.com
```
**Solution**: Increase `REQUEST_TIMEOUT` in `.env`

### SSL Certificate Error
```
SSL: CERTIFICATE_VERIFY_FAILED
```
**Solution**: Update certificates or disable verification (not recommended for production)

### No Data Extracted
**Solution**: 
- Check if the website is blocking scrapers
- Try increasing `MAX_RETRIES`
- Verify website structure hasn't changed

## 📈 Performance Tips

- Reduce `max_pages` for faster scraping
- Increase `REQUEST_TIMEOUT` for slow servers
- Use `USE_SELENIUM=True` only for JavaScript-heavy sites
- Run during off-peak hours for large-scale scraping

## 🧪 Testing

Run the application with common test URLs:

```bash
# Test with a simple website
python main.py https://www.wikipedia.org

# Test with a business site
python main.py https://www.github.com

# Interactive mode
python main.py
```

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## ✉️ Support

For issues, questions, or suggestions, please open an issue on GitHub or contact the maintainers.

---

**Created with ❤️ using CrewAI and Python**

Last Updated: March 28, 2026
