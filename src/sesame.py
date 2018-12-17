from server import Server
from models import BaseModel, User
import peewee as pw

PBKDF2_ITERATIONS = 100000

class Sesame(Server):
    def __init__(self, database: pw.Database):
        super().__init__(database, BaseModel)

    def register_user(self, username, password, email):
        salt = self._generate_salt(32)
        secret = self._generate_salt(32)
        hashed_password = self._hash_password(password, salt, PBKDF2_ITERATIONS)

        salt_in_base = self._bytes_to_base(salt)
        secret_in_base = self._bytes_to_base(secret)
        hash_in_base = self._bytes_to_base(hashed_password)

        #TODO catching exceptions
        User.create(username=username, password=hash_in_base, server_salt=salt_in_base, secret=secret_in_base, email=email)
