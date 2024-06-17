from typing import List
from fastapi import Depends, FastAPI, HTTPException, Request, status, Response
from blog import schemas, models  # absolute imports
from blog.database import SessionLocal, engine, get_db
from sqlalchemy.orm import Session
from .hashing import Hash
from .routers import blog

app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(blog.router)

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

@app.post('/create', status_code=status.HTTP_201_CREATED,  tags=['Blogs'])
async def create_item(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

# @app.get('/blog', response_model=List[schemas.ShowBlog],  tags=['Blogs'])
# async def get_all_blogs(db: Session = Depends(get_db)):
#     blogs = db.query(models.Blog).all()
#     return blogs

@app.get('/blog/{id}', status_code=200, response_model=schemas.ShowBlog,  tags=['Blogs'])
async def get_blog(id, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'error': f'Blog with id {id} not found'}
    return blog

@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT,  tags=['Blogs'])
async def delete_blog(id, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'error': f'Blog with id {id} not found'}
    blog.delete(synchronize_session=False)
    db.commit()
    return "Deleted successfully"

@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED,  tags=['Blogs'])
async def update_blog(id, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with {id} not found.")
    blog.update(request.dict())
    db.commit()
    return "Updated successfully"


@app.post('/user', response_model=schemas.ShowUser,  tags=['Users'])
async def create_user(user: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(name=user.name, email=user.email, password=Hash.bcrypt(user.password))
    # new_user = models.User(Request)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

    
@app.get('/user/{id}', response_model=schemas.ShowUser, tags=['Users'])  
async def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, error=f"User  with {id} is not found")
    return user

