from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    TIMESTAMP,
    Text,
    text,
)

from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        nullable=False
    )

    email = Column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )

    password = Column(
        String(255),
        nullable=False
    )

    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()")
    )

    posts = relationship(
        "Post",
        back_populates="owner",
        cascade="all, delete-orphan"
    )

    votes = relationship(
        "Vote",
        back_populates="user",
        cascade="all, delete-orphan"
    )


class Post(Base):
    __tablename__ = "posts"

    id = Column(
        Integer,
        primary_key=True,
        nullable=False
    )

    title = Column(
        String(100),
        nullable=False
    )

    content = Column(
        Text,
        nullable=False
    )

    published = Column(
        Boolean,
        nullable=False,
        server_default="true"
    )

    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()")
    )

    owner_id = Column(
        Integer,
        ForeignKey(
            "users.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    owner = relationship(
        "User",
        back_populates="posts"
    )

    votes = relationship(
        "Vote",
        back_populates="post",
        cascade="all, delete-orphan"
    )


class Vote(Base):
    __tablename__ = "votes"

    user_id = Column(
        Integer,
        ForeignKey(
            "users.id",
            ondelete="CASCADE"
        ),
        primary_key=True
    )

    post_id = Column(
        Integer,
        ForeignKey(
            "posts.id",
            ondelete="CASCADE"
        ),
        primary_key=True
    )

    user = relationship(
        "User",
        back_populates="votes"
    )

    post = relationship(
        "Post",
        back_populates="votes"
    )