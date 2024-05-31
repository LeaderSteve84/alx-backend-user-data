#!/usr/bin/env python3
"""module of auth.py"""
import bcrypt


def _hash_password(password: str) -> str:
    """in a password string arguments and return32


    s bytes"""
    salt = bcrypt.gensalt()
    encoded_password = password.encode()
    return bcrypt.hashpw(encoded_password, salt)
