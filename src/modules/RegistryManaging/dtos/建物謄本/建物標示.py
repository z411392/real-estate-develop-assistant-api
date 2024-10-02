from typing import List, TypedDict
from src.modules.RegistryManaging.dtos.建物謄本.建物坐落 import 建物坐落
from src.modules.RegistryManaging.dtos.建物謄本.層次 import 層次
from src.modules.RegistryManaging.dtos.建物謄本.附屬建物 import 附屬建物
from src.modules.RegistryManaging.dtos.建物謄本.共有部分 import 共有部分
from src.modules.RegistryManaging.dtos.建物謄本.主建物資料 import 主建物資料


class 建物標示(TypedDict):
    登記日期: str
    登記原因: str
    建物坐落: List[建物坐落]
    建物門牌: str
    主要用途: str
    主要建材: str
    層數: str
    層次: List[層次]
    附屬建物: List[附屬建物]
    建築完成日期: str
    共有部分: List[共有部分]
    主建物資料: List[主建物資料]
    其他登記事項: str
