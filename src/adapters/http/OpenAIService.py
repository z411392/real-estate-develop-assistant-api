from openai import AsyncOpenAI
from src.modules.SnapshotManaging.dtos.Prompts import Prompts
from json import loads
from src.modules.SnapshotManaging.dtos.BuildingRegistry import BuildingRegistry
from src.modules.SnapshotManaging.dtos.LandRegistry import LandRegistry

# from aiofile import async_open

# async def buildingExample1():
#     async with async_open("examples/building-regisitry-1.json", "r") as file:
#         content = await file.read()
#         return f"""```json
#         {content}
#         ```"""


# async def buildingExample2():
#     async with async_open("examples/building-regisitry-2.json", "r") as file:
#         content = await file.read()
#         return f"""```json
#         {content}
#         ```"""

class OpenAIService:
    _client: AsyncOpenAI

    def __init__(self, apiKey: str):
        self._client = AsyncOpenAI(api_key=apiKey)

    async def parseBuildingRegistry(self, text: str):
        messages = [
            dict(role="user", content=Prompts.BuildingRegistryParsing),
            dict(role="user", content=f"```txt\n${text}```"),
        ]
        completion = await self._client.chat.completions.create(
            messages=messages, model="gpt-4o"
        )
        raw: str = "".join((choice.message.content for choice in completion.choices))
        response = raw[raw.find("{"): raw.rfind("}") + 1]
        json: dict = loads(response)
        return BuildingRegistry(**json)

    async def parseLandRegistry(self, text: str):
        messages = [
            dict(role="user", content=Prompts.LandRegistryParsing),
            dict(role="user", content=f"```txt\n${text}```"),
        ]
        completion = await self._client.chat.completions.create(
            messages=messages, model="gpt-4o"
        )
        raw: str = "".join((choice.message.content for choice in completion.choices))
        response = raw[raw.find("{"): raw.rfind("}") + 1]
        json: dict = loads(response)
        return LandRegistry(**json)
