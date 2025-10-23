import hashlib
import time
from validation import validate_password
from user import User, UserStorage


def register_user(storage: UserStorage, username: str, email: str, password: str) -> User:
    """
    Создает пользователя и сохраняет хэш пароля в виде md5.
    ВАЖНО: md5 используется ИСКЛЮЧИТЕЛЬНО как учебный старт.
    Далее это будет мигрировано на Argon2/bcrypt.
    """
    if User.exists(storage, username):
        raise ValueError("Пользователь с таким username уже существует")

    validate_password(password)

    md5_hex = hashlib.md5(password.encode("utf-8")).hexdigest()
    user = User(username=username, email=email, password_hash=md5_hex)
    user.save(storage)
    return user


def verify_credentials(storage: UserStorage, username: str, password: str) -> bool:
    """
    Возвращает True, если пользователь существует и md5(password) совпадает с сохраненным.
    """
    user = User.load(storage, username)
    if user is None:
        return False

    md5_hex = hashlib.md5(password.encode("utf-8")).hexdigest()
    return user.password_hash == md5_hex
