# project/models.py
from sqlalchemy import Column, Integer, String
from .database import Base, engine

class Kittens(Base):
    __tablename__ = "kittens"
    id = Column(Integer, primary_key=True, index=True)
    color = Column(String)
    age = Column(Integer)
    description = Column(String)
    breed = Column(String)  # Поле для породы


# Создание таблиц в базе данных (если еще не созданы)
def create_tables():
    Base.metadata.create_all(bind=engine)  # Используем движок для создания таблиц

create_tables()  # Вызов функции для создания таблиц





