from providers import BaseProvider
from typing import Optional, Dict, Any

class AgentProvider(BaseProvider):
    """Provider for managing intelligent agent lifecycle."""
    
    def configure(self, config: Optional[Dict[str, Any]] = None) -> None:
        """Configure the agent provider with specific settings."""
        super().configure(config)
    
    @classmethod
    def create_agent(cls, config: Optional[Dict[str, Any]] = None) -> 'AgentProvider':
        """
        Create a new agent instance.
        
        Args:
            config (Optional[Dict[str, Any]]): Configuration for the agent.
            
        Returns:
            AgentProvider: A new configured agent instance.
        """
        agent = cls()
        agent.configure(config)
        return agent
