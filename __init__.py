from flask import Flask
from datetime import timedelta

from .constants import DB_PASS, DB_URL, DB_USER, TYPE, UPLOAD_FOLDER


def create_app(config_name):
    app = Flask(__name__)
    if __name__ == "__main__":
        app.run(host='0.0.0.0', port=80)
    print(TYPE + '://'+DB_USER+':'+DB_PASS+'@'+DB_URL)
    app.config['SQLALCHEMY_DATABASE_URI'] = TYPE + \
        '://'+DB_USER+':'+DB_PASS+'@'+DB_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'frase-secreta'
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    return app
