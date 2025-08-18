import os

from fastapi import APIRouter, Depends, status, HTTPException
from typing import List

from sqlmodel import Session, select
from app.models.user import User
from app.routers.user import get_current_user
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
async def get_categories(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    query = select(Category).where(
        Category.user_id == current_user.id,
        Category.is_active == True,
    )
    categories = session.exec(query).all()
    return success_response(data=categories)


@router.post("/", response_model=BaseResponse[CategoryRead], status_code=status.HTTP_201_CREATED)
async def create_category(
    category: CategoryCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    statement = select(Category).where(
        Category.user_id == current_user.id,
        Category.name == category.name,
    )
    existing_category = session.exec(statement).first()
    if existing_category:
        raise AppHTTPException(result_code=status.HTTP_400_BAD_REQUEST,
                               result_message="Category already exists", error_code="E400")

    new_category = Category(**category.model_dump(), user_id=current_user.id)
    session.add(new_category)
    session.commit()
    session.refresh(new_category)
    return success_response(data=new_category)


@router.patch("/{id}", response_model=BaseResponse[CategoryRead])
async def update_category(
    id: str,
    category: CategoryUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    category_db = session.get(Category, id)
    if not category_db or not category_db.is_active or category_db.user_id != current_user.id:
        raise AppHTTPException(
            result_code=404, result_message="Category not found", error_code="E404")
    if category_db.user_id != current_user.id:
        raise AppHTTPException(
            result_code=403, result_message="Cannot update another user's category", error_code="E403")

    category_data = category.model_dump(exclude_unset=True)
    category_db.sqlmodel_update(category_data)
    session.add(category_db)
    session.commit()
    session.refresh(category_db)
    return success_response(data=category_db)


@router.post("/delete")
async def delete_category(
    request: CategoryDelete,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    category_db = session.get(Category, request.category_id)
    if not category_db or not category_db.is_active or category_db.id != current_user.id:
        raise AppHTTPException(
            result_code=404, result_message="Category not found", error_code="E404")
    if category_db.user_id != current_user.id:
        raise AppHTTPException(
            result_code=403, result_message="Cannot delete another user's category", error_code="E403")

    category_db.is_active = False
    session.add(category_db)
    session.commit()
    session.refresh(category_db)
    return success_response()
