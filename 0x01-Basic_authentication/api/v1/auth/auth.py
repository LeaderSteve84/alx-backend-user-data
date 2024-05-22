#!/usr/bin/env python3
"""auth class to manage authentication"""
from flask import request
from typing import List, TypeVAr


class Auth:
    """Auth class"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """returns False - path and excluded_paths
        """
        return False

    def authorization_header(self, request=None) -> str:
        """returns None - request will be the Flask request object
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """returns None - request will be the Flask request object
        """
        return None