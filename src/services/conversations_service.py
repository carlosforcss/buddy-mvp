from utils.ai import AIClient


class ConversationsService:
    def __init__(self, ai_client: AIClient, conversations_repository, logger):
        self.conversations_repository = conversations_repository
        self.logger = logger
        self.ai_client = ai_client

    async def send_simple_message(self, message: str) -> str:
        """
        Send a simple message to the AI client and return the response.
        """
        self.logger.info(f"Sending message: {message}")
        response = self.ai_client.send_message(message)
        self.logger.info(f"Received response: {response}")
        return response
