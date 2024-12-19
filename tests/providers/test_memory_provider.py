import pytest
from providers import BaseProvider
from providers.memorys.base_memory_provider import MemoryProvider

def test_memory_provider_instantiation():
    provider = MemoryProvider()
    assert isinstance(provider, BaseProvider)
    assert not provider.is_initialized()

def test_memory_provider_configuration():
    provider = MemoryProvider()
    test_config = {"test_key": "test_value"}
    provider.configure(test_config)
    assert provider.is_initialized()
    assert provider.get_config() == test_config

def test_memory_provider_reset():
    provider = MemoryProvider()
    test_config = {"test_key": "test_value"}
    provider.configure(test_config)
    provider.reset()
    assert not provider.is_initialized()
    assert provider.get_config() == {}
