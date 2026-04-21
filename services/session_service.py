from models.session import InterviewSession


class SessionService:
    def __init__(self):
        self.sessions = {}

    def create_session(self, user_id, direction, questions):
        session = InterviewSession(user_id, direction, questions)
        self.sessions[user_id] = session
        return session

    def get_session(self, user_id):
        return self.sessions.get(user_id)

    def remove_session(self, user_id):
        if user_id in self.sessions:
            del self.sessions[user_id]
