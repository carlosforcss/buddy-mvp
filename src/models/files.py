from tortoise import fields, Model


class File(Model):
    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=255)
    bucket = fields.CharField(max_length=255) 