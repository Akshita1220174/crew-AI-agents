"""
Example Usage Script - Demonstrates how to use the CrewAI Web Scraper.
Run this script to see the scraper in action.
"""

import json
import sys
from agents.scrapper_agent import WebScrapingCrew

def main():
    """
    Example usage of the Web Scraper.
    """
    # Initialize the crew
    print("🚀 Initializing CrewAI Web Scraper...")
    crew = WebScrapingCrew()

    # Example URLs (using well-structured, scraper-friendly websites)
    example_urls = [
        "https://github.com",
        "https://wikipedia.org",
        "https://python.org",
    ]

    print("\n" + "="*70)
    print("CrewAI Web Scraper - Example Usage")
    print("="*70)

    # Option 1: Scrape the first example URL
    print("\n📍 Example 1: Scraping GitHub.com")
    print("-"*70)
    results = crew.scrape_and_extract(url="https://github.com", max_pages=3)

    if results['success']:
        data = results['data']
        print(f"\n✅ Scraping Successful!")
        print(f"   • Overview length: {len(data['overview'])} characters")
        print(f"   • Services found: {len(data['services'])}")
        print(f"   • Emails found: {len(data['contacts']['emails'])}")
        print(f"   • Phones found: {len(data['contacts']['phones'])}")
        print(f"   • Team members: {len(data['people'])}")
        
        # Display sample data
        if data['services']:
            print(f"\n   Services Sample:")
            for service in data['services'][:3]:
                print(f"   - {service[:60]}...")
    else:
        print(f"❌ Error: {results['error']}")

    # Option 2: User-provided URL
    print("\n" + "="*70)
    print("\n📍 Example 2: Custom URL Scraping")
    print("-"*70)
    
    custom_url = input("\nEnter a URL to scrape (or press Enter to skip): ").strip()
    if custom_url:
        if not custom_url.startswith(("http://", "https://")):
            custom_url = "https://" + custom_url
        
        print(f"\nScraping {custom_url}...")
        results = crew.scrape_and_extract(url=custom_url, max_pages=3)
        
        if results['success']:
            data = results['data']
            print(f"\n✅ Scraping Successful!")
            
            # Save results to file
            output_file = "example_output.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"💾 Results saved to {output_file}")
            
            # Display results
            print(f"\n📊 Extracted Data:")
            print(json.dumps(data, indent=2, ensure_ascii=False)[:800] + "...")
        else:
            print(f"❌ Error: {results['error']}")

    print("\n" + "="*70)
    print("✨ Example usage complete!")
    print("="*70)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Example interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)
