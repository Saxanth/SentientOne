import pytest
from providers import BaseProvider
from providers.personas.base_persona_provider import PersonaProvider

def test_persona_provider_instantiation():
    provider = PersonaProvider()
    assert isinstance(provider, BaseProvider)
    assert not provider.is_initialized()

def test_persona_provider_configuration():
    provider = PersonaProvider()
    test_config = {"test_key": "test_value"}
    provider.configure(test_config)
    assert provider.is_initialized()
    assert provider.get_config() == test_config

def test_persona_provider_reset():
    provider = PersonaProvider()
    test_config = {"test_key": "test_value"}
    provider.configure(test_config)
    provider.reset()
    assert not provider.is_initialized()
    assert provider.get_config() == {}
