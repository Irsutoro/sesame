import peewee as pw
from typing import List

class BaseModel(pw.Model):
    class Meta:
        database = pw.Proxy()

    @classmethod
    def connect(cls, database: pw.Database):
        cls._meta.database.initialize(database)

    @classmethod
    def models(cls) -> List[pw.Model]:
        return cls.__subclasses__()