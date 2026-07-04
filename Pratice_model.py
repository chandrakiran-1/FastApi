from sqlalchemy import Column , Integer , String , Float
from db_pratice import Base

class ProductPratice(Base):

    __tablename__ = "ProductPratice"
    id = Column(Integer , primary_key = True , index = True)
    name = Column(String)
    description = Column(String)
    price = Column(Integer)
    quantity = Column(Integer)