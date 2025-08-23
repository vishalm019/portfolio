import psycopg2

DB_CONFIG = {
    'dbname':'portfolio',
    'user':'postgres',
    'password':'localhost123019',
    'host':'localhost',
    'port':'5432',
}

conn = psycopg2.connect(**DB_CONFIG)
cur = conn.cursor