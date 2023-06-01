#!/usr/bin/env python3
''' create API authentication class '''
from os import getenv
from flask import request
from typing import List, TypeVar


class Auth:
    ''' Auth class that manages API authentication '''
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        ''' requires authentication '''
        path_s = path
        if path is not None and path[-1] != '/':
            path_s = path + '/'
        if not path or excluded_paths is None or len(excluded_paths) == 0\
                or (path not in excluded_paths and
                    path_s not in excluded_paths):
            return True
        return False

    def authorization_header(self, request=None) -> str:
        ''' authorizes headers '''
        if request is None or 'Authorization' not in request.headers:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> None:
        ''' returns current user '''
        return None

    def session_cookie(self, request=None):
        ''' get session value '''
        if request is None:
            return None
        ses_key = getenv('SESSION_NAME')
        cookie = request.cookies.get(ses_key)
        return cookie
