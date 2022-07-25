#!/usr/bin/env python3
"""
contains a class that manages authentication
"""
from flask import request, Request
from typing import TypeVar, List


class Auth:
    """Manages user authentication"""

    def require_auth(self, path: str, execlude_paths: List[str]) -> bool:
        """Checks if a path requires authentication"""
        if path is None:
            return True
        if execlude_paths is None:
            return True
        if path in execlude_paths or path + '/' in execlude_paths:
            return False

        return True

    def authorization_header(self, request: Request = None) -> str:
        """Return authorization header"""
        if request is None:
            return None
        if 'Authorization' not in request.headers:
            return None
        else:
            return request.headers.get('Authorization')
        return None

    def current_user(self, request: Request = None) -> TypeVar('User'):
        """Gets current logged in user"""
        return None
