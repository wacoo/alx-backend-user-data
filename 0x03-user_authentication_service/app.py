#!/usr/bin/env python3
''' In this task, you will set up a basic Flask app. '''
from auth import Auth
from flask import Flask, jsonify, request


app = Flask(__name__)


@app.route('/', strict_slashes=False)
def home():
    ''' return a json data '''
    return jsonify({'message': 'Bienvenue'})

@app.route('/users', methods=['POST'], strict_slashes=False)
def register_user():
    ''' register user '''
    auth = Auth()
    email = request.form.get('email')
    passwd =  request.form.get('password')
    try:
        user = auth.register_user(email, passwd)
        json = {'email': email, 'message': 'user created'}
        return jsonify(json)
    except ValueError:
        json = {'message': 'email already registered'}
        return jsonify(json), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
