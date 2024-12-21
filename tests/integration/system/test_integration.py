"""Integration tests for the system."""
import pytest
from typing import Dict, Any
from unittest.mock import patch
import aiohttp
from framework.core.providers.perplexity_provider import PerplexityProvider
from framework.base.providers.baseprovider import BaseProvider, ProviderMode
from tests.utils.test_helpers import (
    create_mock_provider,
    async_test,
    MockHTTPSession,
    create_test_config
)

def test_provider_inheritance():
    """Test provider inheritance chain."""
    assert issubclass(PerplexityProvider, BaseProvider)

@async_test
async def test_provider_interaction():
    """Test provider interactions."""
    # Create providers
    perplexity = PerplexityProvider(
        api_key="test_key",
        mode=ProviderMode.ACTIVE
    )
    mock = create_mock_provider(BaseProvider, mode=ProviderMode.PASSIVE)
    
    # Mock response data
    mock_response = {
        "results": [
            {
                "title": "Test Result",
                "url": "https://test.com",
                "snippet": "Test content"
            }
        ]
    }

    # Configure providers
    perplexity.configure(create_test_config())
    mock.configure(create_test_config())

    # Test interactions
    session = MockHTTPSession(mock_response)
    with patch('aiohttp.ClientSession', return_value=session):
        results = await perplexity.process("test query")
        mock_result = await mock.process("test input")
    
    # Verify results
    assert len(results) == 1
    assert results[0]["title"] == "Test Result"
    assert mock_result == "Processed: test input"
    
    # Verify provider states
    assert perplexity.mode == ProviderMode.ACTIVE
    assert mock.mode == ProviderMode.PASSIVE

@async_test
async def test_system_integration():
    """Test full system integration."""
    # Create multiple providers
    providers = {
        "perplexity": PerplexityProvider(
            api_key="test_key",
            mode=ProviderMode.ACTIVE
        ),
        "mock": create_mock_provider(BaseProvider, mode=ProviderMode.PASSIVE)
    }
    
    # Configure providers
    for provider in providers.values():
        provider.configure(create_test_config())
    
    # Test system-wide operations
    for name, provider in providers.items():
        assert isinstance(provider, BaseProvider)
        if name == "perplexity":
            assert provider.mode == ProviderMode.ACTIVE
        else:
            assert provider.mode == ProviderMode.PASSIVE

@pytest.mark.parametrize("provider_class,config", [
    (PerplexityProvider, None),
    (create_mock_provider(BaseProvider), None),
])
@async_test
async def test_error_propagation(provider_class, config):
    """Test error handling across providers."""
    # Create provider instance
    if isinstance(provider_class, type):
        provider = provider_class(api_key=None)  # Initialize with None API key
    else:
        provider = provider_class
        
    # Test error handling for invalid config type
    with pytest.raises(TypeError, match="Configuration must be a dictionary"):
        provider.configure("invalid")
            
    # Test error handling for missing API key
    if isinstance(provider, PerplexityProvider):
        with pytest.raises(ValueError, match="API key is required"):
            await provider.search("test")

@async_test
async def test_provider_state_management():
    """Test provider state management."""
    provider = PerplexityProvider(
        api_key="test_key",
        mode=ProviderMode.ACTIVE
    )
    
    # Configure provider
    config = create_test_config()
    provider.configure(config)
    
    # Test state changes
    provider.configure({"max_results": 5})
    assert provider._config["max_results"] == 5
    
    # Test mode changes
    provider.mode = ProviderMode.PASSIVE
    assert provider.mode == ProviderMode.PASSIVE

@pytest.mark.parametrize("provider_class", [PerplexityProvider])
def test_provider_compliance(provider_class):
    """Test provider compliance with base interface."""
    provider = provider_class(api_key="test_key")
    
    # Test required attributes
    assert hasattr(provider, "mode")
    assert hasattr(provider, "configure")
    assert hasattr(provider, "process")
