#!/usr/bin/env python3
''' create a view for session authentication '''
from api.v1.views import app_views
from flask import jsonify, request
from typing import Tuple
from api.v1.app import auth
from os import getenv
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def authenticate() -> Tuple[str, int]:
    ''' authenticate user '''
    email = request.form.get('email')
    password = request.form.get('password')
    user = ''
    error = 'no user found for this email'
    if not email or len(email) == 0:
        return jsonify({'error': 'email missing'}), 400
    if not password or len(password) == 0:
        return jsonify({'error': 'password missing'}), 400
    try:
        users = User.search({'email': email})
    except Exception as e:
        print('XXX', e)
        return jsonify({'error': error}), 404
    if len(user) <= 0:
        return jsonify({'error': error}), 404
    if users[0].is_valid_password(password):
        ses_id = auth.create_session(getattr(users[0], 'id'))
        udata = jsonify(users[0].to_json())
        udata.set_cookie(getenv('SESSION_NAME'), ses_id)
        return udata
    return jsonify({'error': 'wrong password'}), 401
