from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.orm import Session
from database import database
from models.crew import Crew
from models.users import Users
from save_file import save_file
from utils.auth import get_current_user


crew_router = APIRouter()


@crew_router.post("/add")
def add_crew(full_name:str, role:str, image:UploadFile, db: Session = Depends(database),
                    current_user: Users = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(400, 'You are not admin')
    crew = Crew(
        full_name=full_name,
        role=role,
        image=save_file(image)
    )
    db.add(crew)
    db.commit()
    raise HTTPException(201, "Crew add successful !!!")

@crew_router.get("/get")
def get_myself(db: Session = Depends(database),
                    current_user: Users = Depends(get_current_user)):
    if current_user.role != "admin":
       raise HTTPException(404, "You are not admin")
    crew = db.query(Crew).all()
    return crew


@crew_router.put("/update")
def update_crew(ident: id, full_name:str, role:str, image:UploadFile, db: Session = Depends(database),
                    current_user: Users = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(400, 'You are not admin')
    crew = db.query(Crew).filter(Crew.id == ident).first()
    if not crew:
        raise HTTPException(404, 'Crew not found')
    crew.full_name = full_name
    crew.role = role
    crew.image = save_file(image)
    db.commit()
    raise HTTPException(200, "Crew update successful !!!")

@crew_router.delete("/delete")
def delete_crew(ident: int,db: Session = Depends(database),
                    current_user: Users = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(400, 'You are not admin')
    crew = db.query(Crew).filter(Crew.id == ident).first()
    if not crew:
        raise HTTPException(404, 'Crew not found')
    db.delete(crew)
    db.commit()
    return {"message": "Crew deleted successfully"}