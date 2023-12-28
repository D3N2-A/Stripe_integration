from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .schemas import customer
from .database import database, crud


app = FastAPI()

# Dependency


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"hello": "Hello World"}


@app.get("/get_user", response_model=list[customer.CustomerBase])
def get_user(db: Session = Depends(get_db)):

    users = crud.get_all_customers(db)
    if users:
        return users
    else:
        raise HTTPException(status_code=404, detail="Not Found")


@app.post("/create_user", response_model=list[customer.CustomerBase])
def create_user(payload: customer.CustomerBase, db: Session = Depends(get_db)):

    users = crud.create_user(payload.dict(), db)
    if users:
        return users
    else:
        raise HTTPException(status_code=404, detail="Not Found")
