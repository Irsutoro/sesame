import requests
import json
import pyaes
import hashlib
from base64 import b64encode, b64decode
class Client:
    def __init__(self):
        api_url = 'http://127.0.0.1:8080/api'
        self.user_service = api_url + '/user'
        self.password_service = api_url + '/password'
        self.auth_service = api_url + '/auth'
        self.user_info = None
        self.auth_info = None
        self.password = None
#TODO szyfrowanie rzeczy i hashowanie
#TODO lepsze wyjątki
    def login(self, username, password):
        auth_info = requests.auth.HTTPBasicAuth(username, password)
        response = requests.get(self.user_service, auth=auth_info)
        if response.ok:
            self.user_info = self._response_to_dict(response)
            self.auth_info = auth_info
            self.password = password
        else:
            raise ValueError()

    def register(self, username: str, password: str, email: str):
        response = requests.post(self.auth_service, json={'username': username, 'password': password, 'email': email})
        if not response.ok:
            raise ValueError()

    def get_password_labels(self):
        response = requests.get(self.password_service, auth=self.auth_info)
        if response.ok:
            return self._response_to_dict(response)
        else:
            raise ValueError()

    def get_password(self, label):
        response = requests.get(self.password_service + '/' + label, auth=self.auth_info)
        aes = pyaes.AESModeOfOperationCTR(hashlib.sha256(self.password.encode()).digest())
        if response.ok:
            password = aes.decrypt(b64decode(self._response_to_dict(response)[0]))
            print(password)
            return password.decode(), self._response_to_dict(response)[1]
        else:
            raise ValueError()

    def add_password(self, password, label, account_name):
        aes = pyaes.AESModeOfOperationCTR(hashlib.sha256(self.password.encode()).digest())
        cipher = b64encode(aes.encrypt(password)).decode()
        response = requests.post(self.password_service, auth=self.auth_info, json={'password': cipher, 'label': label, 'account_name': account_name})
        if not response.ok:
            raise ValueError()


    def _response_to_dict(self, response):
        return json.loads(response.content.decode())


if __name__ == '__main__':
    c = Client()
    c.login('maciek3001', 'passs')
    #print(c.user_info['email'])
    #c.register('maciek', 'zyga', 'zyga@maciek.pl')
    c.add_password('dupadupa123', 'aaa', 'zyga15')
    a = c.get_password('aaa')
    print(a)