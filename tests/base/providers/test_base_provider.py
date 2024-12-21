import pytest
from typing import Dict, Any
import logging
from framework.base.providers.baseprovider import BaseProvider, ProviderMode, ProviderRegistry
from tests.utils.test_helpers import MockProvider, async_test

def test_base_provider_creation(base_provider_fixture: MockProvider):
    """Test base provider instantiation."""
    assert isinstance(base_provider_fixture, BaseProvider)
    assert base_provider_fixture.mode == ProviderMode.PASSIVE
    assert hasattr(base_provider_fixture, '_config')
    assert hasattr(base_provider_fixture, '_logger')

def test_base_provider_mode(base_provider_fixture: MockProvider):
    """Test provider mode settings."""
    # Test PASSIVE mode
    passive_provider = MockProvider(mode=ProviderMode.PASSIVE)
    assert passive_provider.mode == ProviderMode.PASSIVE
    assert passive_provider.sync_operation() == "sync_result"

    # Test ACTIVE mode
    active_provider = MockProvider(mode=ProviderMode.ACTIVE)
    assert active_provider.mode == ProviderMode.ACTIVE

@pytest.mark.asyncio
async def test_async_provider_operations(async_provider_fixture: MockProvider):
    """Test async provider operations."""
    result = await async_provider_fixture.async_operation()
    assert result == "async_result"

def test_base_provider_configuration(base_provider_fixture: MockProvider, test_config: Dict[str, Any]):
    """Test provider configuration."""
    # Reset provider to clear any previous configuration
    base_provider_fixture.reset()
    base_provider_fixture.configure_called = False
    
    # Test initial state
    assert not base_provider_fixture.configure_called
    assert isinstance(base_provider_fixture._context_memory, dict)

    # Test configuration
    base_provider_fixture.configure(test_config)
    assert base_provider_fixture.configure_called
    assert base_provider_fixture.get_config() == test_config

    # Test reset
    base_provider_fixture.reset()
    assert base_provider_fixture.reset_called
    assert not base_provider_fixture._context_memory

def test_base_provider_logging(base_provider_fixture: MockProvider, mock_logger):
    """Test provider logging capabilities."""
    base_provider_fixture._logger = mock_logger
    
    # Test logging
    test_message = "Test log message"
    base_provider_fixture._logger.info(test_message)
    mock_logger.info.assert_called_once_with(test_message)

def test_base_provider_error_handling(base_provider_fixture: MockProvider):
    """Test provider error handling."""
    # Test invalid configuration
    with pytest.raises(TypeError):
        base_provider_fixture.configure("invalid_string_config")  # String is not a valid config type

    # Test invalid mode
    with pytest.raises(ValueError):
        MockProvider(mode="invalid_mode")

@pytest.mark.parametrize("mode", [ProviderMode.PASSIVE, ProviderMode.ACTIVE])
def test_provider_modes(mode: ProviderMode):
    """Test provider with different modes."""
    provider = MockProvider(mode=mode)
    assert provider.mode == mode
    
    if mode == ProviderMode.PASSIVE:
        assert provider.sync_operation() == "sync_result"
    elif mode == ProviderMode.ACTIVE:
        assert provider.async_operation is not None

def test_context_management(base_provider_fixture: MockProvider):
    """Test provider context management capabilities."""
    # Test context updates
    base_provider_fixture.update_context("test_key", "test_value")
    assert base_provider_fixture.get_context("test_key") == "test_value"
    
    # Test default values
    assert base_provider_fixture.get_context("non_existent", "default") == "default"
    
    # Test multiple context updates
    contexts = {"key1": "value1", "key2": "value2"}
    for k, v in contexts.items():
        base_provider_fixture.update_context(k, v)
    
    for k, v in contexts.items():
        assert base_provider_fixture.get_context(k) == v

def test_interaction_history(base_provider_fixture: MockProvider):
    """Test interaction history logging and retrieval."""
    # Test single interaction
    interaction1 = {"type": "test", "data": "test_data"}
    base_provider_fixture.log_interaction(interaction1)
    history = base_provider_fixture.get_interaction_history()
    assert len(history) == 1
    assert history[0]["type"] == interaction1["type"]
    assert history[0]["data"] == interaction1["data"]
    assert "timestamp" in history[0]
    
    # Test multiple interactions with limit
    interaction2 = {"type": "test2", "data": "test_data2"}
    base_provider_fixture.log_interaction(interaction2)
    limited_history = base_provider_fixture.get_interaction_history(limit=1)
    assert len(limited_history) == 1

