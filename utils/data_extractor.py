"""
Data Extractor Module - Processes and structures scraped data.
Organizes information into required format.
"""

import logging
import json
from typing import Dict, List, Any
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataExtractor:
    """
    Extracts and structures data from scraped website content.
    Organizes information into categories.
    """

    def __init__(self):
        """Initialize the data extractor."""
        self.structured_data = {
            "overview": "",
            "services": [],
            "contacts": {
                "emails": [],
                "phones": [],
                "addresses": []
            },
            "people": []
        }

    def extract_overview(self, text_content: str, title: str = "") -> str:
        """
        Extract website overview from content.

        Args:
            text_content: Full text content from website
            title: Page title

        Returns:
            str: Website overview (first 500 chars of content or meta description)
        """
        try:
            # Try to get first substantial paragraph
            paragraphs = text_content.split("\n")
            overview = ""

            for para in paragraphs:
                if len(para.strip()) > 50:  # Find first substantial paragraph
                    overview = para.strip()[:500]
                    break

            if not overview and title:
                overview = f"Website: {title}"

            return overview
        except Exception as e:
            logger.error(f"Error extracting overview: {str(e)}")
            return title or ""

    def extract_services(self, text_content: str) -> List[str]:
        """
        Extract services/products from text content.
        Looks for common service-related keywords.

        Args:
            text_content: Full text content from website

        Returns:
            List of potential services
        """
        try:
            services = []
            service_keywords = [
                "service", "product", "solution", "offering",
                "feature", "capability", "package", "plan"
            ]

            # Look for sentences containing service keywords
            sentences = re.split(r"[.!?;]", text_content)
            seen_services = set()

            for sentence in sentences:
                sentence_lower = sentence.lower().strip()
                if any(keyword in sentence_lower for keyword in service_keywords):
                    # Extract service-like phrases (short sentences)
                    if 20 < len(sentence.strip()) < 200:
                        service = sentence.strip()
                        if service not in seen_services:
                            services.append(service)
                            seen_services.add(service)

            return services[:10]  # Limit to 10 services
        except Exception as e:
            logger.error(f"Error extracting services: {str(e)}")
            return []

    def extract_addresses(self, text_content: str) -> List[str]:
        """
        Extract physical addresses from text content.

        Args:
            text_content: Full text content from website

        Returns:
            List of potential addresses
        """
        try:
            addresses = []
            # Simple pattern for addresses (street, city, state, zip)
            lines = text_content.split("\n")

            for line in lines:
                line = line.strip()
                # Look for lines with common address components
                if any(keyword in line.lower() for keyword in ["st.", "ave.", "blvd", "address", "located"]):
                    if 20 < len(line) < 200:
                        addresses.append(line)

            return addresses[:5]  # Limit to 5 addresses
        except Exception as e:
            logger.error(f"Error extracting addresses: {str(e)}")
            return []

    def extract_people(self, text_content: str) -> List[Dict[str, str]]:
        """
        Extract person names and designations from text.

        Args:
            text_content: Full text content from website

        Returns:
            List of person dictionaries with name and designation
        """
        try:
            people = []
            # Pattern for common designations
            designation_patterns = [
                r"(?:CEO|CTO|CFO|Founder|Director|Manager|Lead|Engineer|Developer)\s+(?:of|at|:)?\s+([A-Za-z\s]+)",
                r"([A-Z][a-z]+\s+[A-Z][a-z]+)\s+(?:is|as)\s+(?:the\s+)?(?:CEO|CTO|CFO|Founder|Director|Manager|Lead|Engineer)",
            ]

            for pattern in designation_patterns:
                matches = re.finditer(pattern, text_content, re.IGNORECASE)
                for match in matches:
                    name = match.group(1).strip() if len(match.groups()) > 0 else ""
                    if name and len(name.split()) <= 3:  # Names typically 1-3 words
                        people.append({
                            "name": name,
                            "designation": "Team Member"
                        })

            # Remove duplicates
            seen_names = set()
            unique_people = []
            for person in people:
                if person["name"] not in seen_names:
                    unique_people.append(person)
                    seen_names.add(person["name"])

            return unique_people[:10]  # Limit to 10 people
        except Exception as e:
            logger.error(f"Error extracting people: {str(e)}")
            return []

    def structure_data(
        self,
        scraped_data: Dict[str, Any],
        llm_summary: str = ""
    ) -> Dict[str, Any]:
        """
        Structure all scraped data into the required format.

        Args:
            scraped_data: Data from WebScraper
            llm_summary: Optional LLM-generated summary

        Returns:
            Structured data dictionary
        """
        try:
            logger.info("Structuring extracted data...")

            # Combine all content from scraped pages
            all_text = ""
            all_emails = set()
            all_phones = set()

            for page in scraped_data.get("pages", []):
                all_text += f"\n{page.get('content', '')}"
                all_emails.update(page.get("emails", []))
                all_phones.update(page.get("phones", []))

            # Build structured data
            self.structured_data = {
                "overview": llm_summary or self.extract_overview(
                    all_text,
                    scraped_data["pages"][0].get("title", "") if scraped_data["pages"] else ""
                ),
                "services": self.extract_services(all_text),
                "contacts": {
                    "emails": list(all_emails)[:10],
                    "phones": list(all_phones)[:10],
                    "addresses": self.extract_addresses(all_text)
                },
                "people": self.extract_people(all_text)
            }

            logger.info("Data structuring complete")
            return self.structured_data

        except Exception as e:
            logger.error(f"Error structuring data: {str(e)}")
            return self.structured_data

    def to_json(self, data: Dict[str, Any] = None, pretty: bool = True) -> str:
        """
        Convert structured data to JSON string.

        Args:
            data: Data to convert (uses self.structured_data if None)
            pretty: Whether to format JSON with indentation

        Returns:
            str: JSON string
        """
        try:
            data = data or self.structured_data
            if pretty:
                return json.dumps(data, indent=2, ensure_ascii=False)
            return json.dumps(data, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error converting to JSON: {str(e)}")
            return "{}"

    def to_dict(self) -> Dict[str, Any]:
        """
        Get structured data as dictionary.

        Returns:
            Dictionary representation of structured data
        """
        return self.structured_data
