from fastapi import APIRouter, Depends, status, Body, Path
from app.IIko import get_token_iiko, IIko
from app.schemas.combo import ComboCredits, Combo, ComboCategorie, Group
from app.schemas.exception import ComboNotFoundException
from uuid import UUID
from typing import List


combo_router = APIRouter(tags=["Combo"])


@combo_router.post(
    "/combo/iiko",
    status_code=status.HTTP_200_OK,
    response_model= Combo,
    responses={status.HTTP_404_NOT_FOUND: {"detail": "Меню не найдено"}},
)
async def get_menu(
    organization: ComboCredits = Body(...),
    sesion_iiko: IIko = Depends(IIko),
):
    resp = sesion_iiko.get_combos_iiko(organization.organizationId)
    # тоже нужно править так как не сохранит все линки
    new_combo = Combo(**dict(resp))
    await new_combo.save()
    return new_combo


@combo_router.get(
    "/combocategories",
    status_code=status.HTTP_200_OK,
    response_model= List[ComboCategorie],
)
async def get_menu():
    # TODO скорее всего не рабоатет нужно править
    list_combos = ComboCategorie.all().to_list()
    return list_combos


@combo_router.get(
    "/combocategorie/{combo_id}",
    status_code=status.HTTP_200_OK,
    response_model= Group,
)
async def get_menu(
    combo_id: UUID = Path(...)
):
    group = Group.get(combo_id)
    if not group:
        raise ComboNotFoundException(error="Комбо не найдено")
    return  group