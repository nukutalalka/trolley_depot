import json
import mysql.connector
from DBcm import UseDatabase
from flask import Flask, render_template,request,redirect, url_for, Blueprint, current_app, session

zapros3 = Blueprint('zapros3', __name__, template_folder = 'templates', static_folder = 'static')

@zapros3.route('/', methods=['GET','POST'])
def index():
	if 'user' in session:
		with UseDatabase(current_app.config['dbconfig']) as cursor:
			employees = find_employees(cursor)
		return render_template('zapros3.html', employees = employees)
	else:
		session['ind'] = True
		print("------------authorization is needed------------")
		return redirect(url_for('auth_blueprint.auth'))


def find_employees(cursor):
	SQL ="""SELECT name FROM worker w LEFT JOIN departure d ON w.id_driver = d.id_driver WHERE id_departure IS NULL"""
	cursor.execute(SQL)
	result = cursor.fetchall()
	res = []
	schema = ['surname']
	for blank in result:
		res.append(dict(zip(schema,blank)))
	return res

