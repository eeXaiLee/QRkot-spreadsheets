# QRKot — Благотворительный фонд поддержки котиков

QRKot — API-сервис для благотворительного фонда, позволяющий создавать целевые проекты для помощи котикам и принимать персонализированные пожертвования от зарегистрированных пользователей.

Проект является учебным и выполнен в рамках Яндекс.Практикума.

---

## Используемые технологии

- Python 3.12+
- FastAPI - веб-фреймворк
- FastAPI Users - система аутентификации
- SQLAlchemy - ORM для работы с базой данных
- Pydantic - валидация данных
- Alembic - миграции базы данных
- SQLite - база данных (разработка)
- Uvicorn - ASGI сервер
- Dependency Injector - внедрение зависимостей
- Pytest - тестирование
- Google Sheets API - формирование отчётов
- aiogoogle - асинхронный клиент для Google API

---

## Установка и локальный запуск

### 1. Клонирование репозитория

```bash
git clone <repository-url>
cd cat-charity-2
```

### 2. Виртуальное окружение

```bash
python -m venv venv
source venv/bin/activate  # Linux / MacOS
source venv/Scripts/activate   # Windows
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt  # Основная команда
make install  # Альтернатива через Makefile
```

### 4. Переменные окружения

Создайте файл `.env` в корне проекта:

```env
QRKOT_APP_TITLE=Название проекта
QRKOT_DESCRIPTION=Описание проекта
QRKOT_DATABASE_URL=sqlite+aiosqlite:///./fastapi.db
QRKOT_SECRET_KEY=Секретный ключ

QRKOT_TYPE=service_account
QRKOT_PROJECT_ID=your-project-id
QRKOT_PRIVATE_KEY_ID=your-private-key-id
QRKOT_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nYour private key here\n-----END PRIVATE KEY-----\n"
QRKOT_CLIENT_EMAIL=your-service-account@your-project.iam.gserviceaccount.com
QRKOT_CLIENT_ID=your-client-id
QRKOT_AUTH_URI=https://accounts.google.com/o/oauth2/auth
QRKOT_TOKEN_URI=https://oauth2.googleapis.com/token
QRKOT_AUTH_PROVIDER_X509_CERT_URL=https://www.googleapis.com/oauth2/v1/certs
QRKOT_CLIENT_X509_CERT_URL=https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40your-project.iam.gserviceaccount.com
QRKOT_EMAIL=Ваш личный email для доступа к таблице
```

### 5. Запуск приложения

```bash
uvicorn app.main:app --reload  # Основная команда
make run  # Альтернатива через Makefile
```

Сервер будет доступен по адресу:

```
http://127.0.0.1:8000
```
---

## Интеграция с Google Sheets

Проект поддерживает формирование отчётов в Google таблицах. Для использования этой функциональности необходимо настроить доступ к Google API.

### Настройка Google API

