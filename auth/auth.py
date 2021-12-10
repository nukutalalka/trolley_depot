import json
import mysql.connector
from DBcm import UseDatabase
from flask import Flask, render_template,request,redirect, url_for, Blueprint, current_app, session

auth_blueprint = Blueprint('auth_blueprint', __name__, template_folder = 'templates', static_folder = 'static')

@auth_blueprint.route('/auth', methods=['GET','POST'])
def auth():
	print(request.form)
	if 'send' in request.form and request.form['send']=='Войти':
		login = request.form.get('login')
		password = request.form.get('pass')
		if login:
			if password:
				with UseDatabase(current_app.config['dbconfig']) as cursor:
					inf = zap(cursor, login, password)
				if inf:
					session['user'] = login
					if session['ind']:
						return redirect('/zapros1')
					else:
						return redirect('/menu')
				else:
					return render_template('auth.html')

	else:
		return render_template('auth.html')


def zap(cursor, login, password):
    SQL = """SELECT log_group,pass_group
            FROM usr WHERE
            log = '{0}'
            AND pass = '{1}';""".format(login, password)
    cursor.execute(SQL)
    result = cursor.fetchall()
    res = []
    schema = ['login', 'password']
    with open('data_files/dbconfig.json', 'r') as f:
        data = json.load(f)
    for blank in result:
        res.append(dict(zip(schema, blank)))
        data['user'] = blank[0]
        data['password'] = blank[1]
        if blank[0] == "WORK":
            session['admin'] = True
        elif blank[0] == "USER":
            session['admin'] = False
    with open('data_files/dbconfig.json', 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    return res