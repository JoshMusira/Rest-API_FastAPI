from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import models, schemas, database


router = APIRouter()

@router.get('/blog', response_model=List[schemas.ShowBlog],  tags=['Blogs'])
async def get_all_blogs(db: Session = Depends(database.get_db)):
    blogs = db.query(models.Blog).all()
    return blogs