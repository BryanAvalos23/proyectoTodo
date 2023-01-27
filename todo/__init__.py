import os  #permite acceder a ciertas cosas del sistema operativo

from flask import Flask

# nos servira cuando queramos testear o hacer varias instancias de una aplicacion, pero es importante saber que cuando creamos app con flask
# tenemos que usar esta funcion
def create_app():
	app = Flask(__name__)

	app.config.from_mapping(

		# definiendo sesiones en nuestra app
		SECRET_KEY='nikey', #cuando lo pasamos a produccion debemos usar un string mas complejo por seguridad
		DATABASE_HOST=os.environ.get('FLASK_DATABASE_HOST'),
		DATABASE_PASSWORD=os.environ.get('FLASK_DATABASE_PASSWORD'),
		DATABASE_USER=os.environ.get('FLASK_DATABASE_USER'),
		DATABASE=os.environ.get('FLASK_DATABASE')
	)

	from . import db

	db.init_app(app)

	from . import auth
	from . import todo

	app.register_blueprint(auth.bp)
	app.register_blueprint(todo.bp)

	@app.route('/hola')
	def hola():
		return 'Chanchito feliz'

	return app

