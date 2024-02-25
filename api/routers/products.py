import os
from fastapi import APIRouter, HTTPException, Depends, Query
from starlette import status
from models import (
    Product,
    ProductCategory,
    Country,
    Manufacturer,
    AdministrationRoute,
    TherapeuticCategory,
    GenericName,
    Applicant,
    ProductApproval,
    ApprovalStage,
    Users,
    UserRole,
    ProductApprovalComment,
    ProductLicenceStatus,
    ProductLicenceFee,
    ProductVariation,
)
import utils
from schemas.maladis import ProductSchema, ProductApprovalSchema, ProductVariationSchema
from sqlalchemy.orm import Session, joinedload
from database import get_db
from .auth import get_current_user
from typing import Annotated
from sqlalchemy import or_, Update
import math
from dependencies import Security
from sqlalchemy import func
from fastapi import Response
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from io import BytesIO

router = APIRouter()
security = Security()

user_dependency = Annotated[dict, Depends(get_current_user)]


def get_object(id, db, model):
    data = db.query(model).filter(model.id == id).first()
    if data is None:
        raise HTTPException(status_code=404, detail=f"ID {id} : Does not exist")
    return data


@router.get("/")
async def get_products(
    user: user_dependency,
    db: Session = Depends(get_db),
    skip: int = Query(default=1, ge=1),
    limit: int = 10,
    search: str = "",
):
    security.secureAccess("VIEW_PRODUCT", user["id"], db)

    offset = (skip - 1) * limit
    query = (
        db.query(Product)
        .join(ProductCategory, Product.product_category_id == ProductCategory.id)
        .join(Applicant, Product.applicant_id == Applicant.id)
        .join(GenericName, Product.generic_name_id == GenericName.id)
        .join(
            TherapeuticCategory,
            Product.therapeutic_category_id == TherapeuticCategory.id,
        )
        .join(
            AdministrationRoute,
            Product.administration_route_id == AdministrationRoute.id,
        )
        .join(Manufacturer, Product.manufacturer_id == Manufacturer.id)
        .join(Country, Product.country_id == Country.id)
        .filter(
            or_(
                Product.product_name.ilike(f"%{search}%"),
                Product.product_id.ilike(f"%{search}%"),
            )
        )
        .options(
            joinedload(Product.product_category),
            joinedload(Product.applicant),
            joinedload(Product.generic_name),
            joinedload(Product.therapeutic_category),
            joinedload(Product.administration_route),
            joinedload(Product.manufacturer),
            joinedload(Product.country),
        )
        .offset(offset)
        .limit(limit)
        .all()
    )
    total_count = (
        db.query(Product)
        .filter(
            or_(
                Product.product_name.ilike(f"%{search}%"),
                Product.product_id.ilike(f"%{search}%"),
            )
        )
        .count()
    )
    pages = math.ceil(total_count / limit)
    return {"pages": pages, "data": query}


