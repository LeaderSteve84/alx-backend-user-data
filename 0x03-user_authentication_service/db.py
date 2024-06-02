#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """create, adds/save the user(update db) and
        returns a new user object.
        Args:
            email (str): user email address
            hashed_password (str): password of user
        Return: User
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """function that finds a user created
        by using a keyword argument
        """
        if not kwargs:
            raise InvalidRequestError('No key word argument provided')

        for k in kwargs.keys():
            if k not in User.__table__.columns.keys():
                raise InvalidRequestError(f'Invalid attribute: {k}')

        userQuery = self._session.query(User).filter_by(**kwargs).first()

        if userQuery is None:

            raise NoResultFound('No argument found with the given attributes')

        return userQuery

    def update_user(self, user_id: int, **kwargs) -> None:
        """use find_user_by to locate the user to update,"""
        user = self.find_user_by(id=user_id)
        for k in kwargs.keys():
            if k not in User.__table__.columns.keys():
                raise ValueError(f'Invalid attribute: {k}')

        for ki, va in kwargs.items():
            setattr(user, ki, va)

        self._session.commit()
