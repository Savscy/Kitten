from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Строка подключения к PostgreSQL
DATABASE_URL = "postgresql://postgres:1990@localhost:5432/kittens_db"  # Убедитесь, что эта строка верная

engine = create_engine(DATABASE_URL)  # Удалите connect_args={"check_same_thread": False}
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создание базового класса для моделей
Base = declarative_base()

# Функция для создания таблиц
def create_tables():
    Base.metadata.create_all(bind=engine)

# Функция для получения сессии
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()





