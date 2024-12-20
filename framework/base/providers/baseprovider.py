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
        
        # Initialization flag
        self._is_initialized = False
        
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
    
    def configure(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Configure the provider with specific settings.
        
        Args:
            config: Optional configuration dictionary
        """
        if config is not None:
            for key, value in config.items():
                self.update_context(key, value)
        
        # Mark as initialized
        self._is_initialized = True
        
    def reset(self) -> None:
        """
        Reset the provider to its initial state.
        Clears context memory and interaction history.
        """
        self._context_memory.clear()
        self._interaction_history.clear()
        
    def get_config(self) -> Dict[str, Any]:
        """
        Retrieve the current configuration of the provider.
        
        Returns:
            Dictionary of configuration settings
        """
        return dict(self._context_memory)
    
    @property
    def is_initialized(self) -> bool:
        """
        Check if the provider has been initialized or configured.
        
        Returns:
            Boolean indicating initialization state
        """
        return len(self._context_memory) > 0 or len(self._interaction_history) > 0
    
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
    def get_provider(cls, name: str) -> Optional[type[BaseProvider]]:
        """
        Get a provider class by name.
        
        Args:
            name: Name of the provider class
            
        Returns:
            Provider class if found, None otherwise
        """
        return cls._providers.get(name)
    
    @classmethod
    def get_all_providers(cls) -> Dict[str, type[BaseProvider]]:
        """
        Get all registered providers.
        
        Returns:
            Dictionary of provider names to provider classes
        """
        return dict(cls._providers)
    
    @classmethod
    def create(cls, name: str, **kwargs: Any) -> BaseProvider:
        """
        Create a provider instance by name.
        
        Args:
            name: Name of the provider class
            **kwargs: Arguments to pass to provider constructor
            
        Returns:
            Provider instance
            
        Raises:
            KeyError: If provider not found
        """
        provider_class = cls._providers.get(name)
        if not provider_class:
            raise KeyError(f"Provider '{name}' not found")
        return provider_class(**kwargs)
