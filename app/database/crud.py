from sqlalchemy.orm import Session
from .models import Customer
from ..schemas import customer


def get_all_customers(db: Session):
    users = db.query(Customer).all()
    return users


def create_customer(data: customer.CustomerBase, db: Session):
    db_customer = Customer(
        id=data['id'], name=data['name'], email=data['email'])
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer


def delete_customer(id: str, db: Session):
    db_customer = db.query(Customer).filter(Customer.id == id).first()
    db.delete(db_customer)
    db.commit()
