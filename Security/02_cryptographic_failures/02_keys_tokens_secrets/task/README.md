# Кибербезопасность 6. Разработка безопасного ПО. CLI система выдачи токенов (JWT, HS256) (максимальный балл 16, дедлайн 20.11.25 включительно)

В данной задаче вам предстоит реализовать систему выдачи jwt токенов с алгоритмом подписи hs256.
Каркас проекта реализован, ваша задача добиться прохождения тестов. Для этого требуется реализовать функции в модулях `crypto` и `auth`. Изучите конспект, запись занятия и документацию по библиотеке jwt, чтобы реализовать недостающие модули.

## Быстрый старт
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .\.venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python cli.py users add --username alice --email alice@example.com --password "Password123!"
python cli.py login --username alice --password "Password123!"
```

## Команды
```bash
login --username --password → печатает {access_token, refresh_token}

me --access <token> → печатает payload access-токена

refresh --refresh <token> → ротация: выдаёт новую пару, старый refresh отзывется

revoke --token <token> → отзыв токена (access/refresh)

introspect --token <token> → {active: bool, sub?, typ?, exp?, jti?}

users add --username --email --password → регистрация пользователя
```

## Тесты
```bash
pytest -q
```