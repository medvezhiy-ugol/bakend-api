from fastapi import APIRouter, Depends, status, Body
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClientSession
from app.db.connection import get_mongo_session
from app.IIko import get_token_iiko, IIko
from app.query.organizations import  create_organizations
from app.db.connection import get_mongo_session
from app.schemas.organizations import Organization


organization_router = APIRouter(tags=["Организации"])


@organization_router.get("/organization", status_code=status.HTTP_200_OK)
async def get_organizations_mongo(
    session_mongo: AsyncIOMotorClientSession = Depends(get_mongo_session),
):
    res = await Organization.all().to_list()
    return res


@organization_router.post("/organizations", status_code=status.HTTP_200_OK)
async def get_organizations(
    token: str = Depends(get_token_iiko),
    session_mongo: AsyncIOMotorClientSession = Depends(get_mongo_session),
    sesion_iiko: IIko = Depends(IIko),
):
    resp = await sesion_iiko.get_organiztions(token)
    create_organizations(resp, session_mongo)
    return  await Organization.all().to_list()
