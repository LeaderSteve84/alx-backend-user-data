#!/usr/bin/env python3
"""handles all routes for the Session authentication.
"""
from flask import request, jsonify, abort, make_response
from api.v1.views import app_views
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def auth_login():
    """for Auth login
    """
    from api.v1.app import auth
    # get email from form
    email = request.form.get('email', None)
    if not email:
        return jsonify({"error": "email missing"}), 400

    # get password from form
    pwd = request.form.get('password')
    if not pwd:
        return jsonify({"error": "password missing"}), 400

    # search for user by email
    users = User.search({"email": email})
    if not users:
        return jsonify({"error": "no user found for this email"}), 404

    user = users[0]
    if user.is_valid_password(pwd):
        return jsonify({"error": "wrong password"}), 401

    # create session ID and set it in cookie
    session_id = auth.create_session(user.id)
    response = make_response(user.to_json())
    session_name = os.getenv('SESSION_NAME', '_my_session_id')
    response.set_cookie(session_name, session_id)

    return response
