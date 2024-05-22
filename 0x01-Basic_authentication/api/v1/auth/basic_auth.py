#!/usr/bin/env python3
"""class BasicAuth"""
from api.v1.auth.auth import Auth
from base64 import b64decode
from typing import TypeVar, List
from models.user import User
from flask import request


class BasicAuth(Auth):
    """Basic auth class"""
    def extract_base64_authorization_header(
            self, authorization_header: str
    ) -> str:
        """returns the Base64 part of the Authorization header
        for a Basic Authentication:
        """
        if len(str(authorization_header).split(" ")) == 2:
            if authorization_header \
                    is not None and 'Basic' \
                    in str(authorization_header).split(" ")[0]:
                return authorization_header.split(" ")[1]
        return None

    def decode_base64_authorization_header(
            self, base64_authorization_header: str
    ) -> str:
        """returns the decoded value of a Base64 string
        base64_authorization_header:
        """
        try:
            value_of_utf = base64_authorization_header.encode('utf-8')
            decode_value = b64decode(value_of_utf).decode('utf-8')
            return decode_value
        except (AttributeError, ValueError) as e:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str
    ) -> (str, str):
        """returns the user email and password
        from the Base64 decoded value.
        """
        if decoded_base64_authorization_header is None:
            return (None, None)

        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)

        if ':' not in decoded_base64_authorization_header:
            return (None, None)

        return tuple(decoded_base64_authorization_header.split(':', 1))

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str
    ) -> TypeVar('User'):
        """ returns the User instance based on his
        email and password.
        """
        if not isinstance(user_email, str) or user_email is None:
            return None

        if not isinstance(user_pwd, str) or user_pwd is None:
            return None

        try:
            users = User.search({"email", user_email})
        except Exception:
            return None

        for user in users:
            if user.is_valid_password(user_pwd):
                return user

        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """overloads Auth and retrieves the
        User instance for a request:
        """
        basicVal = self.authorization_header(request)
        valueOf64 = self.extract_base64_authorization_header(basicVal)
        decoded_value = self.decode_base64_authorization_header(valueOf64)
        email, pwd = self.extract_user_credentials(decoded_value)
        user = self.user_object_from_credentials(email, pwd)
        return user
