from database import Base
from sqlalchemy import Integer, String, Column


class User(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String,  index=True)
    email = Column(String, unique=True, index=True)
