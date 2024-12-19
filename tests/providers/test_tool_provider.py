import pytest
from providers import BaseProvider
from providers.tools.base_tool_provider import ToolProvider

def test_tool_provider_instantiation():
    provider = ToolProvider()
    assert isinstance(provider, BaseProvider)
    assert not provider.is_initialized()

def test_tool_provider_configuration():
    provider = ToolProvider()
    test_config = {"test_key": "test_value"}
    provider.configure(test_config)
    assert provider.is_initialized()
    assert provider.get_config() == test_config

def test_tool_provider_reset():
    provider = ToolProvider()
    test_config = {"test_key": "test_value"}
    provider.configure(test_config)
    provider.reset()
    assert not provider.is_initialized()
    assert provider.get_config() == {}
