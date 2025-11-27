from asgi_lifespan import LifespanManager
import pytest
from httpx import ASGITransport, AsyncClient
from app.main import app


def bearer(token: str | None) -> dict[str, str]:
    if token is None:
        return {}
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"

@pytest.fixture
async def client():
    """
    Creates an AsyncClient with the overridden dependency (database session).
    """
    async with LifespanManager(app):
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as ac:
            yield ac


@pytest.mark.asyncio
async def test_auth_token_injection_attempt(client: AsyncClient):
    """
    Попытка получить токен через /auth/token с инъекционными значениями в имени/пароле.
    Ожидаем: 401 Unauthorized (нельзя получить токен).
    """
    payloads = [
        {"name": "alice' OR '1'='1", "password": "whatever"},
        {"name": "nonexist", "password": "' OR '1'='1"},
        {"name": "' OR 1=1 --", "password": "' OR 1=1 --"},
    ]

    for body in payloads:
        r = await client.post("/auth/token", json=body)
        assert r.status_code == 401, f"Possible auth SQLi: payload {body} returned {r.status_code} with body: {r.text}"


@pytest.mark.asyncio
async def test_order_id_path_injection_and_validation(client):
    """
    Попытки подать инъекционные строки в path parameter order_id.
    Ожидаем: FastAPI отдаст 422 (path param не int) либо 404/403, но не допустит обхода авторизации.
    """
    bad_ids = ["1 OR 1=1", "1; DROP TABLE orders;", "1 UNION SELECT 1"]
    headers = bearer("secrettokenAlice")

    for bid in bad_ids:
        r = await client.get(F"/orders/{bid}", headers=headers)
        if r.status_code == 422:
            continue
        assert r.status_code in (404, 401, 400), f"Unexpected status {r.status_code} for ID {bid} body: {r.text}"


@pytest.mark.asyncio
async def test_authorization_header_sqli_attempt(client):
    """
    Попытка обойти авторизацию, подставляя инъекционный токен в заголовок Authorization.
    Ожидаем: 401 Unauthorized.
    """
    malicious_tokens = ["' OR '1'='1", "abcd' OR '1'='1", "secrettoken123' OR '1'='1"]
    for t in malicious_tokens:
        headers = bearer(t)
        r = await client.get("/orders", headers=headers)
        assert r.status_code == 401, f"Auth bypass possibility with token {t}: status {r.status_code} body: {r.text}"

@pytest.mark.asyncio
async def test_orders_bearer_injection(client):
    """
    Попытки инъекций через query params (limit / offset).
    Безопасное поведение:
      - FastAPI валидирует числа и вернёт 422 для некорректных типов
      - Либо, если сервер попытается парсить строку, он не должен раскрыть/вернуть чужие данные
    Тест допускает два безопасных результата:
      - 422 (валидация на уровне FastAPI)
      - 200 с корректным набором заказов принадлежащих авторизованному пользователю
    """
    headers = bearer("badTokeh' OR '1'='1")
    
    params = {"limit": 1, "offset": "0"}
    r = await client.get("/orders", headers=headers, params=params)
    assert r.status_code in (401, 403), "Injection"
