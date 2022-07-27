#!/usr/bin/env python3
"""Contains a class that implements Session auth"""
from .auth import Auth
from uuid import uuid4
from models.user import User


class SessionAuth(Auth):
    """Implements Session authentication"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """creates a Session for user"""
        if not user_id or type(user_id) is not str:
            return None
        id = str(uuid4())
        self.user_id_by_session_id[id] = user_id
        return id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Get user ID based on Session ID"""
        if not session_id or type(session_id) is not str:
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """Gets current user"""
        user_id = self.user_id_for_session_id(self.session_cookie(request))
        user = User.get(user_id)
        return user

    def destroy_session(self, request=None):
        """Deletes the user session/logout"""
        if not request:
            return False
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return False
        self.user_id_by_session_id.pop(session_id)
        return True
