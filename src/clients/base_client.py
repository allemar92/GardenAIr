class BaseClient:
    """
    Base class for all LLM clients.
    This allows you to standardize your interface (e.g., LiteLLMClient, OpenAIClient, etc.)
    """
    def get_client(self):
        """
        This method should be implemented by subclasses
        to return a configured client instance.
        """
        raise NotImplementedError("Subclasses must implement get_client()")
