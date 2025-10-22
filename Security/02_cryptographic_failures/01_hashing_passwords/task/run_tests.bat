@echo off
REM Запуск тестов для Argon2 или Bcrypt (Windows)

IF "%~1"=="" (
    echo Использование: run_tests.bat ^<1^|2^>
    echo   1 - тесты для Argon2
    echo   2 - тесты для Bcrypt
    exit /b 1
)

IF "%~1"=="1" (
    echo 🔐 Запуск тестов с HASHER=argon2
    pytest tests/test_migration_argon2.py
    pytest tests/test_password_charset_policy.py
    pytest tests/test_password_length_policy.py
) ELSE IF "%~1"=="2" (
    echo 🔐 Запуск тестов с HASHER=bcrypt
    pytest tests/test_migration_bcrypt.py
    pytest tests/test_password_charset_policy.py
    pytest tests/test_password_length_policy.py
) ELSE (
  echo Неверный аргумент: %1 (должно быть 1 или 2)
  exit /b 1
)
