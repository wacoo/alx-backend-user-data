#!/usr/bin/env python3
''' create API authentication class '''
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
        return None

    def current_user(self, request=None) -> None:
        ''' returns current user '''
        return None
