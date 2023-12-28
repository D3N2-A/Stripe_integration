from pydantic import BaseModel


class CustomerBase(BaseModel):
    id: str
    name: str
    email: str

    class Config:
        orm_mode = True
