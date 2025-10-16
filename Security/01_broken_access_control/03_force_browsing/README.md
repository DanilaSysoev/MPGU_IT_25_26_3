
## Данные тестовых пользователей

### ‼️ Данные пользователей смотрите в логах посева
➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖
---

## Linux / macOS (bash / zsh)

```bash
cd <каталог_проекта>  # проверить можно по наличию файла manage.py

# 1. создать виртуальное окружение
python -m venv .venv

# 2. активировать
source .venv/bin/activate

# 3. установить зависимости (если есть requirements.txt)
pip install --upgrade pip
pip install -r requirements.txt

# 4. миграции
python manage.py makemigrations <название_проекта>  # опционально, можно пропустить если не нужно
python manage.py migrate

# 5. посев демо-данных (если у тебя management command seed_demo)
python manage.py seed_demo

# 6. запустить dev-сервер
python manage.py runserver

# 7. в другом терминале (или после остановки сервера) — запустить тесты
# активируй .venv в новом терминале, затем:
pytest -q
```

---

## Windows (PowerShell)

```powershell
cd <каталог_проекта>  # проверить можно по наличию файла manage.py

# 1. создать venv
python -m venv .venv

# 2. активировать (PowerShell)
.venv\Scripts\Activate.ps1

# 3. установить зависимости
python -m pip install --upgrade pip
pip install -r requirements.txt

# 4. миграции
python manage.py makemigrations <название_проекта>
python manage.py migrate

# 5. посев
python manage.py seed_demo

# 6. запустить сервер
python manage.py runserver

# 7. запуск тестов (в активированном окружении)
pytest -q
# или
python -m pytest -q
```

---
