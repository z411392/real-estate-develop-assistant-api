from base64 import b64encode
from aiohttp import ClientSession


class OCRService:
    _apiKey: str

    def __init__(self, apiKey: str):
        self._apiKey = apiKey

    _endpoint: str = "https://api.ocr.space/parse/image"

    async def ocr(self, buffer: bytes, language: str = "cht"):
        base64Encoded = b64encode(buffer).decode("utf-8")
        base64Image = f"data:image/jpeg;base64,{base64Encoded}"
        body = {
            "apikey": self._apiKey,
            "language": language,
            "base64Image": base64Image,
        }
        async with ClientSession() as session:
            async with session.post(self._endpoint, data=body) as response:
                payload = await response.json()
                if "ParsedResults" not in payload:
                    return None
                results = payload["ParsedResults"]
                joined = "".join((result["ParsedText"] for result in results))
                trimed = joined.replace("\r", "").replace("\n", "").strip()
                return trimed
