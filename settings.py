import os

from decouple import config


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATABASE = {
    'drivername': 'postgres',
    'host': config('DB_HOST', default='localhost'),
    'port': config('DB_PORT', default='5432'),
    'username': config('POSTGRES_USER', 'postgres'),
    'database': config('POSTGRES_DB', default='postgres'),
    'password': config('POSTGRES_PASSWORD'),
}
