"""Test helper utilities."""
import asyncio
import functools
import logging
from typing import Any, Dict, Optional, Type, AsyncIterator
from unittest.mock import MagicMock
from framework.base.providers.baseprovider import BaseProvider, ProviderMode

class AsyncContextManagerMock:
    """Base class for async context manager mocks."""
    
    async def __aenter__(self) -> Any:
        return self
        
    async def __aexit__(self, exc_type: Optional[Type[BaseException]], 
                       exc_val: Optional[BaseException], 
                       exc_tb: Optional[Any]) -> None:
        pass

class MockHTTPResponse(AsyncContextManagerMock):
    """Mock HTTP response."""
    
    def __init__(self, data: Dict[str, Any], status: int = 200):
        self.data = data
        self.status = status
        
    async def json(self) -> Dict[str, Any]:
        return self.data
        
    async def text(self) -> str:
        return str(self.data)

class MockHTTPSession(AsyncContextManagerMock):
    """Mock HTTP session."""
    
    def __init__(self, response_data: Dict[str, Any], status: int = 200):
        self.response = MockHTTPResponse(response_data, status)
        
    def post(self, *args: Any, **kwargs: Any) -> MockHTTPResponse:
        return self.response
        
    def get(self, *args: Any, **kwargs: Any) -> MockHTTPResponse:
        return self.response

class MockProvider(BaseProvider):
    """Mock provider for testing."""
    
    def __init__(self, mode: ProviderMode = ProviderMode.PASSIVE):
        if not isinstance(mode, ProviderMode):
            raise ValueError(f"Mode must be a ProviderMode enum value, got {type(mode)}")
        super().__init__(mode=mode)
        self._config = {}
        self._logger = logging.getLogger(self.__class__.__name__)
        self.configure_called = False
        self.reset_called = False
        
    def configure(self, config: Optional[Dict[str, Any]] = None) -> None:
        """Configure the mock provider."""
        self.configure_called = True
        if config is None:
            return
        if not isinstance(config, dict):
            raise TypeError("Configuration must be a dictionary")
        for key, value in config.items():
            self.update_context(key, value)
        
    def reset(self) -> None:
        """Reset the provider state."""
        self._context_memory.clear()
        self._interaction_history.clear()
        self.configure_called = False
        self.reset_called = True
        
    def sync_operation(self) -> str:
        """Test sync operation."""
        return "sync_result"
        
    async def async_operation(self) -> str:
        """Test async operation."""
        return "async_result"
        
    async def process(self, input_data: Any) -> str:
        """Process input data."""
        return f"Processed: {input_data}"

def create_mock_provider(base_class: Type[BaseProvider], **kwargs: Any) -> BaseProvider:
    """Create a mock provider instance."""
    if not isinstance(kwargs.get("mode", ProviderMode.PASSIVE), ProviderMode):
        raise ValueError("Mode must be a ProviderMode enum value")
    return MockProvider(**kwargs)

def create_test_config() -> Dict[str, Any]:
    """Create test configuration."""
    return {
        "api_key": "test_key",
        "model": "test-model",
        "temperature": 0.7,
        "max_tokens": 100
    }

def async_test(coro):
    """Decorator for async test functions."""
    @functools.wraps(coro)
    def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(coro(*args, **kwargs))
    return wrapper
