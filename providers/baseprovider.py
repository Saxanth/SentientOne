import abc
import uuid
from typing import Any, Dict, List, Optional
from enum import Enum, auto
import logging

class ProviderMode(Enum):
    """Enumeration of provider operational modes."""
    PASSIVE = auto()
    ACTIVE = auto()
    ADAPTIVE = auto()

class BaseProvider(abc.ABC):
    """
    Base Provider for SentientOne Multi-Modal Intelligence Framework
    
    Core Design Principles:
    - Extensibility
    - Multi-Modal Capability
    - Dynamic Adaptation
    - Contextual Intelligence
    """
    
    def __init__(
        self, 
        provider_id: Optional[str] = None,
        name: Optional[str] = None,
        mode: ProviderMode = ProviderMode.PASSIVE
    ):
        """
        Initialize a base provider with core configuration.
        
        Args:
            provider_id: Unique identifier for the provider
            name: Human-readable name for the provider
            mode: Operational mode of the provider
        """
        self.provider_id = provider_id or str(uuid.uuid4())
        self.name = name or self.__class__.__name__
        self.mode = mode
        
        # Semantic memory and context tracking
        self._context_memory: Dict[str, Any] = {}
        self._interaction_history: List[Dict[str, Any]] = []
        
        # Logging configuration
        self._logger = logging.getLogger(f"SentientOne.{self.name}")
        
    @abc.abstractmethod
    def process(self, input_data: Any) -> Any:
        """
        Core processing method to be implemented by specific providers.
        
        Args:
            input_data: Multi-modal input to be processed
        
        Returns:
            Processed output based on provider's capabilities
        """
        raise NotImplementedError("Subclasses must implement processing logic")
    
    def update_context(self, key: str, value: Any) -> None:
        """
        Update the provider's contextual memory.
        
        Args:
            key: Context identifier
            value: Context value
        """
        self._context_memory[key] = value
        
    def get_context(self, key: str, default: Any = None) -> Any:
        """
        Retrieve a specific context value.
        
        Args:
            key: Context identifier
            default: Default value if key not found
        
        Returns:
            Stored context value or default
        """
        return self._context_memory.get(key, default)
    
    def log_interaction(self, interaction: Dict[str, Any]) -> None:
        """
        Log an interaction for observability and potential future learning.
        
        Args:
            interaction: Interaction details to log
        """
        interaction['timestamp'] = uuid.uuid4()  # Unique interaction ID
        self._interaction_history.append(interaction)
        
    def get_interaction_history(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Retrieve interaction history.
        
        Args:
            limit: Optional limit on number of interactions to return
        
        Returns:
            List of interaction records
        """
        return self._interaction_history[:limit] if limit else self._interaction_history
    
    def adapt_mode(self, new_mode: ProviderMode) -> None:
        """
        Dynamically change the provider's operational mode.
        
        Args:
            new_mode: New operational mode
        """
        previous_mode = self.mode
        self.mode = new_mode
        self.log_interaction({
            'event': 'mode_change',
            'from_mode': previous_mode,
            'to_mode': new_mode
        })
    
    def __repr__(self) -> str:
        """
        String representation of the provider.
        
        Returns:
            Detailed provider information
        """
        return (
            f"&lt;{self.__class__.__name__} "
            f"id={self.provider_id} "
            f"mode={self.mode.name} "
            f"context_keys={list(self._context_memory.keys())}&gt;"
        )

# Example of potential extension
class MultiModalProvider(BaseProvider):
    """
    A sample multi-modal provider demonstrating extensibility.
    """
    def process(self, input_data: Any) -> Any:
        # Placeholder for multi-modal processing logic
        self._logger.info(f"Processing input: {input_data}")
        return input_data

# Utility for dynamic provider registration
class ProviderRegistry:
    """
    Manages provider registration and discovery.
    """
    _providers: Dict[str, type[BaseProvider]] = {}
    
    @classmethod
    def register(cls, provider_class: type[BaseProvider]) -> None:
        """
        Register a provider class for dynamic instantiation.
        
        Args:
            provider_class: Provider class to register
        """
        cls._providers[provider_class.__name__] = provider_class
    
    @classmethod
    def create(cls, provider_name: str, **kwargs) -> BaseProvider:
        """
        Dynamically create a provider instance.
        
        Args:
            provider_name: Name of the provider class
            kwargs: Initialization arguments
        
        Returns:
            Instantiated provider
        
        Raises:
            KeyError: If provider is not registered
        """
        if provider_name not in cls._providers:
            raise KeyError(f"Provider {provider_name} not registered")
        return cls._providers[provider_name](**kwargs)
