#!/usr/bin/env python3
''' In this task you will define a _hash_password method that takes in
a password string arguments and returns bytes.

The returned bytes is a salted hash of the input password, hashed with
bcrypt.hashpw.
'''
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
    '''
            if user is None:
            hashed = _hash_password(password)
            self._db.add_user(email, hashed)
        raise ValueError('User {} already exists'.format(email))'''