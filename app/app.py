from typing import List, Dict
import simplejson as json
import sendgrid
import os
from flask import Flask, Response, render_template, redirect, request, session, url_for, g
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor
from markupsafe import Markup
from sendgrid.helpers.mail import Mail, Email, To, Content
from python_http_client.exceptions import HTTPError

app = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)

sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
html_string_license = Markup(
    "Copyright &copy; 2021 Phil Stickna and Paola Leiva <br/>Content provided under the MIT License.")

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'airtravelData'

app.secret_key = 'my_precious'

mysql.init_app(app)


def send_confirm_email(to_email, account_id):
    try:
        sender = Email(os.environ.get('EMAIL_USERNAME'))
        recipient = To(to_email)
        subject = "Please confirm your email"
        content = Content("text/html",
                          "Click <a href=\"http://127.0.0.1/confirm/%s\">here</a> to confirm your email." % account_id)
        mail = Mail(sender, recipient, subject, content)
        mail_json = mail.get()
        response = sg.client.mail.send.post(request_body=mail_json)
        print(response.status_code)
        print(response.headers)
    except HTTPError as e:
        print(e.to_dict)


@app.before_request
def before_request():
    if request.path == url_for('login') or request.path == url_for('register') or url_for('confirm') in request.path:
        return
    elif 'logged_in' in session and session['logged_in'] == True:
        return
    else:
        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', title='Login', copyright_notice=html_string_license)
    elif request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        msg = ''
        cursor = mysql.get_db().cursor()
        cursor.execute("SELECT * FROM accounts WHERE username = %s AND password = %s", (username, password))
        account = cursor.fetchone()

        if account and account['confirmed']:
            session['logged_in'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            return redirect(url_for('index'))
        elif account:
            msg = 'You must confirm your account before you can login!'
        else:
            msg = 'Incorrect username/password!'
        return render_template('login.html', title='Login', msg=msg, copyright_notice=html_string_license)
    else:
        return render_template('login.html', title='Login', msg='Please fill out the form!',
                               copyright_notice=html_string_license)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/confirm', methods=['GET', 'POST'])
@app.route('/confirm/<int:account_id>', methods=['GET', 'POST'])
def confirm(account_id=None):
    if not account_id:
        return render_template('register.html', title='Register', msg="Invalid confirmation link. Please re-register.",
                               copyright_notice=html_string_license)
    elif request.method == 'GET':
        cursor = mysql.get_db().cursor()
        cursor.execute("SELECT * FROM accounts WHERE id = %s", account_id)
        account = cursor.fetchone()
        if account and account['confirmed']:
            return render_template('login.html', title='Login', msg="Your email is already confirmed. Please login.",
                                   copyright_notice=html_string_license)
        elif account:
            return render_template('confirm.html', title='Confirm my Account', account_id=account_id,
                                   msg="Login to confirm your email.", copyright_notice=html_string_license)
        else:
            return render_template('register.html', title='Register',
                                   msg="Invalid confirmation link. Please re-register.",
                                   copyright_notice=html_string_license)
    elif request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.get_db().cursor()
        cursor.execute("SELECT id FROM accounts WHERE username = %s AND password = %s", (username, password))
        account = cursor.fetchone()
        if account:
            cursor.execute("""UPDATE accounts a SET a.confirmed = %s WHERE a.id = %s""", (True, account['id']))
            mysql.get_db().commit()
            session['logged_in'] = True
            session['id'] = account['id']
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return render_template('confirm.html', title='Confirm my Account', account_id=account_id,
                                   msg="Incorrect username/password!", copyright_notice=html_string_license)
    elif request.method == 'POST':
        return render_template('confirm.html', title='Confirm my Account', account_id=account_id,
                               msg="Please fill out the form!", copyright_notice=html_string_license)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html', title='Register', copyright_notice=html_string_license)
    elif request.method == 'POST' and 'username' in request.form and 'password' in request.form and \
            'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.get_db().cursor()
        cursor.execute("SELECT * FROM accounts WHERE email = %s", email)
        account = cursor.fetchone()
        if account:
            return render_template('register.html', title='Register', msg='Email already exists!',
                                   copyright_notice=html_string_license)

        input_data = (username, password, email, False)
        sql_insert_query = """INSERT INTO accounts (username, password, email, confirmed) VALUES (%s, %s, %s, %s)"""
        cursor.execute(sql_insert_query, input_data)
        mysql.get_db().commit()

        cursor.execute("SELECT id FROM accounts WHERE email = %s", email)
        account = cursor.fetchone()
        send_confirm_email(email, account['id'])

        return render_template('login.html', title='Login', msg='Please check your email!',
                               copyright_notice=html_string_license)
    elif request.method == 'POST':
        return render_template('register.html', title='Register', msg="Please fill out the form!",
                               copyright_notice=html_string_license)


@app.route('/', methods=['GET'])
def index():
    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT * FROM airtravelInput")
    result = cursor.fetchall()
    return render_template('index.html', title='Home', airtravels=result, copyright_notice=html_string_license)


@app.route('/chart', methods=['GET'])
def api_airtravel_chartPage():
    return render_template('chart.html', title='Chart', copyright_notice=html_string_license)


@app.route('/api/v1/airtravel_chart', methods=['GET'])
def api_airtravel_stats() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM airtravelInput')
    result = cursor.fetchall()
    json_result = json.dumps(result)
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/view/<int:airtravel_id>', methods=['GET'])
def record_view(airtravel_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM airtravelInput WHERE id=%s', airtravel_id)
    result = cursor.fetchall()
    return render_template('view.html', title='View Form', airtravel=result[0], copyright_notice=html_string_license)


@app.route('/edit/<int:airtravel_id>', methods=['GET'])
def form_edit_get(airtravel_id):
    print(airtravel_id)
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM airtravelInput WHERE id=%s', airtravel_id)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', airtravel=result[0], copyright_notice=html_string_license)


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
    return render_template('new.html', title='New Travel Form', copyright_notice=html_string_license)


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


@app.route('/api/v1/airtravels/<int:airtravel_id>', methods=['GET'])
def api_airtravel_view(airtravel_id) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM airtravelInput WHERE id=%s', airtravel_id)
    result = cursor.fetchall()
    json_result = json.dumps(result)
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/airtravels/<int:airtravel_id>', methods=['PUT'])
def api_airtravel_save(airtravel_id) -> str:
    cursor = mysql.get_db().cursor()
    content = request.json
    inputData = (content['fldYEAR'], content['fldJAN]'], content['fldFEB'], content['fldMAR'], content['fldAPR'],
                 content['fldMAY'], content['fldJUN'], content['fldJUL'], content['fldAUG'], content['fldSEP'],
                 content['fldOCT'], content['fldNOV'], content['fldDECE'], airtravel_id)
    sql_update_query = """UPDATE airtravelInput t SET t.YEAR = %s, t.JAN = %s, t.FEB = %s, t.MAR = %s, t.APR = %s,
    t.MAY = %s, t.JUN = %s, t.JUL = %s, t.AUG = %s, t.SEP = %s, t.OCT = %s, t.NOV = %s, t.DECE = %s WHERE t.id = %s"""
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/airtravels/', methods=['POST'])
def api_add() -> str:

    content = request.json

    cursor = mysql.get_db().cursor()
    inputData = (content['fldYEAR'], content['fldJAN'], content['fldFEB'],
                 content['fldMAR'], content['fldAPR'], content['fldMAY'], content['fldJUN'], content['fldJUL'],
                 content['fldAUG'], content['fldSEP'], content['fldOCT'], content['fldNOV'], content['fldDECE'])
    sql_insert_query = """INSERT INTO airtravelInput (YEAR, JAN, FEB, MAR, APR, MAY, JUN, JUL, AUG, SEP, OCT, NOV, DECE) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/v1/airtravels/<int:airtravel_id>', methods=['DELETE'])
def api_delete(airtravel_id) -> str:
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM airtravelInput WHERE id = %s """
    cursor.execute(sql_delete_query, airtravel_id)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0')