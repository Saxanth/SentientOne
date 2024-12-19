import pytest
from providers import BaseProvider
from providers.learnings.base_learning_provider import LearningProvider

def test_learning_provider_instantiation():
    provider = LearningProvider()
    assert isinstance(provider, BaseProvider)
    assert not provider.is_initialized()

def test_learning_provider_configuration():
    provider = LearningProvider()
    test_config = {"test_key": "test_value"}
    provider.configure(test_config)
    assert provider.is_initialized()
    assert provider.get_config() == test_config

def test_learning_provider_reset():
    provider = LearningProvider()
    test_config = {"test_key": "test_value"}
    provider.configure(test_config)
    provider.reset()
    assert not provider.is_initialized()
    assert provider.get_config() == {}
