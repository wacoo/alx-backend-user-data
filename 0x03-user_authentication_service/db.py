#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine, select, tuple_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from user import Base
from typing import TypeVar
from user import User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db"''',echo=True''')
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
        ''' insert user data to database '''
        user = None
        try:
            user = User(email=email, hashed_password=hashed_password)
            self._session.add(user)
            self._session.commit()
        except Exception:
            self._session.rollback()
            return None
        return user

    def find_user_by(self, **kwargs):
        ''' return the first user data based on input '''
        ukey = []
        uval = []
        for key, val in kwargs.items():
            if hasattr(User, key):
                ukey.append(getattr(User, key))
                uval.append(val)
            else:
                raise InvalidRequestError
        user = self._session.query(User).filter(
                tuple_(*ukey).in_([tuple(uval)])).first()
        if user is None:
            raise NoResultFound()
        return user
