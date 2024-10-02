import pytest
from firebase_admin import db


@pytest.mark.it('要能夠讀取／寫入 Realtime Database')
@pytest.mark.skip()
async def test_RealtimeDatabase():
    key = "test"
    testRef = db.reference(key)
    value = "hello, world!"
    testRef.set(value)
    assert testRef.get() == value
