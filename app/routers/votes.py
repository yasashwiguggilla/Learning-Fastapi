from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from sqlalchemy.orm import Session

from ..database import get_db
from .. import models, schemas

from ..oauth2 import get_current_user


router = APIRouter(
    prefix="/vote",
    tags=["Votes"]
)


@router.post("/")
def vote(
    vote_in: schemas.VoteCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(
        get_current_user
    ),
):

    if vote_in.dir not in (0, 1):
        raise HTTPException(
            status_code=422,
            detail="dir must be 0 or 1"
        )

    post = (
        db.query(models.Post)
        .filter(
            models.Post.id
            == vote_in.post_id
        )
        .first()
    )

    if post is None:
        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )

    existing = (
        db.query(models.Vote)
        .filter(
            models.Vote.post_id
            == vote_in.post_id,
            models.Vote.user_id
            == current_user.id,
        )
        .first()
    )

    if vote_in.dir == 1:

        if existing:
            raise HTTPException(
                status_code=409,
                detail="User has already voted on this post"
            )

        db.add(
            models.Vote(
                post_id=vote_in.post_id,
                user_id=current_user.id,
            )
        )

        db.commit()

        return {
            "message": "Post voted successfully"
        }

    if not existing:
        raise HTTPException(
            status_code=404,
            detail="Vote does not exist"
        )

    db.delete(existing)
    db.commit()

    return {
        "message": "Vote removed successfully"
    }