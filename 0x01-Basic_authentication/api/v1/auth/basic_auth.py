#!/usr/bin/env python3
''' create BasicAuth class '''
import base64
from api.v1.auth.auth import Auth


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
