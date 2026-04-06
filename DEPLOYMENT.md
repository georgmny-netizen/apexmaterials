# ApexMaterials Production Backend

FastAPI + PostgreSQL backend для системы управления RFQ (Request for Quotation).

## Возможности бэкенда

### RFQ Management System
Полноценная система управления запросами на котировки с:
- Создание и отслеживание RFQ
- Управление статусами (submitted → in_review → clarification_required → quoted → rejected/closed)
- Полный аудит всех изменений (история статусов)
- Внутренние заметки для команды
- Автоматическая генерация номеров запросов (RFQ-000001, RFQ-000002...)

### API Endpoints

**RFQ Operations:**
- `POST /api/v1/rfqs` - Создать новый RFQ
- `GET /api/v1/rfqs` - Список всех RFQ (фильтр по статусу)
- `GET /api/v1/rfqs/{id}` - Получить конкретный RFQ
- `POST /api/v1/rfqs/{id}/status` - Изменить статус RFQ
- `POST /api/v1/rfqs/{id}/notes` - Добавить внутреннюю заметку
- `GET /api/v1/rfqs/{id}/history` - История изменений статуса

**Health Check:**
- `GET /health` - Проверка работоспособности API

### Модели данных

**RFQ (Request for Quotation):**
```python
{
  "id": "uuid",
  "inquiry_number": "RFQ-000001",
  "company_name": "string",
  "contact_name": "string",
  "email": "email@example.com",
  "material": "Copper ingots",
  "specification": "99.9999% purity, 100kg",
  "notes_from_requester": "Optional notes",
  "status": "submitted",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

**Статусы RFQ:**
- `submitted` - Новый запрос
- `in_review` - На рассмотрении
- `clarification_required` - Требуется уточнение
- `quoted` - Котировка выдана
- `rejected` - Отклонен
- `closed` - Закрыт

## Технологический стек

- **FastAPI 0.115.6** - Веб-фреймворк
- **PostgreSQL** - База данных
- **SQLAlchemy 2.0.36** - ORM
- **Alembic 1.14.0** - Миграции БД
- **Pydantic 2.10.6** - Валидация данных
- **Uvicorn 0.34.0** - ASGI сервер

## Локальная разработка

### 1. Установка зависимостей

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Настройка окружения

```bash
cp .env.example .env
```

Отредактируйте `.env`:
```env
APP_NAME=ApexMaterials RFQ API
ENVIRONMENT=development
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/apexmaterials
API_PREFIX=/api/v1
```

### 3. Запуск PostgreSQL

```bash
docker compose up -d db
```

### 4. Применение миграций

```bash
alembic upgrade head
```

### 5. Запуск API

```bash
uvicorn app.main:app --reload
```

API будет доступен на http://localhost:8000

**Документация API:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Деплой на Render.com

### Способ 1: Через GitHub (рекомендуется)

**Шаг 1: Загрузить код на GitHub**

```bash
git add .
git commit -m "Initial backend commit"
git remote add origin https://github.com/ваш-username/apexmaterials-backend.git
git branch -M main
git push -u origin main
```

**Шаг 2: Создать PostgreSQL базу данных**

1. Зайдите на https://dashboard.render.com
2. Нажмите **"New +"** → **"PostgreSQL"**
3. Настройки:
   - **Name**: `apexmaterials-db`
   - **Database**: `apexmaterials`
   - **User**: `apexmaterials_user`
   - **Region**: выберите ближайший
   - **Plan**: Free
4. Нажмите **"Create Database"**
5. Скопируйте **Internal Database URL** (понадобится для API)

**Шаг 3: Создать Web Service для API**

1. Нажмите **"New +"** → **"Web Service"**
2. Подключите GitHub репозиторий
3. Настройки:
   - **Name**: `apexmaterials-api`
   - **Region**: тот же, что и БД
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `bash prestart.sh && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free

4. **Environment Variables** (добавьте):
   ```
   DATABASE_URL = [вставьте Internal Database URL из шага 2]
   ENVIRONMENT = production
   APP_NAME = ApexMaterials RFQ API
   API_PREFIX = /api/v1
   ```

5. Нажмите **"Create Web Service"**

**Шаг 4: Готово!**

