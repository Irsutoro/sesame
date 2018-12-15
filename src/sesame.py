from server import Server
from models import BaseModel, User
import peewee as pw
import os
from base64 import b64decode, b64encode
import hashlib

PBKDF2_ITERATIONS = 100000

class Sesame(Server):
    def __init__(self, database: pw.Database):
        super().__init__(database, BaseModel)

    def register_user(self, username, password, email):
        salt = self._generate_salt(32)
        secret = self._generate_salt(32)
        hashed_password = self._hash_password(password, salt)

        salt_in_base = self._bytes_to_base(salt)
        secret_in_base = self._bytes_to_base(secret)
        hash_in_base = self._bytes_to_base(hashed_password)

        #TODO catching exceptions
        User.create(username=username, password=hash_in_base, server_salt=salt_in_base, secret=secret_in_base, email=email)

    def _generate_salt(self, length=32):
        salt = os.urandom(length)
        return salt

    def _hash_password(self, password, salt, iterations=PBKDF2_ITERATIONS):
        hashed_password = hashlib.pbkdf2_hmac('sha512', password.encode(), salt, iterations)
        return hashed_password

    def _bytes_to_base(self, bytes):
        base = b64encode(bytes).decode()
        return base

    def _base_to_bytes(self, base):
        bytes = b64decode(base)
        return bytes