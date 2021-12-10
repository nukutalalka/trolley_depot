from flask import Blueprint,session,redirect
auth_blueprint = Blueprint('auth_blueprint',__name__)
@auth_blueprint.route('/auth', methods=['POST', 'GET'])
def auth():
	login='WORK'
	password ='12345'
	session['user']=login
	return redirect('/menu')