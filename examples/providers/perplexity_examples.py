"""
Examples demonstrating the usage of the Perplexity provider.

This module shows various ways to use the Perplexity provider for:
- Basic text queries
- Advanced search options
- Error handling
"""

import asyncio
import os
from framework.core import PerplexityProvider

async def basic_search_example():
    """Demonstrate basic string query search."""
    provider = PerplexityProvider(api_key=os.getenv("PERPLEXITY_API_KEY"))
    
    query = "What is artificial intelligence?"
    try:
        results = await provider.process(query)
        print(f"\nBasic Search Results for: {query}\n")
        for i, result in enumerate(results, 1):
            print(f"{i}. {result['title']}")
            print(f"   URL: {result['url']}")
            print(f"   {result['snippet']}\n")
    except Exception as e:
        print(f"Error in basic search: {e}")

async def advanced_search_example():
    """Demonstrate advanced search options."""
    provider = PerplexityProvider(api_key=os.getenv("PERPLEXITY_API_KEY"))
    
    try:
        # Example with max results specified
        results = await provider.process({
            "query": "Latest developments in quantum computing",
            "max_results": 3
        })
        
        print(f"\nAdvanced Search Results (Top 3):\n")
        for i, result in enumerate(results, 1):
            print(f"{i}. {result['title']}")
            print(f"   URL: {result['url']}")
            print(f"   {result['snippet']}\n")
    except Exception as e:
        print(f"Error in advanced search: {e}")

async def error_handling_example():
    """Demonstrate error handling scenarios."""
    # Example without API key
    provider = PerplexityProvider()
    try:
        await provider.process("This should fail")
    except ValueError as e:
        print(f"\nExpected error (no API key): {e}")
    
    # Example with empty query
    provider = PerplexityProvider(api_key=os.getenv("PERPLEXITY_API_KEY"))
    try:
        await provider.process({"query": ""})
    except ValueError as e:
        print(f"Expected error (empty query): {e}")

async def main():
    """Run all examples."""
    print("=== Perplexity Provider Examples ===\n")
    
    print("1. Basic Search Example")
    await basic_search_example()
    
    print("\n2. Advanced Search Example")
    await advanced_search_example()
    
    print("\n3. Error Handling Example")
    await error_handling_example()

if __name__ == "__main__":
    asyncio.run(main())
