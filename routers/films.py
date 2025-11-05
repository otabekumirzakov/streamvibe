from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import database
from models.films import Films
from models.users import Users
from schemas.films import FilmsModel
from utils.auth import get_current_user

film_router = APIRouter()


@film_router.post("/add")
def add_film(form: FilmsModel, db: Session = Depends(database),
                current_user: Users = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(400, 'You are not admin')
    film = Films(
        title=form.title,
        description=form.description,
        video_url=form.video_url,
        year=form.year,
        languages=form.languages,
        genres=form.genres,
        view=0
    )
    db.add(film)
    db.commit()
    raise HTTPException(201, "Film add successful !!!")

@film_router.get("/films")
def get_films(title: str = None, film_id: int = None,  db: Session = Depends(database)):
    if film_id:
        film = db.query(Films).filter(Films.id == film_id).all()
        if not film:
            raise HTTPException(status_code=404, detail="Film topilmadi")
        film.view += 1
        db.commit()
        db.refresh(film)
        return film

    if title:
        films = db.query(Films).filter(Films.title.contains(title)).all()
    else:
        films = db.query(Films).all()
    return films


@film_router.get("/most-viewed")
def get_most_viewed_film(db: Session = Depends(database)):
    film = db.query(Films).order_by(Films.view.desc()).first()
    return film


@film_router.get("/get_last")
def get_last_films(db: Session = Depends(database)):
    films = db.query(Films).order_by(Films.id.desc()).all()
    return films


@film_router.put("/update")
def update_film(ident: int, form: FilmsModel, db: Session = Depends(database),
                current_user: Users = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(400, 'You are not admin')
    film = db.query(Films).filter(Films.id == ident).first()
    if not film:
        raise HTTPException(404, 'Film not found')
    film.title = form.title
    film.description = form.description
    film.video_url = form.video_url
    film.year = form.year
    film.languages = form.languages
    film.genres = form.genres
    db.commit()
    raise HTTPException(200, "Film update successful !!!")


@film_router.delete("/delete")
def delete_film(ident: int, db: Session = Depends(database),
                current_user: Users = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(400, 'You are not admin')
    film = db.query(Films).filter(Films.id == ident).first()
    if not film:
        raise HTTPException(404, 'Film not found')
    db.delete(film)
    db.commit()
    return {"message": "Film deleted successfully"}