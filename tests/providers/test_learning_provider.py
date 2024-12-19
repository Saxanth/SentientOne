import pytest
from providers import BaseProvider
from tests.test_utils import ConcreteProviderForTesting
from providers.learning.base_learning_provider import BaseLearningProvider

def test_learning_provider_instantiation():
    provider = ConcreteProviderForTesting.create(BaseLearningProvider)
    assert isinstance(provider, BaseProvider)
    assert not provider.is_initialized()

def test_learning_provider_configuration():
    provider = ConcreteProviderForTesting.create(BaseLearningProvider)
    test_config = {"test_key": "test_value"}
    provider.configure(test_config)
    assert provider.is_initialized()
    assert provider.get_config() == test_config

def test_learning_provider_reset():
    provider = ConcreteProviderForTesting.create(BaseLearningProvider)
    test_config = {"test_key": "test_value"}
    provider.configure(test_config)
    provider.reset()
    assert not provider.is_initialized()
    assert provider.get_config() == {}
