#!/usr/bin/env python3
"""Contains a class that implements Session auth with expiration date"""
from .session_auth import SessionAuth
import os
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """Implements a session id with expiration date"""

    def __init__(self):
        duration = os.getenv('SESSION_DURATION')
        self.session_duration = int(duration) if duration else 0

    def create_session(self, user_id=None):
        """creates session"""
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        self.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Gets user for given session"""
        if not session_id or session_id not in self.user_id_by_session_id:
            return None
        if self.session_duration <= 0:
            return self.user_id_by_session_id[session_id]['user_id']
        if 'created_at' not in self.user_id_by_session_id[session_id]:
            return None
        created_at = self.user_id_by_session_id[session_id].get('created_at')
        expires_at = timedelta(seconds=created_at.timestamp()) + \
            timedelta(seconds=self.session_duration)
        now = timedelta(seconds=datetime.now().timestamp())
        if expires_at < now:
            return None
        return self.user_id_by_session_id[session_id]['user_id']
