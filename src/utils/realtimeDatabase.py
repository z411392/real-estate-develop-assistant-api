from src.utils.threads import ThreadPoolExecutor
from firebase_admin import db
from typing import Any


async def get(key: str):
    async with ThreadPoolExecutor() as execute:
        reference = db.reference(key)
        return execute(reference.get)


async def put(key: str, value: Any):
    async with ThreadPoolExecutor() as execute:
        reference = db.reference(key)
        return execute(reference.set, value)
