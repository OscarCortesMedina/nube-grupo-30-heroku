
from flask import request, send_file

from constants.constants import UPLOAD_FOLDER

from ..sqs_service import sendMessageToQueue
from ..s3_service import downloadFile, uploadFile, deleteFile
from ..modelos import db, User, UsuarioSchema, Task, TaskSchema
from flask_restful import Resource
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from werkzeug.utils import secure_filename
import sys
import os
import time
import uuid

usuario_schema = UsuarioSchema()
task_schema = TaskSchema()

UUID = str(uuid.uuid4())
ALLOWED_EXTENSIONS = {'mp3', 'aac', 'ogg', 'wav', 'wma'}


class VistaLogIn(Resource):

    def post(self):
        try:
            usuario = User.query.filter(
                User.email == request.json["email"], User.password == request.json["password"]).first()
            db.session.commit()
            if usuario is None:
                return "El usuario no existe", 404
            else:
                token_de_acceso = create_access_token(identity=usuario.id)
                return {"mensaje": "Inicio de sesión exitoso", "token": token_de_acceso}
        except Exception:
            e = sys.exc_info()[1]
            print(e.args[0])
            return {"mensaje": "Error", "error": e.args[0]}, 404


class VistaSignUp(Resource):

    def post(self):
        try:
            pass1 = request.json["password1"]
            pass2 = request.json["password2"]
            if (pass1 != pass2):
                error = "Las contraseñas no coinciden"
                return {"mensaje": "Error", "error": error}, 400

            nuevo_usuario = User(
                username=request.json["username"], password=request.json["password1"], email=request.json["email"])
            db.session.add(nuevo_usuario)
            db.session.commit()
            return {"mensaje": "usuario creado exitosamente"}

        except Exception:
            e = sys.exc_info()[1]
            print(e.args[0])
            return {"mensaje": "Error", "error": e.args[0]}, 404


class VistaDownloadFile(Resource):

    @jwt_required()
    def get(self, filename, typefile):
        iduser = get_jwt_identity()
        # 1 para original y 2 para el archivo convertido
        task = Task.query.filter(
            Task.iduser == iduser, Task.filename == filename, ) .first()
        db.session.commit()
        if task is None:
            return "La tarea no existe", 404

        if(typefile == 1):
            filecode = task.filecode
            extension = task.oldformat
        else:
            if task.status != 'processed':
                return "La tarea aún no se ha procesado", 404
            filecode = "new-" + \
                task.filecode.rsplit('.', 1)[0].lower()+"."+task.newformat
            extension = task.newformat

        filename = filename+"."+extension

        # condicional mimetype
        switcher = {
            "mp3": "audio/mpeg",
            'aac': "audio/aac",
            'ogg': "audio/ogg",
            'wav': "audio/wav",
            'wma': "audio/x-ms-wma"
        }
        mime = switcher.get(extension, "Invalid month")
        os.system('sudo rm '+UPLOAD_FOLDER+'*')
        downloadFile(filecode)
        result = send_file(UPLOAD_FOLDER+filecode,  # nombre real del archivo
                           mimetype=mime,  # use appropriate type based on file
                           as_attachment=True,
                           conditional=False)
        # nombre a mostrar del archivo
        result.headers["x-suggested-filename"] = filename
        return result


class VistaTaskId(Resource):
    @jwt_required()
    def get(self, id_tarea):
        return task_schema.dump(Task.query.get_or_404(id_tarea))

    @jwt_required()
    def put(self, id_tarea):
        try:
            iduser = get_jwt_identity()
            task = Task.query.filter(
                Task.id == id_tarea, Task.iduser == iduser).first()
            db.session.commit()

            if task is None:
                return {"mensaje": "Error", "error": "no se encuentra la tarea"}, 404
            if task.status == 'uploaded':
                task.newformat = request.json["newFormat"]
                db.session.commit()
                sendMessageToQueue(id_tarea)
                return {"mensaje": "tarea actualizada"}
            if task.status == 'processed':
                deleteFile(task.newformat)
                task.newformat = request.json["newFormat"]
                task.status = 'uploaded'
                db.session.commit()
                sendMessageToQueue(id_tarea)
                return {"mensaje": "tarea actualizada"}
        except Exception:
            e = sys.exc_info()[1]
            print(e.args[0])
            return {"mensaje": "Error", "error": e.args[0]}, 404

    @jwt_required()
    def delete(self, id_tarea):
        try:
            iduser = get_jwt_identity()
            task = Task.query.filter(
                Task.id == id_tarea, Task.iduser == iduser).first()
            if task is None:
                return {"mensaje": "Error", "error": "no se encuentra la tarea"}, 404
            # borrar archivo original
            deleteFile(task.filecode)
            if task.status == 'processed':
                # borrar archivo anterior
                deleteFile(task.newformat)
            db.session.delete(task)
            db.session.commit()
            return {"mensaje": "tarea borrada con exito"}, 204
        except Exception:
            e = sys.exc_info()[1]
            print(e.args[0])
            return {"mensaje": "Error", "error": e.args[0]}, 404


class VistaTask(Resource):
    @jwt_required()
    def get(self):
        iduser = get_jwt_identity()
        usuario = User.query.get_or_404(iduser)
        # print(usuario)
        # print(usuario.tasks)
        return {"mensaje": "successes", "tasks": [task_schema.dump(al) for al in usuario.tasks]}, 202

    @jwt_required()
    def post(self):
        iduser = get_jwt_identity()
        if 'file' not in request.files:
            return {"mensaje": "Error", "error": "no se detecta archivo"}, 400

        file = request.files['file']
        newformat = request.form['newformat']

        if file.filename == '':
            return {"mensaje": "Error", "error": "no se detecta archivo"}, 400

        if file and ('.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS):
            filename = secure_filename(file.filename)
            now = time.strftime("%Y%m%d-%H%M%S")
            #print("hora", "iduser" + now)
            extension = filename.rsplit('.', 1)[1].lower()

            filecode = str(iduser)+"-" + now+"." + \
                filename.rsplit('.', 1)[1].lower()
            uploadFile(filecode, file)
            filename = filename.rsplit('.', 1)[0].lower()
            # hacer logica de base de datos insert
            nueva_tarea = Task(
                filename=filename,
                oldformat=extension,
                newformat=newformat,
                status='uploaded',
                filecode=filecode,
                iduser=iduser)
            db.session.add(nueva_tarea)
            db.session.commit()
            sendMessageToQueue(nueva_tarea.id)
            return {"mensaje": "archivo cargado con exito"}
        else:
            return {"mensaje": "Error", "error": "extensión no válida"}, 400


class VistaHealth(Resource):
    def get(self):
        return {}, 200


class VistaID(Resource):
    def get(self):
        return {"idMaquina": UUID}, 200

    def delete(self):
        tasks = Task.query.all()
        for task in tasks:
            db.session.delete(task)
        db.session.commit()
        return "All task removed", 200
