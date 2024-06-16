from fastapi import FastAPI
from . import schemas


app = FastAPI()


@app.post('/create')
async def create_item(request: schemas.Blog):
    return {"data": "Blog Created"}