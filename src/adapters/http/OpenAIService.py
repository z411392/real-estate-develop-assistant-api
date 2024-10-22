from openai import AsyncOpenAI
from json import loads


class OpenAIService:
    _client: AsyncOpenAI

    def __init__(self, apiKey: str):
        self._client = AsyncOpenAI(api_key=apiKey)

    async def createCompletion(self, prompt: str, text: str):
        messages = [
            dict(role="user", content=prompt),
            dict(role="user", content=f"```txt\n${text}```"),
        ]
        completion = await self._client.chat.completions.create(
            messages=messages, model="gpt-4o"
        )
        raw: str = "".join((choice.message.content for choice in completion.choices))
        response = raw[raw.find("{"): raw.rfind("}") + 1]
        json: dict = loads(response)
        return json
