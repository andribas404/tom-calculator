"""API endpoints."""
import logging
from typing import Any
import uuid

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, Response, status
from starlette.responses import RedirectResponse

from tom_calculator import schemas, services
from tom_calculator.containers import Container

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get('/')
async def root() -> Any:
    """Root endpoint.

    Redirects to openapi.
    """
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
) -> Any:
    """Endpoint for creating orders from calculator input.

    Returns created order.
    """
    try:
        return await order_service.create(item)
    except services.TaxNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Tax for state {item.state_name} not exist.'
        )


@router.get(
    '/order/{item_id}',
    response_model=schemas.OrderItemOut,
)
@inject
async def order_get(
    item_id: uuid.UUID,
    order_service: services.OrderService = Depends(Provide[Container.order_service]),
) -> Any:
    """Endpoint for retrieving order by id."""
    try:
        return await order_service.get(item_id)
    except services.OrderNotFoundError:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
