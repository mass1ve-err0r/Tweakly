from os import path, environ as env
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from app import create_app

app = create_app()
app.config['UPLOAD_FOLDER'] = path.join(app.root_path, "")
app.config['SERVER_NAME'] = env.get('SERVER_NAME')
app.config['JWT_SECRET_KEY'] = env.get('JWT_SECRET')

jwt = JWTManager(app)
lim = Limiter(app, key_func=get_remote_address)

from Endpoints.Authorization import *
from Endpoints.LookupAPI import *


if __name__ == "__main__":
    app.run(port=2000)
