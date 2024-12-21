"""Configuration for Ollama models."""
from dataclasses import dataclass
from typing import Dict, Any, Optional

@dataclass
class ModelConfig:
    """Model configuration parameters."""
    
    temperature: float = 0.7
    top_p: float = 0.9
    top_k: int = 40
    repeat_penalty: float = 1.1
    max_tokens: Optional[int] = None
    stop: Optional[list] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary.
        
        Returns:
            Configuration dictionary
        """
        config = {
            "temperature": self.temperature,
            "top_p": self.top_p,
            "top_k": self.top_k,
            "repeat_penalty": self.repeat_penalty
        }
        
        if self.max_tokens is not None:
            config["num_predict"] = self.max_tokens
            
        if self.stop:
            config["stop"] = self.stop
            
        return config
        
# Default configurations for different use cases
RESEARCH_CONFIG = ModelConfig(
    temperature=0.7,
    top_p=0.9,
    top_k=40,
    repeat_penalty=1.1
)

CODE_GENERATION_CONFIG = ModelConfig(
    temperature=0.4,
    top_p=0.95,
    top_k=50,
    repeat_penalty=1.2
)

TEST_GENERATION_CONFIG = ModelConfig(
    temperature=0.3,
    top_p=0.9,
    top_k=40,
    repeat_penalty=1.1
)
