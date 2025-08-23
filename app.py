from flask import Flask,request,jso
from db_config import psycopg2,DB_CONFIG
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
app.secret_key = 'my_key'

def execute_query(query, params=None, fetch=False, as_dict=False):
    conn = psycopg2.connect(**DB_CONFIG)
    cursor_factory = RealDictCursor if as_dict else None
    cur = conn.cursor(cursor_factory=cursor_factory)
    try:
        cur.execute(query, params)
        conn.commit()
        if fetch:
            result = cur.fetchall()
        else:
            result = None
        return result
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()


