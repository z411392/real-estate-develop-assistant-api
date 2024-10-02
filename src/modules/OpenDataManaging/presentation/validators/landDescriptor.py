from marshmallow.fields import String, List, Nested
from marshmallow import Schema

city = String(
    required=True,
)
administrativeDistrict = String(
    required=True,
)
section = String(
    required=True,
)
subsection = String(
    required=True,
)
parentLotNumber = String(
    required=True,
)
subLotNumber = String(
    required=True,
)
landDescriptor = Schema.from_dict(
    dict(
        city=city,
        administrativeDistrict=administrativeDistrict,
        section=section,
        subsection=subsection,
        parentLotNumber=parentLotNumber,
        subLotNumber=subLotNumber,
    )
)

landDescriptors = List(Nested(landDescriptor))
