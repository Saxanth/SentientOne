import pytest
from providers import BaseProvider
from tests.test_utils import ConcreteProviderForTesting
from providers.services.base_service_provider import BaseServiceProvider

def test_service_provider_instantiation():
    provider = ConcreteProviderForTesting.create(BaseServiceProvider)
    assert isinstance(provider, BaseProvider)
    assert not provider.is_initialized()

def test_service_provider_configuration():
    provider = ConcreteProviderForTesting.create(BaseServiceProvider)
    test_config = {"test_key": "test_value"}
    provider.configure(test_config)
    assert provider.is_initialized()
    assert provider.get_config() == test_config

def test_service_provider_reset():
    provider = ConcreteProviderForTesting.create(BaseServiceProvider)
    test_config = {"test_key": "test_value"}
    provider.configure(test_config)
    provider.reset()
    assert not provider.is_initialized()
    assert provider.get_config() == {}