@pytest.mark.parametrize("mode", [ProviderMode.PASSIVE, ProviderMode.ACTIVE, ProviderMode.ADAPTIVE])
def test_provider_modes_extended(mode: ProviderMode):
    """Test provider behavior in different operational modes."""
    provider = MockProvider(mode=mode)
    assert provider.mode == mode
    
    # Test mode-specific behavior
    if mode == ProviderMode.PASSIVE:
        assert not provider._is_initialized
    elif mode == ProviderMode.ACTIVE:
        provider.update_context("active_mode", True)
        assert provider.get_context("active_mode")
    elif mode == ProviderMode.ADAPTIVE:
        provider.log_interaction({"adaptation": "test"})
        assert len(provider.get_interaction_history()) > 0

def test_provider_registry():
    """Test provider registration and creation."""
    # Register mock provider
    ProviderRegistry.register(MockProvider)
    
    # Create provider instance
    provider = ProviderRegistry.create("MockProvider", mode=ProviderMode.PASSIVE)
    assert isinstance(provider, MockProvider)
    assert provider.mode == ProviderMode.PASSIVE
    
    # Test invalid provider creation
    with pytest.raises(KeyError):
        ProviderRegistry.create("NonExistentProvider")

def test_provider_configuration_methods(base_provider_fixture: MockProvider):
    """Test provider configuration methods."""
    # Test configure with None
    base_provider_fixture.configure(None)
    assert base_provider_fixture.configure_called
    assert not base_provider_fixture._context_memory  # Should be empty after None config
    
    # Test configure with data
    config = {"key": "value"}
    base_provider_fixture.configure(config)
    assert base_provider_fixture.configure_called
    assert base_provider_fixture._context_memory == config
    
    # Test get_config
    assert base_provider_fixture.get_config() == config
    
    # Test is_initialized property
    assert base_provider_fixture.is_initialized
    
    # Test reset
    base_provider_fixture.reset()
    assert not base_provider_fixture._context_memory
    assert not base_provider_fixture._interaction_history

def test_provider_interaction_logging(base_provider_fixture: MockProvider):
    """Test interaction logging functionality."""
    # Test log_interaction
    interaction = {"type": "test", "data": "test_data"}
    base_provider_fixture.log_interaction(interaction)
    assert len(base_provider_fixture._interaction_history) == 1
    assert "timestamp" in base_provider_fixture._interaction_history[0]
    
    # Test get_interaction_history with limit
    base_provider_fixture.log_interaction({"type": "test2"})
    history = base_provider_fixture.get_interaction_history(limit=1)
    assert len(history) == 1
    
    # Test get_interaction_history without limit
    full_history = base_provider_fixture.get_interaction_history()
    assert len(full_history) == 2

def test_provider_mode_adaptation(base_provider_fixture: MockProvider):
    """Test mode adaptation functionality."""
    # Test adapt_mode
    initial_mode = base_provider_fixture.mode
    new_mode = ProviderMode.ACTIVE
    base_provider_fixture.adapt_mode(new_mode)
    assert base_provider_fixture.mode == new_mode
    
    # Verify interaction logging for mode change
    history = base_provider_fixture.get_interaction_history()
    assert any(
        interaction["event"] == "mode_change" and
        interaction["from_mode"] == initial_mode and
        interaction["to_mode"] == new_mode
        for interaction in history
    )

def test_provider_registry():
    """Test provider registry functionality."""
    # Test registration
    ProviderRegistry.register(MockProvider)
    assert "MockProvider" in ProviderRegistry._providers
    
    # Test get_provider
    provider_class = ProviderRegistry.get_provider("MockProvider")
    assert provider_class == MockProvider
    
    # Test get_provider with invalid name
    assert ProviderRegistry.get_provider("NonExistentProvider") is None
    
    # Test get_all_providers
    providers = ProviderRegistry.get_all_providers()
    assert isinstance(providers, dict)
    assert "MockProvider" in providers

def test_provider_string_representation(base_provider_fixture: MockProvider):
    """Test string representation of provider."""
    # Add some context
    base_provider_fixture.update_context("test_key", "test_value")
    
    # Test __repr__
    repr_str = repr(base_provider_fixture)
    assert "MockProvider" in repr_str
    assert base_provider_fixture.provider_id in repr_str
    assert base_provider_fixture.mode.name in repr_str
    assert "test_key" in repr_str
