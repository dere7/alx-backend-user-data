#!/usr/bin/env python3
"""
e2e test
"""
import requests


def register_user(email: str, password: str) -> None:
    """Registers a new user"""
    res = requests.post('http://localhost:5000/users',
                        {'email': email,
                         'password': password})
    assert res.json() == {"email": email,
                          "message": "user created"}


def log_in_wrong_password(email: str, password: str) -> None:
    """Creates a new session with wron password"""
    res = requests.post('http://localhost:5000/sessions',
                        {'email': email,
                         'password': password})
    assert res.status_code == 401


def log_in(email: str, password: str) -> str:
    """Creates a new session with correct password"""
    res = requests.post('http://localhost:5000/sessions',
                        {'email': email,
                         'password': password})
    assert res.json() == {"email": email, "message": "logged in"}
    return res.cookies.get('session_id')


def profile_unlogged() -> None:
    """Requests a profile endpoint"""
    res = requests.get('http://localhost:5000/profile')
    assert res.status_code == 403


def profile_logged(session_id: str) -> None:
    """Requests a profile endpoint"""
    res = requests.get('http://localhost:5000/profile',
                       cookies={'session_id': session_id})
    assert res.status_code == 200


def log_out(session_id: str) -> None:
    """Logs out or destorys a session"""
    res = requests.delete('http://localhost:5000/sessions',
                          cookies={'session_id': session_id})
    assert res.json() == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    """resets a password with new password"""
    res = requests.post(
        'http://localhost:5000/reset_password', {'email': email})
    assert res.status_code == 200
    return res.json().get('reset_token')


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """resets a password with new password"""
    res = requests.put(
        'http://localhost:5000/reset_password',
        {'email': email,
         'reset_token': reset_token,
         'new_password': new_password})
    assert res.json() == {"email": email, "message": "Password updated"}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


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
