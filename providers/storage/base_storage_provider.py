import abc
import uuid
from typing import Any, Dict, List, Optional, TypeVar, Generic, Union
from enum import Enum, auto
import logging
import json
from datetime import datetime

# Import base provider
import sys
import os

# Ensure the parent directories are in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from baseprovider import BaseProvider, ProviderMode

T = TypeVar('T')

class StorageType(Enum):
    """
    Enumeration of supported storage types.
    """
    IN_MEMORY = auto()
    FILE_SYSTEM = auto()
    RELATIONAL_DB = auto()
    NOSQL_DB = auto()
    OBJECT_STORAGE = auto()
    DISTRIBUTED_STORAGE = auto()

class StorageOperation(Enum):
    """
    Enumeration of storage operations.
    """
    CREATE = auto()
    READ = auto()
    UPDATE = auto()
    DELETE = auto()
    SEARCH = auto()

class StorageConfig:
    """
    Configuration class for storage providers.
    """
    def __init__(
        self, 
        storage_type: StorageType,
        connection_params: Optional[Dict[str, Any]] = None,
        max_retries: int = 3,
        retry_delay: float = 1.0,
        encryption_key: Optional[str] = None
    ):
        """
        Initialize storage configuration.
        
        Args:
            storage_type: Type of storage backend
            connection_params: Connection parameters for the storage
            max_retries: Maximum number of retry attempts for operations
            retry_delay: Delay between retry attempts
            encryption_key: Optional encryption key for data protection
        """
        self.storage_type = storage_type
        self.connection_params = connection_params or {}
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.encryption_key = encryption_key

class BaseStorageProvider(BaseProvider, Generic[T]):
    """
    Abstract Base Storage Provider for SentientOne Framework
    
    Provides:
    - Generic, type-safe storage operations
    - Configurable storage backends
    - Comprehensive error handling
    - Logging and observability
    """
    
    def __init__(
        self, 
        provider_id: Optional[str] = None,
        name: Optional[str] = None,
        mode: ProviderMode = ProviderMode.ADAPTIVE,
        config: Optional[StorageConfig] = None
    ):
        """
        Initialize the BaseStorageProvider.
        
        Args:
            provider_id: Unique identifier for the storage provider
            name: Human-readable name for the storage provider
            mode: Operational mode of the storage provider
            config: Storage configuration parameters
        """
        super().__init__(provider_id, name, mode)
        
        # Storage configuration
        self._config = config or StorageConfig(
            storage_type=StorageType.IN_MEMORY
        )
        
        # Logging
        self._storage_logger = logging.getLogger(
            f"SentientOne.StorageProvider.{self.name}"
        )
    
    @abc.abstractmethod
    async def create(self, item: T, **kwargs) -> str:
        """
        Create a new item in storage.
        
        Args:
            item: Item to be stored
            kwargs: Additional creation parameters
        
        Returns:
            Unique identifier of the created item
        """
        raise NotImplementedError("Subclasses must implement create method")
    
    @abc.abstractmethod
    async def read(self, item_id: str, **kwargs) -> Optional[T]:
        """
        Read an item from storage.
        
        Args:
            item_id: Unique identifier of the item
            kwargs: Additional read parameters
        
        Returns:
            Retrieved item or None if not found
        """
        raise NotImplementedError("Subclasses must implement read method")
    
    @abc.abstractmethod
    async def update(self, item_id: str, item: T, **kwargs) -> bool:
        """
        Update an existing item in storage.
        
        Args:
            item_id: Unique identifier of the item
            item: Updated item data
            kwargs: Additional update parameters
        
        Returns:
            Boolean indicating success of update operation
        """
        raise NotImplementedError("Subclasses must implement update method")
    
    @abc.abstractmethod
    async def delete(self, item_id: str, **kwargs) -> bool:
        """
        Delete an item from storage.
        
        Args:
            item_id: Unique identifier of the item
            kwargs: Additional delete parameters
        
        Returns:
            Boolean indicating success of delete operation
        """
        raise NotImplementedError("Subclasses must implement delete method")
    
    @abc.abstractmethod
    async def search(
        self, 
        query: Optional[Dict[str, Any]] = None, 
        **kwargs
    ) -> List[T]:
        """
        Search for items in storage based on query parameters.
        
        Args:
            query: Search query parameters
            kwargs: Additional search parameters
        
        Returns:
            List of matching items
        """
        raise NotImplementedError("Subclasses must implement search method")
    
    def process(self, input_data: Any) -> Any:
        """
        Default processing method.
        
        Args:
            input_data: Input data to process
        
        Returns:
            Processed data (in this case, stored data)
        """
        # Attempt to create the input data in storage
        try:
            result = self.create(input_data)
            self._storage_logger.info(
                f"Processed and stored input data: {result}"
            )
            return result
        except Exception as e:
            self._storage_logger.error(
                f"Error processing input data: {e}"
            )
            raise
    
    def __repr__(self) -> str:
        """
        String representation of the storage provider.
        
        Returns:
            Detailed storage provider information
        """
        return (
            f"&lt;{self.__class__.__name__} "
            f"id={self.provider_id} "
            f"storage_type={self._config.storage_type.name}&gt;"
        )
