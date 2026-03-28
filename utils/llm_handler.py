"""
LLM Handler Module - Manages integration with LLM providers.
Supports OpenAI and Google Gemini for summarization and data cleaning.
"""

import logging
from typing import Optional
from config import (
    OPENAI_API_KEY, OPENAI_MODEL,
    GEMINI_API_KEY, GEMINI_MODEL,
    LLM_PROVIDER
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LLMHandler:
    """
    Handles LLM interactions for summarization and data processing.
    Supports both OpenAI GPT models and Google Gemini with automatic fallback.
    """

    def __init__(
        self,
        provider: Optional[str] = None,
        api_key: Optional[str] = None,
        model: Optional[str] = None
    ):
        """
        Initialize LLM handler.

        Args:
            provider: LLM provider ("openai" or "gemini"), uses config if None
            api_key: API key (uses config if None)
            model: Model name (uses config if None)
        """
        self.provider = provider or LLM_PROVIDER
        self.openai_client = None
        self.gemini_client = None
        self.model = None
        self.active_provider = None

        # Try to initialize the preferred provider
        if self.provider == "openai":
            self._init_openai(api_key, model)
            if not self.openai_client and GEMINI_API_KEY:
                logger.info("OpenAI not available. Falling back to Gemini.")
                self._init_gemini(GEMINI_API_KEY, GEMINI_MODEL)
        else:  # Gemini preferred
            self._init_gemini(api_key, model)
            if not self.gemini_client and OPENAI_API_KEY:
                logger.info("Gemini not available. Falling back to OpenAI.")
                self._init_openai(OPENAI_API_KEY, OPENAI_MODEL)

    def _init_openai(self, api_key: Optional[str], model: Optional[str]) -> None:
        """Initialize OpenAI client."""
        try:
            api_key = api_key or OPENAI_API_KEY
            if not api_key:
                return

            from openai import OpenAI
            self.openai_client = OpenAI(api_key=api_key)
            self.model = model or OPENAI_MODEL
            self.active_provider = "openai"
            logger.info(f"✓ OpenAI initialized with model: {self.model}")
        except Exception as e:
            logger.debug(f"OpenAI initialization failed: {str(e)}")
            self.openai_client = None

    def _init_gemini(self, api_key: Optional[str], model: Optional[str]) -> None:
        """Initialize Google Gemini client."""
        try:
            api_key = api_key or GEMINI_API_KEY
            if not api_key:
                return

            import google.generativeai as genai
            genai.configure(api_key=api_key)
            self.gemini_client = genai
            self.model = model or GEMINI_MODEL
            self.active_provider = "gemini"
            logger.info(f"✓ Google Gemini initialized with model: {self.model}")
        except Exception as e:
            logger.debug(f"Gemini initialization failed: {str(e)}")
            self.gemini_client = None

    def summarize_content(
        self,
        content: str,
        max_length: int = 500
    ) -> str:
        """
        Summarize website content using the active LLM provider.

        Args:
            content: Text content to summarize
            max_length: Maximum length of summary

        Returns:
            str: Summarized content
        """
        if not self.openai_client and not self.gemini_client:
            logger.warning("No LLM client available. Returning original content preview.")
            return content[:max_length]

        try:
            if self.active_provider == "openai":
                return self._summarize_openai(content, max_length)
            else:  # gemini
                return self._summarize_gemini(content, max_length)
        except Exception as e:
            logger.error(f"Error during summarization: {str(e)}")
            return content[:max_length]

    def _summarize_openai(self, content: str, max_length: int) -> str:
        """Summarize using OpenAI."""
        try:
            prompt = f"""
            Please provide a concise summary of the following website content in {max_length} characters or less.
            Focus on the main purpose and key offerings of the website.

            Content:
            {content[:2000]}
            """

            response = self.openai_client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a website analyst. Provide concise summaries."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.5
            )

            summary = response.choices[0].message.content.strip()
            logger.info("✓ Content summarized using OpenAI")
            return summary
        except Exception as e:
            logger.error(f"OpenAI summarization error: {str(e)}")
            raise

    def _summarize_gemini(self, content: str, max_length: int) -> str:
        """Summarize using Google Gemini."""
        try:
            model = self.gemini_client.GenerativeModel(self.model)
            
            prompt = f"""
            Please provide a concise summary of the following website content in {max_length} characters or less.
            Focus on the main purpose and key offerings of the website.

            Content:
            {content[:2000]}
            """

            response = model.generate_content(prompt)
            summary = response.text.strip()
            logger.info("✓ Content summarized using Gemini")
            return summary
        except Exception as e:
            logger.error(f"Gemini summarization error: {str(e)}")
            raise

    def extract_services(self, content: str) -> list:
        """
        Extract and clean services/products using the active LLM provider.

        Args:
            content: Text content to analyze

        Returns:
            List of identified services
        """
        if not self.openai_client and not self.gemini_client:
            logger.warning("No LLM client available. Using basic extraction.")
            return []

        try:
            if self.active_provider == "openai":
                return self._extract_services_openai(content)
            else:  # gemini
                return self._extract_services_gemini(content)
        except Exception as e:
            logger.error(f"Error during service extraction: {str(e)}")
            return []

    def _extract_services_openai(self, content: str) -> list:
        """Extract services using OpenAI."""
        try:
            prompt = f"""
            From the following website content, identify and list the main services or products offered.
            Return only a JSON array of strings, without markdown formatting or code blocks.
            Example format: ["Service 1", "Service 2", "Service 3"]

            Content:
            {content[:2000]}
            """

            response = self.openai_client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a business analyst. Extract services accurately."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.3
            )

            services_text = response.choices[0].message.content.strip()
            return self._parse_services_json(services_text)

        except Exception as e:
            logger.error(f"OpenAI service extraction error: {str(e)}")
            raise

    def _extract_services_gemini(self, content: str) -> list:
        """Extract services using Google Gemini."""
        try:
            model = self.gemini_client.GenerativeModel(self.model)
            
            prompt = f"""
            From the following website content, identify and list the main services or products offered.
            Return only a JSON array of strings, without markdown formatting or code blocks.
            Example format: ["Service 1", "Service 2", "Service 3"]

            Content:
            {content[:2000]}
            """

            response = model.generate_content(prompt)
            services_text = response.text.strip()
            return self._parse_services_json(services_text)

        except Exception as e:
            logger.error(f"Gemini service extraction error: {str(e)}")
            raise

    def _parse_services_json(self, services_text: str) -> list:
        """Parse services from JSON response."""
        import json
        try:
            # Remove markdown code blocks if present
            if "```" in services_text:
                services_text = services_text.split("```")[1]
                if services_text.startswith("json"):
                    services_text = services_text[4:]

            services = json.loads(services_text)
            logger.info(f"✓ Extracted {len(services)} services")
            return services[:10]
        except json.JSONDecodeError:
            logger.warning("Could not parse services response as JSON")
            return []

    def clean_data(self, data_dict: dict) -> dict:
        """
        Clean and organize extracted data using the active LLM provider.

        Args:
            data_dict: Dictionary with extracted data

        Returns:
            Cleaned data dictionary
        """
        if not self.openai_client and not self.gemini_client:
            logger.warning("No LLM client available. Returning original data.")
            return data_dict

        try:
            if self.active_provider == "openai":
                return self._clean_data_openai(data_dict)
            else:  # gemini
                return self._clean_data_gemini(data_dict)
        except Exception as e:
            logger.error(f"Error during data cleaning: {str(e)}")
            return data_dict

    def _clean_data_openai(self, data_dict: dict) -> dict:
        """Clean data using OpenAI."""
        try:
            prompt = f"""
            Review and clean the following extracted website data. 
            Remove duplicates, fix formatting, and organize it logically.
            Return a JSON object with the structure:
            {{"overview": "...", "services": [...], "contacts": {{"emails": [...], "phones": [...], "addresses": [...]}}, "people": [...]}}

            Original data:
            {str(data_dict)}
            """

            response = self.openai_client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a data cleaning specialist."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.3
            )

            cleaned_text = response.choices[0].message.content.strip()
            return self._parse_cleaned_json(cleaned_text, data_dict)

        except Exception as e:
            logger.error(f"OpenAI data cleaning error: {str(e)}")
            raise

    def _clean_data_gemini(self, data_dict: dict) -> dict:
        """Clean data using Google Gemini."""
        try:
            model = self.gemini_client.GenerativeModel(self.model)
            
            prompt = f"""
            Review and clean the following extracted website data. 
            Remove duplicates, fix formatting, and organize it logically.
            Return a JSON object with the structure:
            {{"overview": "...", "services": [...], "contacts": {{"emails": [...], "phones": [...], "addresses": [...]}}, "people": [...]}}

            Original data:
            {str(data_dict)}
            """

            response = model.generate_content(prompt)
            cleaned_text = response.text.strip()
            return self._parse_cleaned_json(cleaned_text, data_dict)

        except Exception as e:
            logger.error(f"Gemini data cleaning error: {str(e)}")
            raise

    def _parse_cleaned_json(self, cleaned_text: str, original_data: dict) -> dict:
        """Parse cleaned data from JSON response."""
        import json
        try:
            # Remove markdown code blocks if present
            if "```" in cleaned_text:
                cleaned_text = cleaned_text.split("```")[1]
                if cleaned_text.startswith("json"):
                    cleaned_text = cleaned_text[4:]

            cleaned_data = json.loads(cleaned_text)
            logger.info("✓ Data cleaning successful")
            return cleaned_data
        except json.JSONDecodeError:
            logger.warning("Could not parse cleaned data as JSON")
            return original_data

    def validate_response(self, response: str) -> bool:
        """
        Validate LLM response format.

        Args:
            response: Response to validate

        Returns:
            bool: True if response is valid
        """
        return isinstance(response, str) and len(response.strip()) > 0

    def get_provider_info(self) -> dict:
        """
        Get information about the active LLM provider.

        Returns:
            dict: Provider information
        """
        return {
            "active_provider": self.active_provider,
            "model": self.model,
            "openai_available": self.openai_client is not None,
            "gemini_available": self.gemini_client is not None
        }
