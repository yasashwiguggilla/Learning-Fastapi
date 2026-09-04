from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from fastapi.security import (
    OAuth2PasswordRequestForm,
)

from sqlalchemy.orm import Session

from ..database import get_db
from .. import models, schemas

from ..oauth2 import (
    create_access_token,
    get_current_user,
)

from ..utils import verify_password


router = APIRouter(
    tags=["Authentication"]
)


@router.post(
    "/login",
    response_model=schemas.Token
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    user = (
        db.query(models.User)
        .filter(
            models.User.email
            == form_data.username
        )
        .first()
    )

    if (
        user is None
        or not verify_password(
            form_data.password,
            user.password
        )
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid credentials"
        )

    token = create_access_token({
        "user_id": str(user.id)
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@router.get(
    "/me",
    response_model=schemas.UserOut
)
def me(
    current_user: models.User = Depends(
        get_current_user
    )
):
    return current_user