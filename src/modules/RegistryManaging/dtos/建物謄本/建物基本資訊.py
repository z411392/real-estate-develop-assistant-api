from typing import Optional, TypedDict


class 建物基本資訊(TypedDict):
    列印時間: str
    列印公司: str
    謄本種類碼: str
    謄本編號: str
    謄本核發機關: str
    資料管轄機關: str
    行政區: str
    地段: str
    小段: Optional[str]
    建號: str
