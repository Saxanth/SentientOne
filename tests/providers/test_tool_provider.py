import pytest
from providers import BaseProvider
from tests.test_utils import ConcreteProviderForTesting
from providers.tools.base_tool_provider import BaseToolProvider

def test_tool_provider_instantiation():
    provider = ConcreteProviderForTesting.create(BaseToolProvider)
    assert isinstance(provider, BaseProvider)
    assert not provider.is_initialized()

def test_tool_provider_configuration():
    provider = ConcreteProviderForTesting.create(BaseToolProvider)
    test_config = {"test_key": "test_value"}
    provider.configure(test_config)
    assert provider.is_initialized()
    assert provider.get_config() == test_config

def test_tool_provider_reset():
    provider = ConcreteProviderForTesting.create(BaseToolProvider)
    test_config = {"test_key": "test_value"}
    provider.configure(test_config)
    provider.reset()
    assert not provider.is_initialized()
    assert provider.get_config() == {}
