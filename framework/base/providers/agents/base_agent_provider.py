import logging
from typing import Optional, Dict, Any

from providers.baseprovider import BaseProvider, ProviderMode

class BaseAgentProvider(BaseProvider):
    """Provider for managing intelligent agent lifecycle."""
    
    def __init__(self):
        super().__init__()
        self._logger = logging.getLogger(self.__class__.__name__)
    
    def configure(self, config: Optional[Dict[str, Any]] = None) -> None:
        """Configure the agent provider with specific settings."""
        super().configure(config)
    
    def reset(self):
        """Reset the agent provider to its initial state."""
        super().reset()
    
    @classmethod
    def create_agent(cls, config: Optional[Dict[str, Any]] = None) -> 'BaseAgentProvider':
        """
        Create a new agent instance.
        
        Args:
            config (Optional[Dict[str, Any]]): Configuration for the agent.
            
        Returns:
            BaseAgentProvider: A new configured agent instance.
        """
        agent = cls()
        agent.configure(config)
        return agent
