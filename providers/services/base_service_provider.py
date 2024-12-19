from providers import BaseProvider

class ServiceProvider(BaseProvider):
    def configure(self, config=None):
        super().configure(config)
