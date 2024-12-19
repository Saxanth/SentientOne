import pytest
from providers import BaseProvider
from providers.storages.base_storage_provider import StorageProvider

def test_storage_provider_instantiation():
    provider = StorageProvider()
    assert isinstance(provider, BaseProvider)
    assert not provider.is_initialized()

def test_storage_provider_configuration():
    provider = StorageProvider()
    test_config = {"test_key": "test_value"}
    provider.configure(test_config)
    assert provider.is_initialized()
    assert provider.get_config() == test_config

def test_storage_provider_reset():
    provider = StorageProvider()
    test_config = {"test_key": "test_value"}
    provider.configure(test_config)
    provider.reset()
    assert not provider.is_initialized()
    assert provider.get_config() == {}
