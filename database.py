from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine



db_url = "postgresql://postgres:CHANDU%40123@localhost:5432/mydb"

engine =  create_engine(db_url)

SessionLocal = sessionmaker(autocommit = False , autoflush = False , bind = engine)