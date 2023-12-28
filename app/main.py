from fastapi import FastAPI, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from .schemas import customer
from .database import database, crud


app = FastAPI()

# Database dependency


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"hello": "Hello World"}

# Endpoint for Retrieving List of All customers


@app.get("/customers", response_model=list[customer.CustomerBase])
def get_customers(db: Session = Depends(get_db)):

    users = crud.get_all_customers(db)
    if users:
        return users
    else:
        raise HTTPException(status_code=404, detail="Not Found")


# Endpoint for Creating customer


@app.post("/customer", status_code=201)
def create_customer(payload: customer.CustomerBase,
                    db: Session = Depends(get_db)):
    customer = crud.create_customer(payload.dict(), db)
    if customer:
        return customer
    else:
        raise HTTPException(status_code=404, detail="Invalid Format")


# Endpoint for Deleting customer


@app.delete("/customer", status_code=200)
def delete_customer(payload: customer.DeleteCustomer,
                    db: Session = Depends(get_db)):
    id = payload.dict()['id']
    task = crud.delete_customer(id, db)
    if task == 'done':
        return Response(status_code=200)
    else:
        raise HTTPException(
            status_code=404, detail="Customer with id not found")

# Endpoint for Updating customer


@app.put("/customer", status_code=200)
def update_customer(payload: customer.CustomerUpdate,
                    db: Session = Depends(get_db)):
    updated_customer = crud.update_customer(payload.dict(), db)
    if updated_customer:
        return updated_customer.__dict__
    else:
        raise HTTPException(status_code=404, detail="Not Found")


# Webhook for recieving Stripe events

# @app.webhooks.post("/")