API будет доступен по адресу: `https://apexmaterials-api.onrender.com`

Документация: `https://apexmaterials-api.onrender.com/docs`

### Способ 2: Через Blueprint (render.yaml)

Если в репозитории есть `render.yaml`, Render автоматически создаст все сервисы:

1. Загрузите код на GitHub
2. На Render нажмите **"New +"** → **"Blueprint"**
3. Подключите репозиторий
4. Render автоматически создаст БД и API

### Способ 3: Деплой фронтенда + бэкенда вместе

Если хотите задеплоить и фронтенд (папка `website`):

1. Создайте Static Site для фронтенда:
   - **Name**: `apexmaterials-frontend`
   - **Build Command**: `echo "No build required"`
   - **Publish Directory**: `website`

2. Обновите фронтенд для подключения к API:
   - В `website/index.html` или JS файлах замените API URL на `https://apexmaterials-api.onrender.com`

## Тестирование API

### Создать RFQ

```bash
curl -X POST https://apexmaterials-api.onrender.com/api/v1/rfqs \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "Test Company",
    "contact_name": "John Doe",
    "email": "john@example.com",
    "material": "Copper ingots",
    "specification": "99.9999% purity, 100kg",
    "notes_from_requester": "Urgent request"
  }'
```

### Получить список RFQ

```bash
curl https://apexmaterials-api.onrender.com/api/v1/rfqs
```

### Изменить статус

```bash
curl -X POST https://apexmaterials-api.onrender.com/api/v1/rfqs/{rfq_id}/status \
  -H "Content-Type: application/json" \
  -d '{
    "to_status": "in_review",
    "changed_by": "admin@apexmaterials.com",
    "comment": "Starting review process"
  }'
```

## Структура проекта

```
apexmaterials_production_backend_foundation/
├── alembic/                    # Миграции БД
│   ├── versions/
│   │   └── 0001_create_rfq_tables.py
│   └── env.py
├── app/
│   ├── api/
│   │   └── routes_rfq.py      # API endpoints
│   ├── core/
│   │   └── config.py          # Конфигурация
│   ├── db/
│   │   ├── base.py
│   │   └── session.py         # Подключение к БД
│   ├── models/
│   │   └── rfq.py             # SQLAlchemy модели
│   ├── schemas/
│   │   └── rfq.py             # Pydantic схемы
│   ├── services/
│   │   └── rfq_service.py     # Бизнес-логика
│   └── main.py                # Точка входа
├── website/                    # Статический фронтенд
│   └── index.html
├── .env.example
├── alembic.ini
├── docker-compose.yml
├── prestart.sh                 # Скрипт для миграций
├── Procfile                    # Для Render/Heroku
├── render.yaml                 # Blueprint для Render
├── requirements.txt
└── README.md
```

## Мониторинг и логи

На Render.com:
1. Перейдите в ваш Web Service
2. Вкладка **"Logs"** - просмотр логов в реальном времени
3. Вкладка **"Metrics"** - использование ресурсов
4. Вкладка **"Events"** - история деплоев

## Масштабирование

**Free Plan ограничения:**
- 750 часов в месяц
- Засыпает после 15 минут неактивности
- 512 MB RAM

**Для production:**
- Upgrade до Starter ($7/месяц) или выше
- Добавьте Redis для кэширования
- Настройте мониторинг (Sentry, DataDog)
- Добавьте аутентификацию (JWT)

## Безопасность

**TODO для production:**
- [ ] Добавить JWT аутентификацию
- [ ] Настроить CORS правильно
- [ ] Добавить rate limiting
- [ ] Включить HTTPS only
- [ ] Добавить роли (admin, reviewer, user)
- [ ] Валидация входных данных
- [ ] SQL injection защита (уже есть через SQLAlchemy)

## Следующие шаги

1. **Аутентификация**: Добавить JWT токены и роли пользователей
2. **Email уведомления**: Отправка писем при изменении статуса
3. **File uploads**: Загрузка документов к RFQ
4. **Dashboard**: Админ-панель для управления RFQ
5. **Reporting**: Экспорт данных в Excel/PDF
6. **Webhooks**: Интеграция с внешними системами

## Поддержка

Для вопросов и проблем создавайте issue в GitHub репозитории.
