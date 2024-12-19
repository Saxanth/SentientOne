import asyncio
import uuid
import logging
from typing import Any, Callable, Dict, List, Optional, Union, Type
from enum import Enum, auto
from dataclasses import dataclass, field
from datetime import datetime

# Import base dependencies
import sys
import os
import json

# Ensure the parent directories are in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from baseprovider import BaseProvider, ProviderMode
from memory.base_memory_provider import BaseMemoryProvider, MemoryEntryType
from agents.base_persona_provider import BasePersonaProvider

class CommunicationProtocol(Enum):
    """
    Enumeration of communication protocols.
    Supports various communication paradigms.
    """
    DIRECT = auto()       # Direct, point-to-point communication
    BROADCAST = auto()    # One-to-many communication
    MULTICAST = auto()    # Selective group communication
    PUBLISH_SUBSCRIBE = auto()  # Event-driven communication
    NEGOTIATION = auto()  # Collaborative decision-making
    CONSENSUS = auto()    # Distributed agreement

class MessagePriority(Enum):
    """
    Message priority levels for intelligent routing.
    """
    LOW = 1
    NORMAL = 5
    HIGH = 10
    CRITICAL = 15

class MessageStatus(Enum):
    """
    Tracking the lifecycle of a message.
    """
    CREATED = auto()
    QUEUED = auto()
    SENT = auto()
    RECEIVED = auto()
    PROCESSED = auto()
    FAILED = auto()

@dataclass
class CommunicationIdentity:
    """
    Represents a unique communication identity.
    Provides context and routing information.
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: Optional[str] = None
    type: Optional[str] = None  # e.g., 'agent', 'service', 'system'
    
    # Optional routing and access metadata
    address: Optional[str] = None
    permissions: List[str] = field(default_factory=list)

@dataclass
class Message:
    """
    Comprehensive message representation.
    Supports rich, context-aware communication.
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    
    # Message content and metadata
    sender: CommunicationIdentity
    recipients: List[CommunicationIdentity]
    
    content: Any
    timestamp: datetime = field(default_factory=datetime.now)
    
    # Communication context
    protocol: CommunicationProtocol = CommunicationProtocol.DIRECT
    priority: MessagePriority = MessagePriority.NORMAL
    status: MessageStatus = MessageStatus.CREATED
    
    # Optional routing and processing hints
    context: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    
    def serialize(self) -> str:
        """
        Serialize message for transmission.
        
        Returns:
            JSON-encoded message
        """
        return json.dumps({
            'id': self.id,
            'sender': asdict(self.sender),
            'recipients': [asdict(r) for r in self.recipients],
            'content': str(self.content),
            'timestamp': self.timestamp.isoformat(),
            'protocol': self.protocol.name,
            'priority': self.priority.name,
            'status': self.status.name,
            'context': self.context,
            'tags': self.tags
        })
    
    @classmethod
    def deserialize(cls, message_json: str) -> 'Message':
        """
        Deserialize message from JSON.
        
        Args:
            message_json: JSON-encoded message
        
        Returns:
            Reconstructed Message instance
        """
        data = json.loads(message_json)
        return cls(
            id=data['id'],
            sender=CommunicationIdentity(**data['sender']),
            recipients=[CommunicationIdentity(**r) for r in data['recipients']],
            content=data['content'],
            timestamp=datetime.fromisoformat(data['timestamp']),
            protocol=CommunicationProtocol[data['protocol']],
            priority=MessagePriority[data['priority']],
            status=MessageStatus[data['status']],
            context=data['context'],
            tags=data['tags']
        )

