from core.middlewares.i18n_middleware import LocalizationMiddleware
from core.payments.exceptions import NotFoundErrorException
from core.payments.routes import router as paymentsrouter
from core.users.routes import router as usersrouter
from fastapi.responses import JSONResponse 
from fastapi import FastAPI, Request, status


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
            "description": "managing CRUD operations for payments objects",
        }
    ],
)

# app.add_middleware(LocalizationMiddleware)


@app.exception_handler(NotFoundErrorException)
async def payment_not_found_handler(request: Request, exc:NotFoundErrorException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "status":"Payment Not Found",
            "message":exc.message
        }
    )



# اضافه کردن روت‌ها
app.include_router(usersrouter, tags=["users"])
app.include_router(paymentsrouter, tags=["payments"])
