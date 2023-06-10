#!/usr/bin/env python3
''' Create a new module called main.py. Create one function for each
of the following tasks. Use the requests module to query your web
server for the corresponding end-point. Use assert to validate the
response’s expected status code and payload (if any) for each task.
'''

import requests


EMAIL = 'guillaume@holberton.io'
PASSWD = 'b4l0u'
NEW_PASSWD = 't4rt1fl3tt3'
URL = 'http://0.0.0.0:5000'


def register_user(email: str, password: str) -> None:
    ''' test user registration '''
    url = '{}/users'.format(URL)
    cred = {'email': email, 'password': password}
    result = requests.post(url, data=cred)
    assert result.status_code == 200
    assert result.json() == {'email': email, 'message': 'user created'}
    result = requests.post(url, data=cred)
    assert result.status_code == 400
    assert result.json() == {'message': 'email already registered'}


def log_in_wrong_password(email: str, password: str) -> None:
    ''' test login attempt with wrong password  '''
    url = '{}/sessions'.format(URL)
    cred = {'email': email, 'password': password}
    result = requests.post(url, data=cred)
    assert result.status_code == 401


def log_in(email: str, password: str) -> str:
    ''' test successful login '''
    url = '{}/sessions'.format(URL)
    cred = {'email': email, 'password': password}
    result = requests.post(url, data=cred)
    assert result.status_code == 200
    assert result.json() == {'email': email, 'message': 'logged in'}
    return result.cookies.get('session_id')


def profile_unlogged() -> None:
    ''' attempt to get profile info while logged out '''
    url = '{}/profile'.format(URL)
    result = requests.get(url)
    assert result.status_code == 403


def profile_logged(session_id: str) -> None:
    ''' attempt to get profile info while logged in '''
    url = '{}/profile'.format(URL)
    cookies = {'session_id': session_id}
    result = requests.get(url, cookies=cookies)
    assert result.status_code == 200
    assert 'email' in result.json()


def log_out(session_id: str) -> None:
    ''' test logout '''
    url = '{}/sessions'.format(URL)
    cookies = {'session_id': session_id}
    result = requests.delete(url, cookies=cookies)
    assert result.status_code == 200
    assert result.json() == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    ''' test resetting password token '''
    url = '{}/reset_password'.format(URL)
    cred = {'email': email}
    result = requests.post(url, data=cred)
    assert result.status_code == 200
    assert 'email' in res.json()
    assert result.json()['email'] == email
    assert 'reset_token' in res.json()
    return result.json().get('reset_token')


def update_password(email: str, reset_token: str, new_password: str) -> None:
    ''' test updating user password '''
    url = '{}/reset_password'.format(URL)
    cred = {'email': email, 'reset_token': reset_token,
            'new_password': new_password}
    result = requests.put(url, data=cred)
    assert result.status_code == 200
    assert result.json() == {'email': email, 'message': 'Password updated'}


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
