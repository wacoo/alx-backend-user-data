#!/usr/bin/env python3
''' In this task, you will set up a basic Flask app. '''
from auth import Auth
from flask import Flask, jsonify, request, abort, redirect


app = Flask(__name__)

AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def home() -> str:
    ''' return a json data '''
    return jsonify({'message': 'Bienvenue'})


@app.route('/users', methods=['POST'], strict_slashes=False)
def register_user() -> str:
    ''' register user '''
    email = request.form.get('email')
    passwd = request.form.get('password')
    try:
        user = AUTH.register_user(email, passwd)
        json = {'email': email, 'message': 'user created'}
        return jsonify(json)
    except ValueError:
        json = {'message': 'email already registered'}
        return jsonify(json), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    ''' verify if user is authorized '''
    email = request.form.get('email')
    passwd = request.form.get('password')
    if not AUTH.valid_login(email, passwd):
        abort(401)

    sid = AUTH.create_session(email)
    res = jsonify({'email': email, 'message': 'logged in'})
    res.set_cookie('session_id', sid)
    return res


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    ''' logout user '''
    sid = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(sid)
    if user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect('/')


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> str:
    ''' show user profile '''
    sid = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(sid)
    if user is None:
        abort(403)
    return jsonify({'email': user.email})


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token() -> str:
    ''' get reset password token '''
    email = request.form.get('email')
    token = None
    try:
        token = AUTH.get_reset_password_token(email)
    except ValueError:
        token = None
    if token is None:
        abort(403)
    return jsonify({'email': email, 'reset_token': token})


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password() -> str:
    ''' update user password '''
    email = request.form.get('email')
    token = request.form.get('reset_token')
    n_pass = request.form.get('new_password')
    passwd_reset = False
    try:
        AUTH.update_password(token, n_pass)
        passwd_reset = True
    except ValueError:
        passwd_reset = False
    if not passwd_reset:
        abort(403)
    json = {'email': email, 'message': 'Password updated'}
    return jsonify(json)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
