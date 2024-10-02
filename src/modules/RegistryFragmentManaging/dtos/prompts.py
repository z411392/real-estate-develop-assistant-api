解析土地基本資訊 = """請按照土地基本資訊的 typescript 型別，將資料轉換成 JSON Object 給我：
```typescript
type 土地基本資訊 = {
    列印時間: string
    列印公司: string
    謄本種類碼: string
    謄本編號: string
    謄本核發機關: string
    資料管轄機關: string
    行政區: string
    地段: string
    小段?: string // 若無請填寫「空白」
    地號: string // 請移除「地號」字樣
}
```
注意：
- 譬如「北投區立農段二小段0028-0000地號」，行政區是「北投區」，地段是「立農段」，小段是「二小段」，地號是「0028-0000」。
- 地段不會有「區」
"""

解析土地標示 = """請按照土地標示的 typescript 型別，將資料轉換成 JSON Object 給我：
```typescript
type 地上建物建號 = {
    地段: string
    小段?: string // 若無請填寫「空白」
    建號: string // 請移除「建號」字樣
}

type 土地標示 = {
    登記日期: string
    登記原因: string
    面積: string // 請換算為平方公尺並只保留數值部分最後用字串儲存
    使用分區: string
    使用地類別: string|null
    公告土地現值年月: string
    公告土地現值: number // 請換算為「每平方公尺」並只保留數值
    地上建物建號: 地上建物建號[]
    其他登記事項: string
}
```
注意：
- 譬如「大安區仁愛段一小段03493-000建號」，行政區是「大安區」，地段是「仁愛段」，小段是「一小段」，地號是「03493-000」。
- 地段不會有「區」
"""

解析土地所有權 = """請按照土地所有權的 typescript 型別，將資料轉換成 JSON Object 給我：
```typescript
type 土地所有權 = {
    登記次序: string
    登記日期: string
    登記原因: string
    原因發生日期: string
    所有權人: string|null
    統一編號: string|null
    住址: string|null
    權利範圍: string|null // 譬如「10000分之215」請表示為「215/10000」。如果有「全部」的字樣請直接去除，並表示為「1/1」
    權狀字號: string|null
    當期申報地價年月: string
    當期申報地價: number|null // 請換算為「每平方公尺」並只保留數值
    前次移轉現值或原規定地價年月: string
    前次移轉現值或原規定地價: number|null // 請換算為「每平方公尺」並只保留數值
    歷次取得權利範圍: string|null // 譬如「10000分之215」請表示為「215/10000」。如果有「全部」的字樣請直接去除，並表示為「1/1」
    相關他項權利登記次序: string[]
    其他登記事項: string
}
```
"""

解析土地他項權利 = """請按照土地他項權利的 typescript 型別，將資料轉換成 JSON Object 給我：
```typescript
type 共同擔保建號 = {
    地段: string
    小段?: string
    建號: string
}

type 共同擔保地號 = {
    地段: string
    小段?: string
    地號: string
}

type 土地他項權利 = {
    登記次序: string
    權利種類: string
    收件日期: string
    字號: string
    登記日期: string
    登記原因: string
    權利人: string|null
    統一編號: string|null
    住址: string|null
    債權額比例: string|null
    擔保債權總金額: string|null
    擔保債權種類及範圍: string|null // 譬如「10000分之215」請表示為「215/10000」。如果有「全部」的字樣請直接去除，並表示為「1/1」
    擔保債權確定日期: string|null
    償還日期: string|null
    存續期間: string|null
    利息或利率: string|null
    遲延利息或利率: string|null
    違約金: number|null
    其他擔保範圍約定: string|null
    權利標的: string|null
    標的登記次序: string[]
    設定權利範圍: string|null // 譬如「10000分之215」請表示為「215/10000」。如果有「全部」的字樣請直接去除，並表示為「1/1」
    證明書字號: string|null
    共同擔保地號: 共同擔保地號[]
    共同擔保建號: 共同擔保建號[]
    其他登記事項: string
}
```
注意：
- 譬如「北投區立農段二小段0028-0000地號」，行政區是「北投區」，地段是「立農段」，小段是「二小段」，地號是「0028-0000」。
- 譬如「大安區仁愛段一小段03493-000建號」，行政區是「大安區」，地段是「仁愛段」，小段是「一小段」，地號是「03493-000」。
- 地段不會有「區」
"""


