from fastapi import Depends, FastAPI, HTTPException, status, Response
from . import schemas, models
from .database import SessionLocal, engine
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db

    finally:
        db.close()

@app.post('/create', status_code=status.HTTP_201_CREATED)
async def create_item(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get('/blog')
async def get_all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get('/blog/{id}', status_code=200)
async def get_blog(id, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'error': f'Blog with id {id} not found'}
    
    return blog

@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_blog(id, response: Response, db: Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    db.commit()
    return "Deleted successfull"
    # if not blog:
    #     response.status_code = status.HTTP_404_NOT_FOUND
    #     return {'error': f'Blog with id {id} not found'}
    
@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED)
async def update_blog(id, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, error=f"Blog with {id} not found.")
    blog.update(request)
    db.commit()
    
    return "Updated successfully"
    