"""
Web Scraper Module - Handles fetching and parsing web content.
Uses requests and BeautifulSoup for static content.
Optionally uses Selenium for dynamic content.
"""

import logging
from typing import Optional, List, Dict
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup
from config import REQUEST_TIMEOUT, MAX_RETRIES, RETRY_DELAY, USE_SELENIUM
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WebScraper:
    """
    Web scraper class for fetching and parsing HTML content from websites.
    """

    def __init__(self):
        """Initialize the web scraper with default headers."""
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            )
        }
        self.session = requests.Session()
        self.visited_urls: set = set()
        self.base_domain: Optional[str] = None

    def is_valid_url(self, url: str) -> bool:
        """
        Validate if the URL is properly formatted.

        Args:
            url: URL string to validate

        Returns:
            bool: True if URL is valid, False otherwise
        """
        try:
            result = urlparse(url)
            return all([result.scheme in ["http", "https"], result.netloc])
        except Exception as e:
            logger.error(f"URL validation error: {e}")
            return False

    def fetch_page(self, url: str) -> Optional[str]:
        """
        Fetch HTML content from a URL with retry logic.

        Args:
            url: URL to fetch

        Returns:
            str: HTML content or None if fetch fails
        """
        if not self.is_valid_url(url):
            logger.error(f"Invalid URL format: {url}")
            return None

        for attempt in range(MAX_RETRIES):
            try:
                logger.info(f"Fetching: {url} (Attempt {attempt + 1}/{MAX_RETRIES})")
                response = self.session.get(
                    url,
                    headers=self.headers,
                    timeout=REQUEST_TIMEOUT,
                    verify=True
                )
                response.raise_for_status()
                return response.text

            except requests.exceptions.Timeout:
                logger.warning(f"Timeout fetching {url}")
            except requests.exceptions.ConnectionError:
                logger.warning(f"Connection error for {url}")
            except requests.exceptions.HTTPError as e:
                logger.error(f"HTTP error {e.response.status_code}: {url}")
                # Don't retry on 4xx errors
                if 400 <= e.response.status_code < 500:
                    return None
            except Exception as e:
                logger.error(f"Error fetching {url}: {str(e)}")

            # Wait before retrying
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY)

        logger.error(f"Failed to fetch {url} after {MAX_RETRIES} attempts")
        return None

    def parse_html(self, html_content: str) -> Optional[BeautifulSoup]:
        """
        Parse HTML content into BeautifulSoup object.

        Args:
            html_content: Raw HTML content

        Returns:
            BeautifulSoup object or None if parsing fails
        """
        try:
            soup = BeautifulSoup(html_content, "html.parser")
            return soup
        except Exception as e:
            logger.error(f"Error parsing HTML: {str(e)}")
            return None

    def extract_text(self, soup: BeautifulSoup) -> str:
        """
        Extract all text content from parsed HTML.

        Args:
            soup: BeautifulSoup object

        Returns:
            str: Cleaned text content
        """
        try:
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()

            text = soup.get_text()
            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = "\n".join(chunk for chunk in chunks if chunk)
            return text
        except Exception as e:
            logger.error(f"Error extracting text: {str(e)}")
            return ""

    def extract_emails(self, content: str) -> List[str]:
        """
        Extract email addresses from text content.

        Args:
            content: Text content to search

        Returns:
            List of unique email addresses
        """
        import re
        email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        emails = re.findall(email_pattern, content)
        return list(set(emails))

    def extract_phone_numbers(self, content: str) -> List[str]:
        """
        Extract phone numbers from text content.

        Args:
            content: Text content to search

        Returns:
            List of phone numbers
        """
        import re
        # Pattern for various phone formats
        phone_pattern = r"(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}"
        phones = re.findall(phone_pattern, content)
        return list(set(phones))

    def extract_links(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        """
        Extract all links from parsed HTML.

        Args:
            soup: BeautifulSoup object
            base_url: Base URL for resolving relative links

        Returns:
            List of absolute URLs
        """
        try:
            links = []
            base_domain = urlparse(base_url).netloc

            for link in soup.find_all("a", href=True):
                absolute_url = urljoin(base_url, link["href"])
                # Only include links from the same domain
                if urlparse(absolute_url).netloc == base_domain:
                    links.append(absolute_url)

            return list(set(links))
        except Exception as e:
            logger.error(f"Error extracting links: {str(e)}")
            return []

    def scrape_website(
        self,
        url: str,
        max_pages: int = 5,
        follow_links: bool = True
    ) -> Dict[str, any]:
        """
        Scrape website starting from the given URL.

        Args:
            url: Starting URL
            max_pages: Maximum number of pages to scrape from the site
            follow_links: Whether to follow internal links

        Returns:
            Dictionary containing scraped content
        """
        if not self.is_valid_url(url):
            logger.error(f"Invalid starting URL: {url}")
            return {"error": f"Invalid URL: {url}", "pages": []}

        self.base_domain = urlparse(url).netloc
        pages_data = []
        urls_to_visit = [url]
        self.visited_urls = set()

        while urls_to_visit and len(pages_data) < max_pages:
            current_url = urls_to_visit.pop(0)

            if current_url in self.visited_urls:
                continue

            self.visited_urls.add(current_url)
            logger.info(f"Scraping page {len(pages_data) + 1}/{max_pages}: {current_url}")

            html_content = self.fetch_page(current_url)
            if not html_content:
                continue

            soup = self.parse_html(html_content)
            if not soup:
                continue

            text_content = self.extract_text(soup)
            emails = self.extract_emails(text_content)
            phones = self.extract_phone_numbers(text_content)
            links = self.extract_links(soup, current_url)

            pages_data.append({
                "url": current_url,
                "title": soup.title.string if soup.title else "N/A",
                "content": text_content[:2000],  # Limit content size
                "emails": emails,
                "phones": phones,
                "links": links
            })

            # Add new links to visit queue if following links
            if follow_links:
                for link in links:
                    if link not in self.visited_urls and len(pages_data) < max_pages:
                        urls_to_visit.append(link)

        return {
            "domain": self.base_domain,
            "total_pages_scraped": len(pages_data),
            "pages": pages_data
        }
