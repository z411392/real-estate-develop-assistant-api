from enum import Enum


class DataSheetTypes(str, Enum):
    AssessedCurrentLandValues = "assessedCurrentValues"
    ZoningClassifications = "zoningClassifications"

    def __str__(self):
        return self.value
