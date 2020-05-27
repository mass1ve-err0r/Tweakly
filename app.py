from os import path, environ as env
from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = path.join(app.root_path, "")
app.config['JWT_SECRET_KEY'] = env.get('JWT_SECRET')
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']

JWTManager = JWTManager(app)

from Endpoints.Authorization import *
from Endpoints.LookupAPI import *


if __name__ == '__main__':
    app.run(debug=True)
