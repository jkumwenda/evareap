from fastapi import APIRouter, HTTPException, Depends, Query
from starlette import status
from models import GenericName
from schemas.maladis import GenericNameSchema
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
async def get_generic_names(
    user: user_dependency,
    db: Session = Depends(get_db),
    skip: int = Query(default=1, ge=1),
    limit: int = 10,
    search: str = "",
):
    security.secureAccess("VIEW_GENERIC_NAME", user["id"], db)

    offset = (skip - 1) * limit
    query = (
        db.query(GenericName)
        .filter(
            or_(
                GenericName.generic_name.ilike(f"%{search}%"),
                GenericName.description.ilike(f"%{search}%"),
            )
        )
        .offset(offset)
        .limit(limit)
        .all()
    )
    total_count = (
        db.query(GenericName)
        .filter(
            or_(
                GenericName.generic_name.ilike(f"%{search}%"),
                GenericName.description.ilike(f"%{search}%"),
            )
        )
        .count()
    )
    pages = math.ceil(total_count / limit)
    return {"pages": pages, "data": query}


@router.post("/")
async def add_generic_name(
    generic_name_schema: GenericNameSchema,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("ADD_GENERIC_NAME", user["id"], db)
    create_generic_name_model = GenericName(
        generic_name=generic_name_schema.generic_name,
        description=generic_name_schema.description,
    )

    db.add(create_generic_name_model)
    db.commit()
    return generic_name_schema


@router.get("/{generic_name_id}")
async def get_generic_name(
    generic_name_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("VIEW_GENERIC_NAME", user["id"], db)
    generic_name = get_object(generic_name_id, db, GenericName)

    return generic_name


@router.put("/{generic_name_id}")
async def update_generic_name(
    generic_name_id: int,
    user: user_dependency,
    generic_name_schema: GenericNameSchema,
    db: Session = Depends(get_db),
):
    security.secureAccess("UPDATE_GENERIC_NAME", user["id"], db)
    generic_name_model = get_object(generic_name_id, db, GenericName)

    generic_name_model.generic_name = generic_name_schema.generic_name
    generic_name_model.description = generic_name_schema.description

    db.commit()
    db.refresh(generic_name_model)
    return generic_name_schema


@router.delete("/{generic_name_id}")
async def delete_generic_name(
    generic_name_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("DELETE_GENERIC_NAME", user["id"], db)
    get_object(generic_name_id, db, GenericName)
    db.query(GenericName).filter(GenericName.id == generic_name_id).delete()
    db.commit()
    raise HTTPException(
        status_code=status.HTTP_200_OK,
        detail="Generic name successfully deleted",
    )
