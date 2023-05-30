#!/usr/bin/env python3
''' create BasicAuth class '''
import base64
from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    ''' BasicAuth class '''
    def extract_base64_authorization_header(self, authorization_header: str
                                            ) -> str:
        ''' ''extract credentials from auth header '''
        ah = authorization_header
        if ah is None or type(ah) != str or ah[:6] != 'Basic ':
            return None
        return ah[6:]

    def decode_base64_authorization_header(self, base64_authorization_header:
                                           str) -> str:
        ''' decode credentials '''
        try:
            bah = base64_authorization_header
            if bah is None or type(bah) != str:
                return None
            decoded = base64.b64decode(bah)
            return decoded.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header:
                                 str) -> (str, str):
        ''' extract email and password '''
        decoded = decoded_base64_authorization_header
        if decoded is None or type(decoded) != str or ':' not in decoded:
            return (None, None)
        cred = decoded.split(':')
        return (cred[0], cred[1])

    def user_object_from_credentials(self, user_email: str, user_pwd:
                                     str) -> TypeVar('User'):
        ''' returns the user object '''
        if user_email is None or type(user_email) != str or user_pwd\
                is None or type(user_pwd) != str:
            return None
        try:
            email = {'email': user_email}
            usr = User.search(email)
        except Exception:
            return None
        if len(usr) == 0:
            return None
        if usr[0].is_valid_password(user_pwd):
            return usr[0]
        return None
