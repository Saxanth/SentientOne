import asyncio
import uuid
from typing import Any, Dict, List, Optional, Union, Type, TypeVar
from enum import Enum, auto
import logging
import json
from datetime import datetime, timedelta

# Import base provider and storage provider
import sys
import os

# Ensure the parent directories are in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from baseprovider import BaseProvider, ProviderMode
from services.base_service_provider import ServiceEvent
from storage.base_storage_provider import BaseStorageProvider, StorageConfig, StorageType

class MemoryEntryType(Enum):
    """Enumeration of memory entry types."""
    CONTEXT = auto()
    INTERACTION = auto()
    KNOWLEDGE = auto()
    GOAL = auto()
    REASONING = auto()
    SENSORY = auto()

class MemoryEntry:
    """
    Represents a structured memory entry in the SentientOne framework.
    """
    def __init__(
        self, 
        content: Any, 
        entry_type: MemoryEntryType,
        metadata: Optional[Dict[str, Any]] = None,
        expiration: Optional[datetime] = None,
        tags: Optional[List[str]] = None
    ):
        """
        Initialize a memory entry.
        
        Args:
            content: The actual content of the memory entry
            entry_type: Type of memory entry
            metadata: Additional metadata about the entry
            expiration: Optional expiration time for the entry
            tags: Optional list of tags for categorization
        """
        self.id = str(uuid.uuid4())
        self.content = content
        self.type = entry_type
        self.created_at = datetime.now()
        self.metadata = metadata or {}
        self.expiration = expiration
        self.tags = tags or []
    
    def is_expired(self) -> bool:
        """
        Check if the memory entry has expired.
        
        Returns:
            Boolean indicating if the entry is expired
        """
        return self.expiration is not None and datetime.now() > self.expiration
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert memory entry to a dictionary representation.
        
        Returns:
            Dictionary representation of the memory entry
        """
        return {
            'id': self.id,
            'content': self.content,
            'type': self.type.name,
            'created_at': self.created_at.isoformat(),
            'metadata': self.metadata,
            'expiration': self.expiration.isoformat() if self.expiration else None,
            'tags': self.tags
        }

class BaseMemoryProvider(BaseProvider):
    """
    Base Memory Provider for SentientOne Framework
    
    Provides:
    - Semantic memory storage and retrieval
    - Intelligent memory management
    - Context tracking and preservation
    """
    
    def __init__(
        self, 
        provider_id: Optional[str] = None,
        name: Optional[str] = None,
        mode: ProviderMode = ProviderMode.ADAPTIVE,
        max_memory_size: int = 1000,
        default_expiration: timedelta = timedelta(days=30),
        storage_provider: Optional[BaseStorageProvider] = None
    ):
        """
        Initialize the BaseMemoryProvider.
        
        Args:
            provider_id: Unique identifier for the memory provider
            name: Human-readable name for the memory provider
            mode: Operational mode of the memory provider
            max_memory_size: Maximum number of memory entries to store
            default_expiration: Default expiration time for memory entries
            storage_provider: Storage provider for persistent memory storage
        """
        super().__init__(provider_id, name, mode)
        
        # Storage provider
        self._storage_provider = storage_provider or self._create_default_storage()
        
        # Memory management
        self._max_memory_size = max_memory_size
        self._default_expiration = default_expiration
        
        # Logging
        self._memory_logger = logging.getLogger(f"SentientOne.MemoryProvider.{self.name}")
    
    def _create_default_storage(self) -> BaseStorageProvider:
        """
        Create a default in-memory storage provider if no provider is specified.
        
        Returns:
            Default storage provider
        """
        from storage.base_storage_provider import BaseStorageProvider, StorageConfig, StorageType
        
        class DefaultInMemoryStorage(BaseStorageProvider[MemoryEntry]):
            async def create(self, item: MemoryEntry, **kwargs) -> str:
                self._storage_logger.info(f"Storing memory entry: {item.id}")
                return item.id
            
            async def read(self, item_id: str, **kwargs) -> Optional[MemoryEntry]:
                return None  # Placeholder
            
            async def update(self, item_id: str, item: MemoryEntry, **kwargs) -> bool:
                return True  # Placeholder
            
            async def delete(self, item_id: str, **kwargs) -> bool:
                return True  # Placeholder
            
            async def search(
                self, 
                query: Optional[Dict[str, Any]] = None, 
                **kwargs
            ) -> List[MemoryEntry]:
                return []  # Placeholder
        
        return DefaultInMemoryStorage(
            name="DefaultMemoryStorage", 
            config=StorageConfig(storage_type=StorageType.IN_MEMORY)
        )
    
    async def store_memory(
        self, 
        content: Any, 
        entry_type: MemoryEntryType,
        metadata: Optional[Dict[str, Any]] = None,
        expiration: Optional[datetime] = None,
        tags: Optional[List[str]] = None
    ) -> str:
        """
        Store a memory entry.
        
        Args:
            content: The content to be stored
            entry_type: Type of memory entry
            metadata: Additional metadata about the entry
            expiration: Optional expiration time for the entry
            tags: Optional list of tags for categorization
        
        Returns:
            Unique identifier of the stored memory entry
        """
        # Manage memory size (if applicable)
        # Note: Actual size management would depend on the specific storage provider
        
        # Create memory entry
        entry = MemoryEntry(
            content=content,
            entry_type=entry_type,
            metadata=metadata,
            expiration=expiration or (datetime.now() + self._default_expiration),
            tags=tags
        )
        
        # Store using storage provider
        try:
            stored_id = await self._storage_provider.create(entry)
            
            self._memory_logger.info(
                f"Stored memory entry: {stored_id} "
                f"(Type: {entry.type.name}, Tags: {entry.tags})"
            )
            
            return stored_id
        except Exception as e:
            self._memory_logger.error(f"Error storing memory: {e}")
            raise
    
    async def retrieve_memory(
        self, 
        memory_id: Optional[str] = None,
        entry_type: Optional[MemoryEntryType] = None,
        tags: Optional[List[str]] = None,
        metadata_filter: Optional[Dict[str, Any]] = None
    ) -> List[MemoryEntry]:
        """
        Retrieve memory entries based on various filters.
        
        Args:
            memory_id: Specific memory entry ID
            entry_type: Filter by memory entry type
            tags: Filter by tags
            metadata_filter: Filter by metadata
        
        Returns:
            List of matching memory entries
        """
        # Construct search query
        query: Dict[str, Any] = {}
        if memory_id:
            query['id'] = memory_id
        if entry_type:
            query['type'] = entry_type.name
        if tags:
            query['tags'] = tags
        if metadata_filter:
            query['metadata'] = metadata_filter
        
        # Search using storage provider
        try:
            retrieved_entries = await self._storage_provider.search(query)
            
            # Filter out expired entries
            current_time = datetime.now()
            valid_entries = [
                entry for entry in retrieved_entries
                if entry.expiration is None or entry.expiration > current_time
            ]
            
            return valid_entries
        except Exception as e:
            self._memory_logger.error(f"Error retrieving memory: {e}")
            raise
    
    def process(self, input_data: Any) -> Any:
        """
        Process input data and potentially store it in memory.
        
        Args:
            input_data: Input data to process
        
        Returns:
            Processed data
        """
        # Default implementation: store input as a context memory entry
        asyncio.create_task(
            self.store_memory(
                content=input_data, 
                entry_type=MemoryEntryType.CONTEXT
            )
        )
        return input_data
    
    async def clear_memory(self) -> None:
        """
        Clear all memory entries.
        """
        # This would depend on the specific storage provider's capabilities
        # Placeholder implementation
        self._memory_logger.info("Memory clearing initiated")
    
    def __repr__(self) -> str:
        """
        String representation of the memory provider.
        
        Returns:
            Detailed memory provider information
        """
        return (
            f"&lt;{self.__class__.__name__} "
            f"id={self.provider_id} "
            f"storage_type={self._storage_provider._config.storage_type.name}&gt;"
        )
