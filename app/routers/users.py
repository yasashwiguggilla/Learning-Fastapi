from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from sqlalchemy.orm import Session

from ..database import get_db
from .. import models, schemas
from ..utils import hash_password


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post(
    "/",
    response_model=schemas.UserOut,
    status_code=status.HTTP_201_CREATED
)
def create_user(
    user_in: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    existing = (
        db.query(models.User)
        .filter(
            models.User.email == user_in.email
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Email already registered"
        )

    user = models.User(
        email=user_in.email,
        password=hash_password(
            user_in.password
        )
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@router.get(
    "/{user_id}",
    response_model=schemas.UserOut
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = (
        db.query(models.User)
        .filter(
            models.User.id == user_id
        )
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user