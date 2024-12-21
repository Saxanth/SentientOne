"""Base test class for provider testing."""
import pytest
from typing import Dict, Any, Optional
from unittest.mock import MagicMock
import logging
from framework.base.providers.baseprovider import BaseProvider, ProviderMode

class BaseProviderTest:
    """Base test class for all provider tests."""

    @pytest.fixture(autouse=True)
    def setup_method(self, mock_logger: MagicMock):
        """Set up test method."""
        self.logger = mock_logger
        self._setup_provider()
        self._setup_mocks()

    def _setup_provider(self):
        """Set up provider instance. Override in subclass."""
        raise NotImplementedError

    def _setup_mocks(self):
        """Set up mock objects. Override in subclass if needed."""
        pass

    def _create_test_config(self) -> Dict[str, Any]:
        """Create a test configuration."""
        return {
            "api_key": "test_key",
            "model": "test-model",
            "temperature": 0.7,
            "max_tokens": 100
        }

    async def _assert_provider_basics(self, provider: BaseProvider):
        """Assert basic provider functionality."""
        # Test configuration
        config = self._create_test_config()
        provider.configure(config)
        assert provider._config == config

        # Test mode changes
        provider.mode = ProviderMode.ACTIVE
        assert provider.mode == ProviderMode.ACTIVE
        provider.mode = ProviderMode.PASSIVE
        assert provider.mode == ProviderMode.PASSIVE

        # Test reset
        provider.reset()
        assert provider._config == {}

    def _assert_provider_attributes(self, provider: BaseProvider):
        """Assert provider has required attributes."""
        assert hasattr(provider, "mode")
        assert hasattr(provider, "configure")
        assert hasattr(provider, "process")
        assert hasattr(provider, "reset")

    async def _assert_error_handling(self, provider: BaseProvider):
        """Assert provider error handling."""
        # Test invalid configuration
        with pytest.raises(TypeError):
            provider.configure("invalid")

        # Test invalid mode
        with pytest.raises(ValueError):
            provider.mode = "invalid"

        # Test missing required config
        with pytest.raises(ValueError):
            await provider.process(None)

    def _get_mock_api_response(self) -> Dict[str, Any]:
        """Get mock API response."""
        return {
            "status": "success",
            "data": {
                "id": "test_id",
                "type": "test_type",
                "attributes": {
                    "name": "test_name",
                    "value": "test_value"
                }
            }
        }
