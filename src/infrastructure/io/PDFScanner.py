from logging import Logger
from src.utils.development import createLogger
from os import getenv
from src.adapters.http.OCRService import OCRService
from pymupdf import Document
from src.utils.development import createElapsedTimeProfiler
from src.utils.storage import filePathFor, existObject, putObject, getObjectMetaData
from io import StringIO
from base64 import b64decode
from src.modules.SnapshotManaging.errors.MustBeInPDFFormat import MustBeInPDFFormat


class PDFScanner:
    _logger: Logger
    _ocrService: OCRService

    def __init__(self):
        self._logger = createLogger(__name__)
        self._ocrService = OCRService(apiKey=getenv("OCRSPACE_API_KEY"))

    def _extractBlocks(self, buffer: bytes):
        doc = Document(stream=buffer)
        for page in doc:
            dict = page.get_text("dict")
            blocks = dict["blocks"]
            for block in blocks:
                yield block

    def _extractFromTextBlock(self, block: dict):
        for line in block["lines"]:
            for span in line["spans"]:
                text: str = span["text"]
                yield text.strip()

    async def _extractFromImageBlock(self, block: dict):
        width: int = block["width"]
        height: int = block["height"]
        ratio = width // height
        if ratio < 2:
            return None
        buffer: bytes = block["image"]
        filePath = filePathFor(buffer)
        if await existObject(filePath):
            metadata = await getObjectMetaData(filePath)
            return metadata["text"]
        else:
            text = await self._ocrService.ocr(buffer)
            await putObject(buffer, dict(text=text))
            return text

    async def _extractContents(self, buffer: bytes):
        for block in self._extractBlocks(buffer):
            if block["type"] == 0:
                for content in self._extractFromTextBlock(block):
                    if content:
                        yield True, f"\n{content}"
            if block["type"] == 1:
                content = await self._extractFromImageBlock(block)
                if content:
                    yield False, f"\n{content}"

    async def _extractFromPDF(self, buffer: bytes):
        text = StringIO()
        textsCount = 0
        async for isText, content in self._extractContents(buffer):
            text.write(content)
            if isText:
                textsCount += 1
        return text.getvalue() if textsCount > 0 else ""

    async def scan(self, base64Encoded: str):
        buffer = b64decode(base64Encoded)
        filePath = filePathFor(buffer)
        type: str = filePath.split("/")[0]
        if type != "pdf":
            raise MustBeInPDFFormat(expected=["pdf"], acutal=type)
        if await existObject(filePath):
            metadata = await getObjectMetaData(filePath)
            return metadata["text"], filePath
        measureElapsedTime = createElapsedTimeProfiler()
        text = await self._extractFromPDF(buffer)
        self._logger.debug(f"解析 PDF 花費了 {measureElapsedTime()} s")
        await putObject(buffer, dict(text=text))
        return text, filePath
