import json

from peewee import (Proxy,
                    IntegerField, BlobField, DateTimeField,
                    ForeignKeyField, CharField, TextField)
from playhouse.db_url import connect
from playhouse.shortcuts import model_to_dict
from playhouse.signals import Model
from datetime import datetime

from ..common.utils import json_serial


database = Proxy()


def models_init(dsn):
    db = connect(dsn)
    if 'sqlite' in dsn:
        db.pragma('foreign_keys', 1, permanent=True)
    database.initialize(db)
    db.create_tables([m for m in BaseModel.__subclasses__()])


class BaseModel(Model):
    class Meta:
        database = database

    def __str__(self):
        return json.dumps(model_to_dict(self), indent=2,
                          default=json_serial)


class PublicKey(BaseModel):
    e = IntegerField()
    n = BlobField()

    class Meta(BaseModel._meta.__class__):
        table_name = 'public_keys'


class PrivateKey(BaseModel):
    d = BlobField()
    p = BlobField()
    q = BlobField()

    class Meta(BaseModel._meta.__class__):
        table_name = 'private_keys'


class User(BaseModel):
    cloud_id = IntegerField(unique=True)
    name = CharField(unique=True)
    password = CharField()
    public_key = ForeignKeyField(PublicKey, on_delete='CASCADE')
    private_key = ForeignKeyField(PrivateKey, on_delete='CASCADE')
    created_at = DateTimeField(default=datetime.now)

    class Meta(BaseModel._meta.__class__):
        table_name = 'users'


class Message(BaseModel):
    cloud_id = IntegerField(null=True)
    user_from_name = TextField()
    user_to_name = TextField()
    data = TextField()
    status = IntegerField()
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)

    class Meta(BaseModel._meta.__class__):
        table_name = 'messages'
