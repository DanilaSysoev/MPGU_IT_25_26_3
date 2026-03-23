# Урок 5. Модели, PostgreSQL и Безопасность (.env)

**Тип занятия:** Лекция + Live Coding  
**Продолжительность:** 3 астрономических часа  
**Сложность:** Высокая (Настройка окружения, безопасность, Docker)  

## Цели урока

1. Понять принципы безопасности: почему нельзя хранить пароли в коде.
2. Настроить переменные окружения через файл `.env` и библиотеку `python-dotenv`.
3. Запустить PostgreSQL в Docker, используя конфиг из `.env`.
4. Подключить Django к PostgreSQL, используя современный драйвер `psycopg` (v3).
5. Спроектировать первую модель данных и применить миграции.

---

## Часть 1. Конспект лекции

### 1. Конфигурация и Безопасность

* **Проблема:** Если вы напишете пароль от базы данных прямо в `settings.py` и запушите это на GitHub, через 5 минут ваш сервер взломают боты.
* **Решение:** Переменные окружения (Environment Variables).
* **Файл `.env`:** Это простой текстовый файл `КЛЮЧ=ЗНАЧЕНИЕ`, который хранится **только** на вашем компьютере и на сервере. Он **никогда** не попадает в Git.
* **Библиотека `python-dotenv`:** Позволяет Python читать этот файл так, будто это системные переменные.

### 2. Драйвер базы данных (`psycopg`)

Django сам по себе не умеет общаться с PostgreSQL. Ему нужен драйвер (адаптер).

* Раньше стандартом был `psycopg2`.
* Сейчас мы используем **`psycopg` (версия 3)** — это современный, асинхронный и быстрый драйвер.

### 3. ORM и Модели (Повторение концепции)

* **Модель** = Класс Python.
* **Поле модели** = Тип данных в колонке (String, Integer, Boolean).
* **Миграция** = Файл-инструкция, который превращает изменения в коде Python в SQL-команды (`CREATE TABLE`, `ALTER TABLE`).

---

## Часть 2. Практика (Live Coding)

*Преподаватель демонстрирует процесс настройки "с нуля" в текущем проекте.*

### Шаг 1. Установка библиотек

```bash
# Драйвер БД (binary версия проще ставится на Windows/Mac)
pip install "psycopg[binary]"
# Для работы с .env
pip install python-dotenv
# Фиксируем
pip freeze > requirements.txt
```

### Шаг 2. Создание `.env`

В корне проекта (рядом с `manage.py`) создаем файл `.env`:

```ini
# .env
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=supersecretpassword
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=django-insecure-...(ваш ключ из settings.py)...
DEBUG=True
```

### Шаг 3. Игнорирование секретов

Сразу же добавляем `.env` в `.gitignore`!
```text
# .gitignore
venv/
__pycache__/
.env  <-- Обязательно!
```
### Шаг 4. Docker Compose с переменными

Создаем `docker-compose.yml`. Используем `env_file`, чтобы Docker сам подтянул переменные.

```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    restart: always
    volumes:
      - pg_data:/var/lib/postgresql/data/
    env_file:
      - .env  # Читаем переменные отсюда
    environment:
      # Маппинг переменных Django на переменные Postgres
      POSTGRES_DB: ${DB_NAME}
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    ports:
      - "5432:5432"

volumes:
  pg_data:
```

Запускаем: `docker-compose up -d`.

### Шаг 5. Настройка `settings.py`

В самом верху файла `settings.py`:

```python
import os
from pathlib import Path
from dotenv import load_dotenv # Импорт

# Загружаем переменные из .env
load_dotenv()

# ...

SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG') == 'True'

# ...

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}
```

### Шаг 6. Создание Модели и Миграции

1. В `models.py` создаем класс `Item` (или `Post`).
2. `python manage.py makemigrations`.
3. `python manage.py migrate`. (Если настройки верны, Django подключится к Docker-контейнеру).

---

## Часть 3. Домашнее задание №5

**Тема:** Безопасное подключение PostgreSQL и моделирование данных.  
**Срок выполнения:** 1 неделя.  
**Максимальный балл:** 8 баллов.  

### Описание задания

Вам необходимо защитить конфигурацию вашего проекта, вынеся секретные данные в файл `.env`, настроить базу данных PostgreSQL через Docker и создать первые таблицы для вашего приложения.

### Техническое задание (ТЗ)

1. **Безопасность (.env):**
    * Установите `python-dotenv`.
    * Создайте файл `.env`. Перенесите туда `SECRET_KEY`, `DEBUG` и настройки базы данных.
    * **Критически важно:** Добавьте `.env` в `.gitignore`.
    * Настройте `settings.py` на чтение этих переменных через `os.getenv`.

2. **База данных (Docker + Psycopg):**
    * Установите драйвер `psycopg[binary]`.
    * Настройте `docker-compose.yml` на использование файла `.env` (директива `env_file`).
    * Запустите контейнер БД.

3. **Модели (Models):**
    * Создайте модель, описывающую основную сущность вашего проекта (например, `Book`, `Car`, `Article`).
    * Используйте разные типы полей:
        * Строковое (`CharField`) — для названий.
        * Текстовое (`TextField`) — для описаний.
        * Числовое (`IntegerField` / `DecimalField`) — для цены или количества.
        * Дата/Время (`DateTimeField`) — для даты создания (`auto_now_add=True`).
    * Реализуйте метод `__str__` для красивого отображения.

4. **Применение:**
    * Создайте и примените миграции (`migrate`).
    * Зарегистрируйте модель в админке.
    * Создайте 3 тестовых объекта через админ-панель (`http://127.0.0.1:8000/admin`).
  
5. **Результат работы влейте в main с коммитом "Task 5 ready."**

### Критерии оценивания (Аддитивная система)

Максимум: **8 баллов**.

| Критерий | Баллы | Описание |
| :--- | :---: | :--- |
| **Безопасность (.gitignore)** | **+2** | Файл `.env` создан, но **ОТСУТСТВУЕТ** в репозитории GitHub. Это проверяется вручную преподавателем. |
| **Настройка settings.py** | **+1** | Переменные (`SECRET_KEY`, БД) читаются из `os.getenv`. Нет хардкода паролей. |
| **Docker & Env** | **+1** | `docker-compose.yml` использует переменные окружения (syntax `${VAR}` или `env_file`). |
| **Драйвер Psycopg** | **+1** | В `requirements.txt` указан `psycopg` (или `psycopg[binary]`), а не устаревший `psycopg2`. |
| **Модель данных** | **+2** | Модель содержит минимум 4 поля разных типов и метод `__str__`. |
| **Админка** | **+1** | Модель зарегистрирована, через админку можно создавать записи (скриншот или демонстрация). |

### Штрафы

* **-3 балла:** Файл `.env` с паролями залит на GitHub. (Грубейшее нарушение безопасности).
* **-2 балла:** Не работает подключение к БД (ошибка при `migrate`).
* **-1 балл:** Использование `psycopg2` вместо `psycopg`.

---

### Полезные материалы

* [12 Factor App: Config](https://12factor.net/ru/config/) — почему конфиги хранят в переменные окружения.
* [Django Models (Official)](https://docs.djangoproject.com/en/5.0/topics/db/models/)
* [Model Field Reference](https://docs.djangoproject.com/en/5.0/ref/models/fields/) — список всех доступных типов полей.
* [Docker Compose для начинающих](https://habr.com/ru/post/449574/)
* [Python Dotenv Documentation](https://pypi.org/project/python-dotenv/)
