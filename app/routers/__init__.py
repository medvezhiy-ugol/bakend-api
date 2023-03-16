from app.routers.auth import registr_router
from app.routers.menu import menu_router
from app.routers.order import order_router
from app.routers.terminal import terminal_router
from app.routers.organizations import organization_router
from app.routers.roulette import roulette_router

list_of_routes = [
    registr_router,
    menu_router,
    terminal_router,
    order_router,
    organization_router,
    roulette_router
]

__all__ = [
    "list_of_routes",
]
