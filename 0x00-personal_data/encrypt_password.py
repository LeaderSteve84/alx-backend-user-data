#!/usr/bin/env python3
"""Implement a hash_password function"""

import bycrypt


def hash_password(password: str) -> bytes:
    """return a password"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """validate that the provided password and hashed password matches.
    """
    return bcrypt.checkpw(password.encode(), hashed_password)
