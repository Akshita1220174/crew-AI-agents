"""
DEPLOYMENT_CHECKLIST.md - Pre-Deployment Verification
"""

# Deployment Checklist - CrewAI Web Scraper

Complete this checklist before deploying to production.

## ✅ Pre-Deployment Verification

### 1. Environment Setup
- [ ] Python 3.8+ installed
- [ ] Virtual environment created
- [ ] All dependencies installed: `pip install -r requirements.txt`
- [ ] `.env` file created from `.env.example`
- [ ] OpenAI API key added to `.env`
- [ ] Other required environment variables configured

### 2. Code Quality
- [ ] All Python files have proper imports
- [ ] No syntax errors: `python -m py_compile main.py`
- [ ] No hardcoded credentials in source files
- [ ] `.gitignore` includes `.env` and `venv/`
- [ ] Comments and docstrings present
- [ ] Code follows PEP 8 style guidelines

### 3. Configuration Validation
- [ ] API key validation: `python -c "from config import OPENAI_API_KEY; assert OPENAI_API_KEY"`
- [ ] Model specified correctly
- [ ] Timeout values reasonable (5-30 seconds)
- [ ] Retry count appropriate (1-5)
- [ ] Logging configured

### 4. Functionality Testing
- [ ] Basic import test: `python -c "from agents.scrapper_agent import WebScrapingCrew"`
- [ ] Example script runs: `python example_usage.py`
- [ ] Simple URL scrapes: `python main.py https://example.com`
- [ ] Error handling tested (invalid URL, timeout)
- [ ] JSON output valid format
- [ ] Logging to file works: `scraper.log` exists

### 5. Security Audit
- [ ] No API keys in code
- [ ] `.env.example` doesn't contain real credentials
- [ ] SSL verification enabled
- [ ] User-Agent set appropriately
- [ ] Error messages don't expose sensitive info
- [ ] Logs don't contain credentials

### 6. Performance Review
- [ ] Average scraping time acceptable
- [ ] Memory usage reasonable
- [ ] No infinite loops in scraping
- [ ] Timeout handling prevents hangs
- [ ] Rate limiting respected

### 7. Error Handling
- [ ] Invalid URLs handled gracefully
- [ ] Network timeouts caught
- [ ] API failures don't crash app
- [ ] Missing data handled
- [ ] Malformed HTML processed safely
- [ ] API rate limits handled

### 8. Documentation
- [ ] README.md complete and accurate
- [ ] SETUP.md covers all steps
- [ ] Code comments sufficient
- [ ] Example usage provided
- [ ] Troubleshooting section filled
- [ ] Architecture documented

### 9. Deployment Environment
- [ ] Target server Python version checked
- [ ] All dependencies compatible with OS
- [ ] File permissions appropriate
- [ ] Log directory writable
- [ ] API access from server confirmed
- [ ] Network access verified

### 10. Monitoring & Logging
- [ ] Logging level set appropriately
- [ ] Log rotation configured (for long-running)
- [ ] Error alerts configured (optional)
- [ ] Performance metrics tracked
- [ ] API usage monitored

## 🚀 Deployment Steps

### Local Deployment
```bash
# 1. Set up environment
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure
cp .env.example .env
# Edit .env with your API key

# 4. Test
python example_usage.py

# 5. Run
python main.py
```

### Server Deployment
```bash
# 1. Clone repository
git clone https://github.com/Akshita1220174/crew-AI-agents.git
cd crew-AI-agents

# 2. Set up virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
nano .env  # Add your configuration

# 5. Run as background service
nohup python main.py > scraper.log 2>&1 &
```

### Docker Deployment
```bash
# 1. Build image
docker build -t crew-scraper .

# 2. Run container
docker run -e OPENAI_API_KEY=your_key crew-scraper

# 3. For persistent deployment
docker run -d \
  -e OPENAI_API_KEY=your_key \
  -v /data:/app/output \
  crew-scraper
```

## 📊 Post-Deployment Verification

### After Deployment, Verify:

- [ ] Application starts without errors
- [ ] Logs appear in `scraper.log`
- [ ] Can scrape sample website
- [ ] JSON output format correct
- [ ] API calls working
- [ ] No memory leaks after 1 hour runtime
- [ ] Error handling works
- [ ] Performance acceptable

## 🔍 Monitoring Checklist

### Daily Monitoring
- [ ] Check `scraper.log` for errors
- [ ] Monitor API usage
- [ ] Verify recent scraping success rate
- [ ] Check for timeout issues

### Weekly Monitoring
- [ ] Review error patterns
- [ ] Update dependencies if needed
- [ ] Backup logs periodically
- [ ] Verify API key validity

### Monthly Review
- [ ] Analyze scraping statistics
- [ ] Optimize slow operations
- [ ] Review security incidents
- [ ] Plan feature improvements

## 🆘 Rollback Procedure

If issues occur:

```bash
# 1. Stop application
pkill -f "python main.py"

# 2. Check logs
tail -100 scraper.log

# 3. Rollback (if using git)
git checkout HEAD~1

# 4. Restart
python main.py
```

## 📝 Production Configuration Example

```env
# Production .env
OPENAI_API_KEY=sk-prod-1234567890...
OPENAI_MODEL=gpt-3.5-turbo

# For reliability
REQUEST_TIMEOUT=20
MAX_RETRIES=5
RETRY_DELAY=3

# Disable selenium unless needed
USE_SELENIUM=False

# Output formatting
OUTPUT_JSON_INDENT=2
```

## 🔐 Security Hardening

- [ ] Use secrets management (not .env)
- [ ] Rotate API keys regularly
- [ ] Implement IP whitelisting
- [ ] Use HTTPS for API calls
- [ ] Enable audit logging
- [ ] Monitor for unusual activity

## 📈 Performance Optimization

```python
# For high-volume scraping
# - Reduce max_pages parameter
# - Enable caching
# - Use connection pooling
# - Implement async scraping (future version)
```

## 🆘 Emergency Contacts

Document for your team:
- [ ] API Support: OpenAI Support (support@openai.com)
- [ ] Repository Issues: GitHub Issues
- [ ] Project Lead: [Your Name]
- [ ] On-Call: [Contact Info]

## ✨ Success Indicators

Application is ready for production when:

✅ All checklist items complete  
✅ No critical errors in testing  
✅ Performance metrics acceptable  
✅ Documentation reviewed  
✅ Team trained on operation  
✅ Monitoring tools configured  
✅ Backup/rollback plan ready  
✅ Security audit passed  

---

**Deployment Date:** _______________  
**Deployed By:** _______________  
**Approval:** _______________  

---

**Last Updated:** March 28, 2026
