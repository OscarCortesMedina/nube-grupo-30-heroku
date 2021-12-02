from flask import Flask
from datetime import timedelta

UPLOAD_FOLDER = '/home/ubuntu/Proyecto-Grupo30-202120/files-handler/'

def create_app(config_name):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:ZNN9u.GcY9cJ89phCEFKpA3v@database-grupo-30.cjhkdq8p2yhe.us-east-1.rds.amazonaws.com:3306/vinilos'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY']='frase-secreta'
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    return app
