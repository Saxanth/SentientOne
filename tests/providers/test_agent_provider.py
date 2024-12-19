import pytest
from providers import BaseProvider
from providers.agents.base_agent_provider import BaseAgentProvider
from tests.test_utils import ConcreteProviderForTesting

def test_agent_provider_instantiation():
    provider = ConcreteProviderForTesting.create(BaseAgentProvider)
    assert isinstance(provider, BaseProvider)
    assert not provider.is_initialized()

def test_agent_provider_configuration():
    provider = ConcreteProviderForTesting.create(BaseAgentProvider)
    test_config = {"test_key": "test_value"}
    provider.configure(test_config)
    assert provider.is_initialized()
    assert provider.get_config() == test_config

def test_agent_provider_reset():
    provider = ConcreteProviderForTesting.create(BaseAgentProvider)
    test_config = {"test_key": "test_value"}
    provider.configure(test_config)
    provider.reset()
    assert not provider.is_initialized()
    assert provider.get_config() == {}
