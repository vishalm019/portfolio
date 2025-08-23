from flask import Flask,request,jsonify
from db_config import DB_CONFIG
from psycopg2.extras import RealDictCursor
import psycopg2

app = Flask(__name__)
app.secret_key = 'my_key'

def execute_query(query, params=None, fetch=False,get_one=False, as_dict=False):
    conn = psycopg2.connect(**DB_CONFIG)
    cursor_factory = RealDictCursor if as_dict else None
    cur = conn.cursor(cursor_factory=cursor_factory)
    try:
        cur.execute(query, params)
        conn.commit()
        if fetch:
            if get_one:
                result = cur.fetchone()
            else:
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

def json_validate(required_fields):
    payload = request.json
    missing = []
    for field in required_fields:
        value = payload.get(field)
        if value is None or str(value).strip() == "":
            missing.append(field)
    return missing

@app.route('/get_projects',methods=['GET'])
def get_projects():
    try:
        query = """SELECT project_name, description, tech_stack, github_link, demo_link, duration_months, role FROM projects_table"""
        params = ()
        data = execute_query(query,params,fetch=True,get_one=False,as_dict=True)
        return jsonify({'status_code':200,'status':'Successfully fetched project details','details':data})
    except Exception as e:
        return jsonify({'status_code':500,'status':'Failed to fetch data'+str(e)})

@app.route('/insert_project',methods=['POST'])
def insert_project():
    try:
        userid = request.json.get('userid')
        project_name = request.json.get('project_name')
        description = request.json.get('description')
        tech_stack = request.json.get('tech_stack') 
        github_link = request.json.get('github_link')
        demo_link = request.json.get('demo_link')
        duration_month = request.json.get('duration_month')
        role = request.json.get('role')
        validate = ["project_name", "description", "tech_stack", "github_link", "demo_link", "duration_month", "role"]
        missing = json_validate(validate)
        if missing:
            return jsonify({'status_code': 400,'status': 'Failed','message':"Please fill these fields:{value}".format(value=missing)})
        query = """INSERT INTO projects_table (project_name,description,tech_stack,github_link,demo_link,duration_months,role)
        VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING id"""
        params = (project_name,description,tech_stack,github_link,demo_link,duration_month,role,)
        get_id = execute_query(query,params,fetch=True,get_one=True,as_dict=False)
        return jsonify({'status_code':200,'status':'Successfully inserted data','id':get_id[0][0]})
    except Exception as e:
        return jsonify({'status_code':500,'status':'Failed to insert data'+str(e)})

@app.route('/get_singleproject/<int:project_id>',methods=['GET'])
def get_singleproject(project_id):
    try:
        query = """SELECT project_name,description,tech_stack,github_link,demo_link,duration_months,role FROM projects_table WHERE id = %s"""
        params = (project_id,)
        data = execute_query(query,params,fetch=True,get_one=True,as_dict=True)
        if data == []:
            return jsonify({'status_code':404,'status':'Data does not exist'})
        return jsonify({'status_code':200,'status':'Successfully fetched project details','details':data})
    except Exception as e:
        return jsonify({'status_code':500,'status':'Failed to fetch data'+str(e)})

if __name__ == "__main__":
    app.run(debug=True)