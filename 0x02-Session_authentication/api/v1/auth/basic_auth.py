#!/usr/bin/env python3
"""
Contains class that implements Basic auth
"""
from .auth import Auth
import base64
import binascii
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """Implements Basic authentication"""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """gets authorization value from authorization header"""
        if not authorization_header or type(authorization_header) is not str:
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header.split(' ')[1]

    def decode_base64_authorization_header(self,
                                           base64_header: str) -> str:
        """decodes base64 auth header"""
        if not base64_header:
            return None
        if type(base64_header) is not str:
            return None
        try:
            decoded_str = base64.b64decode(base64_header)
            return decoded_str.decode('utf-8')
        except (binascii.Error, UnicodeDecodeError) as err:
            return None

    def extract_user_credentials(self,
                                 decoded_header: str) -> (str, str):
        """gets user email and password from Base64 decoded string"""
        if decoded_header is None:
            return None, None
        if type(decoded_header) is not str:
            return None, None
        indx = decoded_header.find(':')
        if indx == -1:
            return None, None
        email = decoded_header[:indx]
        pwd = decoded_header[indx+1:]
        return email, pwd

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """Gets user instance for given email and password"""
        if not user_email or type(user_email) is not str:
            return None
        if not user_pwd or type(user_pwd) is not str:
            return None

        User.load_from_file()
        users = User.search({'email': user_email})
        if len(users) == 0:
            return None
        user = users[0]
        if not user.is_valid_password(user_pwd):
            return None
        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """gets user information for each requests"""
        auth_token = self.extract_base64_authorization_header(
            self.authorization_header(request))
        email, pwd = self.extract_user_credentials(
            self.decode_base64_authorization_header(auth_token))
        return self.user_object_from_credentials(email, pwd)
