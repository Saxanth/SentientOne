import pytest
from providers import BaseProvider
from providers.services.base_service_provider import ServiceProvider

def test_service_provider_instantiation():
    provider = ServiceProvider()
    assert isinstance(provider, BaseProvider)
    assert not provider.is_initialized()

def test_service_provider_configuration():
    provider = ServiceProvider()
    test_config = {"test_key": "test_value"}
    provider.configure(test_config)
    assert provider.is_initialized()
    assert provider.get_config() == test_config

def test_service_provider_reset():
    provider = ServiceProvider()
    test_config = {"test_key": "test_value"}
    provider.configure(test_config)
    provider.reset()
    assert not provider.is_initialized()
    assert provider.get_config() == {}
