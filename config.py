"""
Configuration settings for the CrewAI Web Scraper Project.
Handles API keys and environment variables.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

# Google Gemini Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-pro")

# LLM Provider Selection (choices: "openai", "gemini")
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")

# LiteLLM Configuration (optional, for other LLM providers)
LITELLM_API_KEY = os.getenv("LITELLM_API_KEY", "")

# Web Scraping Configuration
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "10"))
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
RETRY_DELAY = int(os.getenv("RETRY_DELAY", "2"))

# Selenium Configuration
USE_SELENIUM = os.getenv("USE_SELENIUM", "False").lower() == "true"
SELENIUM_HEADLESS = os.getenv("SELENIUM_HEADLESS", "True").lower() == "true"

# Output Configuration
OUTPUT_JSON_INDENT = int(os.getenv("OUTPUT_JSON_INDENT", "2"))

# Webhook Configuration
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "").strip()

# Validation
if not OPENAI_API_KEY and not GEMINI_API_KEY:
    print("WARNING: No LLM API key found. Please set either OPENAI_API_KEY or GEMINI_API_KEY in .env file.")
    print(f"Currently configured LLM_PROVIDER: {LLM_PROVIDER}")

if LLM_PROVIDER == "openai" and not OPENAI_API_KEY:
    print("WARNING: OPENAI selected but OPENAI_API_KEY not set. Using Gemini if available.")
elif LLM_PROVIDER == "gemini" and not GEMINI_API_KEY:
    print("WARNING: Gemini selected but GEMINI_API_KEY not set. Using OpenAI if available.")
