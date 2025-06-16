from uuid import uuid4
from utils.logger import Logger
from src.repositories import SessionRepository
from src.models import Session, SessionStatus


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

    async def get_session(self, session_id: int) -> Session:
        """
        Get a session by its external ID
        """
        self.logger.info(f"Getting session with id: {session_id}")

        return await self.session_repository.get_by_id(session_id)

    def open_session(self, session_id: str) -> None:
        try:
            self.session_repository.create_session(session_id)
            self.logger.info(f"Session {session_id} opened successfully")
        except Exception as e:
            self.logger.error(f"Error opening session {session_id}: {e}")
            raise

    def close_session(self, session_id: str) -> None:
        try:
            self.session_repository.close_session(session_id)
            self.logger.info(f"Session {session_id} closed successfully")
        except Exception as e:
            self.logger.error(f"Error closing session {session_id}: {e}")
            raise

    def get_session_status(self, session_id: str) -> SessionStatus:
        try:
            return self.session_repository.get_session_status(session_id)
        except Exception as e:
            self.logger.error(f"Error getting session status for {session_id}: {e}")
            raise

    def delete_session(self, session_id: str) -> None:
        try:
            self.session_repository.delete_session(session_id)
            self.logger.info(f"Session {session_id} deleted successfully")
        except Exception as e:
            self.logger.error(f"Error deleting session {session_id}: {e}")
            raise