class BaseCommuncationProvider(BaseProvider):
    """
    Comprehensive communication management provider.
    
    Features:
    - Multi-protocol communication
    - Intelligent message routing
    - Context-aware messaging
    - Secure communication channels
    """
    
    def __init__(
        self, 
        provider_id: Optional[str] = None,
        name: Optional[str] = None,
        mode: ProviderMode = ProviderMode.ADAPTIVE,
        memory_provider: Optional[BaseMemoryProvider] = None,
        persona_provider: Optional[BasePersonaProvider] = None
    ):
        """
        Initialize the BaseCommunicationProvider.
        
        Args:
            provider_id: Unique identifier for the communication provider
            name: Human-readable name for the communication provider
            mode: Operational mode of the communication provider
            memory_provider: Memory provider for tracking communications
            persona_provider: Persona provider for communication context
        """
        super().__init__(provider_id, name, mode)
        
        # Communication management
        self._identities: Dict[str, CommunicationIdentity] = {}
        self._message_queue: asyncio.Queue = asyncio.Queue()
        
        # Contextual providers
        self._memory_provider = memory_provider or self._create_default_memory_provider()
        self._persona_provider = persona_provider
        
        # Logging and tracking
        self._communication_logger = logging.getLogger(f"SentientOne.CommunicationProvider.{self.name}")
        
        # Message processing task
        self._message_processor_task: Optional[asyncio.Task] = None
    
    def _create_default_memory_provider(self) -> BaseMemoryProvider:
        """
        Create a default memory provider if none is specified.
        
        Returns:
            Default memory provider
        """
        return BaseMemoryProvider(
            name=f"{self.name}_DefaultMemory",
            mode=self.mode
        )
    
    def register_identity(
        self, 
        name: str, 
        type: str = 'agent',
        address: Optional[str] = None,
        permissions: Optional[List[str]] = None
    ) -> CommunicationIdentity:
        """
        Register a new communication identity.
        
        Args:
            name: Unique name for the identity
            type: Type of identity
            address: Optional communication address
            permissions: Optional list of communication permissions
        
        Returns:
            Registered CommunicationIdentity
        
        Raises:
            ValueError: If identity already exists
        """
        if name in self._identities:
            raise ValueError(f"Identity {name} already exists")
        
        identity = CommunicationIdentity(
            name=name,
            type=type,
            address=address,
            permissions=permissions or []
        )
        
        self._identities[name] = identity
        
        self._communication_logger.info(
            f"Registered identity: {name} "
            f"(Type: {type}, Address: {address})"
        )
        
        return identity
    
    async def send_message(
        self, 
        sender: Union[str, CommunicationIdentity],
        recipients: Union[str, List[str], CommunicationIdentity, List[CommunicationIdentity]],
        content: Any,
        protocol: CommunicationProtocol = CommunicationProtocol.DIRECT,
        priority: MessagePriority = MessagePriority.NORMAL,
        context: Optional[Dict[str, Any]] = None,
        tags: Optional[List[str]] = None
    ) -> Message:
        """
        Send a message through the communication system.
        
        Args:
            sender: Sender's identity or name
            recipients: Recipients' identities or names
            content: Message content
            protocol: Communication protocol
            priority: Message priority
            context: Optional contextual information
            tags: Optional message tags
        
        Returns:
            Sent Message instance
        """
        # Resolve sender
        if isinstance(sender, str):
            sender = self._identities.get(sender)
        
        # Resolve recipients
        if not isinstance(recipients, list):
            recipients = [recipients]
        
        resolved_recipients = []
        for recipient in recipients:
            if isinstance(recipient, str):
                resolved_recipient = self._identities.get(recipient)
                if not resolved_recipient:
                    raise ValueError(f"Recipient {recipient} not found")
                resolved_recipients.append(resolved_recipient)
            else:
                resolved_recipients.append(recipient)
        
        # Create message
        message = Message(
            sender=sender,
            recipients=resolved_recipients,
            content=content,
            protocol=protocol,
            priority=priority,
            context=context or {},
            tags=tags or []
        )
        
        # Enqueue message
        await self._message_queue.put(message)
        
        # Log message
        self._communication_logger.info(
            f"Message queued: {message.id} "
            f"(From: {sender.name}, Recipients: {len(resolved_recipients)}, "
            f"Priority: {priority.name})"
        )
        
        return message
    
    async def _process_messages(self):
        """
        Asynchronous message processing loop.
        Handles message routing and processing.
        """
        while True:
            try:
                # Wait for and retrieve message
                message = await self._message_queue.get()
                
                # Update message status
                message.status = MessageStatus.RECEIVED
                
                # Process message based on protocol
                if message.protocol == CommunicationProtocol.DIRECT:
                    await self._process_direct_message(message)
                elif message.protocol == CommunicationProtocol.BROADCAST:
                    await self._process_broadcast_message(message)
                # Add more protocol-specific processing as needed
                
                # Store message in memory
                await self._memory_provider.store_memory(
                    content=message.serialize(),
                    entry_type=MemoryEntryType.CONTEXT
                )
                
                # Mark message as processed
                message.status = MessageStatus.PROCESSED
                
            except Exception as e:
                self._communication_logger.error(
                    f"Error processing message: {e}"
                )
                message.status = MessageStatus.FAILED
            
            finally:
                # Always mark task as done
                self._message_queue.task_done()
    
    async def _process_direct_message(self, message: Message):
        """
        Process a direct message to specific recipients.
        
        Args:
            message: Message to process
        """
        # Placeholder for direct message processing
        # In a real implementation, this would route to specific recipients
        self._communication_logger.info(
            f"Processing direct message: {message.id} "
            f"to {len(message.recipients)} recipients"
        )
    
    async def _process_broadcast_message(self, message: Message):
        """
        Process a broadcast message to all registered identities.
        
        Args:
            message: Message to broadcast
        """
        self._communication_logger.info(
            f"Broadcasting message: {message.id} "
            f"to all registered identities"
        )
    
    async def start(self):
        """
        Start the communication provider.
        Initializes message processing loop.
        """
        if not self._message_processor_task:
            self._message_processor_task = asyncio.create_task(
                self._process_messages()
            )
            self._communication_logger.info(
                "Communication provider started"
            )
    
    async def stop(self):
        """
        Stop the communication provider.
        Cancels message processing loop.
        """
        if self._message_processor_task:
            self._message_processor_task.cancel()
            try:
                await self._message_processor_task
            except asyncio.CancelledError:
                pass
            
            self._message_processor_task = None
            self._communication_logger.info(
                "Communication provider stopped"
            )
