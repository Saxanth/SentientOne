"""Raw HTTP implementation of Ollama provider."""
import json
import socket
import http.client
import time
import asyncio
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from .config import ModelConfig
from .config_loader import OllamaConfig
from ...utils.logging import get_logger

logger = get_logger(__name__)

@dataclass
class OllamaResponse:
    """Response from Ollama API."""
    success: bool
    content: Optional[str] = None
    error: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class OllamaProvider:
    """Simple Ollama provider using raw HTTP requests."""
    
    def __init__(
        self,
        config: OllamaConfig
    ):
        """Initialize provider.
        
        Args:
            config: Ollama configuration
        """
        self.config = config
        self._active_requests = 0
        self._request_lock = asyncio.Lock()
        self._validate_connection()
        
    def _get_connection_params(self) -> tuple:
        """Get connection parameters from config.
        
        Returns:
            Tuple of (host, port)
        """
        endpoint = self.config.connection.endpoint
        if ":" in endpoint:
            host, port = endpoint.split(":")
            return host, int(port)
        return endpoint, 11434
        
    def _validate_connection(self) -> None:
        """Validate connection to Ollama server."""
        host, port = self._get_connection_params()
        retries = 0
        last_error = None
        
        while retries < self.config.connection.max_retries:
            try:
                conn = http.client.HTTPConnection(
                    host,
                    port,
                    timeout=self.config.connection.timeout
                )
                conn.request("GET", "/")
                response = conn.getresponse()
                if response.status != 200:
                    raise ConnectionError(
                        f"Ollama server returned status {response.status}"
                    )
                return
            except Exception as e:
                last_error = str(e)
                retries += 1
                if retries < self.config.connection.max_retries:
                    time.sleep(self.config.error_handling.retry_delay)
            finally:
                conn.close()
                
        raise ConnectionError(
            f"Failed to connect to Ollama after {retries} attempts: {last_error}"
        )
            
    async def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None
    ) -> OllamaResponse:
        """Make HTTP request to Ollama API.
        
        Args:
            method: HTTP method
            endpoint: API endpoint
            data: Request data
            
        Returns:
            API response
        """
        # Wait if we've hit the concurrent request limit
        async with self._request_lock:
            if self._active_requests >= self.config.requests.concurrent_limit:
                logger.debug("Waiting for request slot")
                while self._active_requests >= self.config.requests.concurrent_limit:
                    await asyncio.sleep(0.1)
            self._active_requests += 1
            
        try:
            host, port = self._get_connection_params()
            retries = 0
            last_error = None
            
            while retries < self.config.error_handling.max_retries:
                try:
                    conn = http.client.HTTPConnection(
                        host,
                        port,
                        timeout=self.config.requests.request_timeout
                    )
                    
                    headers = {
                        "Content-Type": "application/json"
                    }
                    if self.config.connection.api_key:
                        headers["Authorization"] = f"Bearer {self.config.connection.api_key}"
                    
                    if data:
                        body = json.dumps(data)
                    else:
                        body = None
                        
                    conn.request(
                        method,
                        endpoint,
                        body=body,
                        headers=headers
                    )
                    
                    response = conn.getresponse()
                    response_data = response.read().decode()
                    
                    if response.status != 200:
                        if retries < self.config.error_handling.max_retries - 1:
                            retries += 1
                            time.sleep(self.config.error_handling.retry_delay)
                            continue
                        return OllamaResponse(
                            success=False,
                            error=f"Request failed with status {response.status}: {response_data}"
                        )
                        
                    try:
                        result = json.loads(response_data)
                        return OllamaResponse(
                            success=True,
                            content=result.get("response"),
                            metadata=result
                        )
                    except json.JSONDecodeError:
                        if retries < self.config.error_handling.max_retries - 1:
                            retries += 1
                            time.sleep(self.config.error_handling.retry_delay)
                            continue
                        return OllamaResponse(
                            success=False,
                            error="Failed to parse response JSON"
                        )
                        
                except socket.timeout:
                    last_error = "Request timed out"
                except Exception as e:
                    last_error = str(e)
                    
                if retries < self.config.error_handling.max_retries - 1:
                    retries += 1
                    time.sleep(self.config.error_handling.retry_delay)
                else:
                    break
                    
            return OllamaResponse(
                success=False,
                error=f"Request failed after {retries} retries: {last_error}"
            )
                
        finally:
            conn.close()
            async with self._request_lock:
                self._active_requests -= 1
            
    def _get_model_config(self, task_type: str) -> ModelConfig:
        """Get model configuration for task type.
        
        Args:
            task_type: Type of task
            
        Returns:
            Model configuration
        """
        if task_type in self.config.model_configs:
            config = self.config.model_configs[task_type]
            return ModelConfig(
                temperature=config.temperature,
                top_p=config.top_p,
                top_k=config.top_k,
                repeat_penalty=config.repeat_penalty,
                max_tokens=self.config.requests.max_tokens
            )
        return ModelConfig(max_tokens=self.config.requests.max_tokens)
            
    async def generate(
        self,
        prompt: str,
        task_type: str = "implementation",
        system: Optional[str] = None
    ) -> OllamaResponse:
        """Generate completion from prompt.
        
        Args:
            prompt: Input prompt
            task_type: Type of task (research/implementation/test)
            system: Optional system prompt
            
        Returns:
            Model response
        """
        model = self.config.models.get(task_type, self.config.models["default"])
        config = self._get_model_config(task_type)
        
        data = {
            "model": model,
            "prompt": prompt,
            "stream": False
        }
        
        if system:
            data["system"] = system
            
        data.update(config.to_dict())
            
        return await self._make_request("POST", "/api/generate", data)
        
    async def chat(
        self,
        messages: List[Dict[str, str]],
        task_type: str = "implementation"
    ) -> OllamaResponse:
        """Chat completion.
        
        Args:
            messages: List of chat messages
            task_type: Type of task (research/implementation/test)
            
        Returns:
            Model response
        """
        model = self.config.models.get(task_type, self.config.models["default"])
        config = self._get_model_config(task_type)
        
        data = {
            "model": model,
            "messages": messages,
            "stream": False
        }
        
        data.update(config.to_dict())
            
        return await self._make_request("POST", "/api/chat", data)
