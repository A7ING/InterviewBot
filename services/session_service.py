# OLD VERSION (no session timeout, in-memory persistence):
# class SessionService:
#     def __init__(self):
#         self.sessions = {}
#     def create_session(self, user_id, direction, questions):
#         session = InterviewSession(user_id, direction, questions)
#         self.sessions[user_id] = session
#         return session

import time
import threading
from models.session import InterviewSession

SESSION_TIMEOUT_SECONDS = 1800  # 30 m
CLEANUP_INTERVAL_SECONDS = 300


class SessionService:
    def __init__(self):
        self.sessions = {}
        self._cleanup_thread = threading.Thread(
            target=self._cleanup_sessions, daemon=True
        )
        self._running = True
        self._cleanup_thread.start()

    def _cleanup_sessions(self):
        while self._running:
            time.sleep(CLEANUP_INTERVAL_SECONDS)
            self._remove_expired_sessions()

    def _remove_expired_sessions(self):
        current_time = time.time()
        expired = [
            user_id
            for user_id, session in self.sessions.items()
            if current_time - session.created_at > SESSION_TIMEOUT_SECONDS
        ]
        for user_id in expired:
            self.remove_session(user_id)

    def create_session(self, user_id, direction, questions):
        self.remove_session(user_id)
        session = InterviewSession(user_id, direction, questions)
        self.sessions[user_id] = session
        return session

    def get_session(self, user_id):
        session = self.sessions.get(user_id)
        if session and time.time() - session.created_at > SESSION_TIMEOUT_SECONDS:
            self.remove_session(user_id)
            return None
        return session

    def remove_session(self, user_id):
        if user_id in self.sessions:
            del self.sessions[user_id]

    def shutdown(self):
        self._running = False
