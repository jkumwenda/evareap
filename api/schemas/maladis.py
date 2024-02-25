from pydantic import BaseModel
from datetime import date, datetime


class UserSchema(BaseModel):
    firstname: str
    lastname: str
    phone: str
    email: str
    password: str


class TokenSchema(BaseModel):
    access_token: str
    token_type: str


class RoleSchema(BaseModel):
    role: str
    description: str


class UserRoleSchema(BaseModel):
    user_id: int
    role_id: int


class PermissionSchema(BaseModel):
    permission: str
    permission_code: str


class RolePermissionSchema(BaseModel):
    role_id: int
    permission_id: int


class ManufacturerSchema(BaseModel):
    manufacturer: str
    email: str
    phone: str
    country_id: int
    address: str


class ApplicantSchema(BaseModel):
    applicant: str
    email: str
    phone: str
    country_id: int
    address: str


class ProductCategorySchema(BaseModel):
    product_category: str
    category_code: str
    description: str


class TherapeuticCategorySchema(BaseModel):
    therapeutic_category: str
    description: str


class AdministrationRouteSchema(BaseModel):
    administration_route: str
    description: str


class GenericNameSchema(BaseModel):
    generic_name: str
    description: str


class DosageFormSchema(BaseModel):
    dosage_form: str
    description: str


class ProductSchema(BaseModel):
    applicant_id: int
    product_category_id: int
    product_name: str
    generic_name_id: int
    dosage_form_id: int
    therapeutic_category_id: int
    color: str
    scheduling_status: str
    strength: str
    administration_route_id: int
    manufacturer_id: int
    country_id: int
    entry_date: datetime
    expiry_date: datetime
    active_ingredient: str
    unit_dose: str
    package_size: str
    package_type: str


class WorkflowSchema(BaseModel):
    workflow: str
    description: str


class ApprovalStageSchema(BaseModel):
    workflow_id: int
    role_id: int
    stage_number: int
    stage: str


class ApprovalSchema(BaseModel):
    approval_stage_id: int
    user_id: int
    status: int


class ApprovalCommentSchema(BaseModel):
    approval_id: int
    comment: int


class ProductApprovalSchema(BaseModel):
    product_id: int
    comment: str


class ProductLicenceFeeSchema(BaseModel):
    product_license_fee: int


class ProductVariationSchema(BaseModel):
    product_id: int
    product_category_id: int
    product_name: str
    generic_name_id: int
    dosage_form_id: int
    therapeutic_category_id: int
    color: str
    scheduling_status: str
    strength: str
    administration_route_id: int
    active_ingredient: str
    unit_dose: str
    package_size: str
    package_type: str
