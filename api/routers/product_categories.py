from fastapi import APIRouter, HTTPException, Depends, Query
from starlette import status
from models import ProductCategory
from schemas.maladis import ProductCategorySchema
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
async def get_product_categories(
    user: user_dependency,
    db: Session = Depends(get_db),
    skip: int = Query(default=1, ge=1),
    limit: int = 10,
    search: str = "",
):
    security.secureAccess("VIEW_PRODUCT_CATEGORY", user["id"], db)

    offset = (skip - 1) * limit
    query = (
        db.query(ProductCategory)
        .filter(
            or_(
                ProductCategory.product_category.ilike(f"%{search}%"),
                ProductCategory.category_code.ilike(f"%{search}%"),
                ProductCategory.description.ilike(f"%{search}%"),
            )
        )
        .offset(offset)
        .limit(limit)
        .all()
    )
    total_count = (
        db.query(ProductCategory)
        .filter(
            or_(
                ProductCategory.product_category.ilike(f"%{search}%"),
                ProductCategory.category_code.ilike(f"%{search}%"),
                ProductCategory.description.ilike(f"%{search}%"),
            )
        )
        .count()
    )
    pages = math.ceil(total_count / limit)
    return {"pages": pages, "data": query}


@router.post("/")
async def add_product_category(
    product_category_schema: ProductCategorySchema,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("ADD_PRODUCT_CATEGORY", user["id"], db)
    create_product_category_model = ProductCategory(
        product_category=product_category_schema.product_category,
        category_code=product_category_schema.category_code,
        description=product_category_schema.description,
    )

    db.add(create_product_category_model)
    db.commit()
    return product_category_schema


@router.get("/{product_category_id}")
async def get_product_category(
    product_category_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("VIEW_PRODUCT_CATEGORY", user["id"], db)
    product_category = get_object(product_category_id, db, ProductCategory)

    return product_category


@router.put("/{product_category_id}")
async def update_product_category(
    product_category_id: int,
    user: user_dependency,
    product_category_schema: ProductCategorySchema,
    db: Session = Depends(get_db),
):
    security.secureAccess("UPDATE_PRODUCT_CATEGORY", user["id"], db)
    product_category_model = get_object(product_category_id, db, ProductCategory)

    product_category_model.product_category = product_category_schema.product_category
    product_category_model.category_code = product_category_schema.category_code
    product_category_model.description = product_category_schema.description

    db.commit()
    db.refresh(product_category_model)
    return product_category_schema


@router.delete("/{product_category_id}")
async def delete_product_category(
    product_category_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("DELETE_PRODUCT_CATEGORY", user["id"], db)
    get_object(product_category_id, db, ProductCategory)
    db.query(ProductCategory).filter(ProductCategory.id == product_category_id).delete()
    db.commit()
    raise HTTPException(
        status_code=status.HTTP_200_OK, detail="Product category successfully deleted"
    )