@router.post("/")
async def add_product(
    product_schema: ProductSchema,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("ADD_PRODUCT", user["id"], db)

    product_id = db.query(func.max(Product.product_id)).scalar()
    if product_id is not None:
        product_id = product_id + 1
    else:
        product_id = 1

    create_product_model = Product(
        product_id=product_id,
        applicant_id=product_schema.applicant_id,
        product_category_id=product_schema.product_category_id,
        product_name=product_schema.product_name,
        generic_name_id=product_schema.generic_name_id,
        dosage_form_id=product_schema.dosage_form_id,
        therapeutic_category_id=product_schema.therapeutic_category_id,
        color=product_schema.color,
        scheduling_status=product_schema.scheduling_status,
        strength=product_schema.strength,
        administration_route_id=product_schema.administration_route_id,
        manufacturer_id=product_schema.manufacturer_id,
        country_id=product_schema.country_id,
        entry_date=product_schema.entry_date,
        expiry_date=product_schema.expiry_date,
        active_ingredient=product_schema.active_ingredient,
        unit_dose=product_schema.active_ingredient,
        package_size=product_schema.package_size,
        package_type=product_schema.package_type,
    )
    db.add(create_product_model)
    db.commit()
    db.refresh(create_product_model)

    product_licence_fee = (
        db.query(ProductLicenceFee).filter(ProductLicenceFee.status == 1).first()
    )

    create_product_licence_status_model = ProductLicenceStatus(
        product_id=create_product_model.id,
        product_licence_fee_id=product_licence_fee.id,
        entry_date=product_schema.entry_date,
        expiry_date=product_schema.expiry_date,
    )
    db.add(create_product_licence_status_model)
    db.commit()
    db.refresh(create_product_licence_status_model)

    create_product_variation_model = ProductVariation(
        product_id=create_product_model.id,
        product_category_id=product_schema.product_category_id,
        product_name=product_schema.product_name,
        generic_name_id=product_schema.generic_name_id,
        dosage_form_id=product_schema.dosage_form_id,
        therapeutic_category_id=product_schema.therapeutic_category_id,
        color=product_schema.color,
        scheduling_status=product_schema.scheduling_status,
        strength=product_schema.strength,
        administration_route_id=product_schema.administration_route_id,
        active_ingredient=product_schema.active_ingredient,
        unit_dose=product_schema.active_ingredient,
        package_size=product_schema.package_size,
        package_type=product_schema.package_type,
    )
    db.add(create_product_variation_model)
    db.commit()
    db.refresh(create_product_variation_model)

    return product_schema


@router.get("/{product_id}")
async def get_product(
    product_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("VIEW_PRODUCT", user["id"], db)

    product = get_object(product_id, db, Product)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product_licence_status = (
        db.query(ProductLicenceStatus)
        .filter(ProductLicenceStatus.product_id == product.product_id)
        .first()
    )
    product_variation = (
        db.query(ProductVariation)
        .filter(ProductVariation.product_id == product.product_id)
        .filter(ProductVariation.status == 1)
        .first()
    )

    if not product_licence_status:
        raise HTTPException(status_code=404, detail="Product license status not found")
    if not product_variation:
        raise HTTPException(
            status_code=404, detail="Product default variation not found"
        )

    return {
        "product": {
            "id": product.id,
            "product": product.product_name,
            "product_id": product.product_id,
            "product_category_id": product.product_category_id,
            "product_category": product.product_category.product_category,
            "applicant_id": product.applicant_id,
            "applicant": product.applicant.applicant,
            "applicant_address": product.applicant.address,
            "product_name": product.product_name,
            "generic_name_id": product.generic_name_id,
            "generic_name": product.generic_name.generic_name,
            "dosage_form_id": product.dosage_form_id,
            "dosage_form": product.dosage_form.dosage_form,
            "therapeutic_category_id": product.therapeutic_category_id,
            "therapeutic_category": product.therapeutic_category.therapeutic_category,
            "color": product.color,
            "scheduling_status": product.scheduling_status,
            "strength": product.strength,
            "administration_route_id": product.administration_route_id,
            "administration_route": product.administration_route.administration_route,
            "manufacturer_id": product.manufacturer_id,
            "manufacturer": product.manufacturer.manufacturer,
            "country_id": product.country_id,
            "country": product.country.country,
            "entry_date": product.entry_date,
            "expiry_date": product.expiry_date,
            "active_ingredient": product.active_ingredient,
            "unit_dose": product.unit_dose,
            "package_size": product.package_size,
            "package_type": product.package_type,
        },
        "product_licence_status": {
            "id": product_licence_status.id,
            "entry_date": product_licence_status.entry_date,
            "expiry_date": product_licence_status.expiry_date,
            "status": product_licence_status.status,
            "licence_fee": product_licence_status.product_licence_fee,
        },
        "product_variation": {
            "id": product_variation.id,
            "product": product_variation.product_name,
            "product_category_id": product_variation.product_category_id,
            "product_category": product_variation.product_category.product_category,
            "product_name": product_variation.product_name,
            "generic_name_id": product_variation.generic_name_id,
            "generic_name": product_variation.generic_name.generic_name,
            "dosage_form_id": product_variation.dosage_form_id,
            "dosage_form": product_variation.dosage_form.dosage_form,
            "therapeutic_category_id": product_variation.therapeutic_category_id,
            "therapeutic_category": product_variation.therapeutic_category.therapeutic_category,
            "color": product_variation.color,
            "scheduling_status": product_variation.scheduling_status,
            "strength": product_variation.strength,
            "administration_route_id": product_variation.administration_route_id,
            "administration_route": product_variation.administration_route.administration_route,
            "active_ingredient": product_variation.active_ingredient,
            "unit_dose": product_variation.unit_dose,
            "package_size": product_variation.package_size,
            "package_type": product_variation.package_type,
            "package_type": product_variation.created_at,
        },
        "product_retentions": [
            {
                "id": product_licence_status.id,
                "entry_date": product_licence_status.entry_date,
                "expiry_date": product_licence_status.expiry_date,
                "status": product_licence_status.status,
                "licence_fee": product_licence_status.product_licence_fee,
            }
            for product_licence_status in product.product_licence_status
        ],
        "product_variations": [
            {
                "id": product_variation.id,
                "product": product_variation.product_name,
                "product_category_id": product_variation.product_category_id,
                "product_category": product_variation.product_category.product_category,
                "product_name": product_variation.product_name,
                "generic_name_id": product_variation.generic_name_id,
                "generic_name": product_variation.generic_name.generic_name,
                "dosage_form_id": product_variation.dosage_form_id,
                "dosage_form": product_variation.dosage_form.dosage_form,
                "therapeutic_category_id": product_variation.therapeutic_category_id,
                "therapeutic_category": product_variation.therapeutic_category.therapeutic_category,
                "color": product_variation.color,
                "scheduling_status": product_variation.scheduling_status,
                "strength": product_variation.strength,
                "administration_route_id": product_variation.administration_route_id,
                "administration_route": product_variation.administration_route.administration_route,
                "active_ingredient": product_variation.active_ingredient,
                "unit_dose": product_variation.unit_dose,
                "package_size": product_variation.package_size,
                "package_type": product_variation.package_type,
                "package_type": product_variation.created_at,
            }
            for product_variation in product.product_variation
        ],
        "product_approvals": [
            {
                "id": product_approval.approval_stage_id,
                "user_id": product_approval.user_id,
                "status": product_approval.status,
                "date": product_approval.created_at,
                "stage": product_approval.approval_stage.stage,
                "firstname": product_approval.user.firstname,
                "lastname": product_approval.user.lastname,
            }
            for product_approval in product.product_approval
        ],
    }


@router.put("/{product_id}")
async def update_product(
    product_id: int,
    user: user_dependency,
    product_schema: ProductSchema,
    db: Session = Depends(get_db),
):
    security.secureAccess("UPDATE_PRODUCT", user["id"], db)
    product_model = get_object(product_id, db, Product)

    product_model.applicant_id = product_schema.applicant_id
    product_model.product_category_id = product_schema.product_category_id
    product_model.product_name = product_schema.product_name
    product_model.generic_name_id = product_schema.generic_name_id
    product_model.dosage_form_id = product_schema.dosage_form_id
    product_model.therapeutic_category_id = product_schema.therapeutic_category_id
    product_model.color = product_schema.color
    product_model.scheduling_status = product_schema.scheduling_status
    product_model.strength = product_schema.scheduling_status
    product_model.administration_route_id = product_schema.administration_route_id
    product_model.manufacturer_id = product_schema.manufacturer_id
    product_model.country_id = product_schema.country_id
    product_model.entry_date = product_schema.entry_date
    product_model.expiry_date = product_schema.expiry_date
    product_model.active_ingredient = product_schema.active_ingredient
    product_model.unit_dose = product_schema.active_ingredient
    product_model.package_size = product_schema.package_size
    product_model.package_type = product_schema.package_type
    db.commit()
    db.refresh(product_model)
    return product_schema


@router.delete("/{product_id}")
async def delete_product(
    product_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("DELETE_PRODUCT", user["id"], db)
    get_object(product_id, db, Product)
    db.query(Product).filter(Product.id == product_id).delete()
    db.commit()
    raise HTTPException(
        status_code=status.HTTP_200_OK, detail="Product Successfully deleted"
    )


@router.post("/product_approval/")
async def add_product_approval(
    product_approval_schema: ProductApprovalSchema,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("ADD_PRODUCT", user["id"], db)

    product_approval = (
        db.query(ProductApproval)
        .filter(ProductApproval.product_id == product_approval_schema.product_id)
        .all()
    )

    product = (
        db.query(Product)
        .filter(Product.id == product_approval_schema.product_id)
        .first()
    )

    if len(product_approval) > 0:
        product_approval = (
            db.query(ProductApproval)
            .filter(ProductApproval.status == 0)
            .filter(ProductApproval.product_id == product_approval_schema.product_id)
            .first()
        )
        if product_approval:
            if product_approval.user_id == user["id"]:
                product_approval_model = get_object(
                    product_approval.id, db, ProductApproval
                )

                product_approval_model.status = 1
                db.add(product_approval_model)
                db.commit()
                db.refresh(product_approval_model)

                product_approval_comment_model = ProductApprovalComment(
                    product_approval_id=product_approval.id,
                    comment=product_approval_schema.comment,
                )
                db.add(product_approval_comment_model)
                db.commit()
                db.refresh(product_approval_comment_model)

                # product_approval.approval_stage_id

                approval_stage = (
                    db.query(ApprovalStage)
                    .filter(ApprovalStage.id == product_approval.approval_stage_id)
                    .first()
                )
                next_stage = approval_stage.stage_number + 1
                approval_stage = (
                    db.query(ApprovalStage)
                    .filter(ApprovalStage.stage_number == next_stage)
                    .first()
                )
                if approval_stage:
                    approver = (
                        db.query(Users)
                        .join(Users.user_role)
                        .filter(UserRole.role_id == approval_stage.role_id)
                        .options(joinedload(Users.user_role))
                        .first()
                    )
                    if approver:
                        product_approval_model = ProductApproval(
                            product_id=product_approval_schema.product_id,
                            user_id=approver.id,
                            approval_stage_id=approval_stage.id,
                            status=0,
                        )
                        db.add(product_approval_model)
                        db.commit()
                        db.refresh(product_approval_model)
                        utils.approve_drug_licence(
                            approver.email, approver.firstname, product
                        )
                else:
                    product_licence_status_model = (
                        db.query(ProductLicenceStatus)
                        .filter(
                            ProductLicenceStatus.product_id
                            == product_approval_schema.product_id
                        )
                        .first()
                    )
                    product_licence_status_model.status = 1
                    db.add(product_licence_status_model)
                    db.commit()
                    db.refresh(product_licence_status_model)

                    raise HTTPException(
                        status_code=status.HTTP_200_OK,
                        detail="Product fully approved",
                    )
                raise HTTPException(
                    status_code=status.HTTP_200_OK,
                    detail="Product successfully approved",
                )
    else:
        approval_stage = (
            db.query(ApprovalStage).filter(ApprovalStage.stage_number == 1).first()
        )
        approver = (
            db.query(Users)
            .join(Users.user_role)
            .filter(UserRole.role_id == approval_stage.role_id)
            .options(joinedload(Users.user_role))
            .first()
        )

        if approver:
            if approver.id == user["id"]:
                product_approval_model = ProductApproval(
                    product_id=product_approval_schema.product_id,
                    user_id=approver.id,
                    approval_stage_id=approval_stage.id,
                    status=1,
                )
                db.add(product_approval_model)
                db.commit()
                db.refresh(product_approval_model)
                product_approval_comment_model = ProductApprovalComment(
                    product_approval_id=product_approval_model.id,
                    comment=product_approval_schema.comment,
                )
                db.add(product_approval_comment_model)
                db.commit()
                db.refresh(product_approval_comment_model)

                next_stage = approval_stage.stage_number + 1
                approval_stage = (
                    db.query(ApprovalStage)
                    .filter(ApprovalStage.stage_number == next_stage)
                    .first()
                )
                if approval_stage:
                    approver = (
                        db.query(Users)
                        .join(Users.user_role)
                        .filter(UserRole.role_id == approval_stage.role_id)
                        .options(joinedload(Users.user_role))
                        .first()
                    )
                    if approver:
                        product_approval_model = ProductApproval(
                            product_id=product_approval_schema.product_id,
                            user_id=approver.id,
                            approval_stage_id=approval_stage.id,
                            status=0,
                        )
                        db.add(product_approval_model)
                        db.commit()
                        db.refresh(product_approval_model)
                        # Send email here
                        utils.approve_drug_licence(
                            approver.email, approver.firstname, product
                        )
                else:
                    product_licence_status_model = (
                        db.query(ProductLicenceStatus)
                        .filter(
                            ProductLicenceStatus.product_id
                            == product_approval_schema.product_id
                        )
                        .first()
                    )
                    product_licence_status_model.status = 1
                    db.add(product_licence_status_model)
                    db.commit()
                    db.refresh(product_licence_status_model)
                    raise HTTPException(
                        status_code=status.HTTP_200_OK,
                        detail="Product fully approved",
                    )
                utils.approve_drug_licence(approver.email, approver.firstname, product)
                raise HTTPException(
                    status_code=status.HTTP_200_OK,
                    detail="Product successfully reviewed",
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Matching approver not fond",
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Approver does not exists"
            )
    return product_approval_schema


@router.get("/generate_certificate/{product_id}")
async def generate_certificate_pdf(
    product_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("VIEW_PRODUCT", user["id"], db)

    product = get_object(product_id, db, Product)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Create a BytesIO buffer to store the PDF content
    buffer = BytesIO()

    # Create a PDF document
    pdf = canvas.Canvas(buffer, pagesize=letter)

    logo_path = "assets/logo.png"  # Replace with the path to your logo image
    logo = ImageReader(logo_path)
    pdf.drawImage(logo, 250, 680, width=90, height=90)  # Adjust position

    # Add title
    pdf.setFont("Helvetica-Oblique", 11)
    pdf.drawCentredString(300, 660, "(No. 9 of 2019)")

    pdf.setFont("Helvetica", 11)
    pdf.drawCentredString(300, 645, "PHARMACY, MEDICINES AND POISONS (FEES AND FORMS)")

    pdf.setFont("Helvetica", 11)
    pdf.drawCentredString(300, 630, "REGULATIONS, 1998")

    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawCentredString(300, 615, "PRODUCT LICENCE")

    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawCentredString(300, 600, "(Section 62)")

    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawCentredString(
        300,
        585,
        f"Product Licence No: PMRA/PL{product.product_id}/3 issued at LILONGWE MALAWI",
    )

    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawCentredString(
        300,
        570,
        f"under section 62 of the Pharmacy and Medicines Regulatory Authority Act, 2019 to",
    )

    pdf.setFont("Helvetica-Oblique", 11)
    pdf.drawCentredString(300, 555, product.applicant.applicant)

    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawCentredString(
        300, 540, "(name of person or firm to whom license is issued)"
    )

    pdf.setFont("Helvetica-Oblique", 11)
    pdf.drawCentredString(300, 525, f"of {product.country.country}")

    pdf.setFont("Helvetica-Oblique", 11)
    pdf.drawCentredString(300, 510, f"{product.applicant.address}")

    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawCentredString(300, 495, "Address")

    pdf.setFont("Helvetica-Bold", 9)

    # Add other details as needed
    max_chars_per_line = 120  # Adjust as needed
    long_text = (
        "Who is hereby licenced to engage in any or all of the business activities "
        "outlned under section 62(1) of, and subject to, the Act in regard to the "
        "following medicine product(s) in accordance with special condition specified hereunder"
    )

    # Calculate the number of lines needed
    num_lines = len(long_text) // max_chars_per_line + 1

    # Split the text into lines
    text_lines = [
        long_text[i * max_chars_per_line : (i + 1) * max_chars_per_line]
        for i in range(num_lines)
    ]

    # Draw each line separately
    for i, line in enumerate(text_lines):
        pdf.drawString(50, 480 - i * 14, line)

    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(50, 445, "(A) Medical product identity")

    # Add product details
    pdf.setFont("Helvetica", 11)
    y_position = 425  # Starting y position for product details

    medicine_identity = {
        "(i) Product Name": product.product_name,
        "(ii) Generic Name": product.generic_name.generic_name,
        "(iii) Dosage Form": product.dosage_form.dosage_form,
        "(iv) Strength": product.strength,
        "(v) Manufacturer": product.manufacturer.manufacturer,
        "(B) Therapeutic Category": product.therapeutic_category.therapeutic_category,
        "(C) Scheduling Status": product.scheduling_status,
        "(D) Declarartion of Content :-": "",
        "(i) Active Ingredient": product.active_ingredient,
        "(ii) Color": product.color,
        "(iii) Content per unit dose": product.unit_dose,
        "(E) Package :-": "",
        "(i) Type of package": product.package_type,
        "(ii) Size of package": product.package_size,
    }

    for key, value in medicine_identity.items():
        pdf.drawString(50, y_position, f"{key}: {value}")
        y_position -= 20

    # Add product approvals
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(50, y_position, "Further Conditions of this Product Licence are:")
    y_position -= 25

    # Add product approvals
    pdf.setFont("Helvetica", 11)
    pdf.drawString(50, y_position, "SUBJECT TO REVIEW BY MEDICINES COMMITTEE")
    y_position -= 20

    # Add product approvals
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(50, y_position, f"Valid until: {str(product.expiry_date)}")
    y_position -= 30

    # Add product approvals
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(50, y_position, f"Director general: Kabaghe")
    y_position -= 20

    # Add product approvals
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(50, y_position, f"Chairperson: ")
    y_position -= 20

    # for product_approval in product.product_approval:
    #     pdf.setFont("Helvetica", 11)
    #     approval_text = f"Stage {product_approval.approval_stage_id}: {product_approval.user.firstname} {product_approval.user.lastname} - {product_approval.status}"
    #     pdf.drawString(50, y_position, approval_text)
    #     y_position -= 15

    # Save the PDF content
    pdf.save()

    # Move the buffer's position to the beginning
    buffer.seek(0)

    # Set the response headers to indicate a PDF file download
    headers = {
        "Content-Disposition": "attachment; filename=product_certificate.pdf",
        "Content-Type": "application/pdf",
    }

    # Return the PDF content as a response
    return Response(content=buffer.read(), headers=headers)


@router.post("/add_product_variation")
async def add_product_variation(
    product_variation_schema: ProductVariationSchema,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("ADD_PRODUCT", user["id"], db)

    db.query(ProductVariation).filter(
        ProductVariation.product_id == product_variation_schema.product_id
    ).update({"status": False})

    create_product_variation_model = ProductVariation(
        product_id=product_variation_schema.product_id,
        product_category_id=product_variation_schema.product_category_id,
        product_name=product_variation_schema.product_name,
        generic_name_id=product_variation_schema.generic_name_id,
        dosage_form_id=product_variation_schema.dosage_form_id,
        therapeutic_category_id=product_variation_schema.therapeutic_category_id,
        color=product_variation_schema.color,
        scheduling_status=product_variation_schema.scheduling_status,
        strength=product_variation_schema.strength,
        administration_route_id=product_variation_schema.administration_route_id,
        active_ingredient=product_variation_schema.active_ingredient,
        unit_dose=product_variation_schema.active_ingredient,
        package_size=product_variation_schema.package_size,
        package_type=product_variation_schema.package_type,
    )
    db.add(create_product_variation_model)
    db.commit()
    db.refresh(create_product_variation_model)

    return product_variation_schema


@router.delete("/product_variation/{product_variation_id}")
async def delete_product_variation(
    product_variation_id: int,
    user: user_dependency,
    db: Session = Depends(get_db),
):
    security.secureAccess("DELETE_PRODUCT", user["id"], db)
    get_object(product_variation_id, db, ProductVariation)
    db.query(ProductVariation).filter(
        ProductVariation.id == product_variation_id
    ).delete()
    db.commit()
    raise HTTPException(
        status_code=status.HTTP_200_OK, detail="Product Variation Successfully deleted"
    )
