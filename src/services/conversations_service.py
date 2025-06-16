from utils.ai import OpenAIClient
from utils.logger import Logger
from config.settings import OPENAI_API_KEY


logger = Logger(__name__)


class ConversationsService:
    def __init__(self):
        self.logger = logger
        self.ai_client = OpenAIClient(OPENAI_API_KEY)

    async def send_simple_message(self, message: str) -> str:
        """
        Send a simple message to the AI client and return the response.
        """
        self.logger.info(f"Sending message: {message}")
        response = self.ai_client.send_message(message)
        self.logger.info(f"Received response: {response}")
        return response
