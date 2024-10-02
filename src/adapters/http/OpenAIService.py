from openai import AsyncOpenAI
from src.modules.SnapshotManaging.dtos.Prompts import Prompts
from json import loads
from aiofile import async_open
from src.modules.SnapshotManaging.dtos.BuildingRegistry import BuildingRegistry


async def example1():
    async with async_open("examples/building-regisitry-1.json", "r") as file:
        content = await file.read()
        return f"""```json
        {content}
        ```"""


async def example2():
    async with async_open("examples/building-regisitry-2.json", "r") as file:
        content = await file.read()
        return f"""```json
        {content}
        ```"""


class OpenAIService:
    _client: AsyncOpenAI

    def __init__(self, apiKey: str):
        self._client = AsyncOpenAI(api_key=apiKey)

    async def parseBuildingRegistry(self, text: str):
        messages = [
            dict(role="user", content=Prompts.BuildingRegistryParsing()),
            dict(role="user", content=f"```txt\n${text}```"),
        ]
        completion = await self._client.chat.completions.create(
            messages=messages, model="gpt-4o"
        )
        raw: str = "".join((choice.message.content for choice in completion.choices))
        # raw: str = await example1()
        response = raw[raw.find("{"): raw.rfind("}") + 1]
        json: dict = loads(response)
        return BuildingRegistry(**json)
