#!/usr/bin/env python3
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route('/')
def index():
    """GET /
    - gets json payload
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users():
    """POST /users
        - registers a user
    post body
        - email
        - password
    Returns
        - return success msg if user doesn't exists
        - return 400 if user exists
    """
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login():
    """POST /sessions
        - creates a new session for the user
    Post body
        - email
        - password
    return
        - success msg
        - 401 if login info is incorrect
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        res = jsonify({"email": email, "message": "logged in"})
        res.set_cookie('session_id', session_id)
        return res
    else:
        abort(401)


@app.route('/sessions', methods=['DELETE'])
def logout():
    """DELETE /sessions
        - logout(destory session)
    the request should contain cookie with 'session_id'
    """
    session_id = request.cookies.get('session_id')
    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            AUTH.destroy_session(user.id)
            redirect('/')
        else:
            abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
