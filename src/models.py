import peewee as pw
from typing import List
from datetime import date

class BaseModel(pw.Model):
    class Meta:
        database = pw.Proxy()

    @classmethod
    def connect(cls, database: pw.Database):
        cls._meta.database.initialize(database)

    @classmethod
    def models(cls) -> List[pw.Model]:
        return cls.__subclasses__()

class User(BaseModel):
    username = pw.FixedCharField(max_length=88, unique=True) #base64 of sha512
    password = pw.FixedCharField(max_length=88) #base64 of pbkdf2(sha512)
    server_salt = pw.FixedCharField(max_length=44) #base64 of 32 byte salt
    client_salt = pw.FixedCharField(max_length=44)
    email = pw.CharField(max_length=254, unique=True)
    registration_date = pw.DateField(default=date.today)
    activated = pw.BooleanField(default=False)
    secret = pw.FixedCharField(max_length=44)

class Password(BaseModel):
    user = pw.ForeignKeyField(model=User, backref='passwords')
    value = pw.CharField(max_length=128) #password in base64 (max 96 character password)
    label = pw.CharField(max_length=40) #user-defined identifier of site

class Device(BaseModel):
    identifier = pw.FixedCharField(max_length=44)
    users = pw.ManyToManyField(model=User, backref='devices')
