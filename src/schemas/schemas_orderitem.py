from pydantic import BaseModel, ConfigDict


class SOrderItemAdd(BaseModel):
    product_id: int
    quantity_of_product: int


class SOrderItem(SOrderItemAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)


class SOrderItemId(BaseModel):
    id: int

    model_config = ConfigDict(from_attributes=True)
