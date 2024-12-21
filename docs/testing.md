# SentientOne Testing Documentation

## Overview
This document describes the testing infrastructure and practices for the SentientOne project.

## Test Structure
```
tests/
├── base/                   # Base provider tests
│   └── providers/         # Provider implementation tests
├── core/                  # Core provider tests
│   └── providers/        # Specific provider tests
└── integration/          # Integration tests
```

## Running Tests

### Basic Test Execution
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/path/to/test_file.py

# Run with verbose output
pytest -v
```

### Test Coverage
```bash
# Run tests with coverage report
pytest --cov=framework

# Generate HTML coverage report
pytest --cov=framework --cov-report=html
```

## Test Categories

### Base Provider Tests
Tests for the base provider functionality including:
- Provider creation and configuration
- Mode management (PASSIVE/ACTIVE/ADAPTIVE)
- Context management
- Interaction history
- Error handling

### Perplexity Provider Tests
Tests for the Perplexity search provider including:
- Search functionality
- API interaction
- Result processing
- Error handling
- Input validation

### Integration Tests
Tests for provider interactions and system-wide functionality.

## Test Fixtures

### Common Fixtures
- `event_loop`: Async event loop for testing async functions
- `base_provider_fixture`: Base provider instance
- `mock_logger`: Mock logger for testing logging functionality

### Provider-Specific Fixtures
- `perplexity_provider`: Perplexity provider instance
- `mock_search_response`: Mock API response data

## Async Testing
The project uses pytest-asyncio for testing asynchronous code. Key points:
- Use `@pytest.mark.asyncio` for async test functions
- Configure event loop scope in pytest.ini
- Handle async context managers properly in tests

## Best Practices
1. Keep tests focused and isolated
2. Use appropriate fixtures for setup/teardown
3. Mock external dependencies
4. Test both success and error cases
5. Maintain high test coverage
6. Document complex test scenarios

## Adding New Tests
When adding new tests:
1. Follow the existing directory structure
2. Create appropriate fixtures
3. Test all critical functionality
4. Include both positive and negative test cases
5. Update this documentation as needed
