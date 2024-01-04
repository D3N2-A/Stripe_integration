from sqlalchemy.orm import Session
from .models import Customer
from ..schemas import customer


# Function for retrieving List of All customers
def get_all_customers(db: Session):
    users = db.query(Customer).all()
    return users

# Function for retrieving Customer by email


def get_customer_email(email: str, db: Session):
    user = db.query(Customer).filter(Customer.email == email).first()
    if user:
        return user
    else:
        return None


# Function for creating customers
def create_customer(data: customer.CustomerBase, db: Session):
    check_customer = get_customer_email(data['email'], db)
    if check_customer:
        return "Found"
    else:
        # TODO: Add rollback functionality and check for kafka server
        db_customer = Customer(
            id=data['id'], name=data['name'], email=data['email'])
        db.add(db_customer)
        db.commit()
        db.refresh(db_customer)
        return db_customer


# Function for deleting customer
def delete_customer(id: str, db: Session):
    db_customer = db.query(Customer).filter(Customer.id == id).first()
    if db_customer:
        db.delete(db_customer)
        db.commit()
        return 'done'


# Function for updating customer
def update_customer(data: customer.CustomerUpdate, db: Session):
    db_customer = db.query(Customer).filter(Customer.id == data['id']).first()
    if db_customer:
        if data['name']:
            db_customer.name = data['name']
        if data['email']:
            db_customer.email = data['email']
        db.commit()
        return db_customer
    else:
        return None
