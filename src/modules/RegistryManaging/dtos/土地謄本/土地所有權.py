from typing import List, TypedDict


class 土地所有權(TypedDict):
    登記次序: str
    登記日期: str
    登記原因: str
    原因發生日期: str
    所有權人: str
    統一編號: str
    住址: str
    權利範圍: str
    權狀字號: str
    當期申報地價年月: str
    當期申報地價: int
    前次移轉現值或原規定地價年月: str
    前次移轉現值或原規定地價: int
    歷次取得權利範圍: str
    相關他項權利登記次序: List[str]
    其他登記事項: str
