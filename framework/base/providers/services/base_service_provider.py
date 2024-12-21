import asyncio
import uuid
from typing import Any, Dict, List, Optional, Union
from enum import Enum, auto
import logging

from providers.baseprovider import BaseProvider, ProviderMode

class ServiceEvent(Enum):
    """
    Enumeration of standard service events.
    """
    STARTED = auto()
    STOPPED = auto()
    PAUSED = auto()
    RESUMED = auto()
    ERROR = auto()

class BaseServiceProvider(BaseProvider):
    def __init__(self):
        super().__init__()
        self._logger = logging.getLogger(self.__class__.__name__)

    def configure(self, config=None):
        super().configure(config)

    def reset(self):
        super().reset()
