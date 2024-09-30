import datetime

from pydantic import BaseModel, ConfigDict


class SOrderAdd(BaseModel):
    date_of_creation: datetime.datetime = datetime.datetime.now()
    status: str


class SOrder(SOrderAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)


class SOrderId(BaseModel):
    order_id: int

    model_config = ConfigDict(from_attributes=True)
