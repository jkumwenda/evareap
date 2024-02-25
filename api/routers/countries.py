from fastapi import APIRouter, HTTPException, Depends, Query
from models import Country
from sqlalchemy.orm import Session
from database import get_db
from .auth import get_current_user
from typing import Annotated
from sqlalchemy import or_
import math

router = APIRouter()

user_dependency = Annotated[dict, Depends(get_current_user)]


def get_object(id, db, model):
    data = db.query(model).filter(model.id == id).first()
    if data is None:
        raise HTTPException(status_code=404, detail=f"ID {id} : Does not exist")
    return data


@router.get("/")
async def get_countries(
    user: user_dependency,
    db: Session = Depends(get_db),
    skip: int = Query(default=1, ge=1),
    limit: int = 10,
    search: str = "",
):
    # security.secureAccess("READ_BRANCH", user_id, db)

    offset = (skip - 1) * limit
    query = (
        db.query(Country)
        .filter(
            or_(
                Country.country.ilike(f"%{search}%"),
                Country.short_code.ilike(f"%{search}%"),
            )
        )
        .offset(offset)
        .limit(limit)
        .all()
    )
    total_count = (
        db.query(Country)
        .filter(
            or_(
                Country.country.ilike(f"%{search}%"),
                Country.short_code.ilike(f"%{search}%"),
            )
        )
        .count()
    )
    pages = math.ceil(total_count / limit)
    return {"pages": pages, "data": query}
