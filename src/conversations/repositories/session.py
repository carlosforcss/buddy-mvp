from uuid import UUID
from src.conversations.models.session import Session


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