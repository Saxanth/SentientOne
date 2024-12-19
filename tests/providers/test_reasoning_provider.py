import pytest
from providers import BaseProvider
from tests.test_utils import ConcreteProviderForTesting
from providers.reasoning.base_reasoning_provider import BaseReasoningProvider

def test_reasoning_provider_instantiation():
    provider = ConcreteProviderForTesting.create(BaseReasoningProvider)
    assert isinstance(provider, BaseProvider)
    assert not provider.is_initialized()

def test_reasoning_provider_configuration():
    provider = ConcreteProviderForTesting.create(BaseReasoningProvider)
    test_config = {"test_key": "test_value"}
    provider.configure(test_config)
    assert provider.is_initialized()
    assert provider.get_config() == test_config

def test_reasoning_provider_reset():
    provider = ConcreteProviderForTesting.create(BaseReasoningProvider)
    test_config = {"test_key": "test_value"}
    provider.configure(test_config)
    provider.reset()
    assert not provider.is_initialized()
    assert provider.get_config() == {}
