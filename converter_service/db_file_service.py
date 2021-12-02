from modelos.modelos import Task, User
from . import Base, Session, engine
import datetime


def search_files_to_convert():
    Base.metadata.create_all(engine)
    tasks = []
    session = Session()
    tasks = session.query(Task).filter_by(
        status="uploaded").all()
    session.expunge_all()
    session.close()

    return tasks


def search_file_to_convert(taskId):
    Base.metadata.create_all(engine)
    session = Session()
    task = session.query(Task).get(taskId)
    session.expunge_all()
    session.close()

    return task


def get_user_from_id(iduser):
    user = ''
    Base.metadata.create_all(engine)
    session = Session()
    user = session.query(User).get(iduser)
    session.expunge_all()
    session.close()

    return user


def change_task_to_processed(idtask):
    Base.metadata.create_all(engine)
    session = Session()
    task = session.query(Task).get(idtask)
    task.status = 'processed'
    task.processeddate = datetime.datetime.now()
    session.commit()
    session.close()
