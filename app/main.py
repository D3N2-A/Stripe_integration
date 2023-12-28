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


@app.get("/get_user", response_model=list[customer.CustomerBase])
def get_customers(db: Session = Depends(get_db)):

    users = crud.get_all_customers(db)
    if users:
        return users
    else:
        raise HTTPException(status_code=404, detail="Not Found")


# Endpoint for Creating customer


@app.post("/create_user")
def create_customer(payload: customer.CustomerBase,
                    db: Session = Depends(get_db)):
    user = crud.create_user(payload.dict(), db)
    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail="Something went Bad")


# Endpoint for Deleting customer


@app.delete("/delete_user", status_code=200)
def delete_customer(payload: customer.DeleteCustomer,
                    db: Session = Depends(get_db)):
    id = payload.dict()['id']
    crud.delete_customer(id, db)
    return Response(status_code=200)
