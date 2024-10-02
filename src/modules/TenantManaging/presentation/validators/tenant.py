from marshmallow.fields import String
from marshmallow.validate import Length

name = String(validate=Length(1, 15), required=True)
