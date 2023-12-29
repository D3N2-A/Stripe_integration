from fastapi import FastAPI, Depends, HTTPException, Response, Request
from sqlalchemy.orm import Session
from .schemas import customer
from .database import database, crud
from .queue import kafka_producer
from .utils import serialization
import json

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
    if customer == "Found":
        raise HTTPException(status_code=404, detail="Customer ALready Exists")
    if customer:
        kafka_producer.publish('stripe', serialization.
                               json.dumps({
                                   "id": customer.id, "email": customer.email,
                                   "name": customer.name,
                                   "action": "customer.created"}))
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
        kafka_producer.publish('stripe', json.dumps({'id': str(id),
                                                     'action':
                                                     "customer.deleted"}))
        return Response(status_code=200)
    else:
        raise HTTPException(
            status_code=404, detail="Customer with id not found")

# Endpoint for Updating customer


@app.put("/customer", status_code=200)
def update_customer(payload: customer.CustomerUpdate,
                    db: Session = Depends(get_db)):
    data = payload.dict()
    updated_customer = crud.update_customer(data, db)
    if updated_customer:
        kafka_producer.publish('stripe', serialization.
                               json.dumps({
                                   "id": data['id'], "email": data['email'],
                                   "name": data['name'],
                                   "action": "customer.updated"}))
        return updated_customer.__dict__
    else:
        raise HTTPException(status_code=404, detail="Not Found")


# Webhook for recieving Stripe events

@app.post("/webhooks/stripe")
async def webhook(request: Request, db: Session = Depends(get_db)):
    event = None
    event = await request.json()
    data = event['data']

    if event['type'] == 'customer.created':
        customer_data = customer.CustomerBase(**data['object']).dict()
        db_customer = crud.create_customer(customer_data, db)
        if db_customer == "Found":
            raise HTTPException(
                status_code=404, detail="Customer ALready Exists")
        else:
            print('Customer created with')
    elif event['type'] == 'customer.deleted':
        customer_data = customer.CustomerBase(**data['object'])
    elif event['type'] == 'customer.updated':
        customer_data = customer.CustomerBase(**data['object'])

    else:
        print('Unhandled event type {}'.format(event['type']))
    print(customer_data)
    return {"True"}
