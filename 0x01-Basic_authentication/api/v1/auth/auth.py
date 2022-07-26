#!/usr/bin/env python3
"""Contains a class that manages authentications"""
from flask import Request
from typing import TypeVar, List


class Auth:
    """Manages user authentication and base for other auth classes"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Checks if a path requires authentication"""
        if path is None:
            return True
        if excluded_paths is None:
            return True
        if path in excluded_paths or path + '/' in excluded_paths:
            return False

        return True

    def authorization_header(self, request=None) -> str:
        """Return authorization header"""
        if request is None:
            return None
        if 'Authorization' not in request.headers:
            return None
        else:
            return request.headers.get('Authorization')
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Gets current logged in user"""
        return None
