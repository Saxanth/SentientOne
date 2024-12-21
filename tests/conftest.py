import pytest
import os
import sys
import logging
from typing import Dict, Any, Generator
from unittest.mock import MagicMock

# Add project root to path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from tests.utils.test_helpers import MockProvider, create_mock_provider, create_test_config
from framework.base.providers.baseprovider import BaseProvider, ProviderMode

# Common test fixtures
@pytest.fixture
def mock_logger():
    """Create a mock logger."""
    return MagicMock(spec=logging.Logger)

@pytest.fixture
def base_provider_fixture():
    """Create a base provider instance for testing."""
    provider = MockProvider(mode=ProviderMode.PASSIVE)
    yield provider
    provider.reset()

@pytest.fixture
def async_provider_fixture():
    """Create an async provider instance for testing."""
    provider = MockProvider(mode=ProviderMode.ACTIVE)
    provider.configure(create_test_config())
    yield provider
    provider.reset()

@pytest.fixture
def test_config():
    """Create a test configuration."""
    return create_test_config()
