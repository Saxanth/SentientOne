import pytest
from providers import BaseProvider
from tests.test_utils import ConcreteProviderForTesting
from providers.workflows.base_workflow_provider import BaseWorkflowProvider

def test_workflow_provider_instantiation():
    provider = ConcreteProviderForTesting.create(BaseWorkflowProvider)
    assert isinstance(provider, BaseProvider)
    assert not provider.is_initialized()

def test_workflow_provider_configuration():
    provider = ConcreteProviderForTesting.create(BaseWorkflowProvider)
    test_config = {"test_key": "test_value"}
    provider.configure(test_config)
    assert provider.is_initialized()
    assert provider.get_config() == test_config

def test_workflow_provider_reset():
    provider = ConcreteProviderForTesting.create(BaseWorkflowProvider)
    test_config = {"test_key": "test_value"}
    provider.configure(test_config)
    provider.reset()
    assert not provider.is_initialized()
    assert provider.get_config() == {}
