#!/usr/bin/env python3
''' Implement a hash_password function that expects one string
argument name password and returns a salted, hashed password,
which is a byte string.
Use the bcrypt package to perform the hashing (with hashpw).
'''
import bcrypt


def hash_password(password: str) -> bytes:
    ''' return hashed string as bytes '''
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt(14))
    return hashed


def is_valid(hashed_password: bytes, password) -> bool:
    ''' checks if password and hash are the same '''
    return bcrypt.checkpw(password.encode(), hashed_password)
