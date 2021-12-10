import json
import mysql.connector
from DBcm import UseDatabase
from flask import Flask, render_template,request,redirect, url_for, Blueprint, current_app, session

zapros1 = Blueprint('zapros1', __name__, template_folder = 'templates', static_folder = 'static')

@zapros1.route('/', methods=['GET','POST'])
def index():
	if 'user' in session:
		#print("robit!!!!!!!!!!!!!!")
		if 'send' in request.form and request.form['send']=='Отправить':
			information = request.form.get('route_id')
			print(information)
			if information:
				with UseDatabase(current_app.config['dbconfig']) as cursor:
					employees = find_employees(cursor, information)
				return render_template('zapros1.html', information = information, employees = employees)
			else:
				return render_template('entry.html')
		else:
				return render_template('entry.html')
	else:
		session['ind'] = True
		print("------------authorization is needed------------")
		return redirect(url_for('auth_blueprint.auth'))


def find_employees(cursor, information):
	SQL =  _SQL = """SELECT name 
    FROM worker w, departure d 
    WHERE w.id_driver = d.id_driver AND open_date >= '2017.03.01' 
    AND open_date <= '2017.03.31' AND id_route ='{0}';""".format(information)
	#SQL = _SQL = """SELECT name from worker""".format(information)
	cursor.execute(SQL)
	print(_SQL)
	result = cursor.fetchall()
	res = []
	schema = ['surname']
	for blank in result:
		res.append(dict(zip(schema,blank)))
	return res

