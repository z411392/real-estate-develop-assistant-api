from typing import List
from dataclasses import dataclass, field


@dataclass
class 共同擔保建號:
    地段: str
    小段: str
    建號: str

    @staticmethod
    def from_dict(obj: dict) -> "共同擔保建號":
        _地段 = str(obj.get("地段"))
        _小段 = str(obj.get("小段"))
        _建號 = str(obj.get("建號"))
        return 共同擔保建號(_地段, _小段, _建號)


@dataclass
class 共同擔保地號:
    地段: str
    小段: str
    地號: str

    @staticmethod
    def from_dict(obj: dict) -> "共同擔保地號":
        _地段 = str(obj.get("地段"))
        _小段 = str(obj.get("小段"))
        _地號 = str(obj.get("地號"))
        return 共同擔保地號(_地段, _小段, _地號)


@dataclass
class 土地他項權利部:
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

    @staticmethod
    def from_dict(obj: dict) -> "土地他項權利部":
        _登記次序 = str(obj.get("登記次序"))
        _權利種類 = str(obj.get("權利種類"))
        _收件日期 = str(obj.get("收件日期"))
        _字號 = str(obj.get("字號"))
        _登記日期 = str(obj.get("登記日期"))
        _登記原因 = str(obj.get("登記原因"))
        _權利人 = str(obj.get("權利人"))
        _統一編號 = str(obj.get("統一編號"))
        _住址 = str(obj.get("住址"))
        _債權額比例 = str(obj.get("債權額比例"))
        _擔保債權總金額 = str(obj.get("擔保債權總金額"))
        _擔保債權種類及範圍 = str(obj.get("擔保債權種類及範圍"))
        _擔保債權確定日期 = str(obj.get("擔保債權確定日期"))
        _償還日期 = str(obj.get("償還日期"))
        _存續期間 = str(obj.get("存續期間"))
        _利息或利率 = str(obj.get("利息或利率"))
        _遲延利息或利率 = str(obj.get("遲延利息或利率"))
        _違約金 = str(obj.get("違約金"))
        _其他擔保範圍約定 = str(obj.get("其他擔保範圍約定"))
        _權利標的 = str(obj.get("權利標的"))
        _標的登記次序 = [標的登記次序 for 標的登記次序 in obj.get("標的登記次序")]
        _設定權利範圍 = str(obj.get("設定權利範圍"))
        _證明書字號 = str(obj.get("證明書字號"))
        _共同擔保地號 = [
            共同擔保地號.from_dict(每一共同擔保地號)
            for 每一共同擔保地號 in obj.get("共同擔保地號")
        ]
        _共同擔保建號 = [
            共同擔保建號.from_dict(每一共同擔保建號)
            for 每一共同擔保建號 in obj.get("共同擔保建號")
        ]
        _其他登記事項 = str(obj.get("其他登記事項"))
        return 土地他項權利部(
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
            _共同擔保地號,
            _共同擔保建號,
            _其他登記事項,
        )


@dataclass
class 土地所有權部:
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

    @staticmethod
    def from_dict(obj: dict) -> "土地所有權部":
        _登記次序 = str(obj.get("登記次序"))
        _登記日期 = str(obj.get("登記日期"))
        _登記原因 = str(obj.get("登記原因"))
        _原因發生日期 = str(obj.get("原因發生日期"))
        _所有權人 = str(obj.get("所有權人"))
        _統一編號 = str(obj.get("統一編號"))
        _住址 = str(obj.get("住址"))
        _權利範圍 = str(obj.get("權利範圍"))
        _權狀字號 = str(obj.get("權狀字號"))
        _當期申報地價年月 = str(obj.get("當期申報地價年月"))
        _當期申報地價 = int(obj.get("當期申報地價"))
        _前次移轉現值或原規定地價年月 = str(obj.get("前次移轉現值或原規定地價年月"))
        _前次移轉現值或原規定地價 = int(obj.get("前次移轉現值或原規定地價"))
        _歷次取得權利範圍 = str(obj.get("歷次取得權利範圍"))
        _相關他項權利登記次序 = [
            相關他項權利登記次序
            for 相關他項權利登記次序 in obj.get("相關他項權利登記次序")
        ]
        _其他登記事項 = str(obj.get("其他登記事項"))
        return 土地所有權部(
            _登記次序,
            _登記日期,
            _登記原因,
            _原因發生日期,
            _所有權人,
            _統一編號,
            _住址,
            _權利範圍,
            _權狀字號,
            _當期申報地價年月,
            _當期申報地價,
            _前次移轉現值或原規定地價年月,
            _前次移轉現值或原規定地價,
            _歷次取得權利範圍,
            _相關他項權利登記次序,
            _其他登記事項,
        )


