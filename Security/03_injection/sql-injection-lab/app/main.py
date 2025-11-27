from fastapi import FastAPI, Depends, HTTPException, Query, Path
from typing import Annotated, Any
from .db import get_pool, close_pool
from .auth import get_user_by_token
from contextlib import asynccontextmanager
from pydantic import BaseModel
import hashlib
import secrets

pool = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global pool
    pool = await get_pool()
    yield
    pool = None
    await close_pool()

app = FastAPI(title="SQLi Lab (safe edition)", lifespan=lifespan)

class AuthRequest(BaseModel):
    name: str
    password: str

@app.post("/auth/token")
async def auth_token(body: AuthRequest):
    global pool
    async with pool.acquire() as conn:
        pass_hash = hashlib.md5(body.password.encode()).hexdigest()
        
        row = await conn.fetchrow(f"SELECT id, password_hash FROM users WHERE name = '{body.name}' AND password_hash = '{pass_hash}'")
        if not row:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        token_row = await conn.fetchrow(f"SELECT value FROM tokens WHERE user_id = {row["id"]} AND is_valid = TRUE LIMIT 1", )
        if not token_row:
            token = secrets.token_urlsafe(64)
            await conn.fetch(f"INSERT INTO tokens (user_id, value) VALUES ({row["id"]}, '{token}');", )
        else:
            token = token_row["value"]
        return {"token": token}

@app.get("/orders")
async def list_orders(
    user: Annotated[dict[str, Any], Depends(get_user_by_token)],
    limit,
    offset
):
    global pool
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            f"SELECT id, user_id, created_at FROM orders WHERE user_id = {user["id"]} ORDER BY created_at DESC LIMIT {limit} OFFSET {offset}"
        )
    return [{"id": r["id"], "user_id": r["user_id"], "created_at": r["created_at"].isoformat()} for r in rows]

@app.get("/orders/{order_id}")
async def order_details(user: Annotated[dict[str, Any], Depends(get_user_by_token)], order_id = Path(...)):
    global pool
    async with pool.acquire() as conn:
        order = await conn.fetchrow(
            f"SELECT id, user_id, created_at FROM orders WHERE id = {order_id} AND user_id = {user["id"]}",
        )
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        goods = await conn.fetch(
            f"SELECT id, name, count, price FROM goods WHERE order_id = {order_id}",
        )
    return {
        "order": {"id": order["id"], "user_id": order["user_id"], "created_at": order["created_at"].isoformat()},
        "goods": [{"id": g["id"], "name": g["name"], "count": g["count"], "price": float(g["price"])} for g in goods]
    }
