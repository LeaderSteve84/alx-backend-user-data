#!/usr/bin/env python3
"""auth class to manage API authentication"""
from flask import request
from typing import List, TypeVar
import os


class Auth:
    """Auth class"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """returns False - path and excluded_paths
        """
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True

        if len(path) == 0:
            return True

        if not path.endswith('/'):
            path += '/'

        for excluded_path in excluded_paths:
            if excluded_path.endswith('*'):
                if path.startswith(excluded_path[:-1]):
                    return False

            if not excluded_path.endswith('/'):
                excluded_path += '/'

            if excluded_path == path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """returns None - request will be the Flask request object
        """
        if request is None:
            return None
        else:
            return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        """returns None - request will be the Flask request object
        """
        return None

    def session_cookie(self, request=None):
        """returns a cookie value from a request:"""
        if request is None:
            return None

        if os.getenv('SESSION_NAME') is None:
            return None

        return request.cookies.get(os.getenv('SESSION_NAME'))
