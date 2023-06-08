#!/usr/bin/env python3
''' In this task you will define a _hash_password method that takes in
a password string arguments and returns bytes.

The returned bytes is a salted hash of the input password, hashed with
bcrypt.hashpw.
'''
from typing import Union
from uuid import uuid4
from db import DB
import bcrypt
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    ''' return hashed password '''
    salt = bcrypt.gensalt()
    encoded = password.encode('utf-8')
    return bcrypt.hashpw(encoded, salt)


def _generate_uuid() -> str:
    ''' return a str representation of uuid '''
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        ''' register user to database '''
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            hashed = _hash_password(password)
            user = self._db.add_user(email, hashed)
            return user
        raise ValueError('User {} already exists'.format(email))

    def valid_login(self, email: str, password: str) -> bool:
        ''' check if user is valid  '''
        try:
            user = self._db.find_user_by(email=email)
            if user is None:
                return False
            encoded = password.encode('utf-8')
            result = bcrypt.checkpw(encoded, user.hashed_password)
            return result
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        ''' returns new session id '''
        try:
            user = self._db.find_user_by(email=email)
            s_id = _generate_uuid()
            self._db.update_user(user.id, session_id=s_id)
            return s_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, seesion_id: str) -> Union[User, None]:
        ''' return user based on session id '''
        if sesssion_id is None:
            return None
        user = None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user
