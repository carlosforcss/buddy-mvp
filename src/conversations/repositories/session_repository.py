from enum import Enum
from typing import Optional

class SessionStatus(Enum):
    OPENED = "opened"
    CLOSED = "closed"

class SessionRepository:
    def __init__(self):
        self._sessions = {}

    def create_session(self, session_id: str) -> None:
        self._sessions[session_id] = SessionStatus.OPENED

    def close_session(self, session_id: str) -> None:
        if session_id in self._sessions:
            self._sessions[session_id] = SessionStatus.CLOSED

    def get_session_status(self, session_id: str) -> Optional[SessionStatus]:
        return self._sessions.get(session_id)

    def delete_session(self, session_id: str) -> None:
        if session_id in self._sessions:
            del self._sessions[session_id] 