
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from ..constants import DB_PASS, DB_URL, DB_USER, TYPE


engine = create_engine(
    TYPE+'://'+DB_USER+':'+DB_PASS+'@'+DB_URL)
Session = sessionmaker(bind=engine)

Base = declarative_base()
session = Session()
