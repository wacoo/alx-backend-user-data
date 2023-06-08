#!/usr/bin/env python3
''' In this task, you will set up a basic Flask app. '''
from auth import Auth
from flask import Flask, jsonify, request, abort


app = Flask(__name__)
auth = Auth()


@app.route('/', strict_slashes=False)
def home():
    ''' return a json data '''
    return jsonify({'message': 'Bienvenue'})


@app.route('/users', methods=['POST'], strict_slashes=False)
def register_user():
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
    auth = Auth()
    email = request.form.get('email')
    passwd = request.form.get('password')
    if not auth.valid_login(email, passwd):
        abort(401)
    s_id = auth.create_session(email)
    response = jsonify({'email': email, 'message': 'logged in'})
    response.set_cookie('session_id', s_id)
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
