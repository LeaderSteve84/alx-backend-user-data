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

        sl = True if path[len(path) -1] == '/' else False
        tPath = path if sl else path + '/'

        for path_exc in excluded_paths:
            l_path_exc = len(path_exc)
            if l_path_exc == 0:
                continue

            if path_exc[l_path_exc - 1] != '*':
                if tPath == path_exc:
                    return False
                else:
                    if path_exc[:-1] == path[:l_path_exc - 1]:
                        return False
        return True

    def authorization_header(self, request=None) -> str:
        """returns None - request will be the Flask request object
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """returns None - request will be the Flask request object
        """
        return None
