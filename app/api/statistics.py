from datetime import timedelta, datetime

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
    now = datetime.utcnow()
    from_date = now - timedelta(days=days)

    total_spent = (db.query(func.coalesce(func.sum(models.Bill.amount), 0)).
                   filter(
        models.Bill.user_id == user.id,
        models.Bill.date >= from_date,
        models.Bill.date <= now,
        models.Bill.amount > 0,
        models.Bill.top_up == False
    ).scalar())

    total_earned = (db.query(func.coalesce(func.sum(models.Bill.amount), 0)).
                    filter(
        models.Bill.user_id == user.id,
        models.Bill.date >= from_date,
        models.Bill.date <= now,
        models.Bill.top_up == True
    ).scalar())

    count_over_100 = db.query(func.count()).filter(
        models.Bill.user_id == user.id,
        models.Bill.date >= from_date,
        models.Bill.date <= now,
        models.Bill.amount > 100
    ).scalar()

    return {
        f"total_spent_in_{days}": total_spent,
        f"total_earned_in_{days}": total_earned,
        "count_bills_over_100": count_over_100
    }
