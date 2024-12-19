import pytest
from providers import BaseProvider
from providers.workflows.base_workflow_provider import WorkflowProvider

def test_workflow_provider_instantiation():
    provider = WorkflowProvider()
    assert isinstance(provider, BaseProvider)
    assert not provider.is_initialized()

def test_workflow_provider_configuration():
    provider = WorkflowProvider()
    test_config = {"test_key": "test_value"}
    provider.configure(test_config)
    assert provider.is_initialized()
    assert provider.get_config() == test_config

def test_workflow_provider_reset():
    provider = WorkflowProvider()
    test_config = {"test_key": "test_value"}
    provider.configure(test_config)
    provider.reset()
    assert not provider.is_initialized()
    assert provider.get_config() == {}
