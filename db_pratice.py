from sqlalchemy.orm import  sessionmaker , declarative_base
from sqlalchemy import create_engine

db_url = "postgresql://postgres:CHANDU%40123@localhost:5432/mydb"

Base = declarative_base()

engine = create_engine(db_url)

session = sessionmaker(autocommit = False , autoflush= False , bind = engine)

