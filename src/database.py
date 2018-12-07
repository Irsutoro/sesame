import peewee as pw
from typing import Dict

POSTGRES_SYSTEM = 'postgresql'
SQLITE_SYSTEM = 'sqlite'
IN_MEMORY_SQLITE = 'memory'

#TODO wsparcie dla MySQL

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

#TODO implement methods for concrete database management systems

def _create_postgres_database(config: Dict[str, str]) -> pw.Database:
    return pw.Database(None)

def _create_sqlite_database(config: Dict[str, str]) -> pw.Database:
    return pw.Database(None)

def _create_in_memory_database() -> pw.Database:
    return pw.Database(None)
