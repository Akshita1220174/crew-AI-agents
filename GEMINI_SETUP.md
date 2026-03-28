"""
GEMINI_SETUP.md - Setting Up Google Gemini Free Trial
"""

# Google Gemini Integration Guide

## 🎯 Overview

The CrewAI Web Scraper now supports **both OpenAI and Google Gemini** APIs. You can use them interchangeably or set your preference!

## 📋 Getting Started with Gemini Free Trial

### Step 1: Get Your Gemini API Key

1. Visit [Google AI Studio](https://aistudio.google.com)
2. Click **"Get API key"** button in the left sidebar
3. Select **"Create API key in new project"** or use existing project
4. Copy your API key (keep it secure!)

> **Note**: Google Gemini offers a free tier with generous limits. No credit card required!

### Step 2: Add Gemini Key to .env

Edit your `.env` file:

```env
# OpenAI Configuration (optional if using Gemini)
OPENAI_API_KEY=your_openai_key_here
OPENAI_MODEL=gpt-3.5-turbo

# Google Gemini Configuration
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-pro

# Choose which provider to use (options: "openai" or "gemini")
LLM_PROVIDER=gemini
```

### Step 3: Install Latest Requirements

```bash
pip install -r requirements.txt
```

This includes the new `google-generativeai` library.

## 🔄 Switching Between APIs

### Option 1: Via .env File

Update `LLM_PROVIDER` in `.env`:

```env
# Use Gemini
LLM_PROVIDER=gemini

# Or use OpenAI
LLM_PROVIDER=openai
```

Then run:
```bash
python main.py https://example.com
```

### Option 2: Programmatically

```python
from utils.llm_handler import LLMHandler

# Use Gemini
llm_gemini = LLMHandler(provider="gemini")

# Use OpenAI
llm_openai = LLMHandler(provider="openai")

# Use with custom API key
llm_custom = LLMHandler(
    provider="gemini",
    api_key="your_api_key",
    model="gemini-pro"
)
```

## 💡 Comparison: OpenAI vs Gemini

| Feature | OpenAI (GPT-3.5) | Google Gemini |
|---------|------------------|---------------|
| **Cost (Free)** | Limited ($18 credit) | Generous free tier |
| **API Response** | Very fast | Fast |
| **Quality** | Excellent | Excellent |
| **Context Window** | 4K tokens | 30K tokens |
| **Availability** | Production-proven | Rapidly improving |
| **Use Case** | General purpose | Multimodal capable |

## 🚀 Usage Examples

### Example 1: Use Gemini by Default

```env
# .env
LLM_PROVIDER=gemini
GEMINI_API_KEY=your_key_here
```

```bash
python main.py https://example.com
```

### Example 2: Use OpenAI with Fallback to Gemini

```env
# .env
LLM_PROVIDER=openai
OPENAI_API_KEY=your_openai_key
GEMINI_API_KEY=your_gemini_key  # Fallback
```

No code changes needed! If OpenAI fails, Gemini automatically takes over.

### Example 3: Batch Scraping with Multiple Providers

```python
from agents.scrapper_agent import WebScrapingCrew
import json

urls = ["https://site1.com", "https://site2.com"]

# Process with Gemini (free)
for url in urls:
    crew = WebScrapingCrew()
    result = crew.scrape_and_extract(url, max_pages=3)
    
    if result['success']:
        print(f"✓ {url}: Processed with {result['provider']}")
```

### Example 4: Check Active Provider

```python
from utils.llm_handler import LLMHandler

llm = LLMHandler()
info = llm.get_provider_info()

print(f"Active Provider: {info['active_provider']}")
print(f"Model: {info['model']}")
print(f"OpenAI Available: {info['openai_available']}")
print(f"Gemini Available: {info['gemini_available']}")
```

## ⚙️ Configuration Reference

### .env Variables

```env
# Google Gemini
GEMINI_API_KEY=your_api_key        # Required for Gemini
GEMINI_MODEL=gemini-pro            # or gemini-pro-vision

# Provider Selection
LLM_PROVIDER=gemini                # or "openai"

# OpenAI (Optional)
OPENAI_API_KEY=your_api_key        # For OpenAI or fallback
OPENAI_MODEL=gpt-3.5-turbo
```

### Available Gemini Models

- **gemini-pro** - Best for text (Recommended)
- **gemini-pro-vision** - Supports text + images

## 📊 API Quotas

### Google Gemini (Free Tier)

- **Rate Limit**: 60 requests per minute
- **Queries per Day**: 1,500 free queries daily
- **Input Tokens**: Unlimited reads
- **Output Tokens**: Up to 2,000 per response

### Upgrade Options

If you exceed free tier:
1. Pay-as-you-go pricing: **$0.00075 / 1K input tokens**
2. Generous free quotas allow testing

## 🔍 Monitoring Provider Usage

View logs to see which provider is being used:

```bash
tail -f scraper.log
```

Look for:
```
✓ Google Gemini initialized with model: gemini-pro
✓ Content summarized using Gemini
✓ Extracted 5 services using Gemini
```

## ❌ Troubleshooting

### Issue: "GEMINI_API_KEY not set"

**Solution**:
```bash
# 1. Add key to .env
GEMINI_API_KEY=your_actual_key

# 2. Restart application
python main.py
```

### Issue: Gemini Rate Limited

**Solution**:
```env
# Switch to OpenAI temporarily
LLM_PROVIDER=openai
```

Or wait 1 minute and retry.

### Issue: Model Not Found

**Solution**:
```env
# Use correct model name
GEMINI_MODEL=gemini-pro

# or
GEMINI_MODEL=gemini-pro-vision
```

### Issue: Invalid API Key

**Solution**:
1. Visit [Google AI Studio](https://aistudio.google.com)
2. Create new API key
3. Update `.env` with new key
4. Restart application

## 🎓 Best Practices

### For Development

Use **Gemini free tier** - saves OpenAI credits:

```env
LLM_PROVIDER=gemini
GEMINI_API_KEY=your_key
```

### For Production

Use **OpenAI with Gemini fallback**:

```env
LLM_PROVIDER=openai
OPENAI_API_KEY=your_prod_key
GEMINI_API_KEY=fallback_key
```

### For High Volume

Monitor usage:
```bash
# Check logs
grep "Extracted" scraper.log | wc -l

# Count by provider
grep "Gemini" scraper.log | wc -l
grep "OpenAI" scraper.log | wc -l
```

## 📚 Resources

- [Google AI Studio](https://aistudio.google.com)
- [Gemini API Docs](https://ai.google.dev/docs)
- [Python Client Library](https://github.com/google/generative-ai-python)
- [Pricing Information](https://ai.google.dev/pricing)

## ✨ Tips & Tricks

### Tip 1: Use Gemini for Testing

```bash
export LLM_PROVIDER=gemini
python main.py https://example.com
```

### Tip 2: Batch Switch Providers

```python
# Process with Gemini first, then OpenAI
from utils.llm_handler import LLMHandler

providers = ["gemini", "openai"]
for provider in providers:
    try:
        llm = LLMHandler(provider=provider)
        result = llm.summarize_content("Some content")
        print(f"✓ Success with {provider}")
        break
    except Exception as e:
        print(f"✗ Failed with {provider}: {e}")
```

### Tip 3: Monitor Provider Performance

Check which provider is faster:

```python
import time
from utils.llm_handler import LLMHandler

for provider in ["gemini", "openai"]:
    llm = LLMHandler(provider=provider)
    start = time.time()
    result = llm.summarize_content("test content")
    duration = time.time() - start
    print(f"{provider}: {duration:.2f}s")
```

## 🎉 Getting Started Checklist

- [ ] Created Google account
- [ ] Got Gemini API key from AI Studio
- [ ] Added `GEMINI_API_KEY` to `.env`
- [ ] Set `LLM_PROVIDER=gemini` in `.env`
- [ ] Ran `pip install -r requirements.txt`
- [ ] Tested: `python main.py https://python.org`
- [ ] Verified logs show "✓ Google Gemini initialized"
- [ ] Verified scraping produced results with Gemini

## 📞 Support

**Issue with Gemini?**
- Visit: [Google AI Studio Help](https://support.google.com/ai)
- Check API quotas: [AI Studio dashboard](https://aistudio.google.com)

**Issue with CrewAI integration?**
- Check: [PROJECT_INDEX.md](PROJECT_INDEX.md)
- See: [TROUBLESHOOTING section in SETUP.md](SETUP.md#troubleshooting)

---

**Updated**: March 28, 2026  
**Two APIs, One Tool, Maximum Flexibility** 🚀
