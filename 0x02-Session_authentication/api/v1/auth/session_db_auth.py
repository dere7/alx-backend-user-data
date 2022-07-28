#!/usr/bin/env python3
"""Contains a class that implements SessionExpAuth with Storage"""
from .session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """Implements SessionExpAuth with Storage"""

    def create_session(self, user_id=None):
        """Creates session"""
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Gets user_id by requesting UserSession in the database"""
        UserSession.load_from_file()
        user_session = UserSession.search({'session_id': session_id})
        if not user_session:
            return None
        return user_session[0].user_id

    def destroy_session(self, request=None):
        """Destroys the UserSession from the request cookie"""
        UserSession.load_from_file()
        session_id = self.session_cookie(request)
        user_session = UserSession.search({'session_id': session_id})
        if not user_session:
            return False
        user_session[0].remove()
        return True
