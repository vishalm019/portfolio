from flask import Flask,request,jsonify
from db_config import DB_CONFIG
from psycopg2.extras import RealDictCursor
import psycopg2

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

@app.route('/get_projects',methods=['GET'])
def get_projects():
    try:
        query = """SELECT project_name, description, tech_stack, github_link, demo_link, duration_months, role FROM projects_table"""
        params = ()
        data = execute_query(query,params,fetch=True,as_dict=True)
        return jsonify({'status_code':200,'status':'Successfully fetched project details','details':data})
    except Exception as e:
        return jsonify({'status_code':500,'status':'Failed to fetch data'+str(e)})
    
if __name__ == (__main__):
    app.run(debug=True)