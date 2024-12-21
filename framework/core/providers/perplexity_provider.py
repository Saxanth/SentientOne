"""Perplexity API provider implementation."""
from typing import Dict, Any, List, Optional
import aiohttp
from framework.base.providers.baseprovider import BaseProvider, ProviderMode

class PerplexityProvider(BaseProvider):
    """Provider for Perplexity API integration."""

    def __init__(self, api_key: Optional[str] = None, mode: ProviderMode = ProviderMode.PASSIVE):
        """Initialize the provider.
        
        Args:
            api_key: API key for authentication
            mode: Provider mode (ACTIVE/PASSIVE)
        """
        if not isinstance(mode, ProviderMode):
            raise ValueError(f"Mode must be a ProviderMode enum value, got {type(mode)}")
        super().__init__(mode=mode)
        self.api_key = api_key
        self.base_url = "https://api.perplexity.ai/search"
        self._config = {}

    def configure(self, config: Optional[Dict[str, Any]]) -> None:
        """Configure the provider with the given settings.
        
        Args:
            config: Configuration dictionary
            
        Raises:
            TypeError: If config is not a dictionary or is None
        """
        if config is None:
            raise TypeError("Configuration cannot be None")
        if not isinstance(config, dict):
            raise TypeError("Configuration must be a dictionary")
        self._config = config.copy()

    async def process(self, input_data: Any) -> List[Dict[str, str]]:
        """Process the input query and return search results.
        
        Args:
            input_data: Input query string or dictionary
            
        Returns:
            List of search results
            
        Raises:
            ValueError: If input is invalid
        """
        if isinstance(input_data, dict):
            query = input_data.get("query", "")
            max_results = input_data.get("max_results", 10)
        else:
            query = str(input_data)
            max_results = 10

        if not query.strip():
            raise ValueError("Search query is required")

        return await self.search(query, max_results)

    async def search(self, query: str, max_results: int = 10) -> List[Dict[str, str]]:
        """Perform a search using the Perplexity API.
        
        Args:
            query: Search query string
            max_results: Maximum number of results to return
            
        Returns:
            List of search results
            
        Raises:
            ValueError: If API key is missing
            Exception: If API request fails
        """
        if not self.api_key:
            raise ValueError("API key is required")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.base_url,
                json={"query": query, "max_results": max_results},
                headers=headers
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"Search failed: {error_text}")
                
                data = await response.json()
                return self._process_results(data)

    def _process_results(self, data: Dict[str, Any]) -> List[Dict[str, str]]:
        """Process the API response into a standardized format.
        
        Args:
            data: Raw API response data
            
        Returns:
            List of processed search results
        """
        results = []
        for item in data.get("results", []):
            result = {
                "title": item.get("title", ""),
                "url": item.get("url", ""),
                "snippet": item.get("snippet", "")
            }
            results.append(result)
        return results
