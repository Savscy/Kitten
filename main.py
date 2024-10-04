from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from project.database import SessionLocal, create_tables
from project.schemas import KittenCreate, KittenRead
from project.models import Kittens
from typing import List

app = FastAPI()

@app.on_event("startup")
async def startup():
    create_tables()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/kittens/", response_model=KittenRead, status_code=201)
def create_kitten(kitten: KittenCreate, db: Session = Depends(get_db)):
    db_kitten = Kittens(**kitten.model_dump())
    db.add(db_kitten)
    db.commit()
    db.refresh(db_kitten)
    return db_kitten


@app.get("/kittens", response_model=List[KittenRead])
def read_kittens(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    kittens = db.query(Kittens).offset(skip).limit(limit).all()
    if not kittens:
        raise HTTPException(status_code=404, detail="No kittens found")

    # Фильтрация значений None
    filtered_kittens = [kitten for kitten in kittens if kitten.breed is not None]

    return filtered_kittens


@app.get("/kittens/{kitten_id}", response_model=KittenRead)
def read_kitten(kitten_id: int, db: Session = Depends(get_db)):
    kitten = db.query(Kittens).filter(Kittens.id == kitten_id).first()
    if kitten is None:
        raise HTTPException(status_code=404, detail="Kitten not found")
    return kitten


@app.put("/kittens/{kitten_id}", response_model=KittenRead)
def update_kitten(kitten_id: int, kitten: KittenCreate, db: Session = Depends(get_db)):
    db_kitten = db.query(Kittens).filter(Kittens.id == kitten_id).first()
    if db_kitten is None:
        raise HTTPException(status_code=404, detail="Kitten not found")

    # Обновляем поля котенка
    for key, value in kitten.dict().items():
        setattr(db_kitten, key, value)

    db.commit()
    db.refresh(db_kitten)
    return db_kitten


@app.delete("/kittens/{kitten_id}", status_code=204)
def delete_kitten(kitten_id: int, db: Session = Depends(get_db)):
    db_kitten = db.query(Kittens).filter(Kittens.id == kitten_id).first()
    if db_kitten is None:
        raise HTTPException(status_code=404, detail="Kitten not found")

    db.delete(db_kitten)
    db.commit()

