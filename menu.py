import json
import mysql.connector
from flask import Flask, render_template,request,redirect, url_for, Blueprint, current_app, session

with open('data_files/dbconfig.json', 'r') as f:
	dbconfig = json.load(f)
with open('data_files/menu.json', 'r') as f:
	menu = json.load(f)

app = Flask(__name__)
app.config['dbconfig'] = dbconfig

from zapros1.zapros1 import zapros1
from zapros2.zapros2 import zapros2
from zapros3.zapros3 import zapros3
from zapros4.zapros4 import zapros4
from zapros5.zapros5 import zapros5
from zapros6.zapros6 import zapros6
from zapros7.zapros7 import zapros7
from auth.auth import auth_blueprint
from basket.basket import basket
from schedule.schedule import schedule

app.register_blueprint(zapros1, url_prefix = '/zapros1')
app.register_blueprint(zapros2, url_prefix = '/zapros2')
app.register_blueprint(zapros3, url_prefix = '/zapros3')
app.register_blueprint(zapros4, url_prefix = '/zapros4')
app.register_blueprint(zapros5, url_prefix = '/zapros5')
app.register_blueprint(zapros6, url_prefix = '/zapros6')
app.register_blueprint(zapros7, url_prefix = '/zapros7')
app.register_blueprint(schedule, url_prefix = '/schedule')
app.register_blueprint(basket, url_prefix = '/basket')
app.register_blueprint(auth_blueprint, url_prefix = '/login')

with open('data_files/secret_key.json','r') as f:
	app_config = json.load(f)
	app.secret_key = app_config['secret_key']
@app.route('/')
def home():
    return redirect('/menu')
    
@app.route('/menu/', methods=['GET','POST'])
def menu_zapros():
	session['ind'] = False
	if 'user' in session:
		with open('data_files/dbconfig.json', 'r') as f:
			dbconfig = json.load(f)
		app.config['dbconfig'] = dbconfig
		route_mapping = {'1' : url_for('zapros1.index'),'2' : url_for('zapros2.index'),'3' : url_for('zapros3.index'),'4' : url_for('zapros4.index'),'5' : url_for('zapros5.index'),'6' : url_for('zapros6.index'),'7' : url_for('zapros7.index'),'9' : url_for('schedule.entry'),'10' : url_for('basket.index')}
		point = request.args.get('point')
		if point is None:
			return render_template('main_menu.html', menu = menu)
		elif point in route_mapping:
			return redirect(route_mapping[point])
		else:
			with open('data_files/dbconfig.json', 'r') as f:
				data = json.load(f)
			data['user'] = 'fake_user'
			data['password'] = 'fake'
			with open('data_files/dbconfig.json', 'w') as f:
				json.dump(data, f, ensure_ascii=False, indent=4)
			session.pop('user')
			session['ind'] = False
			return redirect(url_for('auth_blueprint.auth'))
	else:
		return redirect(url_for('auth_blueprint.auth'))

app.run(host='127.0.0.1',port=5001, debug=True)