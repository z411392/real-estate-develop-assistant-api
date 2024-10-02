from typing import List, TypedDict
from src.modules.RegistryManaging.dtos.土地謄本.地上建物建號 import 地上建物建號


class 土地標示(TypedDict):
    登記日期: str
    登記原因: str
    面積: str
    使用分區: str
    使用地類別: str
    公告土地現值年月: str
    公告土地現值: int
    地上建物建號: List[地上建物建號]
    其他登記事項: str
