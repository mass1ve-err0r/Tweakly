from os import environ as env
from flask import jsonify, request
from wsgi import jwt, app
from flask_jwt_extended import create_access_token, jwt_required

'''
# This route is temporarily disabled because we'll use a token which is indefinitely valid
@app.route('/v1/tweakly/xauth/getTokenOnce', subdomain="api")
def cToken():
    ident_ = env.get('API_IDENTIFIER')
    access_token = create_access_token(identity=ident_, expires_delta=False)
    return jsonify(access_token=access_token)
'''


@app.route('/v1/tweakly/protTest', subdomain="api")
@jwt_required
def test_route():
    return "OK protected!"

