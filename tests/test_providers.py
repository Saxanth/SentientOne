import pytest
from typing import Type, Dict, Any
import importlib

from providers import BaseProvider

PROVIDER_MODULES = [
    'agents.base_agent_provider',
    'communication.base_communication_provider',
    'learning.base_learning_provider',
    'memory.base_memory_provider',
    'personas.base_persona_provider',
    'reasoning.base_reasoning_provider',
    'security.base_security_provider',
    'services.base_service_provider',
    'storage.base_storage_provider',
    'tools.base_tool_provider',
    'workflows.base_workflow_provider'
]

def import_provider_class(module_path: str) -> Type[BaseProvider]:
    """
    Dynamically import a provider class from a module path.
    
    Args:
        module_path (str): Dot-separated path to the module
    
    Returns:
        Type[BaseProvider]: The base provider class
    """
    module_name = f'providers.{module_path}'
    class_name = ''.join(word.capitalize() for word in module_path.split('.')[-1].split('_')[:-1])
    
    try:
        module = importlib.import_module(module_name)
        return getattr(module, class_name)
    except (ImportError, AttributeError) as e:
        pytest.fail(f"Could not import {module_name}: {e}")

def test_providers_import():
    """Verify that all providers can be imported successfully."""
    for module_path in PROVIDER_MODULES:
        provider_class = import_provider_class(module_path)
        assert provider_class is not None, f"Failed to import {module_path}"

def test_providers_basic_instantiation():
    """Verify that providers can be instantiated and have basic methods."""
    for module_path in PROVIDER_MODULES:
        provider_class = import_provider_class(module_path)
        
        # Instantiate provider
        provider = provider_class()
        
        # Check basic methods exist
        assert hasattr(provider, 'configure'), f"{provider_class.__name__} missing configure method"
        assert hasattr(provider, 'reset'), f"{provider_class.__name__} missing reset method"
        assert hasattr(provider, 'get_config'), f"{provider_class.__name__} missing get_config method"
        assert hasattr(provider, 'is_initialized'), f"{provider_class.__name__} missing is_initialized method"
        assert hasattr(provider, 'log'), f"{provider_class.__name__} missing log method"

def test_provider_configuration():
    """Test basic configuration and reset functionality."""
    for module_path in PROVIDER_MODULES:
        provider_class = import_provider_class(module_path)
        
        # Instantiate provider
        provider = provider_class()
        
        # Check initial state
        assert not provider.is_initialized()
        assert provider.get_config() == {}
        
        # Configure provider
        test_config = {"test_key": "test_value"}
        provider.configure(test_config)
        
        # Check configuration state
        assert provider.is_initialized()
        assert provider.get_config() == test_config
        
        # Reset provider
        provider.reset()
        
        # Check reset state
        assert not provider.is_initialized()
        assert provider.get_config() == {}

def test_provider_logging():
    """Test logging method."""
    for module_path in PROVIDER_MODULES:
        provider_class = import_provider_class(module_path)
        
        # Instantiate provider
        provider = provider_class()
        
        # Test logging methods
        try:
            provider.log("Test info message")
            provider.log("Test warning message", "warning")
            provider.log("Test error message", "error")
        except Exception as e:
            pytest.fail(f"Logging failed for {provider_class.__name__}: {e}")
