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
        self._engine = create_engine("sqlite:///a.db", echo=True)
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
        """adds, update db and returns anew user object"""
        new_user = User(email=email, hashed_password=hashed_password)
        session = self._session
        # add the new user
        session.add(new_user)
        # update the database
        session.commit()
        session.refresh(new_user)
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """function that finds a user created
        by using a keyword argument
        """
        if kwargs is None:
            raise InvalidRequestError
        for key in kwargs.keys():
            if key not in User.__table__.columns.keys():
                raise InvalidRequestError
        user_query = self._session.query(User).filter_by(**kwargs).first()
        if user_query is None:
            raise NoResultFound
        return user_query
