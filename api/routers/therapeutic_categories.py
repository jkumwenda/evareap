from fastapi import APIRouter, HTTPException, Depends, Query
from starlette import status
from models import TherapeuticCategory
from schemas.maladis import TherapeuticCategorySchema
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
async def get_therapeutic_categories(
    user: user_dependency,
    db: Session = Depends(get_db),
    skip: int = Query(default=1, ge=1),
    limit: int = 10,
    search: str = "",
):
    security.secureAccess("VIEW_THERAPEUTIC_CATEGORY", user["id"], db)

    offset = (skip - 1) * limit
    query = (
        db.query(TherapeuticCategory)
        .filter(
            or_(
                TherapeuticCategory.therapeutic_category.ilike(f"%{search}%"),
                TherapeuticCategory.description.ilike(f"%{search}%"),
            )
        )
        .offset(offset)
        .limit(limit)
        .all()
    )
    total_count = (
        db.query(TherapeuticCategory)
        .filter(
            or_(
                TherapeuticCategory.therapeutic_category.ilike(f"%{search}%"),
                TherapeuticCategory.description.ilike(f"%{search}%"),
            )
        )
        .count()
    )
    pages = math.ceil(total_count / limit)
    return {"pages": pages, "data": query}


@router.post("/")
async def add_therapeutic_category(
    therapeutic_category_schema: TherapeuticCategorySchema,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("ADD_THERAPEUTIC_CATEGORY", user["id"], db)
    create_therapeutic_category_model = TherapeuticCategory(
        therapeutic_category=therapeutic_category_schema.therapeutic_category,
        description=therapeutic_category_schema.description,
    )

    db.add(create_therapeutic_category_model)
    db.commit()
    return therapeutic_category_schema


@router.get("/{therapeutic_category_id}")
async def get_therapeutic_category(
    therapeutic_category_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("VIEW_THERAPEUTIC_CATEGORY", user["id"], db)
    therapeutic_category = get_object(therapeutic_category_id, db, TherapeuticCategory)

    return therapeutic_category


@router.put("/{therapeutic_category_id}")
async def update_therapeutic_category(
    therapeutic_category_id: int,
    user: user_dependency,
    therapeutic_category_schema: TherapeuticCategorySchema,
    db: Session = Depends(get_db),
):
    security.secureAccess("UPDATE_THERAPEUTIC_CATEGORY", user["id"], db)
    therapeutic_category_model = get_object(
        therapeutic_category_id, db, TherapeuticCategory
    )

    therapeutic_category_model.therapeutic_category = (
        therapeutic_category_schema.therapeutic_category
    )
    therapeutic_category_model.description = therapeutic_category_schema.description

    db.commit()
    db.refresh(therapeutic_category_model)
    return therapeutic_category_schema


@router.delete("/{therapeutic_category_id}")
async def delete_therapeutic_category(
    therapeutic_category_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("DELETE_THERAPEUTIC_CATEGORY", user["id"], db)
    get_object(therapeutic_category_id, db, TherapeuticCategory)
    db.query(TherapeuticCategory).filter(
        TherapeuticCategory.id == therapeutic_category_id
    ).delete()
    db.commit()
    raise HTTPException(
        status_code=status.HTTP_200_OK,
        detail="Therapeutic category successfully deleted",
    )
