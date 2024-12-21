"""Tests for the Perplexity provider."""
import pytest
from typing import Dict, Any
import os
from unittest.mock import patch, MagicMock
import sys

# Add project root to path to fix imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from framework.core.providers.perplexity_provider import PerplexityProvider
from framework.base.providers.baseprovider import ProviderMode

@pytest.fixture
def perplexity_provider():
    """Create a Perplexity provider instance."""
    return PerplexityProvider(
        api_key="test_key",
        mode=ProviderMode.ACTIVE
    )

@pytest.fixture
def mock_search_response():
    """Create a mock search API response."""
    return {
        "results": [
            {
                "title": "Test Result 1",
                "url": "https://test.com/1",
                "snippet": "This is test result 1"
            },
            {
                "title": "Test Result 2",
                "url": "https://test.com/2",
                "snippet": "This is test result 2"
            }
        ]
    }

def test_perplexity_provider_creation(perplexity_provider: PerplexityProvider):
    """Test perplexity provider instantiation."""
    assert isinstance(perplexity_provider, PerplexityProvider)
    assert perplexity_provider.mode == ProviderMode.ACTIVE
    assert perplexity_provider.api_key == "test_key"
    assert perplexity_provider.base_url == "https://api.perplexity.ai/search"

@pytest.mark.asyncio
async def test_perplexity_provider_process_string_input(perplexity_provider: PerplexityProvider, mock_search_response: Dict[str, Any]):
    """Test processing string input."""
    with patch('aiohttp.ClientSession.post') as mock_post:
        mock_post.return_value.__aenter__.return_value.status = 200
        mock_post.return_value.__aenter__.return_value.json.return_value = mock_search_response
        
        results = await perplexity_provider.process("test query")
        
        assert len(results) == 2
        assert results[0]["title"] == "Test Result 1"
        assert results[1]["url"] == "https://test.com/2"

@pytest.mark.asyncio
async def test_perplexity_provider_process_dict_input(perplexity_provider: PerplexityProvider, mock_search_response: Dict[str, Any]):
    """Test processing dictionary input."""
    with patch('aiohttp.ClientSession.post') as mock_post:
        mock_post.return_value.__aenter__.return_value.status = 200
        mock_post.return_value.__aenter__.return_value.json.return_value = mock_search_response
        
        results = await perplexity_provider.process({
            "query": "test query",
            "max_results": 3
        })
        
        mock_post.assert_called_once()
        call_kwargs = mock_post.call_args.kwargs
        assert call_kwargs["json"]["max_results"] == 3

@pytest.mark.asyncio
async def test_perplexity_provider_search(perplexity_provider: PerplexityProvider, mock_search_response: Dict[str, Any]):
    """Test search functionality."""
    with patch('aiohttp.ClientSession.post') as mock_post:
        mock_post.return_value.__aenter__.return_value.status = 200
        mock_post.return_value.__aenter__.return_value.json.return_value = mock_search_response
        
        results = await perplexity_provider.search("test query", max_results=2)
        
        assert len(results) == 2
        for result in results:
            assert "title" in result
            assert "url" in result
            assert "snippet" in result

@pytest.mark.asyncio
async def test_perplexity_provider_error_handling(perplexity_provider: PerplexityProvider):
    """Test error handling."""
    # Test missing API key
    perplexity_provider.api_key = None
    with pytest.raises(ValueError, match="API key is required"):
        await perplexity_provider.search("test query")

    # Test API error
    perplexity_provider.api_key = "test_key"
    with patch('aiohttp.ClientSession.post') as mock_post:
        mock_post.return_value.__aenter__.return_value.status = 400
        mock_post.return_value.__aenter__.return_value.text.return_value = "Bad Request"
        
        with pytest.raises(Exception, match="Search failed"):
            await perplexity_provider.search("test query")

def test_perplexity_provider_process_results(perplexity_provider: PerplexityProvider, mock_search_response: Dict[str, Any]):
    """Test results processing."""
    processed = perplexity_provider._process_results(mock_search_response)
    
    assert len(processed) == 2
    assert processed[0]["title"] == "Test Result 1"
    assert processed[0]["url"] == "https://test.com/1"
    assert processed[0]["snippet"] == "This is test result 1"

@pytest.mark.asyncio
async def test_perplexity_provider_empty_query(perplexity_provider: PerplexityProvider):
    """Test handling of empty queries."""
    with pytest.raises(ValueError, match="Search query is required"):
        await perplexity_provider.process({"query": ""})

    with pytest.raises(ValueError, match="Search query is required"):
        await perplexity_provider.process("")

def test_perplexity_provider_invalid_mode():
    """Test provider initialization with invalid mode."""
    with pytest.raises(ValueError, match="Mode must be a ProviderMode enum value"):
        PerplexityProvider(mode="invalid_mode")
