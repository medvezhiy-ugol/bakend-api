from app.routers.auth import registr_router
from app.routers.chat import chat_router


list_of_routes = [
    registr_router,
    chat_router
]

__all__ = [
    "list_of_routes",
]
