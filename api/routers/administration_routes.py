from fastapi import APIRouter, HTTPException, Depends, Query
from starlette import status
from models import AdministrationRoute
from schemas.maladis import AdministrationRouteSchema
from sqlalchemy.orm import Session
from database import get_db
from .auth import get_current_user
from typing import Annotated
from sqlalchemy import or_
import math
from dependencies import Security

router = APIRouter()

security = Security()

user_dependency = Annotated[dict, Depends(get_current_user)]


def get_object(id, db, model):
    data = db.query(model).filter(model.id == id).first()
    if data is None:
        raise HTTPException(status_code=404, detail=f"ID {id} : Does not exist")
    return data


@router.get("/")
async def get_administration_routes(
    user: user_dependency,
    db: Session = Depends(get_db),
    skip: int = Query(default=1, ge=1),
    limit: int = 10,
    search: str = "",
):
    security.secureAccess("VIEW_ADMINISTRATION_ROUTE", user["id"], db)

    offset = (skip - 1) * limit
    query = (
        db.query(AdministrationRoute)
        .filter(
            or_(
                AdministrationRoute.administration_route.ilike(f"%{search}%"),
                AdministrationRoute.description.ilike(f"%{search}%"),
            )
        )
        .offset(offset)
        .limit(limit)
        .all()
    )
    total_count = (
        db.query(AdministrationRoute)
        .filter(
            or_(
                AdministrationRoute.administration_route.ilike(f"%{search}%"),
                AdministrationRoute.description.ilike(f"%{search}%"),
            )
        )
        .count()
    )
    pages = math.ceil(total_count / limit)
    return {"pages": pages, "data": query}


@router.post("/")
async def add_administration_route(
    administration_route_schema: AdministrationRouteSchema,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("ADD_ADMINISTRATION_ROUTE", user["id"], db)
    create_administration_route_model = AdministrationRoute(
        administration_route=administration_route_schema.administration_route,
        description=administration_route_schema.description,
    )

    db.add(create_administration_route_model)
    db.commit()
    return administration_route_schema


@router.get("/{administration_route_id}")
async def get_administration_route(
    administration_route_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("VIEW_ADMINISTRATION_ROUTE", user["id"], db)
    administration_route = get_object(administration_route_id, db, AdministrationRoute)

    return administration_route


@router.put("/{administration_route_id}")
async def update_administration_route(
    administration_route_id: int,
    user: user_dependency,
    administration_route_schema: AdministrationRouteSchema,
    db: Session = Depends(get_db),
):
    security.secureAccess("UPDATE_ADMINISTRATION_ROUTE", user["id"], db)
    administration_route_model = get_object(
        administration_route_id, db, AdministrationRoute
    )

    administration_route_model.administration_route = (
        administration_route_schema.administration_route
    )
    administration_route_model.description = administration_route_schema.description

    db.commit()
    db.refresh(administration_route_model)
    return administration_route_schema


@router.delete("/{administration_route_id}")
async def delete_administration_route(
    administration_route_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("DELETE_ADMINISTRATION_ROUTE", user["id"], db)
    get_object(administration_route_id, db, AdministrationRoute)
    db.query(AdministrationRoute).filter(
        AdministrationRoute.id == administration_route_id
    ).delete()
    db.commit()
    raise HTTPException(
        status_code=status.HTTP_200_OK,
        detail="Administration route successfully deleted",
    )
