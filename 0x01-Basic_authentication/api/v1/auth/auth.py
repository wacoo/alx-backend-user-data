#!/usr/bin/env python3
''' create API authentication class '''
from flask import request
from typing import List, TypeVar


class Auth:
    ''' Auth class that manages API authentication '''
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        ''' requires authentication '''
        for ep in excluded_paths:
            if ep.endswith('*') and path.startswith(ep[:-1]):
                return False
        path_s = path
        if path is not None and not path.endswith('/'):
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
