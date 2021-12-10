import json
import mysql.connector
from DBcm import UseDatabase
from flask import Flask, render_template,request,redirect, url_for, Blueprint, current_app, session

basket = Blueprint('basket', __name__, template_folder = 'templates', static_folder = 'static')

@basket.route('/', methods=['GET','POST'])
def index():
	if 'user' in session:
		with UseDatabase(current_app.config['dbconfig']) as cursor:
			items = find_products(cursor)
			if 'choice' in request.form and request.form['choice'] == 'Выбрать':
				choice_item = {'choice_id': int(request.form.get('choice_id')),
								'choice_name': request.form.get('choice_name')
								}
				print(choice_item)
				put_into_basket(choice_item)
				return render_template('choice_list.html', items=items)
			elif 'show_basket' in request.form and request.form['show_basket'] == 'Показать корзину':
				return render_template('basket.html', basket=session['cart'])
			elif 'delete' in request.form and request.form['delete'] == "Удалить":
				to_del = request.form.get('toDel')
				delete(to_del)
				return render_template('basket.html', basket=session['cart'])
			elif 'save' in request.form and request.form['save'] == "Оформить заказ":
				if session['admin']:
					save_basket(cursor)
					session['cart'] = []
					return render_template('finish.html', items=items)
				else:
					return render_template('fail.html')
			else:
				return render_template('choice_list.html', items=items)
	else:
		session['ind'] = True
		print("Auth failed")
		return redirect(url_for('auth_blueprint.auth'))

def find_products(cursor):
    SQL = """SELECT id_driver, name
            FROM worker"""
    cursor.execute(SQL)
    result = cursor.fetchall()
    res = []
    schema = ['id', 'name']
    for blank in result:
        res.append(dict(zip(schema, blank)))
    return res


def put_into_basket(choice_item):
    if 'cart' not in session:
        session['cart'] = []
    basket_len = len(session['cart'])
    for pos in session['cart']:
        if int(choice_item['choice_id']) == pos['choice_id']:
            return basket_len
    session['cart'] += [{
        'choice_id': int(choice_item['choice_id']),
        'choice_name': choice_item['choice_name']}]
    return basket_len

def save_basket(cursor):
    basket_len=len(session['cart'])
    _SQL = """INSERT INTO crews VALUES(NULL,%s);"""
    for i in range(basket_len):
        values = session['cart'][i].values()
        values=list(values)
        print(values)
        cursor.execute(_SQL,(values[1],))
    return

def delete(name):
    for pos in session['cart']:
        if pos['choice_name'] == name:
            session['cart'].remove(pos)
            session.modified = True
    return
