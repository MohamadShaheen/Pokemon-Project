import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()

username = os.getenv('DATABASE_USERNAME')
password = os.getenv('DATABASE_PASSWORD')
local_host = os.getenv('DATABASE_HOST')
port = os.getenv('DATABASE_PORT')
database_name = os.getenv('DATABASE_NAME')
docker_host = os.getenv('DATABASE_DOCKER_HOST')


# local:
# database_URL = f'mysql+pymysql://{username}:{password}@{local_host}:{port}/{database_name}'

# for docker: mymysql container as host
database_URL = f'mysql+pymysql://{username}:@{docker_host}:{port}/{database_name}'

engine = create_engine(database_URL)

session_local = sessionmaker(bind=engine)

Base = declarative_base()