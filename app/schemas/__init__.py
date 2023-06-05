from app.schemas.terminal import TerminalResponse
from app.schemas.menu import MenuResponse, ItemModel,ItemCategorie
from app.schemas.combo import ComboCategorie, Combo,Group
from app.schemas.organizations import Organization
from app.schemas.order import OrderResponse

__beanie_models__ = [TerminalResponse, MenuResponse, ItemModel,ComboCategorie,Combo,Group,Organization,ItemCategorie, OrderResponse]
