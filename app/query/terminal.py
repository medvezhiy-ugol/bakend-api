from motor.motor_asyncio import AsyncIOMotorClient
from typing import Dict, List
from app.schemas.organizations import Organization


async def create_terminal(documents: List[Organization], client: AsyncIOMotorClient) -> None:
    terms = documents["terminalGroups"]["items"]
    for term in terms:
        term["_id"] = term.pop("id")
    terminal = client.medvejie_ustie.terminal
    await terminal.insert_many(terms)
    terminalsleep = client.medvejie_ustie.terminalsleep
    termsleep = documents["terminalGroupsInSleep"]["items"]
    for term in termsleep:
        term["_id"] = term.pop("id")
    await terminalsleep.insert_many(termsleep)