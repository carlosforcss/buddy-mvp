from uuid import UUID
from src.models import Session, SessionStatus
from utils.logger import Logger


logger = Logger(__name__)


class SessionRepository:
    model = Session

    @staticmethod
    async def create(external_id: UUID) -> Session:
        """Create a new session"""
        logger.info(f"Creating new session with external ID: {external_id}")
        return await Session.create(external_id=external_id)

    @staticmethod
    async def get_by_external_id(external_id: UUID) -> Session:
        """Get a session by its external ID"""
        logger.info(f"Getting session by external ID: {external_id}")
        return await Session.get(external_id=external_id)

    @staticmethod
    async def get_by_id(id: int) -> Session:
        """Get a session by its ID"""
        logger.info(f"Getting session by ID: {id}")
        return await Session.get(id=id)

    @staticmethod
    async def close_session(session: Session) -> Session:
        """Close a session"""
        logger.info(f"Closing session: {session.id}")
        session.status = SessionStatus.CLOSED
        await session.save()
        return session

    @staticmethod
    async def delete_session(session: Session) -> None:
        """Delete a session"""
        logger.info(f"Deleting session: {session.id}")
        await session.delete()

    @staticmethod
    async def get_session_status(session: Session) -> SessionStatus:
        """Get the status of a session"""
        return session.status
