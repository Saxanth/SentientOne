from providers import BaseProvider

class WorkflowProvider(BaseProvider):
    def configure(self, config=None):
        super().configure(config)
