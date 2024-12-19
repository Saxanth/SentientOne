import pytest
from providers import BaseProvider
from providers.communication.base_communication_provider import BaseCommunicationProvider
from tests.test_utils import ConcreteProviderForTesting

def test_communication_provider_instantiation():
    provider = ConcreteProviderForTesting.create(BaseCommunicationProvider)
    assert isinstance(provider, BaseProvider)
    assert not provider.is_initialized()

def test_communication_provider_configuration():
    provider = ConcreteProviderForTesting.create(BaseCommunicationProvider)
    test_config = {"test_key": "test_value"}
    provider.configure(test_config)
    assert provider.is_initialized()
    assert provider.get_config() == test_config

def test_communication_provider_reset():
    provider = ConcreteProviderForTesting.create(BaseCommunicationProvider)
    test_config = {"test_key": "test_value"}
    provider.configure(test_config)
    provider.reset()
    assert not provider.is_initialized()
    assert provider.get_config() == {}
