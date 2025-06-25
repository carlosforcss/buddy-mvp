from typing import List, Optional
from src.models import RealtimeEvent, EventDirection
from utils.logger import Logger


logger = Logger(__name__)


class RealtimeEventRepository:
    model = RealtimeEvent

    @staticmethod
    async def create(session_id: int, event_type: str, event_body: dict, direction: EventDirection) -> RealtimeEvent:
        """Create a new realtime event"""
        logger.info(f"Creating new realtime event for session {session_id}: {event_type} ({direction})")
        return await RealtimeEvent.create(
            session_id=session_id,
            type=event_type,
            event_body=event_body,
            direction=direction
        )

    @staticmethod
    async def get_by_session_id(session_id: int, limit: Optional[int] = None) -> List[RealtimeEvent]:
        """Get all realtime events for a session"""
        logger.info(f"Getting realtime events for session {session_id}")
        query = RealtimeEvent.filter(session_id=session_id).order_by('-created_at')
        if limit:
            query = query.limit(limit)
        return await query

    @staticmethod
    async def get_by_id(event_id: int) -> RealtimeEvent:
        """Get a realtime event by its ID"""
        logger.info(f"Getting realtime event by ID: {event_id}")
        return await RealtimeEvent.get(id=event_id)

    @staticmethod
    async def delete_by_session_id(session_id: int) -> None:
        """Delete all realtime events for a session"""
        logger.info(f"Deleting all realtime events for session {session_id}")
        await RealtimeEvent.filter(session_id=session_id).delete()