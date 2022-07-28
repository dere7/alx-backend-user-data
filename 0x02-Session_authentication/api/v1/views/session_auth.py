#!/usr/bin/env python3
"""handles all routes for the session auth"""
from flask import request, abort, jsonify, make_response
from . import app_views
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """POST /api/v1/auth_session/login
    JSON body:
        - email
        - password
    Return:
        - 400 if one of email or password is missing or empty
        - User
        - 401 if email not found or incorrect password
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400

    users = User.search({'email': email})
    if not users:
        return jsonify({"error": "no user found for this email"}), 404

    users = list(
        filter(lambda user: user.is_valid_password(password), users))
    if not users:
        return jsonify({"error": "wrong password"}), 401

    user = users[0]
    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    resp = jsonify(user.to_json())
    resp.set_cookie('SESSION_NAME', session_id)
    return resp


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def logout():
    """destorys session for user/logout"""
    from api.v1.app import auth
    destoryed = auth.destroy_session(request)
    if not destoryed:
        abort(404)
    else:
        return jsonify({})
