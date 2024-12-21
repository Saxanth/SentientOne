import pytest
import os
from unittest.mock import patch, MagicMock
from examples.providers.perplexity_examples import (
    basic_search_example,
    advanced_search_example,
    error_handling_example,
    main
)

@pytest.fixture
def mock_provider():
    with patch('examples.providers.perplexity_examples.PerplexityProvider') as mock:
        provider_instance = MagicMock()
        mock.return_value = provider_instance
        yield provider_instance

@pytest.fixture
def sample_search_results():
    return [
        {
            'title': 'Test Title 1',
            'url': 'http://example.com/1',
            'snippet': 'Test snippet 1'
        },
        {
            'title': 'Test Title 2',
            'url': 'http://example.com/2',
            'snippet': 'Test snippet 2'
        }
    ]

@pytest.mark.asyncio
async def test_basic_search_example(mock_provider, sample_search_results):
    mock_provider.process.return_value = sample_search_results
    
    with patch('builtins.print') as mock_print:
        await basic_search_example()
    
    mock_provider.process.assert_called_once_with("What is artificial intelligence?")
    assert mock_print.call_count > 0

@pytest.mark.asyncio
async def test_basic_search_example_error(mock_provider):
    mock_provider.process.side_effect = Exception("Test error")
    
    with patch('builtins.print') as mock_print:
        await basic_search_example()
    
    mock_print.assert_called_with("Error in basic search: Test error")

@pytest.mark.asyncio
async def test_advanced_search_example(mock_provider, sample_search_results):
    mock_provider.process.return_value = sample_search_results[:3]
    
    with patch('builtins.print') as mock_print:
        await advanced_search_example()
    
    mock_provider.process.assert_called_once_with({
        "query": "Latest developments in quantum computing",
        "max_results": 3
    })
    assert mock_print.call_count > 0

@pytest.mark.asyncio
async def test_advanced_search_example_error(mock_provider):
    mock_provider.process.side_effect = Exception("Test error")
    
    with patch('builtins.print') as mock_print:
        await advanced_search_example()
    
    mock_print.assert_called_with("Error in advanced search: Test error")

@pytest.mark.asyncio
async def test_error_handling_example_no_api_key(mock_provider):
    mock_provider.process.side_effect = ValueError("No API key provided")
    
    with patch('builtins.print') as mock_print:
        await error_handling_example()
    
    assert any("Expected error (no API key)" in str(call) for call in mock_print.call_args_list)

@pytest.mark.asyncio
async def test_error_handling_example_empty_query(mock_provider):
    # First call succeeds, second call raises ValueError
    mock_provider.process.side_effect = [
        ValueError("No API key provided"),
        ValueError("Empty query")
    ]
    
    with patch('builtins.print') as mock_print:
        await error_handling_example()
    
    assert any("Expected error (empty query)" in str(call) for call in mock_print.call_args_list)

@pytest.mark.asyncio
async def test_main():
    with patch('examples.providers.perplexity_examples.basic_search_example') as mock_basic, \
         patch('examples.providers.perplexity_examples.advanced_search_example') as mock_advanced, \
         patch('examples.providers.perplexity_examples.error_handling_example') as mock_error, \
         patch('builtins.print'):
        await main()
    
    mock_basic.assert_called_once()
    mock_advanced.assert_called_once()
    mock_error.assert_called_once()
