from dataclasses import dataclass
from typing import List
from src.modules.OpenDataManaging.dtos.LandDescriptor import LandDescriptor


@dataclass
class RetrievingLands:
    landDescriptors: List[LandDescriptor]
