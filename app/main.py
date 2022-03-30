# pip install "python-jose[cryptography]"
# to get a string like this run:
# openssl rand -hex 32
# pip install fastapi
# pip install SQLAlchemy==1.4.27
# pip install "python-jose[cryptography]" # For JWT token
# pip install "passlib[bcrypt]" # for password encription
# pip install python-multipart

from fastapi import FastAPI
from random import randrange

from .routers import vote
from . import models
from .database import engine
from . routers import post, user, auth
from .config import Settings
from fastapi.middleware.cors import CORSMiddleware

# If alembic, don't required
# models.Base.metadata.create_all(bind=engine)
app = FastAPI()

# Allow domins talk to us
origins = [
    "http://localhost.tiangolo.com",
    "https://www.google.com",
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:8000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], # "*" means all
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message": "Hello World pushing out to ubuntu"}

