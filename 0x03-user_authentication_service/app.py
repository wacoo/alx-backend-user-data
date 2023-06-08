#!/usr/bin/env python3
''' In this task, you will set up a basic Flask app. '''
from auth import Auth
from flask import Flask, jsonify, request, abort, redirect


app = Flask(__name__)
auth = Auth()


@app.route('/', strict_slashes=False)
def home() -> str:
    ''' return a json data '''
    return jsonify({'message': 'Bienvenue'})


@app.route('/users', methods=['POST'], strict_slashes=False)
def register_user() -> str:
    ''' register user '''
    email = request.form.get('email')
    passwd = request.form.get('password')
    try:
        user = auth.register_user(email, passwd)
        json = {'email': email, 'message': 'user created'}
        return jsonify(json)
    except ValueError:
        json = {'message': 'email already registered'}
        return jsonify(json), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    ''' verify user '''
    email = request.form.get('email')
    passwd = request.form.get('password')
    if not auth.valid_login(email, passwd):
        abort(401)
    s_id = auth.create_session(email)
    response = jsonify({'email': email, 'message': 'logged in'})
    response.set_cookie('session_id', s_id)
    return response


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    ''' logout user '''
    s_id = request.cookies.get('session_id')
    user = auth.get_user_from_session_id(s_id)
    if user is None:
        abort(403)
    auth.destroy_session(user.id)
    return redirect('/')


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> str:
    ''' show user profile '''
    s_id = request.cookies.get('session_id')
    user = auth.get_user_from_session_id(s_id)
    if user is None:
        abort(403)
    return jsonify({'email': user.email})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
