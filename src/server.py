import peewee as pw

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
