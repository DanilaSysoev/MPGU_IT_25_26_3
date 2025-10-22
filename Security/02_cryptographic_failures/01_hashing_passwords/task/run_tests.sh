#!/usr/bin/sh

# Проверяем наличие активного окружения
if [[ -z "$VIRTUAL_ENV" ]]; then
  echo "❌ Виртуальное окружение не активно."
  echo "   source .venv/bin/activate"
  exit 1
fi

if [ -z "$1" ]; then
  echo "Использование: ./run_tests.sh <1|2>"
  echo "  1 - тесты для Argon2"
  echo "  2 - тесты для Bcrypt"
  exit 1
fi

case "$1" in
  1)
    echo "🔐 Запуск тестов с argon2"
    python -m pytest tests/test_migration_argon2.py tests/test_password_charset_policy.py tests/test_password_length_policy.py
    ;;
  2)
    echo "🔐 Запуск тестов с bcrypt"
    python -m pytest tests/test_migration_bcrypt.py tests/test_password_charset_policy.py tests/test_password_length_policy.py
    ;;
  *)
    echo "Неверный аргумент: $1 (должно быть 1 или 2)"
    exit 1
    ;;
esac
