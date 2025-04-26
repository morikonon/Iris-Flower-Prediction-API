# Iris Flower Prediction API 🌸

Этот проект — простой API для предсказания вида ириса с помощью модели машинного обучения.

## О проекте
- Обучение модели (Logistic Regression) на датасете Iris.
- Разработка API на FastAPI.
- Веб-интерфейс на HTML, CSS, JavaScript.
- Предсказания вида цветка на основе введённых параметров.

## Как запустить проект

1. Клонировать репозиторий:

https://github.com/твоя-ссылка.git


2. Установить зависимости:

pip install -r requirements.txt


3. Запустить сервер:

uvicorn app.main:app --reload


4. Перейти в браузере на:

http://127.0.0.1:8000


## Структура проекта

- `app/main.py` — код API
- `app/templates/index.html` — шаблон
- `app/static/` — стили и скрипты
- `final_model.joblib` — обученная модель
- `iris.ipynb` — ноутбук для обучения модели

---
