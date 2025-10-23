#!/usr/bin/sh

# Проверяем наличие активного окружения
if [[ -z "$VIRTUAL_ENV" ]]; then
  echo "❌ Виртуальное окружение не активно."
  echo "   source .venv/bin/activate"
  exit 1
fi

if [ -z "$1" ]; then
  echo "Использование: ./run_tests.sh <1|2>"
  echo "  1 - тесты для Argon2 с блокировкой"
  echo "  2 - тесты для Bcrypt с блокировкой"
  echo "  1 - тесты для Argon2 с ростом задержки"
  echo "  2 - тесты для Bcrypt с ростом задержки"
  exit 1
fi

case "$1" in
  1)
    echo "🔐 Запуск тестов argon2 с блокировкой"
    python -m pytest tests/test_migration_argon2.py tests/test_blocking.py tests/test_password_charset_policy.py tests/test_password_length_policy.py
    ;;
  2)
    echo "🔐 Запуск тестов bcrypt с блокировкой"
    python -m pytest tests/test_migration_bcrypt.py tests/test_blocking.py tests/test_password_charset_policy.py tests/test_password_length_policy.py
    ;;
  3)
    echo "🔐 Запуск тестов argon2 с ростом задержки"
    python -m pytest tests/test_migration_argon2.py tests/test_delay.py tests/test_password_charset_policy.py tests/test_password_length_policy.py
    ;;
  4)
    echo "🔐 Запуск тестов bcrypt с ростом задержки"
    python -m pytest tests/test_migration_bcrypt.py tests/test_delay.py tests/test_password_charset_policy.py tests/test_password_length_policy.py
    ;;
  *)
    echo "Неверный аргумент: $1 (должно быть 1, 2, 3 или 4)"
    exit 1
    ;;
esac
