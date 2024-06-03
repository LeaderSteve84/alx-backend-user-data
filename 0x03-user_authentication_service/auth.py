#!/usr/bin/env python3
"""module of auth.py"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> str:
    """in a password string arguments and return32


    s bytes"""
    salt = bcrypt.gensalt()
    encoded_password = password.encode()
    return bcrypt.hashpw(encoded_password, salt)


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """register a new user with authentication"""
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            encrypt_pwd = _hash_password(password=password)
            return self._db.add_user(email=email, hashed_password=encrypt_pwd)
        else:
            raise ValueError("User {} already exists".format(email))

    def valid_login(self, email: str, password: str) -> bool:
        """return a boolean."""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        else:
            return bcrypt.checkpw(
                    password=password.encode(),
                    hashed_password=user.hashed_password
                )
