
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

from sqlalchemy.orm import Session
from . import models
from .database import engine, SessionLocal


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -----------------------------
# Post Model
# -----------------------------

class Post(BaseModel):
    title: str
    content: str
    published: bool = True


# -----------------------------
# Database Connection
# -----------------------------

while True:

    try:
        connection = psycopg2.connect(
            host="localhost",
            database="fastapi",
            user="postgres",
            password="yashu@2005",
            cursor_factory=RealDictCursor
        )

        cursor = connection.cursor()

        print("Database connection was successful")

        # Check database and schema
        cursor.execute("""
            SELECT current_database(), current_schema()
        """)

        print("Database info:", cursor.fetchone())

        # Check posts table columns
        cursor.execute("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_schema = 'public'
            AND table_name = 'posts'
            ORDER BY ordinal_position
        """)

        print("Posts columns:", cursor.fetchall())

        break

    except Exception as error:
        print("Connecting to database failed")
        print("Error:", error)

        time.sleep(2)


# -----------------------------
# Temporary Posts Data
# -----------------------------

my_posts = [
    {
        "title": "title of post 1",
        "content": "content of post 1",
        "id": 1
    },
    {
        "title": "favorite foods",
        "content": "I like pizza",
        "id": 2
    }
]


# -----------------------------
# Find Post
# -----------------------------

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p


# -----------------------------
# Find Post Index
# -----------------------------

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i


# -----------------------------
# Root
# -----------------------------

@app.get("/")
def root():
    return {"message": "Hello World"}


# -----------------------------
# SQLAlchemy Test
# -----------------------------

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    return {"status": "success"}


# -----------------------------
# Get All Posts
# -----------------------------

@app.get("/posts")
def get_posts():

    cursor.execute("""
        SELECT *
        FROM public.posts
    """)

    posts = cursor.fetchall()

    return {"data": posts}


# -----------------------------
# Create Post
# -----------------------------

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):

    try:

        cursor.execute(
            """
            INSERT INTO public.posts
                (title, content, published)
            VALUES
                (%s, %s, %s)
            RETURNING *
            """,
            (
                post.title,
                post.content,
                post.published
            )
        )

        new_post = cursor.fetchone()

        connection.commit()

        return {"data": new_post}

    except Exception as error:

        connection.rollback()

        print("Create post error:", error)

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# -----------------------------
# Get One Post
# -----------------------------

@app.get("/posts/{id}")
def get_post(id: int):

    cursor.execute(
        """
        SELECT *
        FROM public.posts
        WHERE id = %s
        """,
        (id,)
    )

    post = cursor.fetchone()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found"
        )

    return {"data": post}


# -----------------------------
# Delete Post
# -----------------------------

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):

    cursor.execute(
        """
        DELETE FROM public.posts
        WHERE id = %s
        RETURNING *
        """,
        (id,)
    )

    deleted_post = cursor.fetchone()

    connection.commit()

    if deleted_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist"
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# -----------------------------
# Update Post
# -----------------------------

@app.put("/posts/{id}")
def update_post(id: int, post: Post):

    cursor.execute(
        """
        UPDATE public.posts
        SET
            title = %s,
            content = %s,
            published = %s
        WHERE id = %s
        RETURNING *
        """,
        (
            post.title,
            post.content,
            post.published,
            id
        )
    )

    updated_post = cursor.fetchone()

    connection.commit()

    if updated_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist"
        )

    return {"data": updated_post}
