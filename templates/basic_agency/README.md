# Basic Agency Template

A lightweight template for building AI agent systems with essential functionality.

## Features
- Core agency structure
- Base agent implementation
- Simple configuration management
- Built-in validation

## Directory Structure
```
basic_agency/
├── base/           # Base agent implementation
├── config/         # Configuration management
├── core/           # Core framework components
└── specialized/    # Minimal specialized components
```

## Quick Start
1. Copy this template to your project
2. Update config.yaml with your settings
3. Initialize your Agency:
```python
from basic_agency import Agency, config

# Load configuration
agency = Agency(config)

# Add departments
agency.add_department("research")
agency.add_department("development")

# Start agency
agency.start()
```

## Configuration
See `config.yaml` for configuration options:
- Department settings
- Agent settings
- Task orchestration
- Metrics collection
- Logging

## Extending
1. Add new specialized agents in `specialized/`
2. Create new departments as needed
3. Implement custom validation in `config/validation.py`

## Best Practices
- Keep agent implementations simple
- Use configuration for customization
- Validate all settings
- Follow KISS principles
