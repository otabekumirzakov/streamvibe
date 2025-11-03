from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import database
from models.wishlist import Wishlist
from models.users import Users
from utils.auth import get_current_user
from sqlalchemy import func

wishlist_router = APIRouter()

@wishlist_router.post("/add")
def add_wishlist(film_id: int, db: Session = Depends(database),
                    current_user: Users = Depends(get_current_user)):
    film = db.query(Wishlist).filter(Wishlist.film_id == film_id).first()
    if film:
        db.delete(film)
        db.commit()
        raise HTTPException(200, "Film removed from wish list successfully!!!")

    wishlist = Wishlist(
        user_id=current_user.id,
        film_id=film_id
    )

    db.add(wishlist)
    db.commit()
    raise HTTPException(201, "Wishlist add successful !!!")


@wishlist_router.get("/get")
def get_wishlist(db: Session = Depends(database),
                    current_user: Users = Depends(get_current_user)):
    wishlist = db.query(Wishlist).filter(Wishlist.user_id == current_user.id).all()
    return wishlist


@wishlist_router.get('/most_likes')
def get_most_likes(db: Session = Depends(database)):
    film_wishlist_count = db.query(
        Wishlist.film_id,
        func.count(Wishlist.id).label('like_count')
    ).group_by(Wishlist.film_id).subquery()

    most_liked_films = db.query(Films, film_wishlist_count.c.like_count).join(
        film_wishlist_count,
        Films.id == film_wishlist_count.c.film_id
    ).order_by(film_wishlist_count.c.like_count.desc()).all()

    result = [
        {
            "film": {
                "id": film.id,
                "title": film.title,
                "description": film.description,
                "year": film.year,
                "languages": film.languages,
                "genres": film.genres,
                "view": film.view,
                "video_url": film.video_url
            },
            "like_count": like_count
        }
        for film, like_count in most_liked_films
    ]

    return result