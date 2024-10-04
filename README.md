 Описание запуска приложения 
# Котенок API
1. **Клонируйте репозиторий**:
   ```bash
   git clone https://github.com/Savscy/Kitten.git
   cd Kitten
2. Создайте и активируйте виртуальное окружение:
python -m venv venv
source venv/bin/activate  # Для Linux/Mac
venv\Scripts\activate     # Для Windows

Установите зависимости:
pip install -r requirements.txt
Запустите приложение:
uvicorn main:app --reload
Доступ к Swagger документации: После запуска приложения перейдите по следующему URL в вашем браузере:
http://127.0.0.1:8000/docs


### 2. Документация в формате Swagger

FastAPI автоматически создает документацию Swagger для вашего API. Все, что вам нужно сделать, это запустить ваше приложение, и вы сможете получить доступ к документации, перейдя по адресу `/docs`.

### 3. Минимум данных для проверки работоспособности

Вы можете использовать следующий пример данных для проверки работоспособности вашего API. Добавьте в код метод `create_kitten`, который позволяет добавлять котят в базу данных:

```python
@app.post("/kittens/", response_model=KittenRead, status_code=201)
def create_kitten(kitten: KittenCreate, db: Session = Depends(get_db)):
    db_kitten = Kittens(**kitten.dict())  # Используйте kitten.dict() для передачи данных
    db.add(db_kitten)
    db.commit()
    db.refresh(db_kitten)
    return db_kitten

Вы можете протестировать API с помощью таких данных:
{
    "color": "gray",
    "age": 2,
    "description": "Grown gray kitten",
    "breed": "Siamese"
}

Пример использования Postman или cURL для добавления котенка

curl -X POST "http://127.0.0.1:8000/kittens/" -H "Content-Type: application/json" -d '{"color": "gray", "age": 2, "description": "Grown gray kitten", "breed": "Siamese"}'
