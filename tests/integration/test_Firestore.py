import pytest
from firebase_admin.firestore_async import client


@pytest.mark.it('要能夠讀取／寫入 Firestore')
@pytest.mark.skip()
async def test_RealtimeDatabase():
    db = client()
    collectionName = "test"
    collection = db.collection(collectionName)
    document = collection.document("1")
    content = "hello, world!"
    await document.set(dict(content=content), merge=True)
    snapshot = await document.get()
    assert snapshot.get("exists")
    data = snapshot.get("to_dict")()
    assert bool(data["content"])
    await document.delete()
