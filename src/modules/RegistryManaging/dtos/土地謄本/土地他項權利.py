from typing import List, TypedDict
from src.modules.RegistryManaging.dtos.土地謄本.共同擔保地號 import 共同擔保地號
from src.modules.RegistryManaging.dtos.土地謄本.共同擔保建號 import 共同擔保建號


class 土地他項權利(TypedDict):
    登記次序: str
    權利種類: str
    收件日期: str
    字號: str
    登記日期: str
    登記原因: str
    權利人: str
    統一編號: str
    住址: str
    債權額比例: str
    擔保債權總金額: str
    擔保債權種類及範圍: str
    擔保債權確定日期: str
    償還日期: str
    存續期間: str
    利息或利率: str
    遲延利息或利率: str
    違約金: str
    其他擔保範圍約定: str
    權利標的: str
    標的登記次序: List[str]
    設定權利範圍: str
    證明書字號: str
    共同擔保地號: List[共同擔保地號]
    共同擔保建號: List[共同擔保建號]
    其他登記事項: str
