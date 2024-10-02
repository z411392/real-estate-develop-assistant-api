from typing import Optional, TypedDict


class Land(TypedDict):
    city: str
    administrativeDistrict: str
    section: str
    subsection: str
    parentLotNumber: str
    subLotNumber: str
    year: int
    zoningClassification: Optional[str]
    assessedCurrentValue: Optional[int]