1. Перейдите в [Google Cloud Console](https://console.cloud.google.com/)

2. Создайте новый проект или выберите существующий

3. Включите необходимые API:
   - **Google Sheets API**
   - **Google Drive API**

4. Создайте сервисный аккаунт и скачайте JSON-ключ

5. Скопируйте данные из JSON в соответствующие переменные **.env**

6. Укажите свой личный email в переменной **QRKOT_EMAIL** для доступа к создаваемым таблицам

---

## Команды Makefile

Для удобства используется `Makefile` с командами:

```bash
# Установка зависимостей
make install

# Запуск сервера разработки
make run

# Запуск тестов
make test

# Проверка стиля кода
make lint

# Автоматическое исправление стиля кода
make fix

# Полная проверка (линтер + тесты)
make check

# Миграции базы данных
make migrate           # Создать миграцию с вводом сообщения
make migrate-auto     # Автоматическая миграция
make migrate-up       # Применить все миграции
make migrate-down     # Откатить последнюю миграцию
make migrate-status   # Показать текущую версию
make migrate-history  # Показать историю миграций
```

---

## Документация API (OpenAPI)

После запуска приложения:

- Swagger UI:  
  http://127.0.0.1:8000/docs
- ReDoc:  
  http://127.0.0.1:8000/redoc

---

## Права доступа

### Анонимный пользователь
- Просмотр списка проектов (`GET /charity_project/`)
- Регистрация (`POST /auth/register`)

### Зарегистрированный пользователь
- Просмотр списка проектов
- Создание пожертвований (`POST /donation/`)
- Просмотр своих пожертвований (`GET /donation/my`)
- Просмотр/обновление профиля (`GET/PATCH /users/me`)

### Суперпользователь
- Все права зарегистрированного пользователя
- Создание проектов (`POST /charity_project/`)
- Редактирование проектов (`PATCH /charity_project/{id}`)
- Удаление проектов без инвестиций (`DELETE /charity_project/{id}`)
- Просмотр всех пожертвований (`GET /donation/`)
- Управление другими пользователями (`GET/PATCH /users/{id}`)
- Формирование отчётов в Google Sheets (`POST /google/`)

---

## Основные эндпоинты

### Благотворительные проекты
- `GET /charity_project/` — получить все проекты
- `POST /charity_project/` — создать новый проект *(только суперпользователь)*
- `PATCH /charity_project/{id}` — обновить проект *(только суперпользователь)*
- `DELETE /charity_project/{id}` — удалить проект *(только суперпользователь)*

### Пожертвования
- `GET /donation/` — получить все пожертвования *(только суперпользователь)*
- `POST /donation/` — создать новое пожертвование *(зарегистрированные пользователи)*
- `GET /donation/my` — получить свои пожертвования *(зарегистрированные пользователи)*

### Пользователи
- `POST /auth/jwt/login` — авторизация
- `POST /auth/jwt/logout` — выход
- `POST /auth/register` — регистрация
- `GET /users/me` — получить свой профиль
- `PATCH /users/me` — обновить свой профиль
- `GET /users/{id}` — получить пользователя *(только суперпользователь)*
- `PATCH /users/{id}` — обновить пользователя *(только суперпользователь)*

### Google Отчёты
- `POST /google/` — сформировать Google таблицу с отчётом по закрытым проектам *(только суперпользователь)*
  
  **Что делает эндпоинт:**
  1. Собирает все закрытые проекты (где `fully_invested = True`)
  2. Сортирует их по скорости сбора средств (от самых быстрых к медленным)
  3. Создаёт новую Google таблицу на диске сервисного аккаунта
  4. Выдаёт права на редактирование личному аккаунту (из переменной `EMAIL` в `.env`)
  5. Заполняет таблицу данными в формате:
     
     | Отчет от | 2024/01/15 14:30:00 |
     |----------|---------------------|
     | **Топ проектов по скорости закрытия** | |
     | **Название проекта** | **Время сбора** | **Описание** |
     | Проект А | 2 days, 3:45:12.345678 | Описание проекта А |
     | Проект Б | 5 days, 0:12:30.123456 | Описание проекта Б |
  
  6. Возвращает ID созданной таблицы и подтверждение

---

## Структура проекта

```
cat-charity-2/
├── app/
│ ├── api/
│ │ ├── endpoints/
│ │ │ ├── charity_project.py
│ │ │ ├── donation.py
│ │ │ ├── google_api.py
│ │ │ └── user.py
│ │ ├── routers.py # Маршрутизация
│ │ └── validators.py # Валидаторы
│ ├── containers.py # DI контейнер
│ ├── core/
│ │ ├── base.py # Базовые модели
│ │ ├── config.py # Конфигурация
│ │ ├── db.py # База данных
│ │ ├── google_client.py # Клиент для Google API
│ │ └── user.py # Настройка пользователей
│ ├── models/
│ │ ├── base.py # Базовые классы
│ │ ├── charity_project.py
│ │ ├── donation.py
│ │ └── user.py
│ ├── repositories/
│ │ ├── base.py # Базовый репозиторий
│ │ ├── base_investment.py # Репозиторий для инвестиций
│ │ ├── charity_project.py
│ │ ├── donation.py
│ │ └── google_report.py
│ ├── schemas/
│ │ ├── charity_project.py
│ │ ├── donation.py
│ │ └── user.py
│ ├── services/
│ │ ├── charity_project.py
│ │ ├── google_api.py
│ │ └── investment.py # Распределение инвестиций
│ └── main.py # Точка входа
├── alembic/ # Миграции базы
├── tests/ # Тесты
├── requirements.txt # Зависимости
└── Makefile # Автоматизация команд
```

---

## Валидация и ограничения

### Проекты
- **Название**: 5–100 символов, уникальное
- **Описание**: минимум 10 символов
- **Целевая сумма**: положительное целое число
- Нельзя редактировать закрытые проекты
- Нельзя удалить проект с инвестициями
- Нельзя установить сумму меньше уже вложенной

### Пожертвования
- **Сумма**: положительное целое число
- **Комментарий**: необязательный
- **Привязка к пользователю**: обязательно

### Пользователи
- **Email**: уникальный, валидный формат
- **Пароль**: минимум 3 символа
- Нельзя удалять пользователей через API

---

## Тестирование

```bash
pytest
```

---

## Лицензия

MIT
