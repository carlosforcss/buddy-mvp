from uuid import UUID
from src.conversations.models.session import Session, SessionStatus


class SessionRepository:
    model = Session

    @staticmethod
    async def create(external_id: UUID) -> Session:
        """Create a new session"""
        return await Session.create(external_id=external_id)

    @staticmethod
    async def get_by_external_id(external_id: UUID) -> Session:
        """Get a session by its external ID"""
        return await Session.get(external_id=external_id)

    @staticmethod
    async def get_by_id(id: int) -> Session:
        """Get a session by its ID"""
        return await Session.get(id=id)

    @staticmethod
    async def close_session(session: Session) -> Session:
        """Close a session"""
        session.status = SessionStatus.CLOSED
        await session.save()
        return session

    @staticmethod
    async def delete_session(session: Session) -> None:
        """Delete a session"""
        await session.delete()

    @staticmethod
    async def get_session_status(session: Session) -> SessionStatus:
        """Get the status of a session"""
        return session.status
