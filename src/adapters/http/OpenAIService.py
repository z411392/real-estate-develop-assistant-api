from openai import AsyncOpenAI
from src.modules.RegistryFragmentManaging.errors.NoModelAvailable import NoModelAvailable
from logging import Logger
from src.constants import LanguageModel, LanguageModelInputTokensLimit
from src.utils.calculators import countTokens
from src.modules.RegistryManaging.dtos.建物謄本.建物基本資訊 import 建物基本資訊
from src.modules.RegistryManaging.dtos.建物謄本.建物標示 import 建物標示
from src.modules.RegistryManaging.dtos.建物謄本.建物所有權 import 建物所有權
from src.modules.RegistryManaging.dtos.建物謄本.建物他項權利 import 建物他項權利
from src.modules.RegistryManaging.dtos.土地謄本.土地基本資訊 import 土地基本資訊
from src.modules.RegistryManaging.dtos.土地謄本.土地標示 import 土地標示
from src.modules.RegistryManaging.dtos.土地謄本.土地所有權 import 土地所有權
from src.modules.RegistryManaging.dtos.土地謄本.土地他項權利 import 土地他項權利
from src.utils.characters import fromFullwidthToHalfwidth
from commentjson import loads
from src.modules.RegistryFragmentManaging.dtos.prompts import (
    解析建物基本資訊,
    解析建物標示,
    解析建物所有權,
    解析建物他項權利,
)
from src.modules.RegistryFragmentManaging.dtos.prompts import (
    解析土地基本資訊,
    解析土地標示,
    解析土地所有權,
    解析土地他項權利,
)
from src.modules.RegistryFragmentManaging.presentation.validators.RegistryFragment import (
    行政區,
    地段,
    小段,
    編號,
    範圍,
)
from re import sub
from typing import Optional
from src.utils.development import createLogger


