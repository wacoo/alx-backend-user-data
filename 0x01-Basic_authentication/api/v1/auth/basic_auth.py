#!/usr/bin/env python3
''' create BasicAuth class '''
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    ''' BasicAuth class '''
    def extract_base64_authorization_header(self, authorization_header: str
                                            ) -> str:
        ''' ''decode credentials '''
        ah = authorization_header
        if ah is None or type(ah) != str or ah[:6] != 'Basic ':
            return None
        return ah[6:]
