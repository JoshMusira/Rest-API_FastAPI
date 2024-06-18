from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request, status, Response
from sqlalchemy.orm import Session
from ..repository import blog
from .. import models, schemas, database

get_db = database.get_db

router = APIRouter(
    tags=['Blogs'],
    prefix='/blog'
)

@router.get('/all', response_model=List[schemas.ShowBlog])
async def get_all_blogs(db: Session = Depends(get_db)):
    return blog.getAll(db)


@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create_item(request: schemas.Blog, db: Session = Depends(get_db), current_user: schemas.User=Depends(get_db)):
    return blog.create(request, db)

@router.delete('/delete/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_blog(id, response: Response, db: Session = Depends(get_db)):
    return  blog.destroy(id, db)

@router.get('/single/{id}', status_code=200, response_model=schemas.ShowBlog)
async def get_blog(id, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'error': f'Blog with id {id} not found'}
    return blog

    


@router.put('/update/{id}', status_code=status.HTTP_202_ACCEPTED)
async def update_blog(id, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with {id} not found.")
    blog.update(request.dict())
    db.commit()
    return "Updated successfully"
