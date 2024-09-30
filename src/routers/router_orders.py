from typing import Annotated

from fastapi import APIRouter, Depends

from repository.repository_order import OrderRepository
from schemas.schemas_order import SOrderAdd, SOrder, SOrderId
from schemas.schemas_orderitem import SOrderItemAdd, SOrderItem
from schemas.schemas_product import SProductId

router = APIRouter(
    prefix="/orders",
    tags=["Заказы"]
)

@router.post('')
async def add_order(
        order: Annotated[SOrderAdd, Depends()],
        product_id_data: Annotated[SProductId, Depends()],
        od_data: Annotated[SOrderItemAdd, Depends()]
) -> SOrderId:
    order_id = await OrderRepository.add_one(data=order,
                                             product_id=product_id_data,
                                             od_data=od_data)
    return {"ok": True, "order_id": order_id}


@router.get('/{order_id}')
async def get_order_detail(
        order_id: Annotated[SOrderId, Depends()]
) -> SOrder or str:
    order = await OrderRepository.get_one(order_id.order_id)
    return order


@router.get('')
async def get_orders() -> list[SOrder]:
    orders = await OrderRepository.get_all()
    return orders


@router.patch('/{order_id}/status')
async def patch_order_detail(
        order: Annotated[SOrder, Depends()]
) -> SOrder:
    updated_order = await OrderRepository.patch_one(
        o_id=order.id,
        status=order.status
    )
    return updated_order
