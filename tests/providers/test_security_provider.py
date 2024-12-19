import pytest
from providers import BaseProvider
from providers.securitys.base_security_provider import SecurityProvider

def test_security_provider_instantiation():
    provider = SecurityProvider()
    assert isinstance(provider, BaseProvider)
    assert not provider.is_initialized()

def test_security_provider_configuration():
    provider = SecurityProvider()
    test_config = {"test_key": "test_value"}
    provider.configure(test_config)
    assert provider.is_initialized()
    assert provider.get_config() == test_config

def test_security_provider_reset():
    provider = SecurityProvider()
    test_config = {"test_key": "test_value"}
    provider.configure(test_config)
    provider.reset()
    assert not provider.is_initialized()
    assert provider.get_config() == {}
