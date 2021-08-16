from fastapi import APIRouter, Depends, Response, status
from dependency_injector.wiring import inject, Provide

from tom_calculator.containers import Container
from tom_calculator.services import OrderService

router = APIRouter()


@router.get('/')
async def root():
    return {'message': 'Hello World'}


@router.post('/order', status_code=status.HTTP_201_CREATED)
@inject
def post_order(
    order_service: OrderService = Depends(Provide[Container.order_service]),
):
    return order_service.create_order()
