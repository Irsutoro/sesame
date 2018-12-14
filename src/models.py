import peewee as pw
from typing import List
from datetime import date, datetime

class BaseModel(pw.Model):
    class Meta:
        database = pw.Proxy()

class User(BaseModel):
    username = pw.FixedCharField(max_length=88, unique=True) #base64 of sha512
    password = pw.FixedCharField(max_length=88) #base64 of pbkdf2(sha512)
    server_salt = pw.FixedCharField(max_length=44) #base64 of 32 byte salt
    email = pw.CharField(max_length=254, unique=True)
    registration_date = pw.DateField(default=date.today)
    activated = pw.BooleanField(default=False)
    secret = pw.FixedCharField(max_length=44)
    password_change_date = pw.DateField(default=date.today)

class EncryptingAlgorithm(BaseModel):
    name = pw.CharField(max_length=20)

class Password(BaseModel):
    user = pw.ForeignKeyField(model=User, backref='passwords')
    algorithm = pw.ForeignKeyField(model=EncryptingAlgorithm, backref='passwords')
    value = pw.CharField(max_length=128) #password in base64 (max 96 character password)
    label = pw.CharField(max_length=128) #user-defined identifier of site
    username = pw.CharField(max_length=128)
    modification_date = pw.DateField(default=date.today)

class DeviceType(BaseModel):
    name = pw.CharField(max_length=20)

class Device(BaseModel):
    type = pw.ForeignKeyField(model=DeviceType, backref='devices')
    identifier = pw.FixedCharField(max_length=44)

class UserDevice(BaseModel):
    user = pw.ForeignKeyField(model=User)
    device = pw.ForeignKeyField(model=Device)
    last_time_used = pw.DateTimeField(default=datetime.now)
    name = pw.CharField(max_length=20)
