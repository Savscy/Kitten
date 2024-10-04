from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from project.database import Base, get_db
from project.main import app



# Установка тестовой базы данных
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создаем таблицы в тестовой БД перед запуском тестов
Base.metadata.drop_all(bind=engine)  # Удаляем старые таблицы
Base.metadata.create_all(bind=engine)  # Создаем новые таблицы

# Клиент для тестирования
client = TestClient(app)

# Заменяем зависимость get_db на использование тестовой БД
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Тесты
def test_create_kitten():
    kitten_data = {
        "color": "black",
        "age": 2,
        "description": "Cute little kitten",
        "breed": "Siamese"  # Убедитесь, что breed присутствует
    }
    response = client.post("/kittens/", json=kitten_data)

    assert response.status_code == 201
    data = response.json()
    assert data["color"] == "black"
    assert data["age"] == 2
    assert data["description"] == "Cute little kitten"
    assert data["breed"] == "Siamese"  # Убедитесь, что breed присутствует
    assert "id" in data  # Проверьте, что id присутствует

def test_read_item():
    response = client.get("/items/1")
    assert response.status_code == 200
    assert response.json() == {"item_id": 1}

def test_get_kitten_by_id():
    # Сначала добавим котенка
    create_response = client.post(
        "/kittens/",
        json={
            "color": "white",
            "age": 2,
            "description": "Cute white kitten",
            "breed": "Siamese"  # Убедитесь, что breed присутствует
        }
    )
    assert create_response.status_code == 201
    kitten_id = create_response.json()["id"]

    # Теперь проверим его получение по ID
    response = client.get(f"/kittens/{kitten_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == kitten_id
    assert data["color"] == "white"
    assert data["age"] == 2
    assert data["description"] == "Cute white kitten"
    assert data["breed"] == "Siamese"  # Убедитесь, что breed присутствует


def test_update_kitten():
    # Сначала добавим котенка
    create_response = client.post(
        "/kittens/",
        json={
            "color": "gray",
            "age": 1,
            "description": "Cute gray kitten",
            "breed": "Persian"  # Добавьте breed
        }
    )
    assert create_response.status_code == 201
    kitten_id = create_response.json()["id"]

    # Теперь обновим его
    update_response = client.put(
        f"/kittens/{kitten_id}",
        json={
            "color": "gray",
            "age": 2,
            "description": "Grown gray kitten",
            "breed": "Persian"  # Обязательно передайте все поля
        }
    )
    assert update_response.status_code == 200
    data = update_response.json()
    assert data["id"] == kitten_id
    assert data["color"] == "gray"
    assert data["age"] == 2
    assert data["description"] == "Grown gray kitten"
    assert data["breed"] == "Persian"  # Проверьте breed


def test_delete_kitten():
    create_response = client.post(
        "/kittens/",
        json={"color": "orange", "age": 1, "description": "Cute orange kitten", "breed": "Persian"}
    )
    assert create_response.status_code == 201
    kitten_id = create_response.json()["id"]

    delete_response = client.delete(f"/kittens/{kitten_id}")
    assert delete_response.status_code == 204

    get_response = client.get(f"/kittens/{kitten_id}")
    assert get_response.status_code == 404

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

