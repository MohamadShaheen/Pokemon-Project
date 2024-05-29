import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()

username = os.getenv('DATABASE_USERNAME')
password = os.getenv('DATABASE_PASSWORD')
host = os.getenv('DATABASE_HOST')
port = os.getenv('DATABASE_PORT')
database_name = os.getenv('DATABASE_NAME')


database_URL = f'mysql+pymysql://{username}:{password}@{host}:{port}/{database_name}'

engine = create_engine(database_URL)

session_local = sessionmaker(bind=engine)

Base = declarative_base()