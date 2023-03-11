from fastapi import APIRouter, Depends, status, Body
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClientSession
from app.db.connection import get_mongo_session
from app.IIko import get_token_iiko, IIko
from app.query.terminal import create_terminal
from app.db.connection import get_mongo_session
from app.schemas.terminal import TerminalModel


terminal_router = APIRouter(tags=["Terminal"])


@terminal_router.post("/terminal",
    status_code=status.HTTP_200_OK)
async def get_all_terminals(term: TerminalModel = Body(...),
                            token: str = Depends(get_token_iiko)):
    pass


@terminal_router.post("/terminalIIko",
                  status_code=status.HTTP_200_OK)
async def get_iiko_term(term: TerminalModel = Body(...),
                        token: str = Depends(get_token_iiko),
                        session_mdb:AsyncIOMotorClientSession = Depends(get_mongo_session),
                        sesion_iiko: IIko = Depends(IIko)):
    terminals = await sesion_iiko.take_terminal(token,term)
    await create_terminal(terminals,session_mdb)
    return terminals

