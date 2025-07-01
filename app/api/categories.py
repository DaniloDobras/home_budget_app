from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.schema.category_schema import CategoryRequest, CategoryResponse
from app.db import models
from app.db.database import get_db
from app.utils.security import get_current_user

router = APIRouter(prefix="/categories", tags=["categories"])


@router.post("/", response_model=CategoryResponse)
def create_category(
        category: CategoryRequest,
        db: Session = Depends(get_db),
        user: models.User = Depends(get_current_user)
):
    new_category = models.Category(name=category.name, user_id=user.id)
    db.add(new_category)
    db.commit()
    return new_category


@router.get("/", response_model=list[CategoryResponse])
def get_all_categories(
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    categories = db.query(models.Category).filter_by(user_id=user.id).all()
    return categories


@router.get("/id/{category_id}", response_model=CategoryResponse)
def get_category_by_id(
    category_id: int,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    category = db.query(models.Category).filter_by(
        id=category_id,
        user_id=user.id
    ).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.get("/name/{name}", response_model=CategoryResponse)
def get_category_by_name(
    name: str,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    category = db.query(models.Category).filter_by(
        name=name,
        user_id=user.id
    ).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    updated: CategoryRequest,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    category = db.query(models.Category).filter_by(
        id=category_id,
        user_id=user.id
    ).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    category.name = updated.name
    db.commit()
    db.refresh(category)
    return category


@router.delete("/{category_id}",
               response_model=CategoryResponse
               )
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    category = db.query(models.Category).filter_by(
        id=category_id,
        user_id=user.id
    ).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(category)
    db.commit()
    return category
