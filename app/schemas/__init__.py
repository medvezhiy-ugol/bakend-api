from app.schemas.terminal import TerminalResponse
from app.schemas.menu import MenuResponse, ItemModel
from app.schemas.combo import ComboCategorie, Combo,Group

__beanie_models__ = [TerminalResponse, MenuResponse, ItemModel,ComboCategorie,Combo,Group]
