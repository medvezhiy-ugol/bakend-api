from app.schemas.order import OrderCreate
from fastapi import APIRouter, status, Body,Depends
from app.IIko import get_token_iiko, IIko



order_router = APIRouter(tags=["Orders"])


@order_router.post("/create",status_code=status.HTTP_200_OK)
async def create_new_order(Order: OrderCreate = Body(...),
                           token: str = Depends(get_token_iiko),
                           sesion_iiko: IIko = Depends(IIko)):
    response = await sesion_iiko.create_order(token,**Order)
    return response
