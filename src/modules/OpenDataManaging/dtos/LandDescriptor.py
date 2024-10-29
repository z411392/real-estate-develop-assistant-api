from dataclasses import dataclass


@dataclass
class LandDescriptor:
    city: str
    administrativeDistrict: str
    section: str
    subsection: str
    parentLotNumber: str
    subLotNumber: str
