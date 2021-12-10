import json
import mysql.connector
from DBcm import UseDatabase
from flask import Flask, render_template,request,redirect, url_for, Blueprint, current_app, session

zapros4 = Blueprint('zapros4', __name__, template_folder = 'templates', static_folder = 'static')

@zapros4.route('/', methods=['GET','POST'])
def index():
	if 'user' in session:
		with UseDatabase(current_app.config['dbconfig']) as cursor:
			employees = find_employees(cursor)
			print("employes=",employees)
		return render_template('zapros4.html', employees = employees)
	else:
		session['ind'] = True
		print("------------authorization is needed------------")
		return redirect(url_for('auth_blueprint.auth'))


def find_employees(cursor):
	SQL = f"""SELECT name
    FROM worker w LEFT JOIN departure d ON w.id_driver = d.id_driver
    WHERE open_date >= '2013-03-31' OR open_date <= '2013-03-01'
    GROUP by name;"""
	cursor.execute(SQL)
	result = cursor.fetchall()
	res = []
	schema = ['surname']
	for blank in result:
		res.append(dict(zip(schema,blank)))
	return res

