
from flask_restful import Api
from modelos import db
from vistas.vistas import VistaLogIn, VistaSignUp,  VistaDownloadFile, VistaTask, VistaTaskId, VistaHealth, VistaID
from flask_jwt_extended import JWTManager
from flask_cors import CORS, cross_origin


from flask import Flask
from datetime import timedelta

from constants import DB_PASS, DB_URL, DB_USER, TYPE, UPLOAD_FOLDER


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


app = create_app('default')
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()
cors = CORS(app, expose_headers=["x-suggested-filename"])

api = Api(app)
api.add_resource(VistaLogIn, '/auth/login')
api.add_resource(VistaSignUp, '/auth/signup')

api.add_resource(VistaDownloadFile,
                 '/api/files/<string:filename>/<int:typefile>')
api.add_resource(VistaTask, '/api/tasks')
api.add_resource(VistaTaskId, '/api/tasks/<int:id_tarea>')
api.add_resource(VistaHealth, '/health')
api.add_resource(VistaID, '/id')

jwt = JWTManager(app)