@dataclass
class 地上建物建號:
    地段: str
    小段: str
    建號: str

    @staticmethod
    def from_dict(obj: dict) -> "地上建物建號":
        _地段 = str(obj.get("地段"))
        _小段 = str(obj.get("小段"))
        _地號 = str(obj.get("地號"))
        return 地上建物建號(_地段, _小段, _地號)


@dataclass
class 土地標示部:
    登記日期: str
    登記原因: str
    面積: int
    使用分區: str
    使用地類別: str
    公告土地現值年月: str
    公告土地現值: int
    地上建物建號: List[地上建物建號]
    其他登記事項: str

    @staticmethod
    def from_dict(obj: dict) -> "土地標示部":
        _登記日期 = str(obj.get("登記日期"))
        _登記原因 = str(obj.get("登記原因"))
        _面積 = int(obj.get("面積"))
        _使用分區 = str(obj.get("使用分區"))
        _使用地類別 = str(obj.get("使用地類別"))
        _公告土地現值年月 = str(obj.get("公告土地現值年月"))
        _公告土地現值 = int(obj.get("公告土地現值"))
        _地上建物建號 = [
            地上建物建號.from_dict(單一地上建物建號)
            for 單一地上建物建號 in obj.get("地上建物建號")
        ]
        _其他登記事項 = str(obj.get("其他登記事項"))
        return 土地標示部(
            _登記日期,
            _登記原因,
            _面積,
            _使用分區,
            _使用地類別,
            _公告土地現值年月,
            _公告土地現值,
            _地上建物建號,
            _其他登記事項,
        )


@dataclass
class LandRegistry:
    列印時間: int
    列印公司: str
    謄本種類碼: str
    謄本編號: str
    謄本核發機關: str
    資料管轄機關: str
    行政區: str
    地段: str
    小段: str
    地號: str
    土地標示部: List[土地標示部]
    土地所有權部: List["土地所有權部"] = field(default_factory=list)
    土地他項權利部: List["土地他項權利部"] = field(default_factory=list)

    @staticmethod
    def from_dict(obj: dict) -> "LandRegistry":
        _列印時間 = int(obj.get("列印時間"))
        _列印公司 = str(obj.get("列印公司"))
        _謄本種類碼 = str(obj.get("謄本種類碼"))
        _謄本編號 = str(obj.get("謄本編號"))
        _謄本核發機關 = str(obj.get("謄本核發機關"))
        _資料管轄機關 = str(obj.get("資料管轄機關"))
        _行政區 = str(obj.get("行政區"))
        _地段 = str(obj.get("地段"))
        _小段 = str(obj.get("小段"))
        _地號 = str(obj.get("地號"))
        _土地標示部 = [
            土地標示部.from_dict(每ㄧ土地標示) for 每ㄧ土地標示 in obj.get("土地標示部")
        ]
        _土地所有權部 = [
            土地所有權部.from_dict(每ㄧ土地所有權)
            for 每ㄧ土地所有權 in obj.get("土地所有權部")
        ]
        _土地他項權利部 = [
            土地他項權利部.from_dict(每ㄧ土地他項權利)
            for 每ㄧ土地他項權利 in obj.get("土地他項權利部")
        ]
        return LandRegistry(
            _列印時間,
            _列印公司,
            _謄本種類碼,
            _謄本編號,
            _謄本核發機關,
            _資料管轄機關,
            _行政區,
            _地段,
            _小段,
            _地號,
            _土地標示部,
            _土地所有權部,
            _土地他項權利部,
        )
