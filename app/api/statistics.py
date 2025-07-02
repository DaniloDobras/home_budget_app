from datetime import timedelta, date

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.db import models
from app.db.database import get_db
from app.utils.security import get_current_user

router = APIRouter(prefix="/stats", tags=["statistics"])


@router.get("/{days}")
def get_statistic(
        days: int,
        db: Session = Depends(get_db),
        user: models.User = Depends(get_current_user),
):
    today = date.today()
    from_date = today - timedelta(days=days)

    total_spent = (db.query(func.coalesce(func.sum(models.Bill.amount), 0)).
                   filter(
        models.Bill.user_id == user.id,
        models.Bill.date >= from_date,
        models.Bill.date <= today,
        models.Bill.amount > 0
    ).scalar())

    count_over_100 = db.query(func.count()).filter(
        models.Bill.user_id == user.id,
        models.Bill.date >= from_date,
        models.Bill.date <= today,
        models.Bill.amount > 100
    ).scalar()

    return {
        "total_spent_last_month": total_spent,
        "count_bills_over_100": count_over_100
    }
