import peewee as pw
import hashlib
import os
from base64 import b64decode, b64encode
from typing import List

class Server:

    def __init__(self, database: pw.Database, base_model: pw.Model):
        self.database = None
        self.base_model = base_model
        self.connect_to_database(database)

    def create_tables(self):
        self.database.create_tables(self.models())

    def connect_to_database(self, database: pw.Database):
        self.database = database
        self._initialize_proxy()

    def models(self) -> List[pw.Model]:
        return self.base_model.__subclasses__()

    def _initialize_proxy(self):
        self.base_model._meta.database.initialize(self.database)

    @staticmethod
    def _generate_salt(length: int) -> bytes:
        salt = os.urandom(length)
        return salt

    @staticmethod
    def _hash_password(password: str, salt: bytes, iterations: int, algorithm: str) -> bytes:
        hashed_password = hashlib.pbkdf2_hmac(algorithm, password.encode(), salt, iterations)
        return hashed_password

    @staticmethod
    def _bytes_to_base(value: bytes) -> str:
        result = b64encode(value).decode()
        return result

    @staticmethod
    def _base_to_bytes(value: str) -> bytes:
        result = b64decode(value)
        return result