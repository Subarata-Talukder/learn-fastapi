from fastapi import status, HTTPException, APIRouter
from fastapi.params import Depends
from random import randrange
from sqlalchemy.orm.session import Session
from ..database import get_db
from .. import models
from ..schemas import UserResponse, User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
router = APIRouter(
    prefix="/users",
    tags=['Users']
    )

def get_password_hash(password):
    return pwd_context.hash(password)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user:User, db: Session = Depends(get_db)): 
    
    user.password = get_password_hash(user.password)
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user) # Return SQL query result to new_post variable
    
    return new_user

@router.get("/{id}", response_model=UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):

    user_response = db.query(models.User).filter(models.User.id == id).first()

    if not user_response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} was not found")

    return user_response