import json
import mysql.connector
from DBcm import UseDatabase
from flask import Flask, render_template,request,redirect, url_for, Blueprint, current_app, session

zapros5 = Blueprint('zapros5', __name__, template_folder = 'templates', static_folder = 'static')

@zapros5.route('/', methods=['GET','POST'])
def index():
	if 'user' in session:
		with UseDatabase(current_app.config['dbconfig']) as cursor:
			employees = find_employees(cursor)
			print("employes=",employees)
		return render_template('zapros5.html', employees = employees)
	else:
		session['ind'] = True
		print("------------authorization is needed------------")
		return redirect(url_for('auth_blueprint.auth'))


def find_employees(cursor):
	SQL = f"""SELECT id_driver, adress, name, birthday, on_date 
    From worker WHERE on_date = (SELECT min(on_date) FROM worker);"""
	cursor.execute(SQL)
	result = cursor.fetchall()
	print(result)
	res = []
	schema = ['id_driver','adress','name','birthday','on_date']
	for blank in result:
		res.append(dict(zip(schema,blank)))
	return res

