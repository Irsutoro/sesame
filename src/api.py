import cherrypy
import sesame
from database import create_database

DATABASE = create_database({'System':'sqlite', 'Database':'testy.db'})
SERVER = None

def validate_password(realm, login, password):
    #TODO autoryzacja JWT
    return SERVER.authorize_user(login, password)

CHERRYPY_CONFIG = {
    'server.socket_host': '127.0.0.1',
    'server.socket_port': 8080,
    'tools.auth_basic.on': True,
    'tools.auth_basic.realm': '127.0.0.1',
    'tools.auth_basic.checkpassword': validate_password,
}

def get_user_login():
    return cherrypy.request.login

@cherrypy.expose
class AuthService:
#TODO aktywacja konta

    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def GET(self):
        request = cherrypy.request.json
        #TODO zmiana na zwracanie JWT
        try:
            auth_successful = SERVER.authorize_user(request['login'], request['password'])
        except KeyError:
            raise cherrypy.HTTPError(400)
        if auth_successful:
            #TODO zwrot JWT
            return 'Authorized'
        else:
            raise cherrypy.HTTPError(401)

    @cherrypy.tools.json_in()
    def POST(self):
        request = cherrypy.request.json
        try:
            SERVER.register_user(request['username'], request['password'], request['email'])
        except ValueError:
            raise cherrypy.HTTPError(409, 'Username or email is already used')
        except KeyError:
            raise cherrypy.HTTPError(400)


@cherrypy.expose
class UserService:

    @cherrypy.tools.json_out()
    def GET(self):
        return SERVER.get_user_info(get_user_login())

@cherrypy.expose
class PasswordService:

    @cherrypy.tools.json_out()
    def GET(self, label:str=None):
        user = get_user_login()
        if label:
            return SERVER.get_password(user, label)
        else:
            return SERVER.get_password_labels(user)

    @cherrypy.tools.json_in()
    def POST(self):
        request = cherrypy.request.json
        try:
            SERVER.add_password(get_user_login(), 'AES128', request['password'], request['label'], request['account_name'])
        except KeyError:
            raise cherrypy.HTTPError(400)



if __name__ == '__main__':
    WITHOUT_AUTHENTICATION = {'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher(), 'tools.auth_basic.on': False}}
    WITH_AUTHENTICATION = {'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}}
    SERVER = sesame.Sesame(DATABASE)
    SERVER.create_tables()
    SERVER.add_encrypting_algorithm('AES128')
    cherrypy.config.update(CHERRYPY_CONFIG)
    cherrypy.tree.mount(UserService(), '/api/user', WITH_AUTHENTICATION)
    cherrypy.tree.mount(AuthService(), '/api/auth', WITHOUT_AUTHENTICATION)

    cherrypy.engine.start()
    cherrypy.engine.block()
