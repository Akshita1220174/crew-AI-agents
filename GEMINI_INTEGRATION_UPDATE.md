"""
GEMINI_INTEGRATION_UPDATE.md - CrewAI Dual LLM Support Update
"""

# 🆕 Google Gemini Integration - Complete Update

## 📦 What's New

The CrewAI Web Scraper now supports **both OpenAI GPT and Google Gemini APIs**! You can use them interchangeably based on your convenience and preferences.

## ✨ Key Features Added

### ✅ Dual LLM Provider Support
- **OpenAI GPT-3.5**: Production-proven, fast API
- **Google Gemini**: Free tier available, generous quotas

### ✅ Intelligent Provider Selection
- Set preferred provider via `.env` file
- Automatic fallback if primary provider fails
- Runtime provider switching

### ✅ Seamless Integration
- Same interface for both APIs
- No code changes needed to switch
- Logging shows which provider is active

## 📁 Files Modified/Created

### Modified Files

1. **config.py** - Added Gemini configuration
   - `GEMINI_API_KEY` - Your Gemini API key
   - `GEMINI_MODEL` - Model selection (default: gemini-pro)
   - `LLM_PROVIDER` - Choose "openai" or "gemini"
   - Enhanced validation with dual API support

2. **.env.example** - Updated template
   - Added Gemini API key field
   - Added model selection
   - Added LLM_PROVIDER choice

3. **requirements.txt** - Added dependency
   - `google-generativeai==0.3.0` - Google Gemini library

4. **utils/llm_handler.py** - Complete rewrite
   - Support for both OpenAI and Gemini
   - Provider auto-detection
   - Automatic fallback mechanism
   - Individual methods for each provider
   - `get_provider_info()` method for monitoring

### New Files

1. **GEMINI_SETUP.md** - Complete Gemini setup guide
   - How to get free API key
   - Configuration instructions
   - Usage examples
   - Comparison with OpenAI
   - Troubleshooting

2. **GEMINI_INTEGRATION_UPDATE.md** - This file

## 🚀 Quick Start with Gemini

### Step 1: Get Free Gemini API Key

```bash
# Visit: https://aistudio.google.com
# Click "Get API key" → Create new API key
# Copy and save your key
```

### Step 2: Update .env File

```env
# Add your Gemini key
GEMINI_API_KEY=your_gemini_api_key_here

# Choose Gemini as default provider
LLM_PROVIDER=gemini

# Keep OpenAI for fallback (optional)
OPENAI_API_KEY=your_openai_key_here
```

### Step 3: Install Updated Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run with Gemini

```bash
python main.py https://example.com
```

Check logs to see:
```
✓ Google Gemini initialized with model: gemini-pro
✓ Content summarized using Gemini
```

## 💻 Usage Examples

### Example 1: Use Gemini Exclusively

**.env:**
```env
GEMINI_API_KEY=your_key_here
LLM_PROVIDER=gemini
```

**Run:**
```bash
python main.py https://example.com
```

### Example 2: Use OpenAI with Gemini Fallback

**.env:**
```env
OPENAI_API_KEY=your_openai_key
GEMINI_API_KEY=your_gemini_key
LLM_PROVIDER=openai
```

**Result:** Uses OpenAI by default, automatically switches to Gemini if OpenAI fails

### Example 3: Programmatic Usage

```python
from utils.llm_handler import LLMHandler

# Use specific provider
llm = LLMHandler(provider="gemini")

# Get provider info
info = llm.get_provider_info()
print(f"Using: {info['active_provider']}")
print(f"Model: {info['model']}")

# Use the LLM
summary = llm.summarize_content(website_content)
services = llm.extract_services(website_content)
cleaned_data = llm.clean_data(extracted_data)
```

### Example 4: Batch Processing with Both APIs

