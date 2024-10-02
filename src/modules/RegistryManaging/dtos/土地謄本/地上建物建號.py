from typing import Optional, TypedDict


class 地上建物建號(TypedDict):
    地段: str
    小段: Optional[str]
    建號: str
