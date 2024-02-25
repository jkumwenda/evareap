from fastapi import APIRouter, HTTPException, Depends, Query
from starlette import status
from models import Manufacturer, Country
from schemas.maladis import ManufacturerSchema
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
async def get_manufacturers(
    user: user_dependency,
    db: Session = Depends(get_db),
    skip: int = Query(default=1, ge=1),
    limit: int = 10,
    search: str = "",
):
    security.secureAccess("VIEW_MANUFACTURER", user["id"], db)

    offset = (skip - 1) * limit
    query = (
        db.query(Manufacturer)
        .join(Country, Manufacturer.country_id == Country.id)
        .filter(or_(Manufacturer.manufacturer.ilike(f"%{search}%")))
        .options(
            joinedload(Manufacturer.country),
        )
        .offset(offset)
        .limit(limit)
        .all()
    )
    total_count = (
        db.query(Manufacturer)
        .filter(or_(Manufacturer.manufacturer.ilike(f"%{search}%")))
        .count()
    )
    pages = math.ceil(total_count / limit)
    return {"pages": pages, "data": query}


@router.post("/")
async def add_manufacturer(
    manufacturer_schema: ManufacturerSchema,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("ADD_MANUFACTURER", user["id"], db)

    manufacturer_id = db.query(func.max(Manufacturer.manufacturer_id)).scalar()
    if manufacturer_id is not None:
        manufacturer_id = manufacturer_id + 1
    else:
        manufacturer_id = 1

    create_manufacturer_model = Manufacturer(
        manufacturer=manufacturer_schema.manufacturer,
        manufacturer_id=manufacturer_id,
        email=manufacturer_schema.email,
        phone=manufacturer_schema.phone,
        country_id=manufacturer_schema.country_id,
        address=manufacturer_schema.address,
    )

    db.add(create_manufacturer_model)
    db.commit()
    return manufacturer_schema


@router.get("/{manufacturer_id}")
async def get_manufacturer(
    manufacturer_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("VIEW_MANUFACTURER", user["id"], db)
    manufacturer = get_object(manufacturer_id, db, Manufacturer)

    if not manufacturer:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "manufacturer": {
            "id": manufacturer.id,
            "manufacturer": manufacturer.manufacturer,
            "email": manufacturer.email,
            "phone": manufacturer.phone,
            "address": manufacturer.address,
            "country_id": manufacturer.country_id,
            "country": manufacturer.country.country,
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


@router.put("/{manufacturer_id}")
async def update_manufacturer(
    manufacturer_id: int,
    user: user_dependency,
    manufacturer_schema: ManufacturerSchema,
    db: Session = Depends(get_db),
):
    security.secureAccess("UPDATE_MANUFACTURER", user["id"], db)
    manufacturer_model = get_object(manufacturer_id, db, Manufacturer)

    manufacturer_model.manufacturer = manufacturer_schema.manufacturer
    manufacturer_model.email = manufacturer_schema.email
    manufacturer_model.phone = manufacturer_schema.phone
    manufacturer_model.country_id = manufacturer_schema.country_id
    manufacturer_model.address = manufacturer_schema.address

    db.commit()
    db.refresh(manufacturer_model)
    return manufacturer_schema


@router.delete("/{manufacturer_id}")
async def delete_manufacturer(
    manufacturer_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("DELETE_MANUFACTURER", user["id"], db)
    get_object(manufacturer_id, db, Manufacturer)
    db.query(Manufacturer).filter(Manufacturer.id == manufacturer_id).delete()
    db.commit()
    raise HTTPException(
        status_code=status.HTTP_200_OK, detail="Manufacturer Successfully deleted"
    )
