import os
from dotenv import load_dotenv
load_dotenv()

from Database.MongoDBHandlers import TokenDBHandler
# MongoTokens = TokenDBHandler()

from flask import Flask
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, "")


@app.route('/')
def index():
    return 'Hello World !'


if __name__ == '__main__':
    app.run(debug=True)
