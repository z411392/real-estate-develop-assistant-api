from enum import Enum


class Prompts(str, Enum):
    BuildingRegistryParsing = """請按照這樣的 typescript 型別(BuildingRegistry)，將待會收到的建物謄本轉為 JSON 給我：
```typescript
type 共同擔保建物 = {
    地段: string
    小段: string
    建號: string
}

type 共同擔保土地 = {
    地段: string
    小段: string
    地號: string
}

export type 建物他項權利部 = {
    登記次序: string
    權利種類: string
    收件日期: string
    字號: string
    登記日期: string
    登記原因: string
    權利人: string
    統一編號: string
    住址: string
    債權額比例: string
    擔保債權總金額: string
    擔保債權種類及範圍: string
    擔保債權確定日期: string
    償還日期: string
    利息或利率: string
    遲延利息或利率: string
    違約金: string
    其他擔保範圍約定: string
    權利標的: string
    標的登記次序: string[]
    設定權利範圍: string
    證明書字號: string
    共同擔保土地: 共同擔保土地[]
    共同擔保建物: 共同擔保建物[]
    其他登記事項: string
}

export type 建物所有權部 = {
    登記次序: string
    登記日期: string
    登記原因: string
    原因發生日期: string
    所有權人: string
    統一編號: string
    住址: string
    權利範圍: string
    權狀字號: string
    建物他項權利登記次序: string[]
    其他登記事項: string
}

type 主建物資料 = {
    地段: string
    小段: string
    建號: string
    權利範圍: string
}

type 共有部分 = {
    地段: string
    小段: string
    建號: string
    面積: number
    權利範圍?: string
    其他登記事項: string
}

type 附屬建物 = {
    附屬建物類型: string
    面積: number
}

type 層次 = {
    層次: number
    層次面積: number
    總面積: number
}

type 建物坐落 = {
    地段: string
    小段: string
    地號: string
}

type 建物標示部 = {
    登記日期: string
    登記原因: string
    建物坐落: 建物坐落[]
    建物門牌: string
    主要用途: string
    主要建材: string
    層數: string
    層次: 層次[]
    附屬建物: 附屬建物[]
    建築完成日期: string
    共有部分: 共有部分[]
    主建物資料: 主建物資料[]
    其他登記事項: string
}

export type BuildingRegistry = {
    列印時間: number
    列印公司: string
    謄本種類碼: string
    謄本編號: string
    謄本核發機關: string
    資料管轄機關: string
    行政區: string
    地段: string
    小段: string
    建號: string
    建物標示部: 建物標示部
    建物所有權部: 建物所有權部[]
    建物他項權利部: 建物他項權利部[]
}
```
並請注意：
1. 如果內容是面積，請換算為平方公尺並只保留數值。
2. 如果有全形的數字、符號，請轉為半形。
3. 如果含有中文的次序、分數，請轉為阿拉伯數字及數學式。
4. 如果內容是日期，請轉換為 %Y-%m-%d 的形式。
5. 如果內容是時間，請轉為 unix timestamp 的形式。
6. 若有可能有多筆資料但無資料時，請視為空陣列。
7. 範圍的幾分之幾請轉換為數學表達式，譬如「10000分之215」請表示為「215/10000」。
8. 範圍如果有「全部」的字樣請直接去除。
9. 層次請轉換為阿拉伯數字（譬如「三層」請轉換為「3」，如為「地下三層」請轉為-3，如果為「地下層」請轉為「-1」）。
10. 層數請轉為阿拉伯數字。
11. 地段和小段分開，譬如「大安區仁愛段一小段 03493-000建號」請分成「仁愛段」及「一小段」。
12. 行政區如「大安區仁愛段一小段 03493-000建號」，請只保留「大安區」的部分。
13. 請保留完整建號，如「03505-000」，請記為「03505-000」。
14. 請將全形的阿拉伯數字及符號全轉為半形。"""

    LandRegistryParsing = """請按照這樣的 typescript 型別(LandRegistry)，將待會收到的土地謄本轉為 JSON 給我：
```typescript
type 共同擔保建號 = {
    地段: string
    小段: string
    建號: string
}

type 共同擔保地號 = {
    地段: string
    小段: string
    地號: string
}

export type 土地他項權利部 = {
    登記次序: string
    權利種類: string
    收件日期: string
    字號: string
    登記日期: string
    登記原因: string
    權利人: string
    統一編號: string
    住址: string
    債權額比例: string
    擔保債權總金額: string
    擔保債權種類及範圍: string
    擔保債權確定日期: string
    償還日期: string
    存續期間: string
    利息或利率: string
    遲延利息或利率: string
    違約金: string
    其他擔保範圍約定: string
    權利標的: string
    標的登記次序: string[]
    設定權利範圍: string
    證明書字號: string
    共同擔保地號: 共同擔保地號[]
    共同擔保建號: 共同擔保建號[]
    其他登記事項: string
}

export type 土地所有權部 = {
    登記次序: string
    登記日期: string
    登記原因: string
    原因發生日期: string
    所有權人: string
    統一編號: string
    住址: string
    權利範圍: string
    權狀字號: string
    當期申報地價年月: string
    當期申報地價: number
    前次移轉現值或原規定地價年月: string
    前次移轉現值或原規定地價: number
    歷次取得權利範圍: string
    相關他項權利登記次序: string[]
    其他登記事項: string
}

type 地上建物建號 = {
    地段: string
    小段: string
    建號: string
}

export type 土地標示部 = {
    登記日期: string
    登記原因: string
    面積: number
    使用分區: string
    使用地類別: string
    公告土地現值年月: string
    公告土地現值: number
    地上建物建號: 地上建物建號[]
    其他登記事項: string
}

export type LandRegistry = {
    列印時間: number
    列印公司: string
    謄本種類碼: string
    謄本編號: string
    謄本核發機關: string
    資料管轄機關: string
    行政區: string
    地段: string
    小段: string
    地號: string
    土地標示部: 土地標示部[]
    土地所有權部: 土地所有權部[]
    土地他項權利部: 土地他項權利部[]
}
```
並請注意：
1. 公告土地現值、當期申報地價、移轉現值或原規定地價，請換算為「每平方公尺」並只保留數值。
2. 如果有全形的數字、符號，請轉為半形。
3. 如果含有中文的次序、分數，請轉為阿拉伯數字及數學式。
4. 如果內容是日期，請轉換為 %Y-%m-%d 的形式，如果僅有年月，請補充日期為 01（請將民國年轉為西元年）。
5. 如果內容是時間，請轉為 unix timestamp 的形式。
6. 若有可能有多筆資料但無資料時，請視為空陣列。
7. 範圍的幾分之幾請轉換為數學表達式，譬如「10000分之215」請表示為「215/10000」。
8. 如果有「全部」的字樣請直接去除。
9. 地段和小段分開，譬如「北投區立農段二小段 0028-000地號」請分成「立農段」及「二小段」。
10. 行政區如「北投區立農段二小段 0028-000地號」，請只保留「北投區」的部分。
11. 請保留完整建號，如「0028-000」，請記為「0028-000」。
12. 請將全形的阿拉伯數字及符號全轉為半形。
13. 面積請轉為平方公尺並只保留數值。"""

    def __str__(self):
        return self.value
