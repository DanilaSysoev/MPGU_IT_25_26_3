### Быстрый старт (для любого проекта)

```bash
cd <папка_проекта>
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```

### Демо-аккаунты

* `adminroot / adminroot123` — роль: admin
* `dev / devpass123` — роль: user
* `mod / modpass123` — роль: moderator

### Тесты

```bash
python manage.py test -v 2
```

> Тесты **падают** по умолчанию (это нормально): чтобы их пройти, студентам нужно перенести проверки на **серверную сторону**, корректно реализовать RBAC (использовать `Profile.role` и белые списки ролей), и закрыть доступ к уязвимым действиям (возвращать 403 для не-админов).
