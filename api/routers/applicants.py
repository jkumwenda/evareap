from fastapi import APIRouter, HTTPException, Depends, Query
from starlette import status
from models import Applicant, Country
from schemas.maladis import ApplicantSchema
from sqlalchemy.orm import Session, joinedload
from database import get_db
from .auth import get_current_user
from typing import Annotated
from sqlalchemy import or_
import math
from dependencies import Security
from sqlalchemy import func

router = APIRouter()

security = Security()

user_dependency = Annotated[dict, Depends(get_current_user)]


def get_object(id, db, model):
    data = db.query(model).filter(model.id == id).first()
    if data is None:
        raise HTTPException(status_code=404, detail=f"ID {id} : Does not exist")
    return data


@router.get("/")
async def get_applicants(
    user: user_dependency,
    db: Session = Depends(get_db),
    skip: int = Query(default=1, ge=1),
    limit: int = 10,
    search: str = "",
):
    security.secureAccess("VIEW_APPLICANT", user["id"], db)

    offset = (skip - 1) * limit
    query = (
        db.query(Applicant)
        .join(Country, Applicant.country_id == Country.id)
        .filter(or_(Applicant.applicant.ilike(f"%{search}%")))
        .options(
            joinedload(Applicant.country),
        )
        .offset(offset)
        .limit(limit)
        .all()
    )
    total_count = (
        db.query(Applicant)
        .filter(or_(Applicant.applicant.ilike(f"%{search}%")))
        .count()
    )
    pages = math.ceil(total_count / limit)
    return {"pages": pages, "data": query}


@router.post("/")
async def add_applicant(
    applicant_schema: ApplicantSchema,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("ADD_APPLICANT", user["id"], db)

    applicant_id = db.query(func.max(Applicant.applicant_id)).scalar()
    if applicant_id is not None:
        applicant_id = applicant_id + 1
    else:
        applicant_id = 1

    create_applicant_model = Applicant(
        applicant=applicant_schema.applicant,
        applicant_id=applicant_id,
        email=applicant_schema.email,
        phone=applicant_schema.phone,
        country_id=applicant_schema.country_id,
        address=applicant_schema.address,
    )

    db.add(create_applicant_model)
    db.commit()
    return applicant_schema


@router.get("/{applicant_id}")
async def get_applicant(
    applicant_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("VIEW_APPLICANT", user["id"], db)
    applicant = get_object(applicant_id, db, Applicant)

    if not applicant:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "applicant": {
            "id": applicant.id,
            "applicant": applicant.applicant,
            "email": applicant.email,
            "phone": applicant.phone,
            "address": applicant.address,
            "country_id": applicant.country_id,
            "country": applicant.country.country,
        },
        # "products": [
        #     {
        #         "id": role.id,
        #         "role_id": role.role.id,
        #         "role": role.role.role,
        #     }
        #     for role in user.user_role
        # ],
    }


@router.put("/{applicant_id}")
async def update_applicant(
    applicant_id: int,
    user: user_dependency,
    applicant_schema: ApplicantSchema,
    db: Session = Depends(get_db),
):
    security.secureAccess("UPDATE_APPLICANT", user["id"], db)
    applicant_model = get_object(applicant_id, db, Applicant)

    applicant_model.applicant = applicant_schema.applicant
    applicant_model.email = applicant_schema.email
    applicant_model.phone = applicant_schema.phone
    applicant_model.country_id = applicant_schema.country_id
    applicant_model.address = applicant_schema.address

    db.commit()
    db.refresh(applicant_model)
    return applicant_schema


@router.delete("/{applicant_id}")
async def delete_applicant(
    applicant_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("DELETE_APPLICANT", user["id"], db)
    get_object(applicant_id, db, Applicant)
    db.query(Applicant).filter(Applicant.id == applicant_id).delete()
    db.commit()
    raise HTTPException(
        status_code=status.HTTP_200_OK, detail="Applicant Successfully deleted"
    )
