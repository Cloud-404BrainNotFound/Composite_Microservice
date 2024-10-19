from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.user import User
from app.database import get_db

user_router = APIRouter()


@user_router.get("/first_user")
def get_first_user_id(db: Session = Depends(get_db)):
    first_user = db.query(User).first()

    if not first_user:
        raise HTTPException(status_code=404, detail="No user found")
    return {"id": first_user.id}
