#!/usr/bin/env python3
"""module of a a Flask app"""
from flask import Flask, jsonify, request, abort
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def main():
    """return json payloads"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def get_user():
    """implements the POST /users route"""
    email = request.form.get('email')
    password = request.form.get('password')

    if email is None or password is None:
        abort(400)

    try:
        user = AUTH.register_user(email=email, password=password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400
    else:
        return jsonify({
            "email": f"{user.email}",
            "message": "user created"
            }), 200


@app.route("/sessions", methods=[''], strict_slashes=False)
def login():
    """respond to the POST /sessions route."""
    email = request.form.get('email')
    passwd = request.form.get('password')

    if email is None or passwd is None:
        abort(401)
    isValid = AUTH.valid_login(email=email, password=password)

    if isValid is False:
        abort(401)

    session = AUTH.create_session(email=email)
    response = jsonify({'email': email, 'message': 'logged in'})
    response.set_cookie('session_id', session)
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
