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
            decode_value= b64decode(value_of_utf).decode('utf-8')
            return decode_value
        except (AttributeError, ValueError) as e:
            return None
