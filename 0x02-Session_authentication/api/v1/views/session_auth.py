#!/usr/bin/env python3
''' create a view for session authentication '''
from api.v1.views import app_views
from flask import jsonify, request
from typing import Tuple
from api.v1.app import auth
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def authenticate() -> Tuple[str, int]:
    ''' authenticate user '''
    email = request.form.get('email')
    password = request.form.get('password')
    if not email or email == '':
        return jsonify({'error': 'email missing'}), 400
    if not password or password == '':
        return jsonify({'error': 'password missing'}), 400
    try:
        users = User.search({'email': email})
    except Exception:
        error = 'no user found for this email'
        return jsonify({'error': error}), 404
    if len(user) <= 0:
        return jsonify({'error': error}), 404
    if users[0].is_valid_password(password):
        ses_id = auth.create_session(getattr(users[0], 'id'))
        udata = jsonify(users[0].to_json())
        udata.set_cookie(getenv('SESSION_NAME'), ses_id)
        return udata
    return jsonify({'error': 'wrong password'}), 401
