#!/usr/bin/env python3
"""auth class to manage API authentication"""
from flask import request
from typing import List, TypeVar


class Auth:
    """Auth class"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """returns False - path and excluded_paths
        """
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True

        if len(path) == 0:
            return True

        slh = True if path[len(path) - 1] == '/' else False
        tPath = path if slh else path + '/'

        for excluded_path in excluded_paths:
            length_excluded_path = len(excluded_path)
            if length_excluded_path == 0:
                continue

            if excluded_path[length_excluded_path - 1] == '*':
                if tPath == excluded_path:
                    return False
                else:
                    if excluded_path[:-1] == path[:length_excluded_path - 1]:
                        return False
        return False

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
