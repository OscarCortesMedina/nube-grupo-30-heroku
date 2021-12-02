
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    'mysql+pymysql://admin:ZNN9u.GcY9cJ89phCEFKpA3v@database-grupo-30.cjhkdq8p2yhe.us-east-1.rds.amazonaws.com:3306/vinilos')
Session = sessionmaker(bind=engine)

Base = declarative_base()
session = Session()
