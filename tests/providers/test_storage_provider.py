import pytest
from providers import BaseProvider
from tests.test_utils import ConcreteProviderForTesting
from providers.storage.base_storage_provider import BaseStorageProvider

def test_storage_provider_instantiation():
    provider = ConcreteProviderForTesting.create(BaseStorageProvider)
    assert isinstance(provider, BaseProvider)
    assert not provider.is_initialized()

def test_storage_provider_configuration():
    provider = ConcreteProviderForTesting.create(BaseStorageProvider)
    test_config = {"test_key": "test_value"}
    provider.configure(test_config)
    assert provider.is_initialized()
    assert provider.get_config() == test_config

def test_storage_provider_reset():
    provider = ConcreteProviderForTesting.create(BaseStorageProvider)
    test_config = {"test_key": "test_value"}
    provider.configure(test_config)
    provider.reset()
    assert not provider.is_initialized()
    assert provider.get_config() == {}
