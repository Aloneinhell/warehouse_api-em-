from typing import Optional

from fastapi import HTTPException
from sqlalchemy import select, update, insert
from sqlalchemy.exc import NoResultFound

from database import new_session, OrderOrm, OrderItemOrm, ProductOrm
from schemas.schemas_order import SOrderAdd, SOrder
from schemas.schemas_orderitem import SOrderItemAdd
from schemas.schemas_product import SProduct, SProductId


class OrderRepository:
    @classmethod
    async def add_one(cls, data: SOrderAdd,
                      product_id: SProductId, od_data: SOrderItemAdd
                      ) -> int:
        async with new_session() as session:
            order_dict = data.model_dump()
            order = OrderOrm(**order_dict)
            session.add(order)
            product_query = select(ProductOrm).filter(ProductOrm.id == product_id.product_id)
            product_result = await session.execute(product_query)
            try:
                product_data = product_result.scalars().one()
            except NoResultFound:
                raise HTTPException(status_code=404, detail=f"Товара с id {product_id.product_id} не существует!")
            product_data_obj = SProduct.model_validate(product_data)
            if od_data.quantity_of_product > product_data_obj.quantity:
                raise HTTPException(status_code=406, detail=f"Недостаточное кол-во вещей")
            else:
                oi_cr_stmnt = (
                    insert(OrderItemOrm).
                    values(id=order.id, order_id=order.id, product_id=product_id.product_id,
                           quantity_of_product=od_data.quantity_of_product)
            )
                new_quantity = product_data_obj.quantity - od_data.quantity_of_product

                product_update_stmnt = (
                    update(ProductOrm).
                    where(ProductOrm.id == product_id.product_id).
                    values(quantity=new_quantity)
                )
            await session.execute(oi_cr_stmnt)
            await session.execute(product_update_stmnt)

            await session.flush()
            await session.commit()
            return order.id

    @classmethod
    async def get_all(cls) -> list[SOrder]:
        async with new_session() as session:
            query = select(OrderOrm)
            result = await session.execute(query)
            order_models = result.scalars().all()
            order_schemas = [SOrder.model_validate(order_model) for order_model in order_models]

            return order_schemas

    @classmethod
    async def get_one(cls, o_id) -> Optional[SOrder] or str:
        async with new_session() as session:
            try:
                query = select(OrderOrm).filter(OrderOrm.id == o_id)
                result = await session.execute(query)
                order_model = result.scalars().one()
                order_schema = SOrder.model_validate(order_model)

                return order_schema
            except NoResultFound:
                raise HTTPException(status_code=404, detail=f"Нет заказа с id {o_id}")

    @classmethod
    async def patch_one(
            cls, o_id, status) -> SOrder:
        async with new_session() as session:
            try:
                query = select(OrderOrm).filter(OrderOrm.id == o_id)
                result = await session.execute(query)
                order_model = result.scalars().one()

                stmnt = (
                    update(OrderOrm).
                    where(OrderOrm.id == o_id).
                    values(
                        status=status
                    )

                )
                await session.execute(stmnt)
                await session.commit()
                order_schema = SOrder.model_validate(order_model)
                return order_schema
            except NoResultFound:
                raise HTTPException(status_code=404, detail=f"Нет заказа с id {o_id}")
