import json
import mysql.connector
import datetime
from DBcm import UseDatabase
from flask import Flask, render_template,request,redirect, url_for, Blueprint, current_app, session
date=0
d =datetime.date.today()
schedule = Blueprint('schedule', __name__, template_folder = 'templates', static_folder = 'static')

@schedule.route('/', methods=['GET','POST'])
def index():
	if 'user' in session:
			with UseDatabase(current_app.config['dbconfig']) as cursor:
				items = find_workers(cursor)
				if 'choice' in request.form and request.form['choice'] == 'Выбрать':
					choice_item = {'choice_id': int(request.form.get('choice_id')),
									'choice_name': request.form.get('choice_name'),
									'quantity': request.form.get('quantity')
									}
					put_into_schedule(choice_item)
					return render_template('choice_list1.html', items=items, date=date, month=d.month, year=d.year)
				elif 'show_schedule' in request.form and request.form['show_schedule'] == 'Показать расписание':
					return render_template('schedule.html', schedule=session['cart'], date=date, month=d.month, year=d.year)
				elif 'change_date' in request.form and request.form['change_date'] == 'Поменять дату':
					return redirect(url_for('schedule.entry'))
				elif 'delete' in request.form and request.form['delete'] == "Удалить":
					to_del = request.form.get('toDel')
					delete(to_del)
					return render_template('schedule.html', schedule=session['cart'], date=date, month=d.month, year=d.year)
				elif 'save' in request.form and request.form['save'] == "Оформить заказ":
					if session['admin']:
						save_schedule(cursor)
						session['cart'] = []
						return render_template('finish.html', items=items)
					else:
						return render_template('fail.html')
				else:
					return render_template('choice_list1.html', items=items, date=date, month=d.month, year=d.year)
	else:
		session['ind'] = True
		print("Auth failed")
		return redirect(url_for('auth_blueprint.auth'))

@schedule.route('/entry', methods=['GET','POST'])
def entry():
	if 'user' in session:
		session['cart']=[]
		num_days=[31,28,31,30,31,30,31,31,30,31,30,31]
		if 'send' in request.form and request.form['send']=='Отправить':
			global date
			date = request.form.get('route_id')
			if date:
				if date.isalpha():
					return render_template('entry1.html')
				else:
					if 0 < int(date) < num_days[d.month-1]+1:
						print(date)
						return redirect(url_for('schedule.index'))
					else:
						return render_template('entry1.html')
			else:
				return render_template('entry1.html')
		else:
			return render_template('entry1.html')
	else:
		session['ind'] = True
		print("Auth failed")
		return redirect(url_for('auth_blueprint.auth'))

def find_workers(cursor):
	SQL = """SELECT id_driver, name
			FROM worker"""
	cursor.execute(SQL)
	result = cursor.fetchall()
	res = []
	schema = ['id', 'name']
	for blank in result:
		res.append(dict(zip(schema, blank)))
	return res


def put_into_schedule(choice_item):
    if 'cart' not in session:
        session['cart'] = []
    schedule_len = len(session['cart'])
    for pos in session['cart']:
        print("checking...", pos['choice_name'])
        if int(choice_item['choice_id']) == pos['choice_id']:
            print("im in if")
            return schedule_len
    if choice_item['quantity'] == '':
        return schedule_len
    session['cart'] += [{
        'choice_id': int(choice_item['choice_id']),
        'choice_name': choice_item['choice_name'],
        'quantity': choice_item['quantity']}]
    print(session['cart'])
    return schedule_len

def save_schedule(cursor):
	schedule_len=len(session['cart'])
	_SQL = """INSERT INTO schedule VALUES(NULL,%s,%s,%s);"""
	data=str(d.year)+'-'+str(d.month)+'-'+date
	for i in range(schedule_len):
		values = session['cart'][i].values()
		values=list(values)
		cursor.execute(_SQL,(data,values[1],values[2],))
	return

def delete(name):
	for pos in session['cart']:
		if pos['choice_name'] == name:
			session['cart'].remove(pos)
			session.modified = True
	return
