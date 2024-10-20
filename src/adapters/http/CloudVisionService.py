from base64 import b64encode
from aiohttp import ClientSession
from io import StringIO
from urllib.parse import urlencode
from json import dumps


class CloudVisionService:
    _apiKey: str

    def __init__(self, apiKey: str):
        self._apiKey = apiKey

    _endpoint: str = "https://vision.googleapis.com/v1/images:annotate"

    async def ocr(self, buffer: bytes):
        content = b64encode(buffer).decode("utf-8")
        data = dumps(
            {
                "requests": [
                    {
                        "image": {
                            "content": content,
                        },
                        "features": [
                            {
                                "type": "TEXT_DETECTION",
                            }
                        ],
                    }
                ],
            }
        )
        queryString = urlencode(dict(key=self._apiKey))
        async with ClientSession() as session:
            async with session.post(
                f"{self._endpoint}?{queryString}", data=data
            ) as response:
                payload = await response.json()
                if "responses" not in payload:
                    return None
                responses = payload["responses"]
                results = StringIO()
                for response in responses:
                    if "textAnnotations" not in response:
                        continue
                    for textAnnotation in response["textAnnotations"]:
                        description: str = textAnnotation["description"]
                        result = description.replace(" ", "")
                        if result:
                            results.writelines(result)
                return results.getvalue()
