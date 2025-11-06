import json
import os
import tempfile
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
USERS_PATH = DATA_DIR / "users.json"
TOKENS_PATH = DATA_DIR / "tokens.json"

def _ensure_files():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not USERS_PATH.exists():
        USERS_PATH.write_text(json.dumps({"users": []}, ensure_ascii=False, indent=2), encoding="utf-8")
    if not TOKENS_PATH.exists():
        TOKENS_PATH.write_text(json.dumps({"tokens": []}, ensure_ascii=False, indent=2), encoding="utf-8")

def _atomic_write(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", delete=False, dir=str(path.parent), encoding="utf-8") as tmp:
        json.dump(data, tmp, ensure_ascii=False, indent=2)
        tmp.flush()
        os.fsync(tmp.fileno())
        name = tmp.name
    os.replace(name, path)

def load_users() -> dict[str, Any]:
    _ensure_files()
    return json.loads(USERS_PATH.read_text(encoding="utf-8"))

def save_users(db: dict[str, Any]) -> None:
    _atomic_write(USERS_PATH, db)

def load_tokens() -> dict[str, Any]:
    _ensure_files()
    return json.loads(TOKENS_PATH.read_text(encoding="utf-8"))

def save_tokens(db: dict[str, Any]) -> None:
    _atomic_write(TOKENS_PATH, db)

def clear_data():
    DATA_DIR.mkdir(parents=True, exist_ok=True)    
    USERS_PATH.write_text(json.dumps({"users": []}, ensure_ascii=False, indent=2), encoding="utf-8")    
    TOKENS_PATH.write_text(json.dumps({"tokens": []}, ensure_ascii=False, indent=2), encoding="utf-8")
