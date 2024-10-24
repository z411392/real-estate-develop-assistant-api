from dataclasses import dataclass
from typing import Optional


@dataclass
class Land:
    city: str
    administrativeDistrict: str
    section: str
    subsection: str
    parentLotNumber: str
    subLotNumber: str
    year: int
    zoningClassification: Optional[str]
    assessedCurrentValue: Optional[int]

    @staticmethod
    def from_dict(data: dict):
        return Land(
            zoningClassification=(
                str(data.get("zoningClassification"))
                if data.get("zoningClassification")
                else None
            ),
            assessedCurrentValue=(
                int(data.get("assessedCurrentValue"))
                if data.get("assessedCurrentValue")
                else None
            ),
        )
