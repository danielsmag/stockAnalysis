from marshmallow import Schema, fields,validate


class kwSchema(Schema):
    kw= fields.List(fields.Str())

class PostKwSchema(Schema):
    kw = fields.List(fields.Str())

class UpdateData(Schema):
    timeframe = fields.List(fields.Str(validate=validate.OneOf(['past_7_days', 'past_30_days', 'past_3_month'])))

