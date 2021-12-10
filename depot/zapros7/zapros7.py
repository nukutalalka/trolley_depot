import json
import mysql.connector
from DBcm import UseDatabase
from flask import Flask, render_template,request,redirect, url_for, Blueprint, current_app, session

zapros7 = Blueprint('zapros7', __name__, template_folder = 'templates', static_folder = 'static')

@zapros7.route('/', methods=['GET','POST'])
def index():
	if 'user' in session:
		if 'send' in request.form and request.form['send']=='Отправить':
			information = request.form.get('route_id')
			print(information)
			if information:
				print(dir(current_app))
				with UseDatabase(current_app.config['dbconfig']) as cursor:
					employees = find_employees(cursor, information)
				return render_template('zapros7.html', information = information, employees = employees)
			else:
				return render_template('entry.html')
		else:
				return render_template('entry.html')
	else:
		session['ind'] = True
		print("------------authorization is needed------------")
		return redirect(url_for('auth_blueprint.auth'))


def find_employees(cursor, information):
	SQL ="""SELECT id_driver, adress, name, birthday, on_date FROM lab6 l where id_route = '{0}' 
    group by id_driver order by count(id_route) DESC LIMIT 1;""".format(information)
	cursor.execute(SQL)
	result = cursor.fetchall()
	res = []
	schema = ['id_driver','adress','name','birthday','on_date']
	for blank in result:
		res.append(dict(zip(schema,blank)))
	return res

