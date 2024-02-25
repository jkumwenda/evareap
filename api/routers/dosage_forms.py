from fastapi import APIRouter, HTTPException, Depends, Query
from starlette import status
from models import DosageForm
from schemas.maladis import DosageFormSchema
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
async def get_dosage_forms(
    user: user_dependency,
    db: Session = Depends(get_db),
    skip: int = Query(default=1, ge=1),
    limit: int = 10,
    search: str = "",
):
    security.secureAccess("VIEW_DOSAGE_FORM", user["id"], db)

    offset = (skip - 1) * limit
    query = (
        db.query(DosageForm)
        .filter(
            or_(
                DosageForm.dosage_form.ilike(f"%{search}%"),
                DosageForm.description.ilike(f"%{search}%"),
            )
        )
        .offset(offset)
        .limit(limit)
        .all()
    )
    total_count = (
        db.query(DosageForm)
        .filter(
            or_(
                DosageForm.dosage_form.ilike(f"%{search}%"),
                DosageForm.description.ilike(f"%{search}%"),
            )
        )
        .count()
    )
    pages = math.ceil(total_count / limit)
    return {"pages": pages, "data": query}


@router.post("/")
async def add_dosage_form(
    dosage_form_schema: DosageFormSchema,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("ADD_DOSAGE_FORM", user["id"], db)
    create_dosage_form_model = DosageForm(
        dosage_form=dosage_form_schema.dosage_form,
        description=dosage_form_schema.description,
    )

    db.add(create_dosage_form_model)
    db.commit()
    return dosage_form_schema


@router.get("/{dosage_form_id}")
async def get_dosage_form(
    dosage_form_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("VIEW_DOSAGE_FORM", user["id"], db)
    dosage_form = get_object(dosage_form_id, db, DosageForm)

    return dosage_form


@router.put("/{dosage_form_id}")
async def update_dosage_form(
    dosage_form_id: int,
    user: user_dependency,
    dosage_form_schema: DosageFormSchema,
    db: Session = Depends(get_db),
):
    security.secureAccess("UPDATE_DOSAGE_FORM", user["id"], db)
    dosage_form_model = get_object(dosage_form_id, db, DosageForm)

    dosage_form_model.dosage_form = dosage_form_schema.dosage_form
    dosage_form_model.description = dosage_form_schema.description

    db.commit()
    db.refresh(dosage_form_model)
    return dosage_form_schema


@router.delete("/{dosage_form_id}")
async def delete_dosage_form(
    dosage_form_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("DELETE_DOSAGE_FORM", user["id"], db)
    get_object(dosage_form_id, db, DosageForm)
    db.query(DosageForm).filter(DosageForm.id == dosage_form_id).delete()
    db.commit()
    raise HTTPException(
        status_code=status.HTTP_200_OK,
        detail="Dosage form successfully deleted",
    )
