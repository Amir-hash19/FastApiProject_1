from core.payments.routes import router as paymentsrouter
from core.users.routes import router as usersrouter
from fastapi import FastAPI



app = FastAPI(
    title="Payment Manager API",
    description="""
    This is the part of the Payment app called Payments
""",
    version="1.0.0",
    contact={
        "name": "AmirYkta",
        "url": "https://Amir-hash19.github.io",
        "email": "amirhosein.hydri1381@email.com",
    },
    license_info={
        "name": "MIT",
        
    },
    openapi_tags=[
        {
            "name": "Payments",
            "description": "managing CRUD operations for payments objects"
        }
    ],
)



# اضافه کردن روت‌ها
app.include_router(usersrouter, tags=["users"])
app.include_router(paymentsrouter, tags=["payments"])


