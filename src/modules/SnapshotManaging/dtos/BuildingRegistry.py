from typing import List, Optional
from dataclasses import dataclass, field


@dataclass
class 共同擔保建物:
    地段: str
    小段: Optional[str]
    建號: str

    @staticmethod
    def from_dict(data: dict):
        _地段 = str(data.get("地段"))
        _小段 = str(data.get("小段")) if data.get("小段") else None
        _建號 = str(data.get("建號"))
        return 共同擔保建物(_地段, _小段, _建號)


@dataclass
class 共同擔保土地:
    地段: str
    小段: Optional[str]
    地號: str

    @staticmethod
    def from_dict(data: dict):
        _地段 = str(data.get("地段"))
        _小段 = str(data.get("小段")) if data.get("小段") else None
        _地號 = str(data.get("地號"))
        return 共同擔保土地(_地段, _小段, _地號)


@dataclass
class 建物他項權利部:
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
    共同擔保土地: List[共同擔保土地]
    共同擔保建物: List[共同擔保建物]
    其他登記事項: str

    @staticmethod
    def from_dict(data: dict):
        _登記次序 = str(data.get("登記次序"))
        _權利種類 = str(data.get("權利種類"))
        _收件日期 = str(data.get("收件日期"))
        _字號 = str(data.get("字號"))
        _登記日期 = str(data.get("登記日期"))
        _登記原因 = str(data.get("登記原因"))
        _權利人 = str(data.get("權利人"))
        _統一編號 = str(data.get("統一編號"))
        _住址 = str(data.get("住址"))
        _債權額比例 = str(data.get("債權額比例"))
        _擔保債權總金額 = str(data.get("擔保債權總金額"))
        _擔保債權種類及範圍 = str(data.get("擔保債權種類及範圍"))
        _擔保債權確定日期 = str(data.get("擔保債權確定日期"))
        _償還日期 = str(data.get("償還日期"))
        _存續期間 = str(data.get("存續期間"))
        _利息或利率 = str(data.get("利息或利率"))
        _遲延利息或利率 = str(data.get("遲延利息或利率"))
        _違約金 = str(data.get("違約金"))
        _其他擔保範圍約定 = str(data.get("其他擔保範圍約定"))
        _權利標的 = str(data.get("權利標的"))
        _標的登記次序 = [標的登記次序 for 標的登記次序 in data.get("標的登記次序")]
        _設定權利範圍 = str(data.get("設定權利範圍"))
        _證明書字號 = str(data.get("證明書字號"))
        _共同擔保土地 = [
            共同擔保土地.from_dict(每一共同擔保土地)
            for 每一共同擔保土地 in data.get("共同擔保土地")
        ]
        _共同擔保建物 = [
            共同擔保建物.from_dict(每一共同擔保建物)
            for 每一共同擔保建物 in data.get("共同擔保建物")
        ]
        _其他登記事項 = str(data.get("其他登記事項"))
        return 建物他項權利部(
            _登記次序,
            _權利種類,
            _收件日期,
            _字號,
            _登記日期,
            _登記原因,
            _權利人,
            _統一編號,
            _住址,
            _債權額比例,
            _擔保債權總金額,
            _擔保債權種類及範圍,
            _擔保債權確定日期,
            _償還日期,
            _存續期間,
            _利息或利率,
            _遲延利息或利率,
            _違約金,
            _其他擔保範圍約定,
            _權利標的,
            _標的登記次序,
            _設定權利範圍,
            _證明書字號,
            _共同擔保土地,
            _共同擔保建物,
            _其他登記事項,
        )


@dataclass
class 建物所有權部:
    登記次序: str
    登記日期: str
    登記原因: str
    原因發生日期: str
    所有權人: str
    統一編號: str
    住址: str
    權利範圍: str
    權狀字號: str
    建物他項權利登記次序: List[str]
    其他登記事項: str

    @staticmethod
    def from_dict(data: dict):
        _登記次序 = str(data.get("登記次序"))
        _登記日期 = str(data.get("登記日期"))
        _登記原因 = str(data.get("登記原因"))
        _原因發生日期 = str(data.get("原因發生日期"))
        _所有權人 = str(data.get("所有權人"))
        _統一編號 = str(data.get("統一編號"))
        _住址 = str(data.get("住址"))
        _權利範圍 = str(data.get("權利範圍"))
        _權狀字號 = str(data.get("權狀字號"))
        _建物他項權利登記次序 = [
            建物他項權利登記次序
            for 建物他項權利登記次序 in data.get("建物他項權利登記次序")
        ]
        _其他登記事項 = str(data.get("其他登記事項"))
        return 建物所有權部(
            _登記次序,
            _登記日期,
            _登記原因,
            _原因發生日期,
            _所有權人,
            _統一編號,
            _住址,
            _權利範圍,
            _權狀字號,
            _建物他項權利登記次序,
            _其他登記事項,
        )


@dataclass
class 主建物資料:
    地段: str
    小段: Optional[str]
    建號: str
    權利範圍: str

    @staticmethod
    def from_dict(data: dict):
        _地段 = str(data.get("地段"))
        _小段 = str(data.get("小段")) if data.get("小段") else None
        _建號 = str(data.get("建號"))
        _權利範圍 = str(data.get("權利範圍"))
        return 主建物資料(_地段, _小段, _建號, _權利範圍)


