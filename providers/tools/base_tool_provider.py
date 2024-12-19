from providers import BaseProvider

class ToolProvider(BaseProvider):
    def configure(self, config=None):
        super().configure(config)
