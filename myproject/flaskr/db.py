import sqlite3

import click
from flask import current_app, g

# g is a special object that is unique for each request. it is used to store data that might be accessed by multiple functions during the request

# the connection is stored and reused instead of creating a new connection if get_db is called a second time in the same request

def get_db():
	if 'db' not in g:
		g.db = sqlite3.connect(
			# sqlite3.connect establishes a connection to the file pointed at by the DB configuration key 
			current_app.config['DATABASE'],
			detect_types=sqlite3.PARSE_DECLTYPES
		)
		g.db.row_factory = sqlite3.Row

	return g.db

def close_db(e=None):
	db = g.pop('db', None)

	if db is not None:
		db.close()


def init_db():
	db = get_db()

	with current_app.open_resource('schema.sql') as f:
		db.executescript(f.read().decode('utf8'))

@click.command('init-db')
def init_db_command():
	"""Clear the existing data and create new tables."""
	init_db()
	click.echo("Initialized the database")