@dataclass
class 共有部分:
    地段: str
    小段: Optional[str]
    建號: str
    面積: str
    權利範圍: str
    其他登記事項: str

    @staticmethod
    def from_dict(data: dict):
        _地段 = str(data.get("地段"))
        _小段 = str(data.get("小段")) if data.get("小段") else None
        _建號 = str(data.get("建號"))
        _面積 = str(data.get("面積"))
        _權利範圍 = str(data.get("權利範圍"))
        _其他登記事項 = str(data.get("其他登記事項"))
        return 共有部分(_地段, _小段, _建號, _面積, _權利範圍, _其他登記事項)


@dataclass
class 附屬建物:
    附屬建物類型: str
    面積: str

    @staticmethod
    def from_dict(data: dict):
        _附屬建物類型 = str(data.get("附屬建物類型"))
        _面積 = str(data.get("面積"))
        return 附屬建物(_附屬建物類型, _面積)


@dataclass
class 層次:
    層次: int
    層次面積: str
    總面積: str

    @staticmethod
    def from_dict(data: dict):
        _層次 = str(data.get("層次"))
        _層次面積 = str(data.get("層次面積"))
        _總面積 = str(data.get("總面積"))
        return 層次(_層次, _層次面積, _總面積)


@dataclass
class 建物坐落:
    地段: str
    小段: Optional[str]
    地號: str

    @staticmethod
    def from_dict(data: dict):
        _地段 = str(data.get("地段"))
        _小段 = str(data.get("小段")) if data.get("小段") else None
        _地號 = str(data.get("地號"))
        return 建物坐落(_地段, _小段, _地號)


@dataclass
class 建物標示部:
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

    @staticmethod
    def from_dict(data: dict):
        _登記日期 = str(data.get("登記日期"))
        _登記原因 = str(data.get("登記原因"))
        _建物坐落 = [
            建物坐落.from_dict(單一建物坐落) for 單一建物坐落 in data.get("建物坐落")
        ]
        _建物門牌 = str(data.get("建物門牌"))
        _主要用途 = str(data.get("主要用途"))
        _主要建材 = str(data.get("主要建材"))
        _層數 = str(data.get("層數"))
        _層次 = [層次.from_dict(單一層次) for 單一層次 in data.get("層次")]
        _附屬建物 = [
            附屬建物.from_dict(單一附屬建物) for 單一附屬建物 in data.get("附屬建物")
        ]
        _建築完成日期 = str(data.get("建築完成日期"))
        _共有部分 = [
            共有部分.from_dict(單一共有部分) for 單一共有部分 in data.get("共有部分")
        ]
        _主建物資料 = [
            主建物資料.from_dict(單一主建物資料)
            for 單一主建物資料 in data.get("主建物資料")
        ]
        _其他登記事項 = str(data.get("其他登記事項"))
        return 建物標示部(
            _登記日期,
            _登記原因,
            _建物坐落,
            _建物門牌,
            _主要用途,
            _主要建材,
            _層數,
            _層次,
            _附屬建物,
            _建築完成日期,
            _共有部分,
            _主建物資料,
            _其他登記事項,
        )


@dataclass
class BuildingRegistry:
    列印時間: int
    列印公司: str
    謄本種類碼: str
    謄本編號: str
    謄本核發機關: str
    資料管轄機關: str
    行政區: str
    地段: str
    小段: Optional[str]
    建號: str
    建物標示部: 建物標示部
    建物所有權部: List["建物所有權部"] = field(default_factory=list)
    建物他項權利部: List["建物他項權利部"] = field(default_factory=list)

    @staticmethod
    def from_dict(data: dict):
        _列印時間 = int(data.get("列印時間"))
        _列印公司 = str(data.get("列印公司"))
        _謄本種類碼 = str(data.get("謄本種類碼"))
        _謄本編號 = str(data.get("謄本編號"))
        _謄本核發機關 = str(data.get("謄本核發機關"))
        _資料管轄機關 = str(data.get("資料管轄機關"))
        _行政區 = str(data.get("行政區"))
        _地段 = str(data.get("地段"))
        _小段 = str(data.get("小段")) if data.get("小段") else None
        _建號 = str(data.get("建號"))
        _建物標示部 = 建物標示部.from_dict(data.get("建物標示部"))
        _建物所有權部 = [
            建物所有權部.from_dict(每ㄧ建物所有權)
            for 每ㄧ建物所有權 in data.get("建物所有權部")
        ]
        _建物他項權利部 = [
            建物他項權利部.from_dict(每ㄧ建物他項權利)
            for 每ㄧ建物他項權利 in data.get("建物他項權利部")
        ]
        return BuildingRegistry(
            _列印時間,
            _列印公司,
            _謄本種類碼,
            _謄本編號,
            _謄本核發機關,
            _資料管轄機關,
            _行政區,
            _地段,
            _小段,
            _建號,
            _建物標示部,
            _建物所有權部,
            _建物他項權利部,
        )
