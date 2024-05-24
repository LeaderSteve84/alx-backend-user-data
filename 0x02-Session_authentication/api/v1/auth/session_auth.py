#!/usr/bin/env python3
"""Session Auth"""
from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """class for session Authentication"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """function that create a Session ID for a user_id"""
        if user_id is None:
            return None

        if not isinstance(user_id, str):
            return None

        session_ID = str(uuid.uuid4())
        self.user_id_by_session_id[session_ID] = user_id

        return session_ID
