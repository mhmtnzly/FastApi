from typing import Optional
from fastapi import FastAPI, Request, Header, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from .database import models
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
templates = Jinja2Templates(directory='app/templates')


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
def startup_populate_db():
    db = SessionLocal()
    num_films = db.query(models.Film).count()
    if num_films == 0:
        films = [
            {
                "name": "Blade Runner1",
                "director": "Ridley Scott"
            },
            {
                "name": "Blade Runner2",
                "director": "Ridley Scott"
            },
            {
                "name": "Blade Runner3",
                "director": "Ridley Scott"
            },
            {
                "name": "Blade Runner4",
                "director": "Ridley Scott"
            }
        ]
        for film in films:
            db.add(models.Film(**film))
        db.commit()
    else:
        print(f"{num_films} films already in db")


@app.get("/index/", response_class=HTMLResponse)
async def movielist(request: Request,
                    hx_request: Optional[str] = Header(None),
                    db: Session = Depends(get_db),
                    page: int = 1):
    N = 2
    OFFSET = (page - 1) * N
    films = db.query(models.Film).offset(OFFSET).limit(N)
    context = {"request": request, 'films': films, "page": page}
    if hx_request:
        return templates.TemplateResponse("partials/table.html", context)
    return templates.TemplateResponse("index.html", context)
