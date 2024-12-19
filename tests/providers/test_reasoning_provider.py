import pytest
from providers import BaseProvider
from providers.reasonings.base_reasoning_provider import ReasoningProvider

def test_reasoning_provider_instantiation():
    provider = ReasoningProvider()
    assert isinstance(provider, BaseProvider)
    assert not provider.is_initialized()

def test_reasoning_provider_configuration():
    provider = ReasoningProvider()
    test_config = {"test_key": "test_value"}
    provider.configure(test_config)
    assert provider.is_initialized()
    assert provider.get_config() == test_config

def test_reasoning_provider_reset():
    provider = ReasoningProvider()
    test_config = {"test_key": "test_value"}
    provider.configure(test_config)
    provider.reset()
    assert not provider.is_initialized()
    assert provider.get_config() == {}
