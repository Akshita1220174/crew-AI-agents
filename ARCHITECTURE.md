"""
ARCHITECTURE.md - Technical Architecture & Design Documentation
"""

# CrewAI Web Scraper - Technical Architecture

## Overview

This document outlines the technical architecture and design decisions of the CrewAI Web Scraper project.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        User Interface                        │
│                     (main.py - CLI/Interactive)             │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
┌───────▼──────┐ ┌──▼──────────┐ │
│ WebScraper   │ │ DataExtractor│ │
│  - Fetching  │ │ - Structuring│ │
│  - Parsing   │ │ - Organizing│ │
│  - Cleaning  │ │              │ │
└───────┬──────┘ └──┬───────────┘ │
        │           │             │
        └───────────┬─────────────┘
                    │
            ┌───────▼────────┐
            │  LLMHandler    │
            │ - Summarizing  │
            │ - Cleaning     │
            │ - Structuring  │
            └────────────────┘
                    │
            ┌───────▼─────────────┐
            │  CrewAI Framework   │
            │ - Agent Orchestration
            │ - Task Management   │
            └─────────────────────┘
```

## Component Details

### 1. Web Scraper Module (`web_scraper.py`)

**Responsibilities:**
- HTTP request handling with retry logic
- HTML parsing and DOM manipulation
- Text extraction and cleaning
- Pattern matching for email/phone numbers
- Multi-page scraping with domain boundary checking

**Key Features:**
- Exponential backoff retry mechanism
- User-Agent rotation for detection avoidance
- Session persistence
- Memory-efficient streaming parsing

**Data Flow:**
```
URL → Validation → Fetch (with retries) → Parse → Extract → Structure
```

### 2. Data Extractor Module (`data_extractor.py`)

**Responsibilities:**
- Aggregating data from multiple pages
- Identifying services/products
- Extracting contact information
- Person/team member detection
- JSON schema compliance

**Extraction Strategies:**
- Keyword-based service identification
- Regex patterns for emails/phones
- Named entity recognition for people
- Sentence-based address detection

**Output Schema:**
```json
{
  "overview": "string",
  "services": ["string"],
  "contacts": {
    "emails": ["string"],
    "phones": ["string"],
    "addresses": ["string"]
  },
  "people": [
    {"name": "string", "designation": "string"}
  ]
}
```

### 3. LLM Handler Module (`llm_handler.py`)

**Responsibilities:**
- OpenAI API integration
- Content summarization
- AI-based data validation
- Error handling for API failures

**LLM Capabilities:**
- Abstractive summarization
- Service classification
- Data deduplication
- Schema validation

**Fallback Strategy:**
- If LLM unavailable: Use rule-based extraction
- API timeout: Return best-effort results
- Invalid response: Log error and continue

### 4. CrewAI Agent Module (`scrapper_agent.py`)

**Responsibilities:**
- Agent personality definition
- Task orchestration
- Crew coordination

**Agent Profile:**
- Role: Web Researcher
- Goal: Extract structured website data
- Expertise: Website analysis, information organization

**Task Pipeline:**
1. URL validation
2. Content fetching
3. Information extraction
4. Data organization
5. Result delivery

### 5. Configuration Module (`config.py`)

**Responsibilities:**
- Environment variable management
- Default value provisioning
- Setting validation

**Configurable Parameters:**
- API keys and endpoints
- Network timeouts
- Retry behavior
- Output formatting

## Data Flow Architecture

```
┌─────────────────────────────────────────────────────────┐
│ 1. INPUT VALIDATION                                     │
│    URL Format Check → Domain Reachability Check        │
└────────────────┬────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────────┐
│ 2. WEB SCRAPING                                         │
│    Fetch → Parse → Extract Text, Links, Metadata      │
└────────────────┬────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────────┐
│ 3. MULTI-PAGE CRAWLING                                  │
│    Follow Internal Links → Repeat Scraping (Max Pages) │
└────────────────┬────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────────┐
│ 4. PATTERN EXTRACTION                                   │
│    Email/Phone/Address Regex → Name Detection         │
└────────────────┬────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────────┐
│ 5. LLM PROCESSING                                       │
│    Summarization → Validation → Cleaning              │
└────────────────┬────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────────┐
│ 6. DATA STRUCTURING                                     │
│    Organize → Deduplicate → Format JSON               │
└────────────────┬────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────────┐
│ 7. OUTPUT & EXPORT                                      │
│    Return JSON → Save File → Display Results          │
└─────────────────────────────────────────────────────────┘
```

## Error Handling Strategy

```
Network Errors
  ├─ Timeout → Retry with exponential backoff
  ├─ 4xx Status → Skip (likely permanent)
  └─ 5xx Status → Retry

Parsing Errors
  ├─ Invalid HTML → Skip, log warning
  ├─ Encoding Issues → Attempt recovery
  └─ Missing Elements → Continue with partial data

LLM Errors
  ├─ API Rate Limit → Queue and retry
  ├─ Invalid Response → Use fallback
  └─ Timeout → Continue without LLM
```

## Performance Considerations

### Optimization Strategies:

1. **Concurrent Requests** (Future):
   - Use asyncio for parallel scraping
   - Reduce total execution time

2. **Caching**:
   - Cache DNS lookups
   - Session persistence for cookies

3. **Memory Management**:
   - Stream-based HTML parsing
   - Chunk large content
   - Limit stored pages

4. **Smart Crawling**:
   - Respect robots.txt
   - Follow crawl delay hints
   - Prioritize important pages

## Security Architecture

### Input Validation:
- URL format validation
- Scheme whitelisting (http/https only)
- Domain boundary checking

### Output Security:
- Sanitize sensitive data
- No API keys in logs
- Secure error messages

### Network Security:
- SSL certificate verification
- User-Agent randomization
- Rate limiting

## Extension Points

The architecture supports these extensions:

1. **New Extractors**: Subclass `DataExtractor` for custom patterns
2. **Alternative LLMs**: Implement `LLMHandler` interface for other providers
3. **Database Storage**: Add persistence layer
4. **API Output**: Create REST API wrapper
5. **Scheduling**: Add task scheduling system

## Dependencies & Alternatives

| Component | Primary | Alternative |
|-----------|---------|-------------|
| HTTP | requests | httpx, aiohttp |
| Parsing | BeautifulSoup | lxml, Parsel |
| Dynamic Content | Selenium | Playwright, Puppeteer |
| LLM | OpenAI | Anthropic, HuggingFace |
| Orchestration | CrewAI | LangChain, AutoGen |

---

**Last Updated**: March 28, 2026
