from fastapi import APIRouter, HTTPException, Depends, Query
from starlette import status
from models import ProductLicenceFee
from schemas.maladis import ProductLicenceFeeSchema
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
async def get_product_licence_fees(
    user: user_dependency,
    db: Session = Depends(get_db),
    skip: int = Query(default=1, ge=1),
    limit: int = 10,
    search: str = "",
):
    security.secureAccess("VIEW_PRODUCT_LICENCE_FEE", user["id"], db)

    offset = (skip - 1) * limit
    query = (
        db.query(ProductLicenceFee)
        .filter(
            or_(
                ProductLicenceFee.product_license_fee.ilike(f"%{search}%"),
            )
        )
        .offset(offset)
        .limit(limit)
        .all()
    )
    total_count = (
        db.query(ProductLicenceFee)
        .filter(
            or_(
                ProductLicenceFee.product_license_fee.ilike(f"%{search}%"),
            )
        )
        .count()
    )
    pages = math.ceil(total_count / limit)
    return {"pages": pages, "data": query}


@router.post("/")
async def add_product_licence_fee(
    product_licence_fee_schema: ProductLicenceFeeSchema,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("ADD_PRODUCT_LICENCE_FEE", user["id"], db)
    create_product_licence_fee_model = ProductLicenceFee(
        product_license_fee=product_licence_fee_schema.product_license_fee,
    )

    db.add(create_product_licence_fee_model)
    db.commit()
    return product_licence_fee_schema


@router.get("/{product_licence_fee_id}")
async def get_product_licence_fee(
    product_licence_fee_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("VIEW_PRODUCT_LICENCE_FEE", user["id"], db)
    product_licence_fee = get_object(product_licence_fee_id, db, ProductLicenceFee)
    if not product_licence_fee:
        raise HTTPException(status_code=404, detail="ProductLicenceFee not found")

    return {
        "product_licence_fee": {
            "id": product_licence_fee.id,
            "product_licence_fee": product_licence_fee.product_license_fee,
        },
        # "permissions": [
        #     {
        #         "id": permission.id,
        #         "permission_id": permission.permission.id,
        #         "permission": permission.permission.permission,
        #         "permission_code": permission.permission.permission_code,
        #     }
        #     for permission in product_licence_fee.product_licence_fee_permission
        # ],
    }


@router.put("/{product_licence_fee_id}")
async def update_product_licence_fee(
    product_licence_fee_id: int,
    user: user_dependency,
    product_licence_fee_schema: ProductLicenceFeeSchema,
    db: Session = Depends(get_db),
):
    security.secureAccess("UPDATE_PRODUCT_LICENCE_FEE", user["id"], db)
    product_licence_fee_model = get_object(
        product_licence_fee_id, db, ProductLicenceFee
    )

    product_licence_fee_model.product_license_fee = (
        product_licence_fee_schema.product_license_fee
    )

    db.commit()
    db.refresh(product_licence_fee_model)
    return product_licence_fee_schema


@router.delete("/{product_licence_fee_id}")
async def delete_product_licence_fee(
    product_licence_fee_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("DELETE_PRODUCT_LICENCE_FEE", user["id"], db)
    get_object(product_licence_fee_id, db, ProductLicenceFee)
    db.query(ProductLicenceFee).filter(
        ProductLicenceFee.id == product_licence_fee_id
    ).delete()
    db.commit()
    raise HTTPException(
        status_code=status.HTTP_200_OK,
        detail="Product Licence Fee Successfully deleted",
    )
