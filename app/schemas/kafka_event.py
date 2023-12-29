from pydantic import BaseModel


class KafkaEventBase(BaseModel):
    action: str


class KafkaCreate(KafkaEventBase):
    id: str
    email: str
    name: str


class KafkaDelete(KafkaEventBase):
    id: str
