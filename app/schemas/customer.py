from pydantic import BaseModel


class CustomerBase(BaseModel):
    id: str
    name: str
    email: str

    class Config:
        orm_mode = True


class DeleteCustomer(BaseModel):
    id: str


class CustomerUpdate(BaseModel):
    id: str
    name: str | None = None
    email: str | None = None
