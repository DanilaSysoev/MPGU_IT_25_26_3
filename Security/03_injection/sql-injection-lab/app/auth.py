from fastapi import HTTPException, Header
from .db import get_pool

async def get_user_by_token(authorization: str | None = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    if not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Invalid Authorization header")
    token_value = authorization[7:]
    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            f"SELECT u.id, u.name FROM tokens t JOIN users u ON u.id = t.user_id WHERE t.value = '{token_value}' AND t.is_valid = TRUE",
        )
    if not row:
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"id": row["id"], "name": row["name"]}
