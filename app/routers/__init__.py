from app.routers.auth import registr_router
from app.routers.menu import menu_router


list_of_routes = [
    registr_router,
    menu_router
]

__all__ = [
    "list_of_routes",
]
