# 🔐 ЗАНЯТИЕ 2 — КЛЮЧИ, ТОКЕНЫ И УПРАВЛЕНИЕ СЕКРЕТАМИ

## 1. Цель

Понять, как правильно:

* хранить и использовать криптографические ключи;
* формировать токены (session, bearer, JWT);
* проверять подписи и срок действия токенов;
* защищать ключи от утечки.

---

## 2. Типичные криптографические ошибки

1. Ключи хранятся в коде или в репозитории.
2. Токены не подписаны (base64 без HMAC).
3. Отсутствие проверки срока действия токена.
4. Использование предсказуемых значений (например, user_id + timestamp).
5. Использование «None» алгоритма в JWT.
6. Отсутствие ротации секретов.

---

## 3. Ключевые понятия

* **Секрет (Secret key)** — строка, известная только серверу, используется для подписи.
* **Подпись (HMAC)** — способ убедиться, что данные не подделаны.
* **Токен** — средство аутентификации пользователя без пароля.
* **JWT (JSON Web Token)** — токен в формате JSON, подписанный HMAC или RSA.

---

## 4. HMAC (Hash-based Message Authentication Code)

Формула:

```
HMAC = hash(secret + message)
```

**Зачем нужен:**
Позволяет проверить, что данные не были изменены.
Используется в API и JWT.

**Пример:**

```python
import hmac, hashlib

msg = b"username=admin"
secret = b"topsecret"
signature = hmac.new(secret, msg, hashlib.sha256).hexdigest()
```

---

## 5. Base64 ≠ безопасность

Многие разработчики думают, что токен вроде

```python
token = base64.b64encode(f"{username}:{timestamp}".encode())
```

безопасен.
Но base64 — **просто кодирование**, не шифрование.
Его можно раскодировать и изменить.

---

## 6. JWT (JSON Web Token)

JWT состоит из 3 частей:

```
header.payload.signature
```

### Пример:

```
eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1c2VyMSIsImlhdCI6MTcxNjA3NDI2OSwiZXhwIjoxNzE2MDc0ODI5fQ.NL56M0U0...
```

### Декодирование:

```python
import jwt
SECRET = "mysecret"
payload = jwt.decode(token, SECRET, algorithms=["HS256"])
```

---

## 7. Преимущества JWT

* Самодостаточен: не требует хранения сессий на сервере.
* Можно задать срок действия (`exp`).
* Можно проверять подпись без БД.

---

## 8. Опасности JWT

1. Алгоритм `"none"` → токен можно подделать.
2. Использование асимметрии как симметрии (подмена публичного ключа).
3. Неограниченный срок жизни (`exp` отсутствует).
4. Утечка `SECRET_KEY`.

---

## 9. Как хранить секреты

| Неправильно                      | Правильно                         |
| -------------------------------- | --------------------------------- |
| В коде (`SECRET_KEY = "12345"`)  | В .env файле                      |
| В Git                            | В secrets manager (Vault, AWS SM) |
| В cookie без флагов              | С флагами Secure, HttpOnly        |
| Долгоживущий токен без ревокации | Refresh токен с ротацией          |

Пример `.env`:

```
SECRET_KEY=change-me
JWT_EXPIRATION=600
```

---

## 10. Refresh токен

* Access-токен: живёт 5–15 минут.
* Refresh-токен: живёт дольше, хранится безопасно.
* При обновлении access-токена — refresh заменяется новым (rotate-on-use).

---

## 11. Ротация ключей

* Старый ключ → `kid=1`, новый → `kid=2`.
* Сервер хранит оба и может верифицировать старые токены.
* При деплое можно добавлять новые ключи без «принудительного выхода» всех пользователей.

---

## 12. Проверка подлинности токенов

```python
def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise Unauthorized("Token expired")
    except jwt.InvalidTokenError:
        raise Unauthorized("Invalid token")
```

---

## 13. Безопасность транспортного уровня

* Всегда использовать HTTPS.
* Никогда не передавать токен в URL.
* Для браузеров — предпочтительно хранить токен в cookie с HttpOnly + Secure.

---

## 14. Практические меры

✅ Не храните секреты в коде.<br/>
✅ Не используйте Base64 в качестве защиты.<br/>
✅ Настройте срок жизни токена (`exp`).<br/>
✅ Реализуйте refresh flow и revocation list.<br/>
✅ Регулярно обновляйте ключи.<br/>
✅ Логируйте не содержимое токенов, а только `sub` или `kid`.<br/>

---

## 15. Для обсуждения

* Что произойдёт, если `SECRET_KEY` утечёт?
* Почему нельзя хранить токен в localStorage?
* В чём разница между “шифровать токен” и “подписывать токен”?

---

## 16. Для самостоятельного чтения

* [OWASP JSON Web Token Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_Cheat_Sheet_for_Java.html)
* [OWASP Cryptographic Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html)
* [RFC 7519: JSON Web Token (JWT)](https://datatracker.ietf.org/doc/html/rfc7519)

---

## 17. Контрольные вопросы

1. Что делает подпись в HMAC?
2. Почему base64-токен легко подделать?
3. Как проверить, что токен не устарел?
4. Что такое ротация ключей?
5. Почему секрет нельзя хранить в Git?

---
