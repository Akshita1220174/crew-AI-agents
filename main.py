"""
Main Entry Point - CrewAI Web Scraping and Data Extraction System.
User-friendly interface for scraping websites and extracting structured information.
"""

import logging
import json
import sys
import requests
from typing import Optional
from agents.scrapper_agent import WebScrapingCrew
from config import OUTPUT_JSON_INDENT, WEBHOOK_URL

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('scraper.log')
    ]
)
logger = logging.getLogger(__name__)


class WebScraperApp:
    """
    Main application class for web scraping.
    Provides user-friendly interface for scraping and data extraction.
    """

    def __init__(self):
        """Initialize the web scraper application."""
        self.crew = WebScrapingCrew()
        logger.info("Web Scraper Application initialized")

    def validate_url(self, url: str) -> bool:
        """
        Validate URL format.

        Args:
            url: URL to validate

        Returns:
            bool: True if URL is valid
        """
        if not url.startswith(("http://", "https://")):
            return False
        return len(url) > 10

    def get_user_input(self) -> Optional[str]:
        """
        Get and validate user input for URL.

        Returns:
            str: Valid URL or None
        """
        print("\n" + "="*70)
        print("CrewAI Web Scraper - Intelligent Information Extraction")
        print("="*70)
        print("\nThis tool will scrape a website and extract:")
        print("  • Website overview")
        print("  • Services/Products offered")
        print("  • Contact information (emails, phones, addresses)")
        print("  • Team member details (names, designations)")
        print("\n" + "-"*70)

        url = input("\nEnter website URL (e.g., https://example.com): ").strip()

        if not url:
            print("❌ URL cannot be empty. Please try again.")
            return None

        if not self.validate_url(url):
            print("❌ Invalid URL format. Please ensure it starts with http:// or https://")
            return None

        return url

    def display_results(self, results: dict) -> None:
        """
        Display extraction results in a formatted manner.

        Args:
            results: Dictionary containing extraction results
        """
        if not results.get("success"):
            print("\n" + "="*70)
            print("❌ EXTRACTION FAILED")
            print("="*70)
            print(f"Error: {results.get('error', 'Unknown error occurred')}")
            return

        data = results.get("data", {})

        print("\n" + "="*70)
        print("✅ EXTRACTION SUCCESSFUL")
        print("="*70)
        print(f"\n📍 Website: {results.get('url', 'N/A')}")

        # Display Overview
        print("\n" + "-"*70)
        print("📋 WEBSITE OVERVIEW:")
        print("-"*70)
        overview = data.get("overview", "No overview available")
        print(f"{overview[:500]}..." if len(overview) > 500 else overview)

        # Display Services
        print("\n" + "-"*70)
        print("🛍️  SERVICES/PRODUCTS:")
        print("-"*70)
        services = data.get("services", [])
        if services:
            for idx, service in enumerate(services[:5], 1):
                print(f"  {idx}. {service[:80]}...")
        else:
            print("  No services found")

        # Display Contact Information
        print("\n" + "-"*70)
        print("📞 CONTACT INFORMATION:")
        print("-"*70)
        contacts = data.get("contacts", {})

        emails = contacts.get("emails", [])
        if emails:
            print("  📧 Emails:")
            for email in emails[:5]:
                print(f"     • {email}")
        else:
            print("  📧 No emails found")

        phones = contacts.get("phones", [])
        if phones:
            print("  📱 Phone Numbers:")
            for phone in phones[:5]:
                print(f"     • {phone}")
        else:
            print("  📱 No phone numbers found")

        addresses = contacts.get("addresses", [])
        if addresses:
            print("  🏢 Addresses:")
            for address in addresses[:3]:
                print(f"     • {address}")
        else:
            print("  🏢 No addresses found")

        # Display People
        print("\n" + "-"*70)
        print("👥 TEAM MEMBERS:")
        print("-"*70)
        people = data.get("people", [])
        if people:
            for idx, person in enumerate(people[:5], 1):
                name = person.get("name", "N/A")
                designation = person.get("designation", "N/A")
                print(f"  {idx}. {name}")
                print(f"     Designation: {designation}")
        else:
            print("  No team members found")

        # Option to export JSON
        print("\n" + "-"*70)
        self.offer_json_export(data)

    def send_to_webhook(self, data: dict, webhook_url: str) -> None:
        """
        Send JSON data to a webhook URL via POST.

        Args:
            data: Extracted data to send
            webhook_url: Destination URL for webhook
        """
        try:
            headers = {'Content-Type': 'application/json'}
            response = requests.post(webhook_url, json=data, headers=headers, timeout=30)
            response.raise_for_status()
            print(f"✅ Payload successfully sent to webhook: {webhook_url} (status {response.status_code})")
        except requests.RequestException as e:
            print(f"❌ Webhook request failed: {str(e)}")

    def offer_json_export(self, data: dict) -> None:
        """
        Offer to export results as JSON file or send to webhook.

        Args:
            data: Extracted data to export
        """
        choice = input("Choose output destination: file / webhook / none (default file): ").strip().lower() or "file"

        if choice in ["webhook", "hook"]:
            webhook_url = WEBHOOK_URL
            if not webhook_url:
                webhook_url = input("Enter webhook URL (or set WEBHOOK_URL in .env): ").strip()
            if not webhook_url:
                print("❌ Webhook URL is not configured.")
                return
            self.send_to_webhook(data, webhook_url)
            return

        if choice in ["file", "f"]:
            filename = input("Enter filename (default: 'extraction_results.json'): ").strip()
            if not filename:
                filename = "extraction_results.json"

            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=OUTPUT_JSON_INDENT, ensure_ascii=False)
                print(f"✅ Results exported to '{filename}'")
            except Exception as e:
                print(f"❌ Error exporting JSON: {str(e)}")
            return

        print("ℹ️  No output destination selected.")

    def run_interactive(self) -> None:
        """Run the application in interactive mode."""
        while True:
            url = self.get_user_input()
            if not url:
                continue

            print(f"\n🔄 Starting scraping process for: {url}")
            print("This may take a few moments...\n")

            # Execute scraping and extraction
            results = self.crew.scrape_and_extract(url=url, max_pages=5)

            # Display results
            self.display_results(results)

            # Ask if user wants to scrape another URL
            print("\n" + "="*70)
            another = input("Would you like to scrape another website? (yes/no): ").strip().lower()
            if another not in ["yes", "y"]:
                print("\n👋 Thank you for using CrewAI Web Scraper. Goodbye!")
                break

    def run_cli(self, url: str) -> None:
        """
        Run the application with command-line argument.

        Args:
            url: URL to scrape
        """
        if not self.validate_url(url):
            print(f"❌ Invalid URL: {url}")
            sys.exit(1)

        print(f"🔄 Starting scraping process for: {url}\n")
        results = self.crew.scrape_and_extract(url=url, max_pages=5)
        self.display_results(results)

        # Output JSON to stdout for piping
        if results.get("success"):
            print("\n" + "="*70)
            print("📄 RAW JSON OUTPUT:")
            print("="*70)
            print(json.dumps(results.get("data", {}), indent=OUTPUT_JSON_INDENT, ensure_ascii=False))


def main():
    """
    Main entry point of the application.
    Handles command-line arguments and interactive mode.
    """
    app = WebScraperApp()

    # Check for command-line arguments
    if len(sys.argv) > 1:
        # Run with provided URL
        url = sys.argv[1]
        app.run_cli(url)
    else:
        # Run in interactive mode
        app.run_interactive()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Application interrupted by user.")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}", exc_info=True)
        print(f"\n❌ Fatal error: {str(e)}")
        sys.exit(1)
