from . import create_app
from flask_restful import Api
from .modelos import db
from .vistas import VistaLogIn, VistaSignUp,  VistaDownloadFile,VistaTask,VistaTaskId,VistaHealth,VistaID
from flask_jwt_extended import JWTManager
from flask_cors import CORS, cross_origin


app = create_app('default')
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()
cors = CORS(app, expose_headers=["x-suggested-filename"])

api = Api(app)
api.add_resource(VistaLogIn, '/auth/login')
api.add_resource(VistaSignUp, '/auth/signup')

api.add_resource(VistaDownloadFile, '/api/files/<string:filename>/<int:typefile>')
api.add_resource(VistaTask, '/api/tasks')
api.add_resource(VistaTaskId, '/api/tasks/<int:id_tarea>')
api.add_resource(VistaHealth, '/health')
api.add_resource(VistaID, '/id')

jwt = JWTManager(app)