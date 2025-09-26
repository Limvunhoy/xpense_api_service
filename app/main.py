import os
import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from app.database import create_db_and_tables, test_connection
from app.routers import user, transaction, wallet, category
from app.exceptions import AppHTTPException
from app.core.settings import settings

logging.basicConfig(level=logging.INFO)
logging.info(f"Loaded ENV: {settings.ENV}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("App startup: testing DB connection")
    if not test_connection():
        logging.warning(
            "Database not available at startup, continuing anyway...")
    try:
        create_db_and_tables()
    except Exception as e:
        logging.warning(f"Skipping table creation: {e}")
    yield
    logging.info("App shutdown")


app = FastAPI(lifespan=lifespan)

# Mount static files
app.mount("/static/icons", StaticFiles(directory="app/static/icons"),
          name="static_icons")

# Include routers
app.include_router(user.router)
app.include_router(transaction.router)
app.include_router(wallet.router)
app.include_router(category.router)


@app.get("/")
def root():
    return {"message": "Welcome to Xpense API Service"}


@app.exception_handler(AppHTTPException)
async def http_exception_handler(request: Request, exc: AppHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "result_code": exc.status_code,
            "result_message": exc.detail,
            "error_code": exc.error_code
        },
    )


if __name__ == "__main__":
    # Use Cloud Run port
    port = int(os.environ.get("PORT", 8080))
    logging.info(f"Starting FastAPI on port {port}")
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, log_level="info")
