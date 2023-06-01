#!/usr/bin/env python3
''' create a class for session authentication '''
from api.v1.auth.auth import Auth
from uuid import uuid4


class SessionAuth(Auth):
    ''' SessionAuth class for session authentication '''
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        ''' returns new session id '''
        if user_id is None:
            return None
        elif type(user_id) != str:
            return None
        ses_id = str(uuid4())
        SessionAuth.user_id_by_session_id[ses_id] = user_id
        return ses_id
