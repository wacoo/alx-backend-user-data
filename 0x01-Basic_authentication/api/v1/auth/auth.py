#!/usr/bin/env python3
''' create API authentication class '''
from flask import request
from typing import List, TypeVar


class Auth:
    ''' Auth class that manages API authentication '''
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        ''' requires authentication '''
        return False

    def authorization_header(self, request=None) -> str:
        ''' authorizes headers '''
        return None

    def current_user(self, request=None) -> None:
        ''' returns current user '''
        return None
