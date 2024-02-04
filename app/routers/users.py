from fastapi import Response, status, HTTPException, Depends, APIRouter
from database import models
from schemas import schemas
from controllers import controllers
from database.database import get_db
from sqlalchemy.orm import Session


# Set APIRouter class with URL prefix and swagger docs tag
router = APIRouter(
    prefix = "/users",
    tags = ['Users']
)

# POST Route to create a user
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()

    if not existing_user:
        user.password = controllers.hash(user.password)
        new_user = models.User(**user.model_dump())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    
    # Exception for if user already exists in the database
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User with email: {user.email} already exists.")