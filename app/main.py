from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from .routers import (
    auth,
    posts,
    users,
    votes,
)





app = FastAPI(
    title="Social Posts API",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(votes.router)


@app.get("/")
def root():
    return {
        "message": "Welcome to the Social Posts API"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }