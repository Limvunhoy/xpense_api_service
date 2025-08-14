import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlmodel import Session, SQLModel, create_engine
from contextlib import asynccontextmanager
from app.database import get_session, create_db_and_tables
from .routers import transaction, account, category
from app.exceptions import AppHTTPException
from fastapi.staticfiles import StaticFiles


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        create_db_and_tables()
    except Exception as e: 
        print("Error creating tables: ", e)
    yield

app = FastAPI(lifespan=lifespan)

app.mount("/static/icons", StaticFiles(directory="app/static/icons"), name="static_icons")

app.include_router(transaction.router)
app.include_router(account.router)
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
    import uvicorn
    uvicorn.run("app/main:app", host="0.0.0.0", port=8000,
                log_level="info", reload=True)
