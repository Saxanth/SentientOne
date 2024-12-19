import logging
from providers.baseprovider import BaseProvider, ProviderMode

class BaseWorkflowProvider(BaseProvider):
    def __init__(self):
        super().__init__()
        self._logger = logging.getLogger(self.__class__.__name__)

    def configure(self, config=None):
        super().configure(config)

    def reset(self):
        """Reset the provider to its initial state."""
        super().reset()
