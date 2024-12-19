import pytest
from providers import BaseProvider
from providers.communications.base_communication_provider import CommunicationProvider

def test_communication_provider_instantiation():
    provider = CommunicationProvider()
    assert isinstance(provider, BaseProvider)
    assert not provider.is_initialized()

def test_communication_provider_configuration():
    provider = CommunicationProvider()
    test_config = {"test_key": "test_value"}
    provider.configure(test_config)
    assert provider.is_initialized()
    assert provider.get_config() == test_config

def test_communication_provider_reset():
    provider = CommunicationProvider()
    test_config = {"test_key": "test_value"}
    provider.configure(test_config)
    provider.reset()
    assert not provider.is_initialized()
    assert provider.get_config() == {}
