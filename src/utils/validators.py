from marshmallow.fields import Integer
from marshmallow.validate import Range

page = Integer(validate=Range(min=1), missing=1)
