from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import desc, asc
from sqlalchemy.orm import Session

from app.api.schema.bill_schema import BillRequest, BillResponse
from app.db import models
from app.db.database import get_db
from app.utils.security import get_current_user

router = APIRouter(prefix="/bills", tags=["bills"])


@router.post("/", response_model=BillResponse)
def create_bill(
    bill: BillRequest,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    if user.balance < bill.amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    new_bill = models.Bill(
        description=bill.description,
        amount=bill.amount,
        date=bill.date,
        category_id=bill.category_id,
        user_id=user.id
    )

    user.balance -= bill.amount
    db.add(new_bill)
    db.commit()
    db.refresh(new_bill)
    return new_bill


@router.get("/", response_model=list[BillResponse])
def get_all_bills(
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    return db.query(models.Bill).filter_by(user_id=user.id).all()


@router.get("/{bill_id}", response_model=BillResponse)
def get_bill(
    bill_id: int,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    bill = db.query(models.Bill).filter_by(id=bill_id, user_id=user.id).first()
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    return bill


@router.put("/{bill_id}", response_model=BillResponse)
def update_bill(
    bill_id: int,
    updated: BillRequest,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    bill = db.query(models.Bill).filter_by(id=bill_id, user_id=user.id).first()
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")

    balance_diff = updated.amount - bill.amount
    if user.balance < balance_diff:
        raise HTTPException(
            status_code=400,
            detail="Insufficient balance for update"
        )

    bill.description = updated.description
    bill.amount = updated.amount
    bill.date = updated.date
    bill.category_id = updated.category_id

    user.balance -= balance_diff
    db.commit()
    db.refresh(bill)
    return bill


@router.delete("/{bill_id}", response_model=BillResponse)
def delete_bill(
    bill_id: int,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    bill = db.query(models.Bill).filter_by(id=bill_id, user_id=user.id).first()
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")

    user.balance += bill.amount
    db.delete(bill)
    db.commit()
    return bill


@router.get("/by/max", response_model=BillResponse)
def get_max_price_bill(
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    bill = (
        db.query(models.Bill)
        .filter_by(user_id=user.id)
        .order_by(desc(models.Bill.amount))
        .first()
    )
    if not bill:
        raise HTTPException(status_code=404, detail="No bills found")
    return bill


@router.get("/by/min", response_model=BillResponse)
def get_min_price_bill(
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    bill = (
        db.query(models.Bill)
        .filter_by(user_id=user.id)
        .order_by(asc(models.Bill.amount))
        .first()
    )
    if not bill:
        raise HTTPException(status_code=404, detail="No bills found")
    return bill


@router.get("/by/range", response_model=list[BillResponse])
def get_bills_within_range(
    min_price: float = Query(..., ge=0),
    max_price: float = Query(..., ge=0.01),
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    if min_price > max_price:
        raise HTTPException(
            status_code=400,
            detail="min_price cannot be greater than max_price")

    bills = (
        db.query(models.Bill)
        .filter(
            models.Bill.user_id == user.id,
            models.Bill.amount >= min_price,
            models.Bill.amount <= max_price,
        )
        .order_by(models.Bill.amount)
        .all()
    )
    return bills
