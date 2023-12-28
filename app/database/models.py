from .database import Base
from sqlalchemy import String, Column


class Customer(Base):
    __tablename__ = "customers"

    id = Column(String, primary_key=True, index=True)
    name = Column(String,  index=True)
    email = Column(String, unique=True, index=True)
