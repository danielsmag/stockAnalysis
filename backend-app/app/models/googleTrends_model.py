from marshmallow import Schema, fields


class kwSchema(Schema):
    kw= fields.List(fields.Str())

class PostKwSchema(Schema):
    kw = fields.List(fields.Str())

