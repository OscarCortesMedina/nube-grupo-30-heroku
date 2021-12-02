from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
import datetime

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(100))
    email = db.Column(db.String(50))
    tasks = db.relationship('Task', cascade='all, delete, delete-orphan')


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100))
    oldformat = db.Column(db.String(30))
    newformat = db.Column(db.String(30))
    createdate = db.Column(db.DateTime, default=datetime.datetime.now)
    processeddate = db.Column(db.DateTime)
    status = db.Column(db.String(50))
    filecode = db.Column(db.String(100))
    iduser = db.Column(db.Integer, db.ForeignKey("user.id"))


class EnumADiccionario(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return {"llave": value.name, "valor": value.value}


class UsuarioSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_relationships = True
        load_instance = True


class TaskSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Task
        include_relationships = True
        load_instance = True
