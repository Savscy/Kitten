from database import SessionLocal
from models import Kittens

def add_kitten(color: str, age: int, description: str):
    session = SessionLocal()
    new_kitten = Kittens(color=color, age=age, description=description)
    session.add(new_kitten)
    session.commit()
    session.refresh(new_kitten)
    session.close()
    return new_kitten


def get_all_kittens():
    session = SessionLocal()
    kittens = session.query(Kittens).all()
    session.close()
    return kittens

def get_kittens_by_breed(breed: str):
    session = SessionLocal()
    kittens = session.query(Kittens).filter(Kittens.breed == breed).all()
    session.close()
    return kittens

