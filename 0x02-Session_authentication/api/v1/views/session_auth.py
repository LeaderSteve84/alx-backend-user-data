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
    if (email is None or len(email)) == 0:
        return jsonify({"error": "email missing"}), 400

    # get password from form
    pwd = request.form.get('password')
    if pwd is None or len(pwd) == 0:
        return jsonify({"error": "password missing"}), 400
    
    # search for user by email
    users = User.search({"email": email})
    if len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    
    for user in users:
        if user.is_valid_password(pwd):
            response = make_response(user.to_json())
            SESSION_NAME = os.getenv('SESSION_NAME')
            response.set_cookie(SESSION_NAME, auth.create_session(user.id))
            return response
    return jsonify({"error": "wrong password"}), 401
