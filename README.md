# ЖКП — Backend API

Backend-компонент вебдодатку **«Житлово-комунальні послуги»**.
Реалізований на **FastAPI** (Python) і надає REST API у форматі JSON для роботи
із заявками квартиронаймачів, спеціалістами та бригадами (планом робіт).

## Предметна область

Квартиронаймач надсилає **Заявку** із зазначенням типу робіт (електричні,
сантехнічні, загальні), обсягу робіт та бажаного часу виконання. Диспетчер
формує **Бригаду** з відповідних **Спеціалістів** і реєструє її у **Плані робіт**
(заявка переходить у статус `assigned`).

## Технології та підходи

| Вимога | Реалізація |
| --- | --- |
| Менеджер пакетів | `pip` + `requirements.txt` |
| Routing / Front Controller | FastAPI-додаток (`app/main.py`) з роутерами та route-патернами (`/api/requests/{id}`) |
| MVC | **Model** — ORM-моделі (`app/models`), **Controller** — роутери (`app/controllers`), **View** — відповідь у форматі JSON (Pydantic-схеми `app/schemas`) |
| ORM | SQLAlchemy 2.0 (`app/models`, `app/repositories`) |
| База даних | SQLite за замовчуванням, PostgreSQL через змінну `DATABASE_URL` |
| Міграції схеми | Alembic (`migrations/`) |
| Автентифікація / авторизація | JWT (`app/core/security.py`, `app/controllers/dependencies.py`) |
| Логування | модуль `logging` (`app/core/logging_config.py`) |
| ООП | класи, успадкування, поліморфізм, інкапсуляція (`app/services/domain.py`, `app/repositories`) |
| Unit-тести | `pytest` (`tests/`) |

### ООП

* **Інкапсуляція** — репозиторії та клієнти ховають стан у protected-атрибутах
  (`app/repositories/base.py`).
* **Успадкування** — `TimestampMixin` для моделей, `BaseRepository` для
  репозиторіїв, ієрархія `Person` у `app/services/domain.py`.
* **Поліморфізм** — `Person.role()` перевизначається в кожному підкласі;
  `BrigadeRepository.list()` перевизначає базовий метод.
* **Абстракція** — `Person` є абстрактним класом (`abc.ABC`).

## Структура проєкту

```
backend/
├── app/
│   ├── main.py               # Front controller (FastAPI), реєстрація роутерів
│   ├── core/                 # конфігурація, БД, безпека (JWT), логування
│   ├── models/               # ORM-моделі (SQLAlchemy)
│   ├── schemas/              # Pydantic-схеми (View / валідація)
│   ├── repositories/         # шар доступу до даних (узагальнений + конкретні)
│   ├── services/             # бізнес-логіка + доменні ООП-класи
│   └── controllers/          # HTTP-контролери (роутери) + залежності
├── migrations/               # міграції Alembic
├── tests/                    # unit / integration тести
├── seed.py                   # початкові дані (демо-користувачі)
├── alembic.ini
└── requirements.txt
```

## Запуск

```bash
# 1. Віртуальне середовище та залежності
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 2. (необов'язково) налаштування оточення
cp .env.example .env

# 3. Застосувати міграції та створити демо-дані
alembic upgrade head
python seed.py

# 4. Запустити сервер
uvicorn app.main:app --reload
```

API буде доступне на `http://localhost:8000`, інтерактивна документація — на
`http://localhost:8000/docs`.

### Демо-користувачі (зі `seed.py`)

| Логін | Пароль | Роль |
| --- | --- | --- |
| `dispatcher` | `dispatcher123` | dispatcher |
| `tenant` | `tenant123` | tenant |

## API-ендпоінти

| Метод | Шлях | Доступ |
| --- | --- | --- |
| POST | `/api/auth/register` | публічний |
| POST | `/api/auth/login` | публічний |
| GET | `/api/auth/me` | автентифікований |
| GET | `/api/requests` | автентифікований |
| POST | `/api/requests` | автентифікований |
| PUT/DELETE | `/api/requests/{id}` | dispatcher |
| GET | `/api/specialists` | автентифікований |
| POST/PUT/DELETE | `/api/specialists[/{id}]` | dispatcher |
| GET | `/api/brigades` | автентифікований |
| POST/DELETE | `/api/brigades[/{id}]` | dispatcher |

## Тести

```bash
pytest
```

## Робота з міграціями

```bash
# створити нову міграцію після зміни моделей
alembic revision --autogenerate -m "опис змін"
alembic upgrade head
```
