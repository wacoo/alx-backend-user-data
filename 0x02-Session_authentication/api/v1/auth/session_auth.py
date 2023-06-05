#!/usr/bin/env python3
''' create a class for session authentication '''
from api.v1.auth.auth import Auth
from uuid import uuid4
from models.user import User


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

    def user_id_for_session_id(self, session_id: str = None) -> str:
        ''' returns the user id for given session id '''
        if session_id is None:
            return None
        elif type(session_id) != str:
            return None
        return SessionAuth.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        ''' return user instance '''
        session = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session)
        return User.get(user_id)
    def destroy_session(self, request=None):
        ''' deletes user session at logout '''
        if request is None:
            return False
        cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session)
        if cookie is None:
            return False
        if user_id is None:
            return False
        '''ses_id = self.session_cookie(request)
        if ses_id in SessionAuth.user_id_session_id:
            del SessionAuth.user_id_session_id[ses_id]
        return True'''
