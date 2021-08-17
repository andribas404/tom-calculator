from uuid import UUID
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status
from starlette.responses import RedirectResponse

from tom_calculator.containers import Container
from tom_calculator import schemas, services

router = APIRouter()


@router.get('/')
async def root():
    response = RedirectResponse(url='/docs#/default/order_create_order_post')
    return response


@router.post(
    '/order',
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.OrderItemOut,
)
@inject
async def order_create(
    item: schemas.CalculatorIn,
    order_service: services.OrderService = Depends(Provide[Container.order_service]),
):
    return await order_service.create(item.dict())


@router.get(
    '/order/{item_id}',
    response_model=schemas.OrderItemOut,
)
@inject
async def order_get(
    item_id: UUID,
    order_service: services.OrderService = Depends(Provide[Container.order_service]),
):
    return await order_service.get(item_id)
