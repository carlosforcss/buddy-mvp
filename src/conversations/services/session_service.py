from uuid import uuid4
from utils.logger import Logger
from src.conversations.repositories.session import SessionRepository
from src.conversations.models.session import Session


class SessionService:
    def __init__(
        self,
        session_repository: SessionRepository,
        logger: Logger,
    ):
        self.session_repository = session_repository
        self.logger = logger

    async def create_session(self) -> Session:
        """
        Create a new session with a unique external ID
        """
        self.logger.info("Creating new session")
        external_id = uuid4()
        session = await self.session_repository.create(external_id=external_id)
        self.logger.info(f"Created session with external_id: {external_id}")
        return session

    async def get_session(self, external_id: str) -> Session:
        """
        Get a session by its external ID
        """
        self.logger.info(f"Getting session with external_id: {external_id}")
        return await self.session_repository.get_by_external_id(external_id) 