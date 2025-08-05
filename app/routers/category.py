from fastapi import APIRouter, Depends, status, HTTPException
from typing import List

from sqlmodel import Session, select
from app.schemas.category import CategoryRead, CategoryCreate, CategoryUpdate
from app.models.category import Category
from app.database import get_session

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/", response_model=List[CategoryRead])
async def get_categories(session: Session = Depends(get_session)) -> List[CategoryRead]:
    """Retrieve all categories from the database."""

    query = select(Category)
    categories = session.exec(query).all()

    if not categories:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No categories found")

    return categories


@router.post("/", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
async def create_category(category: CategoryCreate, session: Session = Depends(get_session)):
    # Check if category already exists
    statement = select(Category).where(Category.name == category.name)
    existing_category = session.exec(statement).first()

    if existing_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Category already exists")

    new_category = Category(**category.model_dump(exclude_unset=True))
    session.add(new_category)
    session.commit()
    session.refresh(new_category)
    return new_category


@router.patch("/{id}", response_model=CategoryRead)
async def update_category(id: str, category: CategoryUpdate, session: Session = Depends(get_session)):
    category_db = session.get(Category, id)
    if not category_db:
        raise HTTPException(status_code=404, detail="Category not found!")
    category_data = category.model_dump(exclude_unset=True)
    category_db.sqlmodel_update(category_data)
    session.add(category_db)
    session.commit()
    session.refresh(category_db)
    return category_db


@router.delete("/{id}")
async def delete_category(id: str, session: Session = Depends(get_session)):
    category_data = session.get(CategoryRead, id)
    if not category_data:
        raise HTTPException(status_code=404, detail="Category not found!")
    session.delete(category_data)
    session.commit()
    return {"message": "Category deleted"}
