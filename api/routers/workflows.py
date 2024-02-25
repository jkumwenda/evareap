from fastapi import APIRouter, HTTPException, Depends, Query
from starlette import status
from models import Workflow, ApprovalStage
from schemas.maladis import WorkflowSchema, ApprovalStageSchema
from sqlalchemy.orm import Session, joinedload
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
async def get_workflows(
    user: user_dependency,
    db: Session = Depends(get_db),
    skip: int = Query(default=1, ge=1),
    limit: int = 10,
    search: str = "",
):
    security.secureAccess("VIEW_WORKFLOW", user["id"], db)

    offset = (skip - 1) * limit
    query = (
        db.query(Workflow)
        .filter(
            or_(
                Workflow.workflow.ilike(f"%{search}%"),
                Workflow.description.ilike(f"%{search}%"),
            )
        )
        .offset(offset)
        .limit(limit)
        .all()
    )
    total_count = (
        db.query(Workflow)
        .filter(
            or_(
                Workflow.workflow.ilike(f"%{search}%"),
                Workflow.description.ilike(f"%{search}%"),
            )
        )
        .count()
    )
    pages = math.ceil(total_count / limit)
    return {"pages": pages, "data": query}


@router.post("/")
async def add_workflow(
    workflow_schema: WorkflowSchema,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("ADD_WORKFLOW", user["id"], db)
    create_workflow_model = Workflow(
        workflow=workflow_schema.workflow,
        description=workflow_schema.description,
    )

    db.add(create_workflow_model)
    db.commit()
    return workflow_schema


@router.get("/{workflow_id}")
async def get_workflow(
    workflow_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("VIEW_WORKFLOW", user["id"], db)

    workflow = get_object(workflow_id, db, Workflow)

    return {
        "workflow": {
            "id": workflow.id,
            "workflow": workflow.workflow,
            "description": workflow.description,
        },
        "approval_stages": [
            {
                "id": approval_stage.id,
                "role_id": approval_stage.role_id,
                "stage_number": approval_stage.stage_number,
                "stage": approval_stage.stage,
            }
            for approval_stage in workflow.approval_stage
        ],
    }


@router.get("/name/{workflow}")
async def get_workflow_name(
    workflow: str,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("VIEW_WORKFLOW", user["id"], db)

    workflow = (
        db.query(Workflow)
        .options(joinedload(Workflow.approval_stage).joinedload(ApprovalStage.role))
        .filter(Workflow.workflow == workflow)
        .first()
    )
    if workflow is None:
        raise HTTPException(
            status_code=404, detail=f"Workflow {workflow} : Does not exist"
        )
    return {
        "workflow": {
            "id": workflow.id,
            "workflow": workflow.workflow,
            "description": workflow.description,
        },
        "approval_stages": [
            {
                "id": approval_stage.id,
                "role_id": approval_stage.role_id,
                "role_name": approval_stage.role.role,
                "stage_number": approval_stage.stage_number,
                "stage": approval_stage.stage,
            }
            for approval_stage in workflow.approval_stage
        ],
    }


@router.put("/{workflow_id}")
async def update_workflow(
    workflow_id: int,
    user: user_dependency,
    workflow_schema: WorkflowSchema,
    db: Session = Depends(get_db),
):
    security.secureAccess("UPDATE_WORKFLOW", user["id"], db)
    workflow_model = get_object(workflow_id, db, Workflow)

    workflow_model.workflow = workflow_schema.workflow
    workflow_model.description = workflow_schema.description

    db.commit()
    db.refresh(workflow_model)
    return workflow_schema


@router.delete("/{workflow_id}")
async def delete_workflow(
    workflow_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("DELETE_WORKFLOW", user["id"], db)
    get_object(workflow_id, db, Workflow)
    db.query(Workflow).filter(Workflow.id == workflow_id).delete()
    db.commit()
    raise HTTPException(
        status_code=status.HTTP_200_OK,
        detail="workflow form successfully deleted",
    )


@router.post("/approval_stage/")
async def add_approval_stage(
    approval_stage_schema: ApprovalStageSchema,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("ADD_WORKFLOW", user["id"], db)
    approval_stage_model = ApprovalStage(
        workflow_id=approval_stage_schema.workflow_id,
        role_id=approval_stage_schema.role_id,
        stage=approval_stage_schema.stage,
        stage_number=approval_stage_schema.stage_number,
    )
    db.add(approval_stage_model)
    db.commit()
    db.refresh(approval_stage_model)
    return approval_stage_model


@router.put("/approval_stage/{approval_stage_id}")
async def update_approval_stage(
    approval_stage_id: int,
    approval_stage_schema: ApprovalStageSchema,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("UPDATE_WORKFLOW", user["id"], db)
    approval_stage_model = (
        db.query(ApprovalStage).filter(ApprovalStage.id == approval_stage_id).first()
    )
    approval_stage_model.workflow_id = approval_stage_schema.workflow_id
    approval_stage_model.role_id = approval_stage_schema.role_id
    approval_stage_model.stage = approval_stage_schema.stage
    approval_stage_model.stage_number = approval_stage_schema.stage_number

    db.add(approval_stage_model)
    db.commit()
    db.refresh(approval_stage_model)
    return approval_stage_model


@router.delete("/approval_stage/{approval_stage_id}")
async def delete_approval_stage(
    approval_stage_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("DELETE_WORKFLOW", user["id"], db)

    get_object(approval_stage_id, db, ApprovalStage)

    db.query(ApprovalStage).filter(ApprovalStage.id == approval_stage_id).delete()
    db.commit()

    raise HTTPException(status_code=200, detail="Approval stage successfully deleted")
