"""
SETUP.md - Detailed Installation and Setup Guide
"""

# CrewAI Web Scraper - Comprehensive Setup Guide

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Verification](#verification)
5. [Troubleshooting](#troubleshooting)
6. [Advanced Setup](#advanced-setup)

## Prerequisites

### System Requirements

- **Python**: Version 3.8 or higher
- **OS**: Windows, macOS, or Linux
- **Memory**: At least 2GB RAM
- **Internet**: Active connection for API calls

### Prerequisites Check

```bash
# Check Python version
python --version

# Should output: Python 3.8.0 or higher
```

## Installation

### Step 1: Clone the Repository

```bash
# Using Git
git clone https://github.com/Akshita1220174/crew-AI-agents.git
cd crew-AI-agents

# Or download as ZIP and extract
```

### Step 2: Create Virtual Environment

**On Windows (PowerShell):**
```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1
```

**On Windows (Command Prompt):**
```cmd
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
# Upgrade pip first
pip install --upgrade pip

# Install required packages
pip install -r requirements.txt
```

The installation will include:
- crewai - AI agent framework
- requests - HTTP client
- beautifulsoup4 - HTML parser
- selenium - Dynamic content support
- openai - LLM integration
- And more (see requirements.txt)

### Step 4: Verify Installation

```bash
# Check if packages installed correctly
pip list

# Should include: crewai, requests, beautifulsoup4, openai, etc.
```

## Configuration

### Step 1: Create Environment File

```bash
# Copy example file
cp .env.example .env

# On Windows (PowerShell)
Copy-Item .env.example .env
```

### Step 2: Get OpenAI API Key

1. Visit [OpenAI API Platform](https://platform.openai.com/)
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key

### Step 3: Configure .env File

Edit `.env` file and add your settings:

```env
# Required: Your OpenAI API Key
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxx

# Optional: Choose your LLM model
OPENAI_MODEL=gpt-3.5-turbo

# Network Configuration
REQUEST_TIMEOUT=10        # Timeout in seconds
MAX_RETRIES=3            # Retry attempts
RETRY_DELAY=2            # Delay between retries in seconds

# Advanced: Selenium for dynamic content
USE_SELENIUM=False
SELENIUM_HEADLESS=True

# Output Configuration
OUTPUT_JSON_INDENT=2
```

### Step 4: Verify Configuration

```python
# Test configuration loading
python -c "from config import OPENAI_API_KEY; print('✓ Config OK' if OPENAI_API_KEY else '✗ Missing API Key')"
```

## Verification

### Test 1: Import Modules

```bash
# Run this Python command
python -c "
from agents.scrapper_agent import WebScrapingCrew
from utils.web_scraper import WebScraper
from utils.data_extractor import DataExtractor
from utils.llm_handler import LLMHandler
print('✓ All modules imported successfully')
"
```

### Test 2: Run Example Script

```bash
# Run the example usage
python example_usage.py
```

You should see the scraper in action with example output.

### Test 3: Test with Simple URL

```bash
# Test with a simple website
python main.py https://www.python.org

# Should display:
# - Website overview
# - Any services found
# - Contact information
# - Team members identified
```

### Test 4: Check Logging

```bash
# View log file
tail -f scraper.log  # On macOS/Linux
Get-Content -Tail 20 -Wait scraper.log  # On Windows PowerShell
```

## Troubleshooting

### Issue: Module Not Found

```
ModuleNotFoundError: No module named 'crewai'
```

**Solution:**
```bash
# Ensure virtual environment is activated
# On Windows
.\venv\Scripts\activate

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Issue: API Key Not Recognized

```
WARNING: OPENAI_API_KEY not set
```

**Solution:**
1. Check `.env` file exists in project root
2. Verify `OPENAI_API_KEY` line is correct (no spaces around =)
3. Double-check API key is valid
4. Try: `python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('OPENAI_API_KEY'))"`

### Issue: Connection Timeout

```
Timeout fetching https://example.com
```

**Solutions:**
1. Increase timeout: Edit `.env` → `REQUEST_TIMEOUT=20`
2. Check internet connection
3. Try different website
4. Disable proxy if applicable

### Issue: SSL Certificate Error

```
SSL: CERTIFICATE_VERIFY_FAILED
```

**Solutions:**
```bash
# Update certificates (if using macOS)
/Applications/Python\ 3.x/Install\ Certificates.command

# Or modify config.py temporarily for testing (not recommended for production):
# In web_scraper.py, change: verify=False
```

### Issue: Permission Denied

```
PermissionError: [Errno 13] Permission denied
```

**Solutions:**
```bash
# Check file permissions
ls -la  # macOS/Linux

# Fix permissions
chmod +x main.py
chmod +x example_usage.py
```

## Advanced Setup

### Using Different LLM Providers

#### Using Azure OpenAI

```env
# In .env file
OPENAI_API_KEY=your-azure-key
OPENAI_MODEL=gpt-35-turbo
```

#### Using LiteLLM (Multiple Providers)

The `llm_handler.py` supports LiteLLM for providers like Anthropic, Cohere, etc.

```python
# In config.py or llm_handler.py, update:
from litellm import completion

# Then use any supported model
```

### Running with Selenium

For JavaScript-heavy websites:

```env
USE_SELENIUM=True
SELENIUM_HEADLESS=True
```

Install webdriver:
```bash
pip install webdriver-manager
```

### Docker Setup (Optional)

Create `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV OPENAI_API_KEY=${OPENAI_API_KEY}

CMD ["python", "main.py"]
```

Build and run:

```bash
docker build -t crew-scraper .
docker run -e OPENAI_API_KEY=your_key crew-scraper
```

### Setting Up Logging

The app automatically creates `scraper.log`. To customize:

Edit `main.py`:

```python
logging.basicConfig(
    level=logging.DEBUG,  # Change to DEBUG for more detail
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('scraper.log')
    ]
)
```

### Performance Optimization

For large-scale scraping:

```env
# Reduce per-site scraping
# In your code:
crew.scrape_and_extract(url=url, max_pages=2)

# Implement caching
# Reduce API calls by using local models
USE_SELENIUM=False  # Faster than Selenium
```

### Production Deployment

1. **Security:**
   - Never commit `.env` files
   - Use environment-specific configs
   - Implement rate limiting

2. **Monitoring:**
   - Set up log aggregation
   - Monitor API usage
   - Track scraping success rates

3. **Scaling:**
   - Use task queues (Celery, RQ)
   - Implement database storage
   - Add API caching layer

## Getting Help

### Resources

- [CrewAI Documentation](https://docs.crewai.com/)
- [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [Requests Documentation](https://requests.readthedocs.io/)

### Common Questions

**Q: Can I scrape password-protected sites?**
A: No, this tool is designed for public content only.

**Q: What's the rate limit?**
A: Depends on your OpenAI plan. Scraping itself has no rate limit; the LLM calls do.

**Q: Can I use this commercially?**
A: Yes, with proper licensing. Check your website's terms of service.

**Q: How do I run multiple scrapings concurrently?**
A: Future versions will support async operations. For now, run multiple instances.

---

**Last Updated**: March 28, 2026
**Version**: 1.0.0
