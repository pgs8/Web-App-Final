import simplejson as json
from flask import Flask, request, Response, redirect, render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

app = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'airtravelData'
mysql.init_app(app)


@app.route('/', methods=['GET'])
def index():
    user = {'username': 'Air Travel'}
    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT * FROM airtravelInput")
    result = cursor.fetchall()
    return render_template('index.html', title='Home', user=user, airtravels=result)


@app.route('/view/<int:airtravel_id>', methods=['GET'])
def record_view(airtravel_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM airtravelInput WHERE id=%s', airtravel_id)
    result = cursor.fetchall()
    return render_template('view.html', title='View Form', airtravel=result[0])


@app.route('/edit/<int:airtravel_id>', methods=['GET'])
def form_edit_get(airtravel_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM airtravelInput WHERE id=%s', airtravel_id)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', airtravel=result[0])


@app.route('/edit/<int:airtravel_id>', methods=['POST'])
def form_update_post(airtravel_id):
    cursor = mysql.get_db().cursor()
    input_data = (request.form.get('fldYEAR'), request.form.get('fldJAN'), request.form.get('fldFEB'),
                  request.form.get('fldMAR'), request.form.get('fldAPR'), request.form.get('fldMAY'),
                  request.form.get('fldJUN'), request.form.get('fldJUL'), request.form.get('fldAUG'),
                  request.form.get('fldSEP'), request.form.get('fldOCT'), request.form.get('fldNOV'),
                  request.form.get('fldDECE'), airtravel_id)
    sql_update_query = """UPDATE airtravelInput t SET t.YEAR = %s, t.JAN = %s, t.FEB = %s, t.MAR = %s, t.APR = %s,
    t.MAY = %s, t.JUN = %s, t.JUL = %s, t.AUG = %s, t.SEP = %s, t.OCT = %s, t.NOV = %s, t.DECE = %s WHERE t.id = %s"""
    cursor.execute(sql_update_query, input_data)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/airtravels/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', title='New Travel Form')


@app.route('/airtravels/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    input_data = (request.form.get('fldYEAR'), request.form.get('fldJAN'), request.form.get('fldFEB'),
                  request.form.get('fldMAR'), request.form.get('fldAPR'), request.form.get('fldMAY'),
                  request.form.get('fldJUN'), request.form.get('fldJUL'), request.form.get('fldAUG'),
                  request.form.get('fldSEP'), request.form.get('fldOCT'), request.form.get('fldNOV'),
                  request.form.get('fldDECE'))
    sql_insert_query = """INSERT INTO airtravelInput (YEAR, JAN, FEB, MAR, APR, MAY, JUN, JUL, AUG, SEP, OCT, NOV, DECE)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    cursor.execute(sql_insert_query, input_data)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/delete/<int:airtravel_id>', methods=['POST'])
def form_delete_post(airtravel_id):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM airtravelInput WHERE id = %s """
    cursor.execute(sql_delete_query, airtravel_id)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/api/v1/airtravels', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM airtravelInput')
    result = cursor.fetchall()
    json_result = json.dumps(result)
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/airtravels/<int:airtravel_id>', methods=['GET'])
def api_retrieve(airtravel_id) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM airtravelInput WHERE id=%s', airtravel_id)
    result = cursor.fetchall()
    json_result = json.dumps(result)
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/airtravels/', methods=['POST'])
def api_add() -> str:
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/v1/airtravels/<int:airtravel_id>', methods=['PUT'])
def api_edit(airtravel_id) -> str:
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/airtravels/<int:airtravel_id>', methods=['DELETE'])
def api_delete(airtravel_id) -> str:
    resp = Response(status=210, mimetype='application/json')
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
