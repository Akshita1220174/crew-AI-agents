"""
CrewAI Agent Configuration for Web Scraping and Data Extraction.
Defines the agent, tools, and tasks for intelligent web scraping.
"""

import logging
from crewai import Agent, Task, Crew
from utils.web_scraper import WebScraper
from utils.data_extractor import DataExtractor
from utils.llm_handler import LLMHandler
from config import OPENAI_API_KEY

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WebScrapingCrew:
    """
    Orchestrates CrewAI agents and tasks for web scraping and data extraction.
    """

    def __init__(self):
        """Initialize the web scraping crew with required components."""
        self.web_scraper = WebScraper()
        self.data_extractor = DataExtractor()
        self.llm_handler = LLMHandler()
        self.crew = None

    def _create_web_researcher_agent(self) -> Agent:
        """
        Create the Web Researcher/Scraper agent.
        This agent is responsible for fetching and analyzing website content.

        Returns:
            Agent: CrewAI Agent configured for web scraping
        """
        agent = Agent(
            role="Web Researcher",
            goal="Scrape website content, extract structured information, and provide comprehensive analysis.",
            backstory="""You are an expert web researcher with deep knowledge of website structures,
            data extraction techniques, and information organization. You excel at identifying
            key information about businesses, services, and people from websites. You are thorough,
            accurate, and attention to detail is your strength.""",
            verbose=True,
            allow_delegation=False
        )
        return agent

    def _create_data_extraction_task(self, agent: Agent, url: str) -> Task:
        """
        Create the data extraction task.

        Args:
            agent: The agent that will execute this task
            url: The website URL to scrape

        Returns:
            Task: CrewAI Task for data extraction
        """
        task = Task(
            description=f"""Analyze and extract structured information from the website: {url}
            
            Follow these steps:
            1. Validate the URL is accessible and properly formatted
            2. Scrape the website content (multiple pages if possible)
            3. Extract the following information:
               - General website overview (what the site is about)
               - Services or products offered
               - Contact information (emails, phone numbers, addresses)
               - Human-related details (names, designations, team members, authors)
            4. Organize all extracted data in a structured JSON format
            5. Return the results in the specified JSON schema
            
            Return the extracted data as JSON with this exact structure:
            {{
                "overview": "Website summary",
                "services": ["service1", "service2"],
                "contacts": {{
                    "emails": ["email@example.com"],
                    "phones": ["123-456-7890"],
                    "addresses": ["123 Main St"]
                }},
                "people": [
                    {{"name": "John Doe", "designation": "CEO"}}
                ]
            }}""",
            expected_output="Structured JSON data with website information",
            agent=agent
        )
        return task

    def scrape_and_extract(self, url: str, max_pages: int = 5) -> dict:
        """
        Execute the web scraping and data extraction pipeline.

        Args:
            url: Website URL to scrape
            max_pages: Maximum number of pages to scrape

        Returns:
            dict: Structured extraction results
        """
        try:
            logger.info(f"Starting web scraping pipeline for: {url}")

            # Step 1: Web Scraping
            logger.info("Step 1: Fetching website content...")
            scraped_data = self.web_scraper.scrape_website(
                url=url,
                max_pages=max_pages,
                follow_links=True
            )

            if "error" in scraped_data:
                logger.error(f"Scraping error: {scraped_data['error']}")
                return {
                    "success": False,
                    "error": scraped_data["error"],
                    "data": None
                }

            logger.info(f"Successfully scraped {scraped_data['total_pages_scraped']} pages")

            # Step 2: LLM-based Summarization
            logger.info("Step 2: Generating AI summary...")
            if scraped_data.get("pages"):
                main_content = scraped_data["pages"][0].get("content", "")
                summary = self.llm_handler.summarize_content(main_content)
            else:
                summary = ""

            # Step 3: Data Extraction and Structuring
            logger.info("Step 3: Structuring extracted data...")
            structured_data = self.data_extractor.structure_data(
                scraped_data=scraped_data,
                llm_summary=summary
            )

            # Step 4: LLM-based Data Cleaning (Optional)
            logger.info("Step 4: Cleaning and validating data...")
            # Only clean if we have valid contact information
            if structured_data.get("contacts", {}).get("emails"):
                cleaned_data = self.llm_handler.clean_data(structured_data)
                structured_data = cleaned_data

            logger.info("Web scraping pipeline completed successfully")

            return {
                "success": True,
                "url": url,
                "data": structured_data
            }

        except Exception as e:
            logger.error(f"Error in scraping pipeline: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "data": None
            }

    def create_crew(self) -> Crew:
        """
        Create and configure the CrewAI Crew.

        Returns:
            Crew: Configured CrewAI Crew instance
        """
        try:
            # Create agent
            web_researcher_agent = self._create_web_researcher_agent()

            # Create a placeholder URL for crew initialization
            # In actual usage, this will be replaced with real URLs
            placeholder_url = "https://example.com"
            data_extraction_task = self._create_data_extraction_task(
                web_researcher_agent,
                placeholder_url
            )

            # Create crew
            self.crew = Crew(
                agents=[web_researcher_agent],
                tasks=[data_extraction_task],
                verbose=True
            )

            logger.info("CrewAI Crew created successfully")
            return self.crew

        except Exception as e:
            logger.error(f"Error creating crew: {str(e)}")
            return None
