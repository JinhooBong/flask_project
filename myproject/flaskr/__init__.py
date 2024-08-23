import os

from flask import Flask

def create_app(test_config=None):
	# create and configure the app
	app = Flask(__name__, instance_relative_config=True)
	# this creates the Flask instance
	# __name__ is the name of the current Python module - the app needs to know where it's located to set up some paths
	# instance_relative_config=True tells the app that configuration files are relative to the instance folder. 
		# ths instance folder is located outside the flaskr package and can hold local data that shouldn't be committed
		# to version control, such as configuration secrets and the database files
	app.config.from_mapping(
		SECRET_KEY='dev',
		DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
	)

	if test_config is None:
		# load the instance config, if it exists, when not testing
		app.config.from_pyfile('config.py', silent=True)
		# overrides the default configuration with values taken from the config.py file in the instance folder if it exists.
	else:
		# load the test config if passed in
		app.config.from_mapping(test_config)
	
	# ensure the instance folder exists
	try:
		os.makedirs(app.instance_path)
		# Flask doesn't create the instance folder automatically, but it needs to be created because your project will create the SQLite database files there 
	except OSError:
		pass

	# a simple page that says hello
	@app.route('/hello')
	def hello():
		return "Hello, World!"

	from . import db
	db.init_app(app)

	return app