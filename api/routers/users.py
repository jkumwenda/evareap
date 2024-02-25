import os
from fastapi import (
    APIRouter,
    HTTPException,
    Depends,
    Query,
    status,
    File,
    UploadFile,
    Form,
)
from starlette import status
from models import Users, UserRole
from schemas.maladis import UserSchema, UserRoleSchema
from sqlalchemy.orm import Session
from database import get_db
from .auth import get_current_user
from typing import Annotated
from sqlalchemy import or_
import math
from passlib.hash import bcrypt
from dependencies import Security
from fastapi.responses import FileResponse
import uuid

router = APIRouter()

user_dependency = Annotated[dict, Depends(get_current_user)]
security = Security()


def get_object(id, db, model):
    data = db.query(model).filter(model.id == id).first()
    if data is None:
        raise HTTPException(status_code=404, detail=f"ID {id} : Does not exist")
    return data


@router.get("/")
async def get_users(
    user: user_dependency,
    db: Session = Depends(get_db),
    skip: int = Query(default=1, ge=1),
    limit: int = 10,
    search: str = "",
):
    security.secureAccess("VIEW_USER", user["id"], db)
    offset = (skip - 1) * limit
    query = (
        db.query(Users)
        .filter(
            or_(
                Users.firstname.ilike(f"%{search}%"),
                Users.lastname.ilike(f"%{search}%"),
                Users.email.ilike(f"%{search}%"),
            )
        )
        .offset(offset)
        .limit(limit)
        .all()
    )
    total_count = (
        db.query(Users)
        .filter(
            or_(
                Users.firstname.ilike(f"%{search}%"),
                Users.lastname.ilike(f"%{search}%"),
                Users.email.ilike(f"%{search}%"),
            )
        )
        .count()
    )
    pages = math.ceil(total_count / limit)
    return {"pages": pages, "data": query}


@router.post("/")
async def add_user(
    user_schema: UserSchema,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("ADD_USER", user["id"], db)
    create_user_model = Users(
        firstname=user_schema.firstname,
        lastname=user_schema.lastname,
        phone=user_schema.phone,
        email=user_schema.email,
        hashed_password=bcrypt.hash(user_schema.password),
        verified=1,
    )

    db.add(create_user_model)
    db.commit()
    return user_schema


@router.get("/{user_id}")
async def get_user(
    user_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("VIEW_USER", user["id"], db)
    model = Users
    user = get_object(user_id, db, model)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "user": {
            "id": user.id,
            "email": user.email,
            "firstname": user.firstname,
            "lastname": user.lastname,
            "phone": user.phone,
        },
        "roles": [
            {
                "id": role.id,
                "role_id": role.role.id,
                "role": role.role.role,
            }
            for role in user.user_role
        ],
        "signatures": [
            {
                "id": signature.id,
                "file_name": signature.file_name,
                "file_location": signature.file_location,
            }
            for signature in user.user_signature
        ],
    }


@router.put("/{user_id}")
async def update_user(
    user_id: int,
    user: user_dependency,
    user_schema: UserSchema,
    db: Session = Depends(get_db),
):
    security.secureAccess("UPDATE_USER", user["id"], db)
    user_model = get_object(user_id, db, Users)

    user_model.firstname = (user_schema.firstname,)
    user_model.lastname = (user_schema.lastname,)
    user_model.phone = (user_schema.phone,)
    user_model.email = (user_schema.email,)

    db.commit()
    db.refresh(user_model)
    return user_schema


@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("DELETE_USER", user["id"], db)
    get_object(user_id, db, Users)
    db.query(Users).filter(Users.id == user_id).delete()
    db.commit()
    raise HTTPException(
        status_code=status.HTTP_200_OK, detail="Users Successfully deleted"
    )


@router.post("/roles/")
async def add_user_role(
    user_role_schema: UserRoleSchema,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("ADD_USER", user["id"], db)
    user_role_model = UserRole(
        user_id=user_role_schema.user_id, role_id=user_role_schema.role_id
    )

    db.add(user_role_model)
    db.commit()
    db.refresh(user_role_model)
    return user_role_model


@router.put("/roles/{user_role_id}")
async def update_user_role(
    user_role_id: int,
    user_role_schema: UserRoleSchema,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("UPDATE_USER", user["id"], db)
    user_role_model = db.query(UserRole).filter(UserRole.id == user_role_id).first()
    user_role_model.user_id = (user_role_schema.user_id,)
    user_role_model.role_id = user_role_schema.role_id
    db.add(user_role_model)
    db.commit()
    db.refresh(user_role_model)
    return user_role_model


@router.delete("/roles/{user_role_id}")
async def delete_user_role(
    user_role_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("DELETE_USER", user["id"], db)

    db.query(UserRole).filter(UserRole.id == user_role_id).delete()
    db.commit()
    raise HTTPException(status_code=200, detail="Users role successfully deleted")

