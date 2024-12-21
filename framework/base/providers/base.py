"""
Base provider implementation for the SentientOne framework.
"""

import abc
import uuid
from typing import Any, Dict, List, Optional
from enum import Enum, auto
import logging

class ProviderMode(Enum):
    """Enumeration of provider operational modes."""
    PASSIVE = auto()    # Provider operates in passive mode, responding only to direct requests
    ACTIVE = auto()     # Provider actively processes and initiates operations
    ADAPTIVE = auto()   # Provider adapts its behavior based on context and learning

class BaseProvider(abc.ABC):
    """
    Base Provider class defining the fundamental interface and functionality
    for all SentientOne providers.
    
    Core Design Principles:
    - Extensibility: Easy to extend and customize
    - Multi-Modal: Support for various types of data and interactions
    - Dynamic Adaptation: Ability to modify behavior based on context
    - Contextual Intelligence: Understanding and using context effectively
    """
    
    def __init__(
        self, 
        provider_id: Optional[str] = None,
        name: Optional[str] = None,
        mode: ProviderMode = ProviderMode.PASSIVE
    ):
        """Initialize the base provider with core configuration."""
        self.provider_id = provider_id or str(uuid.uuid4())
        self.name = name or self.__class__.__name__
        self.mode = mode
        
        # Semantic memory and context tracking
        self._context_memory: Dict[str, Any] = {}
        self._interaction_history: List[Dict[str, Any]] = []
        
        # Logging configuration
        self._logger = logging.getLogger(f"SentientOne.{self.name}")
        
        # Initialization flag
        self._is_initialized = False
        
    @abc.abstractmethod
    async def process(self, input_data: Any) -> Any:
        """
        Core processing method to be implemented by specific providers.
        
        Args:
            input_data: Multi-modal input to be processed
        
        Returns:
            Processed output based on provider's capabilities
        """
        raise NotImplementedError("Subclasses must implement processing logic")
    
    def update_context(self, key: str, value: Any) -> None:
        """Update the provider's contextual memory."""
        self._context_memory[key] = value
        self._logger.debug(f"Updated context: {key}")
        
    def get_context(self, key: str, default: Any = None) -> Any:
        """Retrieve a specific context value."""
        return self._context_memory.get(key, default)
    
    def log_interaction(self, interaction: Dict[str, Any]) -> None:
        """Log an interaction for observability and learning."""
        interaction['timestamp'] = uuid.uuid4()
        self._interaction_history.append(interaction)
        self._logger.info(f"Logged interaction: {interaction.get('type', 'unknown')}")
        
    def get_interaction_history(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Retrieve interaction history with optional limit."""
        history = self._interaction_history
        if limit:
            history = history[-limit:]
        return history
    
    async def initialize(self) -> None:
        """Initialize the provider. Override for custom initialization."""
        self._is_initialized = True
        self._logger.info(f"Initialized provider: {self.name}")
        
    @property
    def is_initialized(self) -> bool:
        """Check if the provider is initialized."""
        return self._is_initialized
