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
        user = None
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        sid = _generate_uuid()
        self._db.update_user(user.id, session_id=sid)
        return sid

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        ''' return user based on session id '''
        if session_id is None:
            return None
        user = None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user

    def destroy_session(self, user_id: int) -> None:
        ''' destroys session '''
        if user_id is None:
            return None
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        ''' provides reset password token '''
        try:
            user = self._db.find_user_by(email=email)
            if user is None:
                raise ValueError
            token = _generate_uuid()
            self._db.update_user(user.id, reset_token=token)
            return token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        ''' update password based on reset token given '''
        user = None
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError
        if user is None:
            raise ValueError
        hashed = _hash_password(password)
        self._db.update_user(user.id, password=hashed, reset_token=None)
