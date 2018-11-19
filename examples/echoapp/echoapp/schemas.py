from webargs import fields, validate


hello_args = {"name": fields.Str(missing="Friend")}

add_args = {"x": fields.Float(required=True), "y": fields.Float(required=True)}

dateadd_args = {
    "value": fields.Date(required=False),
    "addend": fields.Int(required=True, validate=validate.Range(min=1)),
    "unit": fields.Str(missing="days", validate=validate.OneOf(["minutes", "days"])),
}