解析建物基本資訊 = """請按照建物基本資訊的 typescript 型別，將資料轉換成 JSON Object 給我：
```typescript
type 建物基本資訊 = {
    列印時間: string
    列印公司: string
    謄本種類碼: string
    謄本編號: string
    謄本核發機關: string
    資料管轄機關: string
    行政區: string
    地段: string
    小段?: string
    建號: string
}
```
注意：
- 譬如「大安區仁愛段一小段03493-000建號」，行政區是「大安區」，地段是「仁愛段」，小段是「一小段」，地號是「03493-000」。
- 地段不會有「區」
"""

解析建物標示 = """請按照建物標示的 typescript 型別，將資料轉換成 JSON Object 給我：
```typescript
type 主建物資料 = {
    地段: string
    小段?: string
    建號: string
    權利範圍: string
}

type 共有部分 = {
    地段: string
    小段?: string
    建號: string
    面積: string
    權利範圍: string // 譬如「10000分之215」請表示為「215/10000」。如果有「全部」的字樣請直接去除，並表示為「1/1」
    其他登記事項: string
}

type 附屬建物 = {
    附屬建物類型: string
    面積: string // 請換算為平方公尺並只保留數值部分最後用字串儲存
}

type 層次 = {
    層次: number // 請轉換為阿拉伯數字（譬如「三層」請轉換為「3」如為「地下三層」請轉為-3）
    層次面積: string // 請換算為平方公尺並只保留數值部分最後用字串儲存
    總面積: string // 請換算為平方公尺並只保留數值部分最後用字串儲存
}

type 建物坐落 = {
    地段: string
    小段?: string
    地號: string
}

type 建物標示 = {
    登記日期: string
    登記原因: string
    建物坐落: 建物坐落[]
    建物門牌: string
    主要用途: string
    主要建材: string
    層數: number // 請轉為阿拉伯數字
    層次: 層次[]
    附屬建物: 附屬建物[]
    建築完成日期: string
    共有部分: 共有部分[]
    主建物資料: 主建物資料[]
    其他登記事項: string
}
```
注意：
- 譬如「北投區立農段二小段0028-0000地號」，行政區是「北投區」，地段是「立農段」，小段是「二小段」，地號是「0028-0000」。
- 譬如「大安區仁愛段一小段03493-000建號」，行政區是「大安區」，地段是「仁愛段」，小段是「一小段」，地號是「03493-000」。
"""

解析建物所有權 = """請按照建物所有權的 typescript 型別，將資料轉換成 JSON Object 給我：
```typescript
type 建物所有權 = {
    登記次序: string
    登記日期: string
    登記原因: string
    原因發生日期: string|null
    所有權人: string|null
    統一編號: string|null
    住址: string|null
    權利範圍: string|null // 譬如「10000分之215」請表示為「215/10000」。如果有「全部」的字樣請直接去除，並表示為「1/1」
    權狀字號: string|null
    建物他項權利登記次序: string[]
    其他登記事項: string
}
```"""

解析建物他項權利 = """請按照建物他項權利的 typescript 型別，將資料轉換成 JSON Object 給我：
```typescript
type 共同擔保建物 = {
    地段: string
    小段?: string
    建號: string
}

type 共同擔保土地 = {
    地段: string
    小段?: string
    地號: string
}

type 建物他項權利 = {
    登記次序: string
    權利種類: string
    收件日期: string
    字號: string
    登記日期: string
    登記原因: string
    權利人: string|null
    統一編號: string|null
    住址: string|null
    債權額比例: string|null
    擔保債權總金額: number|null
    擔保債權種類及範圍: string|null // 譬如「10000分之215」請表示為「215/10000」。如果有「全部」的字樣請直接去除，並表示為「1/1」
    擔保債權確定日期: string
    償還日期: string
    利息或利率: string|null
    遲延利息或利率: string|null
    違約金: number|null
    其他擔保範圍約定: string|null // 譬如「10000分之215」請表示為「215/10000」。如果有「全部」的字樣請直接去除，並表示為「1/1」
    權利標的: string|null
    標的登記次序: string[]
    設定權利範圍: string|null // 譬如「10000分之215」請表示為「215/10000」。如果有「全部」的字樣請直接去除，並表示為「1/1」
    證明書字號: string|null
    共同擔保土地: 共同擔保土地[]
    共同擔保建物: 共同擔保建物[]
    其他登記事項: string
}
```
注意：
- 譬如「北投區立農段二小段0028-0000地號」，行政區是「北投區」，地段是「立農段」，小段是「二小段」，地號是「0028-0000」。
- 譬如「大安區仁愛段一小段03493-000建號」，行政區是「大安區」，地段是「仁愛段」，小段是「一小段」，地號是「03493-000」。
"""
