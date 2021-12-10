import json
import mysql.connector
from DBcm import UseDatabase
from flask import Flask, render_template,request,redirect, url_for, Blueprint, current_app, session

zapros2 = Blueprint('zapros2', __name__, template_folder = 'templates', static_folder = 'static')

@zapros2.route('/', methods=['GET','POST'])
def index():
	if 'user' in session:
		with UseDatabase(current_app.config['dbconfig']) as cursor:
			employees = find_employees(cursor)
		return render_template('zapros2.html', employees = employees)
	else:
		session['ind'] = True
		print("------------authorization is needed------------")
		return redirect(url_for('auth_blueprint.auth'))


def find_employees(cursor):
	SQL = f"""SELECT id_driver, name, sum(hour(TIMEDIFF(time_arr,time_dep))) as total_hours FROM lab l WHERE open_date >= '2017.03.01' AND open_date <= '2017.03.30' group by id_driver;"""
	cursor.execute(SQL)
	result = cursor.fetchall()
	res = []
	schema = ['id_driver','name','total_hours']
	for blank in result:
		res.append(dict(zip(schema,blank)))
	return res

