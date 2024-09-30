from pydantic import BaseModel, ConfigDict


class SProductAdd(BaseModel):
    name: str
    description: str
    price: int
    quantity: int


class SProduct(SProductAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)


class SProductId(BaseModel):
    product_id: int

    model_config = ConfigDict(from_attributes=True)