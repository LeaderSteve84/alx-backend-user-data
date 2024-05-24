#!/usr/bin/env python3
"""auth class to manage API authentication"""
from flask import request
from typing import List, TypeVar

class Auth:
    """Auth class"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Checks if authentication is required for the given path"""
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True

        # Ensure path always ends with a slash for comparison
        if not path.endswith('/'):
            path += '/'

        for excluded_path in excluded_paths:
            # Handle wildcard exclusion paths
            if excluded_path.endswith('*'):
                if path.startswith(excluded_path[:-1]):
                    return False

            # Ensure excluded_path always ends with a slash for comparison
            if not excluded_path.endswith('/'):
                excluded_path += '/'

            # Exact match for non-wildcard paths
            if excluded_path == path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """Returns None - request will be the Flask request object"""
        if request is None:
            return None
        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns None - request will be the Flask request object"""
        return None
