import peewee as pw
import hashlib
import os
from base64 import b64decode, b64encode

class Server:

    def __init__(self, database: pw.Database, base_model: pw.Model):
        self.database = database
        self.base_model = base_model
        self._initialize_proxy()

    def create_tables(self):
        self.database.create_tables(self.models())

    def models(self):
        return self.base_model.__subclasses__()

    def _initialize_proxy(self):
        self.base_model._meta.database.initialize(self.database)

    @staticmethod
    def _generate_salt(length=32):
        salt = os.urandom(length)
        return salt

    @staticmethod
    def _hash_password(password, salt, iterations, algorithm='sha512'):
        hashed_password = hashlib.pbkdf2_hmac(algorithm, password.encode(), salt, iterations)
        return hashed_password

    @staticmethod
    def _bytes_to_base(bytes):
        base = b64encode(bytes).decode()
        return base

    @staticmethod
    def _base_to_bytes(base):
        bytes = b64decode(base)
        return bytes