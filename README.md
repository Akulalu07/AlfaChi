# AlfaChi

Telegram-бот с AI-помощниками для малого бизнеса в России. Проект состоит из FastAPI бэкенда и Telegram бота, использующего различные специализированные AI-помощники.

## Быстрый старт

### Запуск проекта

Необходимо создать переменные окружения (см. ниже)
```bash
docker compose up --build
```

Проект запустит следующие сервисы:
- **Backend** (FastAPI) - на порту `8080`
- **Bot** (Telegram бот) - работает в фоне
- **PostgreSQL** - база данных на порту `5432`

### Доступ к сервисам

- **Backend API**: [http://localhost:8080](http://localhost:8080)
- **API документация**: [http://localhost:8080/docs](http://localhost:8080/docs) (Swagger UI)
- **PostgreSQL**: `localhost:5432`

## Модули проекта

### Backend (`backend/`)

#### 1. Модуль аутентификации (`source/auth/`)
- **Регистрация пользователей** - создание нового пользователя по Telegram ID
- **Управление профилем** - получение и обновление данных пользователя
- **Аутентификация** - проверка пользователя через заголовок `X-Telegram-User-Id`

**API эндпоинты:**
- `POST /auth/register` - регистрация нового пользователя
- `GET /auth/me` - получение информации о текущем пользователе
- `PUT /auth/me` - обновление профиля пользователя

#### 2. Модуль чатов (`source/chat/`)
- **Управление чатами** - создание, получение и удаление чатов
- **Отправка сообщений** - отправка сообщений пользователя и получение ответов от LLM
- **История сообщений** - получение истории переписки

**Типы чатов (0-5):**
- `0` - Юридический помощник
- `1` - Маркетинговый помощник
- `2` - Финансовый помощник
- `3` - HR помощник
- `4` - Помощник по подсказкам и напоминаниям
- `5` - Гайд-помощник

**API эндпоинты:**
- `POST /chats` - создание нового чата
- `GET /chats` - получение списка чатов пользователя
- `GET /chats/{id}` - получение чата с сообщениями
- `DELETE /chats/{id}` - удаление чата
- `POST /chats/messages` - отправка сообщения
- `GET /chats/{id}/messages` - получение сообщений чата

#### 3. Конфигурация (`source/config.py`)
- Настройки подключения к базе данных
- Настройки OpenRouter API
- Модель LLM по умолчанию

### Bot (`bot/`)

#### 1. Обработчики (`source/core/handlers/`)
- Регистрация пользователей через Telegram
- Выбор типа помощника
- Отправка вопросов и получение ответов от AI

#### 2. Сервис бэкенда (`source/services/backend.py`)
- HTTP клиент для взаимодействия с бэкенд API
- Управление сессиями aiohttp

## Используемая LLM

Проект использует **OpenRouter API** для доступа к различным языковым моделям.

### Текущая модель

**Модель по умолчанию:** `deepseek/deepseek-r1-0528-qwen3-8b:free`

Эта модель предоставляется бесплатно через OpenRouter и подходит для различных задач бизнес-помощников.

### Настройки LLM

- **API провайдер:** OpenRouter
- **Base URL:** `https://openrouter.ai/api/v1`
- **Temperature:** `0.3` (для более детерминированных ответов)
- **Timeout:** `60` секунд
- **Максимальная длина ответа:** 3500 символов

## Как изменить LLM

### Способ 1: Изменение модели через переменную окружения

Добавьте переменную окружения `OPEN_ROUTER_MODEL` в `.env` файл:

```env
OPEN_ROUTER_MODEL=anthropic/claude-3.5-sonnet  # Новая модель
```

### Способ 2: Изменение в коде

Отредактируйте файл `backend/source/config.py`:

```python
OPEN_ROUTER_MODEL: str = "your-model-name"  # Например: "openai/gpt-4"
```

### Доступные модели на OpenRouter

Вы можете использовать любую модель, доступную на [OpenRouter](https://openrouter.ai/models). Примеры:

- `openai/gpt-4-turbo` - GPT-4 Turbo от OpenAI
- `anthropic/claude-3.5-sonnet` - Claude 3.5 Sonnet от Anthropic
- `google/gemini-pro-1.5` - Gemini Pro от Google
- `meta-llama/llama-3.1-70b-instruct` - Llama 3.1 от Meta
- `deepseek/deepseek-r1-0528-qwen3-8b:free` - Текущая бесплатная модель

**Важно:** Убедитесь, что у вас достаточно средств на балансе OpenRouter для платных моделей.

## Переменные окружения

### Backend

| Переменная | Описание | Значение по умолчанию | Обязательная |
|------------|----------|----------------------|--------------|
| `OPEN_ROUTER` | API ключ для OpenRouter | - | ✅ Да |
| `OPEN_ROUTER_MODEL` | Название модели LLM | `deepseek/deepseek-r1-0528-qwen3-8b:free` | ❌ Нет |
| `POSTGRES_USER` | Пользователь БД | `postgres` | ❌ Нет |
| `POSTGRES_PASSWORD` | Пароль БД | `password` | ❌ Нет |
| `POSTGRES_DB` | Имя базы данных | `data` | ❌ Нет |

### Bot

| Переменная | Описание | Значение по умолчанию | Обязательная |
|------------|----------|----------------------|--------------|
| `BOT_TOKEN` | Токен Telegram бота от @BotFather | - | ✅ Да |
| `BACKEND_URL` | URL бэкенд API | `http://backend:8080` | ❌ Нет |

### Настройка переменных окружения



Создайте файл `.env` в корне проекта:

```env
# Backend
OPEN_ROUTER=sk-or-v1-your-api-key-here
OPEN_ROUTER_MODEL=your-model-name

# Bot
BOT_TOKEN=your-telegram-bot-token
BACKEND_URL=http://backend:8080

# Database
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your-secret-password
POSTGRES_DB=your-db-name
```

## Структура проекта

```
AlfaChi/
├── backend/              # FastAPI бэкенд
│   ├── source/
│   │   ├── auth/        # Модуль аутентификации
│   │   ├── chat/        # Модуль чатов и LLM
│   │   ├── config.py    # Конфигурация
│   │   ├── database.py  # Настройки БД
│   │   └── main.py      # Точка входа
│   ├── Dockerfile
│   └── requirements.txt
├── bot/                 # Telegram бот
│   ├── source/
│   │   ├── core/
│   │   │   ├── handlers/    # Обработчики команд
│   │   │   ├── keyboards.py # Клавиатуры
│   │   │   ├── states.py    # Состояния FSM
│   │   │   └── utils.py      # Утилиты
│   │   ├── services/
│   │   │   └── backend.py    # Сервис для работы с API
│   │   ├── assets/          # Ресурсы (языки и т.д.)
│   │   ├── main.py          # Точка входа
│   │   └── stuff.py
│   ├── Dockerfile
│   └── requirements.txt
├── docker-compose.yml   # Конфигурация Docker Compose
└── README.md           # Readme файл
```

## Дополнительная информация

### Системные промпты

Каждый тип чата имеет свой специализированный системный промпт:
- Все ответы ограничены 3500 символами
- Ответы не используют Markdown форматирование
- Каждый помощник настроен на конкретную область бизнеса

### База данных

Проект использует **Tortoise ORM** с PostgreSQL. Автоматическая миграция происходит при первом запуске.

**Таблицы:**
- `users` - пользователи
- `chats` - чаты
- `messages` - сообщения

### Безопасность

**Важно для продакшена:**
- Используйте `.env` файлы и добавьте их в `.gitignore`

## Документация API

После запуска проекта документация доступна по адресу:
- Swagger UI: [http://localhost:8080/docs](http://localhost:8080/docs)
