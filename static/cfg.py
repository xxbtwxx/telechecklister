env = 'debug'
key = 'somekey'

db_cfg = { 
    'debug': {
        'user': 'root',
        'password': 'pass',
        'host': 'localhost',
        'database': 'database',
        'raise_on_warnings': True,
    }, 'production': {
        'user': 'root',
        'password': 'pass',
        'host': 'some.host',
        'database': 'database',
        'raise_on_warnings': True,
    }
}
