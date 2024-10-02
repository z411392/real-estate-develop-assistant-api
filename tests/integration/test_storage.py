import pytest
from firebase_admin import storage
from aiofile import async_open
from src.utils.storage import filePathFor, existObject, putObject, getObjectURL, deleteObjectURL


async def readTestFile(filePath: str):
    async with async_open(filePath, mode="rb") as fp:
        buffer: bytes = await fp.read()
        return buffer


@pytest.mark.it('要能夠上傳/刪除檔案')
@pytest.mark.skip()
async def test_Storage():
    bucket = storage.bucket()
    assert bucket.exists()
    buffer = await readTestFile("test.jpeg")
    assert isinstance(buffer, bytes)
    filePath = filePathFor(buffer)
    existsBeforeCreation = await existObject(filePath)
    assert existsBeforeCreation == False
    await putObject(buffer)
    existsAfterCreation = await existObject(filePath)
    assert existsAfterCreation
    url = await getObjectURL(filePath)
    assert bool(url)
    await deleteObjectURL(filePath)
    existsAfterDeletion = await existObject(filePath)
    assert existsAfterDeletion == False
