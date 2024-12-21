"""
Base provider package containing fundamental provider implementations.
"""

from .baseprovider import BaseProvider, ProviderMode

__all__ = ['BaseProvider', 'ProviderMode']

"""
SentientOne Providers Package

This package contains the core provider implementations for the SentientOne framework.
Each provider represents a specialized computational resource or capability.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import logging

class BaseProvider(ABC):
    """
    Abstract base class for all SentientOne providers.
    Defines the core interface and basic functionality for providers.
    """
    
    def __init__(self, name: Optional[str] = None):
        """
        Initialize the base provider.
        
        Args:
            name (Optional[str]): Optional name for the provider instance.
        """
        self.name = name or self.__class__.__name__
        self.logger = logging.getLogger(self.name)
        self._config: Dict[str, Any] = {}
        self._is_initialized = False
    
    @abstractmethod
    def configure(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Configure the provider with specific settings.
        
        Args:
            config (Optional[Dict[str, Any]]): Configuration dictionary.
        """
        if config:
            self._config.update(config)
        self._is_initialized = True
    
    def reset(self) -> None:
        """
        Reset the provider to its initial state.
        """
        self._config.clear()
        self._is_initialized = False
    
    def get_config(self) -> Dict[str, Any]:
        """
        Retrieve the current configuration.
        
        Returns:
            Dict[str, Any]: Current provider configuration.
        """
        return self._config.copy()
    
    def is_initialized(self) -> bool:
        """
        Check if the provider has been initialized.
        
        Returns:
            bool: Initialization status.
        """
        return self._is_initialized
    
    def log(self, message: str, level: str = 'info') -> None:
        """
        Log a message with the provider's logger.
        
        Args:
            message (str): Message to log.
            level (str, optional): Logging level. Defaults to 'info'.
        """
        log_method = getattr(self.logger, level.lower(), self.logger.info)
        log_method(f"[{self.name}] {message}")

# Configure basic logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
