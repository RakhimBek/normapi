import contextvars

import psycopg2


def get_connection():
	host = contextvars.ContextVar('HOST').get()
	port = contextvars.ContextVar('PORT').get()
	database = contextvars.ContextVar('DATABASE').get()
	user = contextvars.ContextVar('USER').get()
	password = contextvars.ContextVar('PASSWORD').get()

	return psycopg2.connect(
		host=host,
		port=port,
		database=database,
		user=user,
		password=password,
	)
