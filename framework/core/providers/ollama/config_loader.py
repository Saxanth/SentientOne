"""Configuration loader for Ollama provider."""
import yaml
from dataclasses import dataclass
from typing import Dict, Any, Optional
from pathlib import Path

@dataclass
class OllamaConnectionConfig:
    """Ollama connection configuration."""
    endpoint: str
    api_key: Optional[str]
    timeout: int
    max_retries: int

@dataclass
class OllamaModelConfig:
    """Model-specific configuration."""
    temperature: float
    top_p: float
    top_k: int
    repeat_penalty: float

@dataclass
class OllamaRequestConfig:
    """Request configuration."""
    max_tokens: int
    batch_size: int
    concurrent_limit: int
    request_timeout: int

@dataclass
class OllamaErrorConfig:
    """Error handling configuration."""
    retry_delay: float
    max_retries: int
    fallback_behavior: str

@dataclass
class OllamaConfig:
    """Complete Ollama configuration."""
    connection: OllamaConnectionConfig
    models: Dict[str, str]
    model_configs: Dict[str, OllamaModelConfig]
    requests: OllamaRequestConfig
    error_handling: OllamaErrorConfig

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'OllamaConfig':
        """Create config from dictionary.
        
        Args:
            data: Configuration dictionary
            
        Returns:
            OllamaConfig instance
        """
        ollama_data = data.get('ollama', {})
        
        connection = OllamaConnectionConfig(
            endpoint=ollama_data['connection']['endpoint'],
            api_key=ollama_data['connection'].get('api_key'),
            timeout=ollama_data['connection']['timeout'],
            max_retries=ollama_data['connection']['max_retries']
        )
        
        model_configs = {
            name: OllamaModelConfig(**config)
            for name, config in ollama_data['model_configs'].items()
        }
        
        requests = OllamaRequestConfig(
            max_tokens=ollama_data['requests']['max_tokens'],
            batch_size=ollama_data['requests']['batch_size'],
            concurrent_limit=ollama_data['requests']['concurrent_limit'],
            request_timeout=ollama_data['requests']['request_timeout']
        )
        
        error_handling = OllamaErrorConfig(
            retry_delay=ollama_data['error_handling']['retry_delay'],
            max_retries=ollama_data['error_handling']['max_retries'],
            fallback_behavior=ollama_data['error_handling']['fallback_behavior']
        )
        
        return cls(
            connection=connection,
            models=ollama_data['models'],
            model_configs=model_configs,
            requests=requests,
            error_handling=error_handling
        )

def load_config(config_path: str = "config.yaml") -> OllamaConfig:
    """Load configuration from YAML file.
    
    Args:
        config_path: Path to config file
        
    Returns:
        OllamaConfig instance
        
    Raises:
        FileNotFoundError: If config file doesn't exist
        ValueError: If config is invalid
    """
    config_path = Path(config_path)
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
        
    try:
        with open(config_path) as f:
            config_data = yaml.safe_load(f)
            return OllamaConfig.from_dict(config_data)
    except Exception as e:
        raise ValueError(f"Failed to load config: {str(e)}")