class OpenAIService:
    _client: AsyncOpenAI
    _logger: Logger

    def __init__(self, apiKey: str):
        self._client = AsyncOpenAI(api_key=apiKey)
        self._logger = createLogger(__name__)

    async def _createCompletion(
        self, prompt: str, text: str, multipleResults: bool = False
    ):
        tokensCount = countTokens(text)
        tokensDifference = LanguageModelInputTokensLimit - tokensCount
        if tokensDifference < 0:
            raise NoModelAvailable(tokensDifference=tokensDifference)
        messages = [
            dict(role="user", content=prompt),
            dict(role="user", content=f"```txt\n${text}```"),
        ]
        completion = await self._client.chat.completions.create(
            messages=messages,
            model=LanguageModel,
        )
        raw: str = "".join((choice.message.content for choice in completion.choices))
        response: str = (
            raw[raw.find("["): raw.rfind("]") + 1]
            if multipleResults
            else raw[raw.find("{"): raw.rfind("}") + 1]
        )
        return response

    def _validate(self, field: str, value: str):
        try:
            if field == "行政區":
                行政區.deserialize(value)
            elif field == "地段":
                地段.deserialize(value)
            elif field == "小段":
                小段.deserialize(value)
            elif field == "建號":
                編號.deserialize(value)
            elif field == "地號":
                編號.deserialize(value)
            elif field == "權利範圍":
                範圍.deserialize(value)
        except Exception:
            raise Exception(f"{field}的值(={value})有誤")

    def _purify(self, field: str, value: Optional[str]):
        if value is None:
            return value
        if field == "地段":
            value = sub(r"^.*?區", "", value)
        return value

    async def 解析建物基本資訊(self, text: str):
        response = await self._createCompletion(text=text, prompt=解析建物基本資訊)
        data = 建物基本資訊(loads(fromFullwidthToHalfwidth(response)))
        self._validate("行政區", data["行政區"])
        data["地段"] = self._purify("地段", data["地段"])
        self._validate("地段", data["地段"])
        if not data.get("小段"):
            data["小段"] = "空白"
        self._validate("小段", data["小段"])
        self._validate("建號", data["建號"])
        return data

    async def 解析建物標示(self, text: str):
        response = await self._createCompletion(text=text, prompt=解析建物標示)
        data = 建物標示(loads(fromFullwidthToHalfwidth(response)))
        for index, 建物坐落 in enumerate(data["建物坐落"]):
            建物坐落["地段"] = self._purify("地段", 建物坐落["地段"])
            self._validate("地段", 建物坐落["地段"])
            if 建物坐落.get("小段"):
                self._validate("小段", 建物坐落["小段"])
            self._validate("地號", 建物坐落["地號"])
            data["建物坐落"][index] = 建物坐落
        for index, 共有部分 in enumerate(data["共有部分"]):
            共有部分["地段"] = self._purify("地段", 共有部分["地段"])
            self._validate("地段", 共有部分["地段"])
            if 共有部分.get("小段"):
                self._validate("小段", 共有部分["小段"])
            self._validate("建號", 共有部分["建號"])
            self._validate("權利範圍", 共有部分["權利範圍"])
            data["共有部分"][index] = 共有部分
        for index, 主建物資料 in enumerate(data["主建物資料"]):
            主建物資料["地段"] = self._purify("地段", 主建物資料["地段"])
            self._validate("地段", 主建物資料["地段"])
            if 主建物資料.get("小段"):
                self._validate("小段", 主建物資料["小段"])
            self._validate("建號", 主建物資料["建號"])
            self._validate("權利範圍", 主建物資料["權利範圍"])
            data["主建物資料"][index] = 主建物資料
        return data

    async def 解析建物所有權(self, text: str):
        response = await self._createCompletion(text=text, prompt=解析建物所有權)
        data = 建物所有權(loads(fromFullwidthToHalfwidth(response)))
        self._validate("權利範圍", data["權利範圍"])
        return data

    async def 解析建物他項權利(self, text: str):
        response = await self._createCompletion(text=text, prompt=解析建物他項權利)
        data = 建物他項權利(loads(fromFullwidthToHalfwidth(response)))
        for index, 共同擔保土地 in enumerate(data["共同擔保土地"]):
            共同擔保土地["地段"] = self._purify("地段", 共同擔保土地["地段"])
            self._validate("地段", 共同擔保土地["地段"])
            if 共同擔保土地.get("小段"):
                self._validate("小段", 共同擔保土地["小段"])
            self._validate("地號", 共同擔保土地["地號"])
            data["共同擔保土地"][index] = 共同擔保土地
        for index, 共同擔保建物 in enumerate(data["共同擔保建物"]):
            共同擔保建物["地段"] = self._purify("地段", 共同擔保建物["地段"])
            self._validate("地段", 共同擔保建物["地段"])
            if 共同擔保建物.get("小段"):
                self._validate("小段", 共同擔保建物["小段"])
            self._validate("建號", 共同擔保建物["建號"])
            data["共同擔保建物"][index] = 共同擔保建物
        return data

    async def 解析土地基本資訊(self, text: str):
        response = await self._createCompletion(text=text, prompt=解析土地基本資訊)
        data = 土地基本資訊(loads(fromFullwidthToHalfwidth(response)))
        self._validate("行政區", data["行政區"])
        data["地段"] = self._purify("地段", data["地段"])
        self._validate("地段", data["地段"])
        if not data.get("小段"):
            data["小段"] = "空白"
        self._validate("小段", data["小段"])
        self._validate("地號", data["地號"])
        return data

    async def 解析土地標示(self, text: str):
        response = await self._createCompletion(text=text, prompt=解析土地標示)
        data = 土地標示(loads(fromFullwidthToHalfwidth(response)))
        for index, 地上建物建號 in enumerate(data["地上建物建號"]):
            地上建物建號["地段"] = self._purify("地段", 地上建物建號["地段"])
            self._validate("地段", 地上建物建號["地段"])
            if 地上建物建號.get("小段"):
                self._validate("小段", 地上建物建號["小段"])
            self._validate("建號", 地上建物建號["建號"])
            data["地上建物建號"][index] = 地上建物建號
        return data

    async def 解析土地所有權(self, text: str):
        response = await self._createCompletion(text=text, prompt=解析土地所有權)
        data = 土地所有權(loads(fromFullwidthToHalfwidth(response)))
        self._validate("權利範圍", data["權利範圍"])
        return data

    async def 解析土地他項權利(self, text: str):
        response = await self._createCompletion(text=text, prompt=解析土地他項權利)
        data = 土地他項權利(loads(fromFullwidthToHalfwidth(response)))
        for index, 共同擔保地號 in enumerate(data["共同擔保地號"]):
            共同擔保地號["地段"] = self._purify("地段", 共同擔保地號["地段"])
            self._validate("地段", 共同擔保地號["地段"])
            if 共同擔保地號.get("小段"):
                self._validate("小段", 共同擔保地號["小段"])
            self._validate("地號", 共同擔保地號["地號"])
            data["共同擔保地號"][index] = 共同擔保地號
        for index, 共同擔保建號 in enumerate(data["共同擔保建號"]):
            共同擔保建號["地段"] = self._purify("地段", 共同擔保建號["地段"])
            self._validate("地段", 共同擔保建號["地段"])
            if 共同擔保建號.get("小段"):
                self._validate("小段", 共同擔保建號["小段"])
            self._validate("建號", 共同擔保建號["建號"])
            data["共同擔保建號"][index] = 共同擔保建號
        return data
