from sqlalchemy.orm import Session
from .models import Customer


def get_all_customers(db: Session):
    users = db.query(Customer).all()
    print(users)
    return users
