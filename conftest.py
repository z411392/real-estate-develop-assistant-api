import pytest
from src.bootstrap import bootstrap


@pytest.fixture(autouse=True)
async def setup():
    async with bootstrap():
        yield
