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
        return jsonify({'status_code':200,'status':'Successfully inserted data','id':get_id[0]})
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

@app.route('/get_skills',methods=['GET'])
def get_skills():
    try:
        query = """SELECT skill_name,category,proficiency,experience_years FROM skills_table"""
        params = ()
        data = execute_query(query,params,fetch=True,get_one=False,as_dict=True)
        return jsonify({'status_code':200,'status':'Successfully fetched project details','details':data})
    except Exception as e:
        return jsonify({'status_code':500,'status':'Failed to fetch data'+str(e)})

@app.route('/insert_skills',methods=['POST'])
def insert_skills():
    try:
        userid = request.json.get('userid')
        skill_name = request.json.get('skill_name')
        category = request.json.get('category')
        proficiency = request.json.get('proficiency')
        experience_years = request.json.get('experience_years') 

        validate = ["skill_name","category","proficiency","experience_years","userid"]
        missing = json_validate(validate)
        if missing:
            return jsonify({'status_code': 400,'status': 'Failed','message':"Please fill these fields:{value}".format(value=missing)})
        query = """INSERT INTO skills_table (skill_name,category,proficiency,experience_years)
        VALUES (%s,%s,%s,%s) RETURNING id"""
        params = (skill_name,category,proficiency,experience_years,)
        get_id = execute_query(query,params,fetch=True,get_one=True,as_dict=False)
        return jsonify({'status_code':200,'status':'Successfully inserted data','id':get_id[0]})
    except Exception as e:
        return jsonify({'status_code':500,'status':'Failed to insert data'+str(e)})

@app.route('/get_singleskill/<int:skill_id>',methods=['GET'])
def get_singleskill(skill_id):
    try:
        query = """SELECT skill_name,category,proficiency,experience_years FROM skills_table WHERE id = %s"""
        params = (skill_id,)
        data = execute_query(query,params,fetch=True,get_one=True,as_dict=True)
        if data == []:
            return jsonify({'status_code':404,'status':'Data does not exist'})
        return jsonify({'status_code':200,'status':'Successfully fetched skill details','details':data})
    except Exception as e:
        return jsonify({'status_code':500,'status':'Failed to fetch data'+str(e)})

@app.route('/get_experience', methods=['GET'])
def get_experience():
    try:
        query = """SELECT company, role, start_date, end_date, tech_used, highlights FROM experience_table"""
        data = execute_query(query, fetch=True, get_one=False, as_dict=True)
        return jsonify({'status_code': 200, 'status': 'Successfully fetched experience details', 'details': data})
    except Exception as e:
        return jsonify({'status_code': 500, 'status': 'Failed to fetch data ' + str(e)})

@app.route('/insert_experience',methods=['POST'])
def insert_experience():
    try:
        userid = request.json.get('userid')
        company = request.json.get('company') 
        role = request.json.get('role') 
        start_date = request.json.get('start_date') or None
        end_date = request.json.get('end_date') or None
        tech_used = request.json.get('tech_used') 
        highlights = request.json.get('highlights')  

        validate = ["userid","company","role","start_date","end_date","tech_used","highlights"]
        missing = json_validate(validate)
        if missing:
            return jsonify({'status_code': 400,'status': 'Failed','message':"Please fill these fields:{value}".format(value=missing)})
        if type(tech_used) != list:
            return jsonify({'status_code':403,'status':'Invalid input type for tech_used'})   
        query = """INSERT INTO experience_table (company,role,start_date,end_date,tech_used,highlights)
        VALUES (%s,%s,%s,%s,%s,%s) RETURNING id"""
        params = (company, role, start_date, end_date, tech_used, highlights,)
        get_id = execute_query(query,params,fetch=True,get_one=True,as_dict=False)
        return jsonify({'status_code':200,'status':'Successfully inserted data','id':get_id[0]})
    except Exception as e:
        return jsonify({'status_code':500,'status':'Failed to insert data'+str(e)})

@app.route('/get_singleexp/<int:exp_id>',methods=['GET'])
def get_singleexp(exp_id):
    try:
        query = """SELECT company,role,start_date,end_date,tech_used,highlights FROM experience_table WHERE id = %s"""
        params = (exp_id,)
        data = execute_query(query,params,fetch=True,get_one=True,as_dict=True)
        if data == []:
            return jsonify({'status_code':404,'status':'Data does not exist'})
        return jsonify({'status_code':200,'status':'Successfully fetched skill details','details':data})
    except Exception as e:
        return jsonify({'status_code':500,'status':'Failed to fetch data'+str(e)})

if __name__ == "__main__":
    app.run(debug=True)