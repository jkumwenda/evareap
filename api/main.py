from fastapi import FastAPI
from routers import (
    auth,
    users,
    roles,
    permissions,
)
from fastapi.middleware.cors import CORSMiddleware

# from config import settings

app = FastAPI(
    title="EVAREAP API",
    description="EVAREAP API",
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "MUST Dev Team",
        "url": "https://github.com/jkumwenda",
        "email": "jkumwenda@gmail.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

origins = [
    # settings.CLIENT_ORIGIN,
]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# Allow all origins for CORS. Customize as needed for production.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, tags=["Auth"], prefix="/auth")
app.include_router(users.router, tags=["User"], prefix="/users")
app.include_router(roles.router, tags=["Role"], prefix="/roles")
app.include_router(permissions.router, tags=["Permission"], prefix="/permissions")
# app.include_router(countries.router, tags=["Country"], prefix="/countries")
# app.include_router(applicants.router, tags=["Applicant"], prefix="/applicants")
# app.include_router(manufacturers.router, tags=["Manufacturer"], prefix="/manufacturers")
# app.include_router(
#     product_categories.router, tags=["Product Categories"], prefix="/product_categories"
# )
# app.include_router(
#     therapeutic_categories.router,
#     tags=["Therapeutic Categories"],
#     prefix="/therapeutic_categories",
# )
# app.include_router(
#     administration_routes.router,
#     tags=["Administration Route"],
#     prefix="/administration_routes",
# )
# app.include_router(
#     generic_names.router,
#     tags=["Generic Names"],
#     prefix="/generic_names",
# )
# app.include_router(
#     dosage_forms.router,
#     tags=["Dosage Forms"],
#     prefix="/dosage_forms",
# )
# app.include_router(
#     products.router,
#     tags=["Products"],
#     prefix="/products",
# )
# app.include_router(
#     workflows.router,
#     tags=["Workflows"],
#     prefix="/workflows",
# )

# app.include_router(
#     product_licence_fees.router,
#     tags=["Product Licence Fees"],
#     prefix="/product_licence_fees",
# )
