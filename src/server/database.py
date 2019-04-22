import peewee as pw
from typing import Dict

POSTGRES_SYSTEM = 'postgresql'
SQLITE_SYSTEM = 'sqlite'
IN_MEMORY_SQLITE = 'memory'

#TODO support for MySQL

def create_database(config: Dict[str, str]) -> pw.Database:
    try:
        system = config['System'].lower()
    except KeyError:
        raise KeyError('Key \'System\' is not found. You have to specify which database management system you want to use.')

    if system == POSTGRES_SYSTEM:
        db = _create_postgres_database(config)
    elif system == SQLITE_SYSTEM:
        db = _create_sqlite_database(config)
    elif system == IN_MEMORY_SQLITE:
        db = _create_in_memory_database()
    else:
        raise ValueError('System specified in config is not supported or misspelled')

    return db

def _create_postgres_database(config: Dict[str, str]) -> pw.Database:
    try:
        return pw.PostgresqlDatabase(
            database = config['Database'],
            user = config.get('Username'),
            password = config.get('Password'),
            host = config.get('Host'),
            port = int(config.get('Port')),
        )
    except KeyError:
        raise KeyError('You need to specify database name in \'Database\' parameter')

def _create_sqlite_database(config: Dict[str, str]) -> pw.Database:
    try:
        return pw.SqliteDatabase(config['Database'])
    except KeyError:
        raise KeyError('You need to specify database path in \'Database\' parameter')

def _create_in_memory_database() -> pw.Database:
    return pw.SqliteDatabase(':memory:')