```python
from agents.scrapper_agent import WebScrapingCrew

urls = ["https://site1.com", "https://site2.com"]

# Process with Gemini (free tier)
for url in urls:
    crew = WebScrapingCrew()
    result = crew.scrape_and_extract(url)
    
    if result['success']:
        print(f"✓ Processed: {url}")
        print(f"  Overview: {result['data']['overview'][:100]}...")
```

## 🔄 Provider Switching

### At Runtime

Edit `.env` and restart:
```env
# For Gemini
LLM_PROVIDER=gemini

# For OpenAI
LLM_PROVIDER=openai
```

### In Code

```python
# Gemini
from utils.llm_handler import LLMHandler
llm_free = LLMHandler(provider="gemini")

# OpenAI
llm_pro = LLMHandler(provider="openai")

# With automatic selection
llm_auto = LLMHandler()  # Uses LLM_PROVIDER from config
```

## 📊 Architecture Changes

### Before (OpenAI Only)
```
LLMHandler
  ├── self.client (OpenAI)
  └── Methods: summarize, extract, clean
```

### After (Dual Support)
```
LLMHandler
  ├── self.openai_client (Optional)
  ├── self.gemini_client (Optional)
  ├── self.active_provider (Selected)
  ├── self.model (Current model)
  └── Methods:
      ├── Public: summarize, extract, clean (Provider-agnostic)
      ├── Provider-specific: _summarize_openai, _summarize_gemini
      ├── Helpers: _parse_services_json, _parse_cleaned_json
      └── New: get_provider_info()
```

## 🔧 Configuration Reference

### config.py Variables

```python
# OpenAI (existing)
OPENAI_API_KEY      # str - Your OpenAI API key
OPENAI_MODEL        # str - Model name (default: gpt-3.5-turbo)

# Google Gemini (new)
GEMINI_API_KEY      # str - Your Gemini API key
GEMINI_MODEL        # str - Model name (default: gemini-pro)

# Provider Selection (new)
LLM_PROVIDER        # str - "openai" or "gemini" (default: openai)

# Existing features
REQUEST_TIMEOUT     # int - HTTP timeout
MAX_RETRIES        # int - Retry attempts
# ... other settings
```

### .env File Template

```env
# OpenAI (optional if using Gemini)
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-3.5-turbo

# Google Gemini
GEMINI_API_KEY=AIzaSy...
GEMINI_MODEL=gemini-pro

# Provider choice
LLM_PROVIDER=gemini  # or openai

# Other settings remain the same...
```

## 📈 Benefits

### Using Gemini Free Tier

✅ **No Cost**: Generous free tier (1,500 requests/day)  
✅ **Testing Friendly**: Perfect for development and testing  
✅ **Backup**: Fallback option if OpenAI has issues  
✅ **Learning**: Experiment with different LLM providers  

### Using OpenAI

✅ **Production-Proven**: Stable, reliable API  
✅ **Faster Response**: Optimized for speed  
✅ **Advanced Models**: Access to latest GPT models  
✅ **Enterprise**: Better rate limits with paid tier  

## 🔄 Fallback Mechanism

```
User Request
    ↓
Check LLM_PROVIDER setting
    ↓
Try Primary Provider
    ├─ Success → Use it
    └─ Fails → Check Fallback
        ├─ Success → Use fallback
        └─ Fails → Return default response
```

## 📝 Logging & Monitoring

### View Active Provider

```bash
grep "initialized" scraper.log
```

Output:
```
✓ Google Gemini initialized with model: gemini-pro
✓ Content summarized using Gemini
```

### Check Provider Info

```python
from utils.llm_handler import LLMHandler

llm = LLMHandler()
info = llm.get_provider_info()

print(json.dumps(info, indent=2))
# Output:
# {
#   "active_provider": "gemini",
#   "model": "gemini-pro",
#   "openai_available": true,
#   "gemini_available": true
# }
```

## ✅ Testing the Integration

### Test 1: Check Configuration

