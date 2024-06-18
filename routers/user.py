from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..hashing import Hash

from .. import models, schemas, database

get_db = database.get_db

router = APIRouter(
        tags=['Users'],
        prefix='/auth'
)


@router.post('/signup', response_model=schemas.ShowUser)
async def create_user(user: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(name=user.name, email=user.email, password=Hash.bcrypt(user.password))
    # new_user = models.User(Request)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

    
@router.get('/bgId/{id}', response_model=schemas.ShowUser)  
async def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, error=f"User  with {id} is not found")
    return user
