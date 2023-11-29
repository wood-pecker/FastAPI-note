import json
from os import environ

import databases
from sqlalchemy import MetaData, create_engine

DB_USER = "postgres"
DB_PASS = "postgres"
DB_HOST = "localhost"

# if json.loads(environ.get("TESTING").lower()):
#     DB_NAME = "test_fast_notes"
# else:
DB_NAME = "fast_notes"


SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}"
)

database = databases.Database(SQLALCHEMY_DATABASE_URL)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=10,
    max_overflow=2,
    pool_recycle=300,
    pool_pre_ping=True,
    pool_use_lifo=True,
)

metadata = MetaData()