```bash
python -c "from config import GEMINI_API_KEY, LLM_PROVIDER; print(f'Provider: {LLM_PROVIDER}, Has Gemini Key: {bool(GEMINI_API_KEY)}')"
```

### Test 2: Test Gemini Import

```bash
python -c "import google.generativeai; print('✓ Gemini library OK')"
```

### Test 3: Test LLM Handler

```python
from utils.llm_handler import LLMHandler

handler = LLMHandler()
info = handler.get_provider_info()
print(f"✓ Active provider: {info['active_provider']}")
```

### Test 4: Real Scraping Test

```bash
python main.py https://python.org
```

## 🚨 Troubleshooting

### Issue: Gemini not working

```bash
# Check API key
python -c "from config import GEMINI_API_KEY; print('Key set' if GEMINI_API_KEY else 'No key')"

# Check provider setting
python -c "from config import LLM_PROVIDER; print(f'Provider: {LLM_PROVIDER}')"
```

### Issue: Both APIs failing

```bash
# Use basic extraction (no LLM)
# Set in config or through code
llm = LLMHandler()
if not llm.active_provider:
    print("Using basic extraction without LLM")
```

### Issue: Wrong provider active

```env
# Verify .env contains:
LLM_PROVIDER=gemini

# Restart application
python main.py
```

## 📚 Documentation Structure

- **GEMINI_SETUP.md** - Setup guide and getting started
- **GEMINI_INTEGRATION_UPDATE.md** - This file (technical details)
- **config.py** - Configuration code
- **utils/llm_handler.py** - Implementation
- **README.md** - Updated with dual API mention
- **QUICK_START.md** - Updated with Gemini examples

## 🎯 Migration Guide

### If You Currently Use OpenAI

**No action needed!** Works exactly as before.

```env
OPENAI_API_KEY=your_key
LLM_PROVIDER=openai  # Default, can be omitted
```

### If You Want to Add Gemini

1. Get free API key from [aistudio.google.com](https://aistudio.google.com)
2. Add to `.env`:
   ```env
   GEMINI_API_KEY=your_key
   LLM_PROVIDER=gemini
   ```
3. Install: `pip install -r requirements.txt`
4. Test: `python main.py https://example.com`

## 💡 Best Practices

### For Development

Use Gemini free tier to save costs:

```env
LLM_PROVIDER=gemini
GEMINI_API_KEY=your_free_key
OPENAI_API_KEY=leave_empty_or_fallback  # Optional fallback
```

### For Production

Use OpenAI with Gemini fallback:

```env
LLM_PROVIDER=openai
OPENAI_API_KEY=your_production_key
GEMINI_API_KEY=free_tier_fallback
```

### For High-Volume Scraping

Monitor provider switching:

```bash
# See provider usage
grep "using" scraper.log | grep -i provider | head -20
```

## 📞 Support Resources

- **Gemini**: [Google AI Studio](https://aistudio.google.com)
- **Gemini Docs**: [Generative AI Python Docs](https://ai.google.dev/docs)
- **OpenAI**: [OpenAI API Docs](https://platform.openai.com/docs)
- **Project**: [PROJECT_INDEX.md](PROJECT_INDEX.md)

## 🎉 Summary

You now have:

✅ **Dual LLM Support** - OpenAI + Gemini  
✅ **Free Option** - Gemini free tier (no card needed)  
✅ **Paid Option** - OpenAI for production  
✅ **Automatic Fallback** - Never lose service  
✅ **Easy Switching** - One config change  
✅ **Full Documentation** - Guides and examples  

### Next Steps

1. Get Gemini key: https://aistudio.google.com
2. Update `.env` with both API keys
3. Set `LLM_PROVIDER=gemini` to start
4. Run: `python main.py https://example.com`
5. Check logs: `tail -f scraper.log`

---

**Updated**: March 28, 2026  
**Dual LLM Support**: Complete ✓  
**Ready for Production**: Yes  
**Both APIs Working**: Yes  

Enjoy flexible AI-powered web scraping! 🚀
