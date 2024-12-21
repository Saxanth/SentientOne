# SentientOne Examples

This directory contains example implementations and usage patterns for the SentientOne framework.

## Directory Structure

```
examples/
├── providers/           # Provider-specific examples
│   ├── __init__.py
│   └── perplexity_examples.py
└── README.md           # This file
```

## Running Examples

### Provider Examples

#### Perplexity Provider
```bash
# Set your API key
export PERPLEXITY_API_KEY=your_api_key_here

# Run the examples
python -m examples.providers.perplexity_examples
```

The perplexity examples demonstrate:
- Basic text queries
- Advanced search options with parameters
- Error handling scenarios

## Adding New Examples

When adding new examples:
1. Create a new file in the appropriate subdirectory
2. Include comprehensive docstrings and comments
3. Demonstrate both basic and advanced usage
4. Include error handling examples
5. Update this README.md with running instructions
