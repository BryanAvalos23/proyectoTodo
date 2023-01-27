import functools

from flask import (
	Blueprint, 
	flash,
	g, 
	render_template, 
	request, 
	url_for, 
	session,
	redirect
)

from werkzeug.security import check_password_hash, generate_password_hash

from todo.db import get_db

# creando el blueprint
bp = Blueprint('auth', __name__, url_prefix='/auth', template_folder='../templates')

# routeando el blueprint y creando funcion de registro
@bp.route('/register', methods=['GET', 'POST'])
def register():
	if request.method == 'POST':
		username = request.form.get("username", False)
		password = request.form.get("password", False)
		db, c = get_db()
		error = None
		c.execute(
			'select id from users where username = %s',(username,)
		)

		# validando datos de error
		if not username:
			error = 'username is required'
		if not password:
			error = 'password is required'
		elif c.fetchone() is not None:
			error = 'Usuario {} se encuentra registrado.'.format(username)

		if error is None:
			c.execute(
				'insert into users (username, password) values (%s, %s)',
				(username, generate_password_hash(password))
			)
			db.commit()

			return redirect(url_for('auth.login'))

		flash(error)
	return render_template('auth/register.html')

# routeando blueprint y creando la funcion de login
@bp.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		username = request.form.get("username", False)
		password = request.form.get("password", False)
		db, c = get_db()
		error = None
		c.execute(
			'select * from users where username = %s', (username,)
		)
		user = c.fetchone()
		if user is None:
			error = 'Usuario y/o contraseña invalida'
		elif not check_password_hash(user['password'], password):
			error = 'Usuario y/o contraseña invalida'

		if error is None:
			session.clear()
			session['user_id'] = user['id']
			return redirect(url_for('todo.index'))

		flash(error)
	return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
	user_id = session.get('user_id')

	if user_id is None:
		g.user = None
	else:
		db, c = get_db()
		c.execute(
			'select * from users where id = %s', (user_id, )
		)
		g.user = c.fetchone()

def login_required(view):
	@functools.wraps(view)
	def wrapped_view(**kwargs):
		if g.user is None:
			return redirect(url_for('auth.login'))
			
		return view(**kwargs)

	return wrapped_view

