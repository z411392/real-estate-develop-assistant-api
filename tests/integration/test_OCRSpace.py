import pytest
from aiofile import async_open
from src.adapters.http.OCRService import OCRService
from src.bootstrap import container
from os import getenv


async def readTestFile(filePath: str):
    async with async_open(filePath, mode="rb") as fp:
        buffer: bytes = await fp.read()
        return buffer


@pytest.mark.it('要能夠對圖片作 OCR')
@pytest.mark.skip()
async def test_OCRSpace():
    ocrService = OCRService(apiKey=getenv("OCRSPACE_API_KEY"))
    buffer = await readTestFile("test.jpeg")
    text = await ocrService.ocr(buffer)
    assert bool(text)
