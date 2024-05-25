#!/usr/bin/env python3
"""Session Auth"""
from api.v1.auth.auth import Auth
import uuid
from models.user import User


class SessionAuth(Auth):
    """class for session Authentication"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """function that create a Session ID for a user_id"""
        if user_id is None:
            return None

        if not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        print(f"Created session ID: {session_id} for user ID: {user_id}")  # Debug statement
        print(self.user_id_by_session_id)

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """returns a User ID based on a Session ID
        """
        if session_id is None:
            return None

        elif not isinstance(session_id, str):
            return None

        else:
            user_id = self.user_id_by_session_id.get(session_id)
            print(f"Retrieved user ID: {user_id} for session ID: {session_id}")  # Debug statement
            return user_id

    def session_cookie(self, request=None):
        """Returns the value of the session cookie"""
        if request is None:
            return None
        cookie = request.cookies.get('_my_session_id')
        print("Session cookie:", cookie)  # Debug statement
        return cookie

    def current_user(self, request=None):
        """returns a User instance based on a cookie value:"""
        session_id = self.session_cookie(request)
        print("Session ID:", session_id)  # Debug statement
        if session_id is None:
            return None
        user_id = self.user_id_for_session_id(session_id)
        print("User ID:", user_id)  # Debug statement
        if user_id:
            return User.get(user_id)
        return None
