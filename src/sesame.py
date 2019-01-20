from server import Server
from models import BaseModel, User, EncryptingAlgorithm, Password
import peewee as pw

PBKDF2_ITERATIONS = 100000
PBKDF2_ALGORITHM = 'sha512'
SALT_LENGTH = 32

class Sesame(Server):
    def __init__(self, database: pw.Database):
        super().__init__(database, BaseModel)

    def register_user(self, username: str, password: str, email: str):
        salt = self._generate_salt(SALT_LENGTH)
        secret = self._generate_salt(SALT_LENGTH)
        hashed_password = self._hash_password(password, salt, PBKDF2_ITERATIONS, PBKDF2_ALGORITHM)

        salt_in_base = self._bytes_to_base(salt)
        secret_in_base = self._bytes_to_base(secret)
        hash_in_base = self._bytes_to_base(hashed_password)

        #TODO catching exceptions
        try:
            User.create(username=username, password=hash_in_base, salt=salt_in_base, secret=secret_in_base, email=email)
        except pw.IntegrityError:
            raise ValueError('User Already Exists')

    def authorize_user(self, username: str, password: str):
        user = User.get_or_none(username=username)
        if user:
            salt = self._base_to_bytes(user.salt)
            hashed_password = self._hash_password(password, salt, PBKDF2_ITERATIONS, PBKDF2_ALGORITHM)
            return hashed_password == self._base_to_bytes(user.password)
        return False

    def activate_user(self, username: str):
        query = User.update(activated=True).where(User.username == username)
        query.execute()

    def get_user_info(self, username: str):
        user = User.get_or_none(username=username)
        return {
            'username': username,
            'email': user.email,
            'registration_date': user.registration_date.strftime('%d/%m/%Y'),
            'password_change_date': user.password_change_date.strftime('%d/%m/%Y'),
        }

    def add_encrypting_algorithm(self, name: str):
        EncryptingAlgorithm.create(name=name)

    def add_password(self, username: str, algorithm_name: str, password: str, label: str, account_name: str):
        user = User.get(User.username == username)
        algorithm = EncryptingAlgorithm.get(EncryptingAlgorithm.name == algorithm_name)
        Password.create(user=user, algorithm=algorithm, value=password, label=label, username=account_name)

    def get_password(self, username: str, label: str):
        user = User.get(User.username == username)
        passw = Password.get(user=user, label=label)
        return passw.value, passw.algorithm.name

    def get_password_labels(self, username: str):
        user = User.get(User.username == username)
        passw = Password.select().where(Password.user==user).dicts()
        result = [row['value'] for row in passw]
        return result

