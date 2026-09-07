from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models, schemas
from ..oauth2 import get_current_user


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


# GET ALL POSTS
@router.get("/", response_model=list[schemas.PostOut])
def get_posts(
    db: Session = Depends(get_db),
    limit: int = 10,
    skip: int = 0,
    search: str | None = None
):
    query = db.query(models.Post)

    if search:
        query = query.filter(
            models.Post.title.ilike(f"%{search}%")
        )

    posts = (
        query
        .order_by(models.Post.id.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    return posts


# GET MY POSTS
# IMPORTANT: This must come BEFORE /{post_id}
@router.get("/mine", response_model=list[schemas.PostOut])
def get_my_posts(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    posts = (
        db.query(models.Post)
        .filter(models.Post.owner_id == current_user.id)
        .all()
    )

    return posts


# GET ONE POST
@router.get("/{post_id}", response_model=schemas.PostOut)
def get_post(
    post_id: int,
    db: Session = Depends(get_db)
):
    post = (
        db.query(models.Post)
        .filter(models.Post.id == post_id)
        .first()
    )

    if post is None:
        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )

    return post


# CREATE POST
@router.post(
    "/",
    response_model=schemas.PostOut,
    status_code=status.HTTP_201_CREATED
)
def create_post(
    post_in: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    post = models.Post(
        **post_in.model_dump(),
        owner_id=current_user.id
    )

    db.add(post)
    db.commit()
    db.refresh(post)

    return post


# UPDATE POST
@router.put("/{post_id}", response_model=schemas.PostOut)
def update_post(
    post_id: int,
    post_in: schemas.PostUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    post = (
        db.query(models.Post)
        .filter(models.Post.id == post_id)
        .first()
    )

    if post is None:
        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )

    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to update this post"
        )

    for key, value in post_in.model_dump().items():
        setattr(post, key, value)

    db.commit()
    db.refresh(post)

    return post


# DELETE POST
@router.delete(
    "/{post_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    post = (
        db.query(models.Post)
        .filter(models.Post.id == post_id)
        .first()
    )

    if post is None:
        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )

    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to delete this post"
        )

    db.delete(post)
    db.commit()

    return None