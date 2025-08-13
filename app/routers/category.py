import os
from uuid import UUID
from fastapi import APIRouter, Depends, status, HTTPException
from typing import List

from sqlmodel import Session, select
from app.schemas.category import CategoryDelete, CategoryRead, CategoryCreate, CategoryUpdate
from app.models.category import Category
from app.database import get_session
from app.schemas.base_response import BaseResponse
from app.exceptions import AppHTTPException
from app.core.helper.success_response import success_response

router = APIRouter(prefix="/categories", tags=["Categories"])

ICON_DIR = "app/static/icons"
ICON_BASE_URL = "/static/icons"


@router.get("/icons", response_model=BaseResponse[List[str]])
async def get_icons():
    """
    List all icon filenames (or URLs) available in the icons folder.
    """

    try:
        files = [
            f for f in os.listdir(ICON_DIR)
            if os.path.isfile(os.path.join(ICON_DIR, f)) and f.lower().endswith(((".svg", ".png", ".jpg", ".jpeg", ".ico")))
        ]
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to read icons folder: {str(e)}"
        )

    icon_urls = [f"{ICON_BASE_URL}/{filename}" for filename in files]
    return success_response(data=icon_urls)


@router.get("/", response_model=BaseResponse[List[CategoryRead]])
async def get_categories(session: Session = Depends(get_session)) -> List[CategoryRead]:
    """Retrieve all categories from the database."""

    query = select(Category).where(
        Category.is_active == True
    )
    categories = session.exec(query).all()

    return success_response(data=categories or [])


@router.post("/", response_model=BaseResponse[CategoryRead], status_code=status.HTTP_201_CREATED)
async def create_category(category: CategoryCreate, session: Session = Depends(get_session)):
    # Check if category already exists
    statement = select(Category).where(Category.name == category.name)
    existing_category = session.exec(statement).first()

    if existing_category:
        raise AppHTTPException(
            result_code=status.HTTP_400_BAD_REQUEST,
            result_message="Category already exists",
            error_code="E400"
        )

    new_category = Category(**category.model_dump())
    session.add(new_category)
    session.commit()
    session.refresh(new_category)
    return success_response(
        result_code=status.HTTP_201_CREATED,
        data=new_category,
    )


@router.patch("/{id}", response_model=BaseResponse[CategoryRead])
async def update_category(id: UUID, category: CategoryUpdate, session: Session = Depends(get_session)):
    category_db = session.get(Category, id)
    if category_db is None or not category_db.is_active:
        raise AppHTTPException(
            result_code=404,
            result_message="Category not found",
            error_code="E400"
        )
    category_data = category.model_dump(exclude_unset=True)
    category_db.sqlmodel_update(category_data)
    session.add(category_db)
    session.commit()
    session.refresh(category_db)
    return success_response(data=category_db)


# @router.delete("/{id}")
# async def delete_category(id: str, session: Session = Depends(get_session)):
#     category_data = session.get(Category, id)
#     if not category_data:
#         raise AppHTTPException(
#             result_code=404,
#             result_message="Category not found",
#             error_code="E404"
#         )
#     session.delete(category_data)
#     session.commit()
#     return success_response()

@router.post("/delete", response_model=BaseResponse)
async def delete_category(
    request: CategoryDelete,
    session: Session = Depends(get_session)
):
    category_db = session.get(Category, request.category_id)
    if not category_db:
        raise AppHTTPException(
            result_code=404,
            result_message="Category not found",
            error_code="E404"
        )
    category_db.is_active = False

    session.add(category_db)
    session.commit()
    session.refresh(category_db)

    return success_response()
