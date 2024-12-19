import pytest
from providers import BaseProvider
from tests.test_utils import ConcreteProviderForTesting
from providers.security.base_security_provider import BaseSecurityProvider

def test_security_provider_instantiation():
    provider = ConcreteProviderForTesting.create(BaseSecurityProvider)
    assert isinstance(provider, BaseProvider)
    assert not provider.is_initialized()

def test_security_provider_configuration():
    provider = ConcreteProviderForTesting.create(BaseSecurityProvider)
    test_config = {"test_key": "test_value"}
    provider.configure(test_config)
    assert provider.is_initialized()
    assert provider.get_config() == test_config

def test_security_provider_reset():
    provider = ConcreteProviderForTesting.create(BaseSecurityProvider)
    test_config = {"test_key": "test_value"}
    provider.configure(test_config)
    provider.reset()
    assert not provider.is_initialized()
    assert provider.get_config() == {}
