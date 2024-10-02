from marshmallow.fields import String
from marshmallow.validate import Regexp, NoneOf, ContainsNoneOf

行政區 = String(required=True, validate=ContainsNoneOf("段"))
地段 = String(required=True, validate=ContainsNoneOf("區"))
小段 = String(required=True, validate=NoneOf(["", "null", "None", "undefined"]))
編號 = String(
    required=True,
    validate=Regexp(r"^\d+-\d+$"),
)
範圍 = String(
    required=True,
    validate=Regexp(r"^\d+/\d+$"),
)
